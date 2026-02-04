# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import os
import json
from src.functions import db_connect, emp_load, vac_load, ins_tab_vac, load_vac_from_emp
from src.cl_parser_hhe import HeadHunterEmp
from src.cl_parser_hhv import HeadHunterVac



ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
if __name__ == '__main__':
    # считывание данных работодателей с API
    # cl_Emp = HeadHunterEmp()
    # list_emp = cl_Emp.load_employers("Якутск") # Загрузка работодателей с API
    # with open(ROOT_DIR + '\\data\\emp_1.json', 'w', encoding='utf-8') as f:
    #     json.dump(list_emp, f, indent=4, sort_keys=True, ensure_ascii=False)
    # print("emp_1.json записан из данных API")
    # считывание данных работодателя с json временно
    with open(ROOT_DIR + '\\data\\emp_1.json', 'r', encoding="utf-8") as f:
         list_emp = json.load(f)

    # считывание вакансий с API
    # cl_Vac = HeadHunterVac()
    # list_vac = cl_Vac.load_vacancies("Python")
    # with open(ROOT_DIR + '\\data\\vac_1.json', 'w', encoding='utf-8') as f:
    #     json.dump(list_vac, f, indent=4, sort_keys=True, ensure_ascii=False)
    # print("vac_1.json записан из данных API")
    # считывание данных с json временно
    # with open(ROOT_DIR + '\\data\\vac_1.json', 'r', encoding="utf-8") as f:
    #     list_vac = json.load(f)f


    db_connect("vacancy_db")

    print("Загрузка работодателей")
    list_emp_class = emp_load(list_emp) #из списка вакансий создаем список работодателей
    print("Данные работодателей считаны")

    print("Загрузка вакансий", list_emp)

    load_vac_from_emp(list_emp)
    # list_vac_class = vac_load(list_vac)

    # ins_tab_vac("vacancy_db", list_vac_class)
    print("Данные вакансий считаны")
