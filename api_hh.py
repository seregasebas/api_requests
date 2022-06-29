from crypt import methods
import functions_hh
from flask import Flask, render_template, request
'''
!ID - id вакансии (восклицательный знак обязателен)
NAME - название вакансии
!COMPANY_ID - id компании (восклицательный знак обязателен)
COMPANY_NAME - название компании
DESCRIPTION - описание вакансии
'''

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/contacts/')
def contacts():
    contact = {'e_mail':'parser@gmail.com',
               'phone':'+7953777777',
               'fax':'no',
               'adress':'Russia, all cities'}
    return render_template('contacts.html', **contact)

@app.route('/form/', methods=['GET'])
def form_get():
    return render_template('form.html')

@app.route('/form/', methods=['POST'])
def form_post():
    vacancy = request.form['vacancy']
    #название города для вывода на странице
    city_return = request.form['query_string']
    #получаем id города для дальнейшего парсинга
    city = functions_hh.id_name(city_return)    
    keywords = request.form['key_words']
    #получаем данные с сайта по заданным параметрам
    res_all, vacancy_count = functions_hh.api_hh(vacancy, city)
    #средняя зп по всем найденым вакансиям по поиску
    salary_mean = functions_hh.salary_mean(res_all)
    #количество нацденных вакансий по посику
    requirements = functions_hh.requirements(res_all)
    #вакансии по ключевым словам и количесвто этих вакансий
    requirement_count, count_key_words = functions_hh.requirement_count(requirements, keywords)
    #новый словарь с нужными нам данными
    new_dict = functions_hh.merged_dict(vacancy, keywords, requirement_count, vacancy_count, salary_mean, count_key_words)
    #заливаем в json файл
    api_hh = functions_hh.save_file(new_dict)
    return render_template('results.html', city = city_return, new_dict = new_dict)

@app.route('/results/')
def results():
    return render_template('results.html')

if __name__ == "__main__":
    app.run(debug=True)
