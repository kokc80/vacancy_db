# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from src.functions import  db_connect
from src.cl_parser_hhv import HeadHunterVac
from src.cl_parser_hhe import HeadHunterEmp


if __name__ == '__main__':
    cl_Vac = HeadHunterVac()
    cl_Emp = HeadHunterEmp()
    db_connect("vacancy_db")
    list_vac = cl_Vac.load_vacancies("Python")
    list_emp = cl_Emp.load_employers("E")
    print("V\n", list_vac, "\nE\n", list_emp)
