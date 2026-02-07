# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import json
import os

from src.cl_DBManager import DBManager
from src.cl_parser_hhe import HeadHunterEmp
from src.func_db import db_connect, exec_query
from src.functions import compile_vac_from_emp, emp_load, vac_load


def print_top10(tmp_list):
    i_tmp = 0
    for row in tmp_list:
        i_tmp += 1
        if i_tmp <= 10:
            print(row)


ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
if __name__ == "__main__":
    db_connect("vacancy_db")

    print("Загрузка работодателей")
    # считывание данных работодателей с API
    cl_Emp = HeadHunterEmp()
    list_emp = cl_Emp.load_employers("Якутск")  # Загрузка работодателей с API
    with open(ROOT_DIR + "\\data\\emp_1.json", "w", encoding="utf-8") as f:
        json.dump(list_emp, f, indent=4, sort_keys=True, ensure_ascii=False)

    # считывание данных работодателя с json временно
    # with open(ROOT_DIR + "\\data\\emp_1.json", "r", encoding="utf-8") as f:
    #     list_emp = json.load(f)

    list_emp_class = emp_load(
        list_emp
    )  # из списка вакансий создаем класс работодателей
    i = 0
    ins_count = 0
    ins_count_err = 0
    # заполнение tab_emp
    for item_class in list_emp_class:
        # print("Работодатели", item_class)
        try:
            q_insert = (
                f"insert into tab_emp (emp_id, emp_name, emp_url, emp_vac_url, open_vac) values "
                f"('{item_class.emp_idd}','{item_class.emp_name}','{item_class.emp_url}',"
                f"'{item_class.vac_url}',{item_class.open_vac})"
            )
            ins_count += 1
            exec_query("vacancy_db", q_insert)
        except Exception as e:
            print(f"Ошибка вставки в tab_emp \n {q_insert}", {e})
            ins_count_err += 1
        finally:
            i += 1
    print(
        f"Вставлено работодателей: {str(ins_count)} записей из {i} записей \n Ошибок записи: {str(ins_count_err)}"
    )

    # считывание данных вакансий с учетом работодателей с API
    print("Загрузка вакансий от работодателей\n")
    list_emp_vac = compile_vac_from_emp(list_emp)
    # Записать вакансии в json
    with open(ROOT_DIR + "\\data\\emp_vac.json", "w", encoding="utf-8") as f:
        json.dump(list_emp_vac, f, indent=4, sort_keys=True, ensure_ascii=False)
    i = 0
    ins_count = 0
    ins_count_err = 0
    # заполнение tab_vac
    list_vac_class = vac_load(
        list_emp_vac
    )  # из списка работодателей создаем класс вакансий
    for item_cl in list_vac_class:
        q_insert = ""
        try:
            q_insert = (
                f"insert into tab_vac (vac_id, vac_name, vac_url, sal_from, sal_to, sal_mode, sal_mode_n, "
                f"sal_cur, sn_requirement, sn_responsibility, emp_id, emp_name) values "
                f"('{item_cl.vac_idd}','{item_cl.vac_name}','{item_cl.vac_url}',{item_cl.sal_from},"
                f"{item_cl.sal_to},'{item_cl.sal_mode}','{item_cl.sal_mode_n}','{item_cl.sal_cur}',"
                f"'{item_cl.sn_req}','{item_cl.sn_res}','{item_cl.emp_idd}','{item_cl.emp_name}')"
            )
            ins_count += 1
            exec_query("vacancy_db", q_insert)
        except Exception as e:
            print(f"Ошибка вставки в tab_vac \n {q_insert}", {e})
            ins_count_err += 1
        finally:
            i += 1
    print(
        f"Вставлено вакансий: {str(ins_count)} записей из {i} записей \n Ошибок записи: {str(ins_count_err)}"
    )
    print("Вакансии записаны в emp_vac.json")

    db_manage = DBManager()
    result_list = db_manage.get_companies_and_vacancies_count("vacancy_db")
    print_top10(result_list)
    print(
        f"Список всех компаний и количество вакансий Количество: {len(result_list)}\n"
    )

    result_list = db_manage.get_all_vacancies("vacancy_db")
    print_top10(result_list)
    print(f"Список всех вакансий Количество: {len(result_list)}\n")

    result_list = db_manage.get_avg_salary("vacancy_db")
    print(f"Средняя зарплата по вакансиям: {result_list}")

    result_list = db_manage.get_vacancies_with_higher_salary("vacancy_db")
    print_top10(result_list)
    print(
        f"Список вакансий с зарплатой больше средней Количество: {len(result_list)}\n"
    )

    result_list = db_manage.get_vacancies_with_keyword("vacancy_db", "инженер")
    print_top10(result_list)
    print(f"Список вакансий с ключ словом Количество: {len(result_list)}\n")
