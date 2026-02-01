# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import os
import json
from src.functions import db_connect, emp_load, vac_load, ins_tab
from src.cl_parser_hhv import HeadHunterVac
from src.cl_parser_hhe import HeadHunterEmp


ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
if __name__ == '__main__':
    cl_Vac = HeadHunterVac()
    cl_Emp = HeadHunterEmp()

    # считывание работодателей с API
    list_emp = cl_Emp.load_employers("000")
    with open(ROOT_DIR + '\\data\\emp_1.json', 'w', encoding='utf-8') as f:
        json.dump(list_emp, f, indent=4, sort_keys=True, ensure_ascii=False)
    print("emp_1.json записан")
    # считывание вакансий с API
    list_vac = cl_Vac.load_vacancies("Python")
    with open(ROOT_DIR + '\\data\\vac_1.json', 'w', encoding='utf-8') as f:
        json.dump(list_vac, f, indent=4, sort_keys=True, ensure_ascii=False)
    print("vac_1.json записан")

    # данных с json временно
    # with open(ROOT_DIR + '\\data\\emp_1.json', 'r', encoding="utf-8") as f:
    #     list_emp = json.load(f)
    # with open(ROOT_DIR + '\\data\\vac_1.json', 'r', encoding="utf-8") as f:
    #     list_vac = json.load(f)

    db_connect("vacancy_db")

    print("Данные считаны")
    # print("Запись работодателей в таблицу", list_emp)
    list_emp_class = emp_load(list_emp)
    list_vac_class = vac_load(list_vac)
    print("Данные записаны в таблицу")

    ins_tab('vacancy_db', list_emp_class, list_vac_class)
