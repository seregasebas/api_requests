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

res_all, vacancy_count = functions.api_hh(vacancy, city)

salary_mean = functions.salary_mean(res_all)

requirements = functions.requirements(res_all)

requirement_count = functions.requirement_count(requirements, keywords)



print(f'Количество вакансий = {vacancy_count}, средняя ЗП =  {salary_mean}, {requirement_count}')

