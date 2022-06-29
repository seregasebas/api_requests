# print(result.status_code)
# pprint.pprint(result.text)
# pprint.pprint(result.content)
#import pprint
import requests
import json

#функция получения словаря id - name города
def id_name(city):
    goroda = requests.get('https://api.hh.ru/areas/').json()
    city = city.lower()
    id_name = {}
    for i in range(len(goroda)):
        for e in range(len(goroda[i]['areas'])):
            id_name[goroda[i]['areas'][e]['name'].lower()] = goroda[i]['areas'][e]['id']
    
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
            'text': f'NAME:({vacancy})', #вакансия
            'area': city,                #Город
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
    return f'{round((res_mean), 0)}'

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
    dict_word_sorted = sorted(dict_word.items(), key = lambda x: x[1], reverse = True)

    #количество вакасний по ключевым словам
    count_key_words = 1
    for i in range(len(dict_word_sorted)):
        count_key_words += dict_word_sorted[i][1]

    #словарь с вакансиями и проыентами по ключевым словам
    dict_word_new = {'requirement_count':[{} for i in range(len(dict_word_sorted))]}
    for i in range(len(dict_word_new['requirement_count'])):
        dict_word_new['requirement_count'][i]['name'] = dict_word_sorted[i][0]
        dict_word_new['requirement_count'][i]['count'] = dict_word_sorted[i][1]
        dict_word_new['requirement_count'][i]['persent'] = f'{round((dict_word_sorted[i][1]/count_key_words)*100, 2)}%'

    return dict_word_new, count_key_words

#Функция объединения данных в словарь для создания файла json
def merged_dict(vacancy, keywords, requirement_count, vacancy_count, salary_mean, count_key_words):
    new_dict = {}
    new_dict['vacancy'] = vacancy
    new_dict['keywords'] = keywords
    new_dict['vacancy_count'] = vacancy_count
    new_dict['count_key_words'] = count_key_words
    new_dict['salary_mean'] = salary_mean
    new_dict['requirement_count'] = requirement_count['requirement_count']
    return new_dict

#функция сохранения json файла
def save_file(new_dict):
    with open("api_hh.json", "w", encoding='utf-8') as write_file:
        json.dump(new_dict, write_file)

