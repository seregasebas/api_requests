# print(result.status_code)
# pprint.pprint(result.text)
# pprint.pprint(result.content)

import requests
import pprint
import json

#функция получения словаря id - name города
def id_name(city):
    goroda = requests.get('https://api.hh.ru/areas/').json()

    id_name = {}
    for i in range(len(goroda)):
        for e in range(len(goroda[i]['areas'])):
            id_name[goroda[i]['areas'][e]['name']] = goroda[i]['areas'][e]['id']
    return id_name[city]


#функция получения с сайта данных
def api_hh(vacancy, city):

    url = 'https://api.hh.ru/vacancies'

    params = {
        'text': f'NAME:({vacancy})', #вакансия
        'area': city,                #Город
    }

    #Записываем количество страниц с найденной инфой
    pages = requests.get(url, params=params).json()['pages']
    num = requests.get(url, params=params).json()['per_page']
    #количество вакансий
    found_vacations = requests.get(url, params=params).json()['found']
    
    print(f'количество страниц: {pages}')
    print(f'количество tiks на странице: {num}')
    #Переберем все страницы с нужными нам параметрами и запишем в список
    res_all = []
    for page in range(pages):
        print(f'страница номер: {page+1}')
        params = {
            'text': f'NAME:({vacancy})', #AND COMPANY_NAME:(1 OR 2 OR YANDEX) AND (DJANGO OR SPRING)
            'area': city,                #Город
            'page': page,                   #индекс страницы
            # 'per_page': 50               #кол-во вакансий на 1 стр
            }
        res_all.append(requests.get(url, params=params).json())
    
    return res_all, found_vacations

def salary_mean(res_all):
    #Достаем зарплаты - оба числа от и до
    res = []
    for i in range(len(res_all)):
        for e in range(len(res_all[i]['items'])):
            if res_all[i]['items'][e]['salary'] != None:
                res.append(res_all[i]['items'][e]['salary']['from'])
                res.append(res_all[i]['items'][e]['salary']['to'])
    #Убираем None
    res_sum = []
    for salary in res:
        if salary != None:
            res_sum.append(salary)
    #Вычисляем среднюю
    res_mean = sum(res_sum)/len(res_sum)
    
    return res_mean

#Достанем все требования к вакансиям
def requirements(res_all):
    requirement = []
    for i in range(len(res_all)):
        for e in range(len(res_all[i]['items'])):
            requirement.append(res_all[i]['items'][e]['snippet']['requirement'])
    return requirement

def requirement_count(requirement, keywords):
    word = keywords.split(',')
    total = 0
    dict_word = {}
    for i in word:
        for req in range(len(requirement)):
            if requirement[req] != None:
                if i.lower() in requirement[req].lower():
                    total += 1
        dict_word[i] = total
    # dict_word_sorted = sorted(dict_word.items(), key = lambda x: x[:-1])
    # dict_word = dict(dict_word_sorted)
    return dict_word

def save_file(salary_mean, vacancy_count, requirement_count):

    res = open('api_hh.txt', 'w', encoding='utf-8')
    res.write(f'{salary_mean}\n')
    res.write(f'{vacancy_count}\n')
    res.write(f'{requirement_count}\n')
    res.close()

