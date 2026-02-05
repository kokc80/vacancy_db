# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import os
import json
from src.functions import emp_load, vac_load, compile_vac_from_emp
from src.func_db import db_connect, ins_tab_vac
from src.cl_parser_hhe import HeadHunterEmp
from src.cl_parser_hhv import HeadHunterVac



ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
if __name__ == '__main__':
    db_connect("vacancy_db")

    print("Загрузка работодателей")
    # считывание данных работодателей с API
    # cl_Emp = HeadHunterEmp()
    # list_emp = cl_Emp.load_employers("Якутск") # Загрузка работодателей с API
    # with open(ROOT_DIR + '\\data\\emp_1.json', 'w', encoding='utf-8') as f:
    #     json.dump(list_emp, f, indent=4, sort_keys=True, ensure_ascii=False)
    # считывание данных работодателя с json временно
    with open(ROOT_DIR + '\\data\\emp_1.json', 'r', encoding="utf-8") as f:
         list_emp = json.load(f)
    list_emp_class = emp_load(list_emp) #из списка вакансий создаем класс работодателей
    for item_class in list_emp_class:
        print("Работодатели",item_class)
    print("Данные работодателей считаны\n\n")

    # Загрузка вакансий по работодателю
    print("Загрузка вакансий от работодателей\n")
    list_emp_vac = compile_vac_from_emp(list_emp)
    # Записать вакансии в json
    with open(ROOT_DIR + '\\data\\emp_vac.json', 'w', encoding='utf-8') as f:
        json.dump(list_emp_vac, f, indent=4, sort_keys=True, ensure_ascii=False)
    print("Вакансии записаны в emp_vac.json")
    list_vac_class = vac_load(list_emp_vac) #из списка работодателей создаем класс вакансий
    for item_class in list_vac_class:
        print(item_class)
    print("Данные вакансий считаны")

    # ins_tab_vac("vacancy_db", list_vac_class)
