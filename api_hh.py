import functions_hh
'''
!ID - id вакансии (восклицательный знак обязателен)
NAME - название вакансии
!COMPANY_ID - id компании (восклицательный знак обязателен)
COMPANY_NAME - название компании
DESCRIPTION - описание вакансии
'''
vacancy = input('введите вакансию: ')
city = functions_hh.id_name(input('введите город: '))
keywords = input('введите ключевые слова через , : ')
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


