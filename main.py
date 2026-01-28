# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import os, json
from src.functions import db_connect, emp_load, insert_emp
from src.cl_parser_hhv import HeadHunterVac
from src.cl_parser_hhe import HeadHunterEmp


ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
if __name__ == '__main__':
    cl_Vac = HeadHunterVac()
    cl_Emp = HeadHunterEmp()
    # db_connect("vacancy_db", True)

    # list_vac = cl_Vac.load_vacancies("Python")
    with open(ROOT_DIR + '\\data\\vac_1.json', 'r', encoding="utf-8") as f:
        list_vac = json.load(f)
    # with open(ROOT_DIR + '\\data\\vac_1.json', 'w', encoding='utf-8') as f:
    #     json.dump(list_vac, f, indent=4, sort_keys=True, ensure_ascii=False)

    list_emp = cl_Emp.load_employers("Яку")
    # with open(ROOT_DIR + '\\data\\emp_1.json', 'w', encoding='utf-8') as f:
    #     json.dump(list_vac, f, indent=4, sort_keys=True, ensure_ascii=False)
    with open(ROOT_DIR + '\\data\\emp_1.json', 'r', encoding="utf-8") as f:
        list_emp = json.load(f)

    # db_connect("vacancy_db", False)

print("Данные считаны")
list_emp_class = emp_load(list_emp)
insert_emp('vacancy_db',list_emp_class)