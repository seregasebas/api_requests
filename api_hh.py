import functions
'''
!ID - id вакансии (восклицательный знак обязателен)
NAME - название вакансии
!COMPANY_ID - id компании (восклицательный знак обязателен)
COMPANY_NAME - название компании
DESCRIPTION - описание вакансии
'''
vacancy = input('введите вакансию: ')
city = functions.id_name(input('введите город: '))
keywords = input('введите ключевые слова через , : ')
#получаем данные с сайта по заданным параметрам
res_all, vacancy_count = functions.api_hh(vacancy, city)
#средняя зп по всем найденым вакансиям по поиску
salary_mean = functions.salary_mean(res_all)
#количество нацденных вакансий по посику
requirements = functions.requirements(res_all)
#вакансии по ключевым словам и количесвто этих вакансий
requirement_count, count_key_words = functions.requirement_count(requirements, keywords)
#новый словарь с нужными нам данными
new_dict = functions.merged_dict(vacancy, keywords, requirement_count, vacancy_count, salary_mean, count_key_words)
#заливаем в json файл
api_hh = functions.save_file(new_dict)


