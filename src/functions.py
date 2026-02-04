from os.path import exists

import psycopg2
import requests
from src.cl_emlpoyers import Employers
from src.cl_vacancy import Vacancy


def db_connect(db_name: str):
    """Подключение или инициализация БД"""
    conn = psycopg2.connect(
        host="localhost",
        user="postgres",
        password="678330",
        port="5432")
    conn.autocommit = True
    try:
        cur = conn.cursor()
    except:
        print("Ошибка подключения db_connect True")
    finally:
        print("Соединение успешно")
    # Удаление BD
    try:
        cur.execute(f"DROP DATABASE {db_name};")
        print(f"Удаление БД '{db_name}' выполнено")
        cur.execute(f"CREATE DATABASE {db_name};")
        print(f"Создание БД - {db_name}")
    except:
        print(f"Ошибка обработки, БД -'{db_name}")
    finally:
        print(f"Инициализация БД {db_name} прошла успешно")
    # Создание новой BD
    # Закрытие курсора и соединения
    cur.close()
    conn.close()
    try:
        conn = psycopg2.connect(
            host="localhost",
            database=db_name,
            user="postgres",
            password="678330",
            port="5432")
        conn.autocommit = True
        cur = conn.cursor()
        try:
            cur.execute("CREATE TABLE tab_vac (v_id int, v_name varchar, v_url varchar, emp_id varchar, "
                        "emp_name varchar, emp_url varchar, snippet_req varchar, snippet_res varchar, sal_cur varchar, "
                        "sal_from float, sal_to float)")
            print("Таблица tab_vac создана")
        except:
            print("Ошибка создания таблицы tab_vac")
        try:
            cur.execute("CREATE TABLE tab_emp (emp_id int, emp_name varchar, emp_url varchar, emp_vac_url varchar, "
                        "open_vac int, emp_descr varchar")
            print("Таблица tab_emp создана")
        except:
            print("Ошибка создания таблицы tab_emp")
        cur.close()
        conn.close()
    except:
        print("Ошибка подключения db_connect False")
    finally:
        print(f"Соединение и создание таблиц успешно c {db_name}")


def emp_load(emp_list: list) -> Employers():
    """Заполнение класса работодателей"""
    emp_class_item = Employers()
    i = 0
    # print("emp_list", emp_list)
    emp_class_list = [Employers]
    for emp_list_item in emp_list:
        emp_class_item = Employers()
        emp_class_item.emp_idd = emp_list_item["id"]
        emp_class_item.emp_name = emp_list_item["name"]
        emp_class_item.emp_url = emp_list_item.get("employer", {}.get("url", "NONE"))
        emp_class_item.vac_url = emp_list_item.get("vacancies_url", "NONE")
        emp_class_item.open_vac = emp_list_item.get("open_vacancies", 0)
        emp_class_list.append(emp_class_item)
        i += 1
    return (emp_class_list)


def vac_load(vac_list: list):
    """Заполнение класса вакансий"""
    vac_class_item = Vacancy
    i = 0
    # print("Func vac_list", vac_list)
    vac_class_list = []
    while i < len(vac_list):
        vac_list_item = vac_list[i]
        vac_class_item = Vacancy()
        vac_class_item.idd = vac_list_item["id"]
        vac_class_item.name = vac_list_item["name"]
        vac_class_item.url = vac_list_item.get("url", "NONE")
        if vac_list_item.get("employer", None) is not None:
            # employers_dict = vac_list_item["employer"]
            # print("emp_dict существует",employers_dict)
            if vac_list_item.get("employer", {}).get("id", None) is not None:
                vac_class_item.emp_id = vac_list_item["employer"]["id"]
            else:
                vac_class_item.emp_id = 0
            if vac_list_item.get("employer", {}).get("name", None) is not None:
                vac_class_item.emp_name = vac_list_item["employer"]["name"]
            else:
                vac_class_item.emp_name = "Нет названия"
            if vac_list_item.get("employer", {}).get("url", None) is not None:
                vac_class_item.emp_url = vac_list_item["employer"]["url"]
            else:
                vac_class_item.emp_url = "Нет ссылки"
        else:
            # print("employer не существует" )
            vac_class_item.emp_id = 0
            vac_class_item.emp_name = "Нет названия"
            vac_class_item.emp_url = "Нет ссылки"
        if vac_list_item["salary"] is not None:
            if vac_list_item["salary"]["currency"] is not None:
                vac_class_item.sal_cur = vac_list_item["salary"]["currency"]
            else:
                vac_class_item.sal_cur = "NON"
            if vac_list_item["salary"]["from"] is not None:
                vac_class_item.sal_from = vac_list_item["salary"]["from"]
            else:
                vac_class_item.sal_from = -1
            if vac_list_item["salary"]["to"] is not None:
                vac_class_item.sal_to = vac_list_item["salary"]["to"]
            else:
                vac_class_item.sal_to = -1
        else:
            vac_class_item.sal_cur = "NON"
            vac_class_item.sal_from = -1
            vac_class_item.sal_to = -1
        if vac_list_item["snippet"] is not None:
            if vac_list_item["snippet"]["requirement"] is not None:
                vac_class_item.sn_req = vac_list_item["snippet"]["requirement"]
            else:
                vac_class_item.sn_req = "NONE"
            if vac_list_item["snippet"]["responsibility"] is not None:
                vac_class_item.sn_res = vac_list_item["snippet"]["responsibility"]
            else:
                vac_class_item.sn_res = "NONE"
        else:
            vac_class_item.sn_res = "NONE"
            vac_class_item.sn_req = "NONE"
        vac_class_list.append(vac_class_item)
        # print(vac_list_item,f"\nпроверка vac_load \neee id {vac_class_item.emp_id} ddd {vac_class_item.emp_name}")
        i += 1
    return (vac_class_list)


def ins_tab_vac(db_name: str, list_vac_class: Vacancy()):
    conn = psycopg2.connect(
        host="localhost",
        database=db_name,
        user="postgres",
        password="678330",
        port="5432"
    )
    print("Вакансии", len(list_vac_class))
    conn.autocommit = True
    cur = conn.cursor()
    i = 0
    ins_count = 0
    ins_count_err = 0

    # emp_class_item = Employers
    # while i < len(list_vac_class):
    #     emp_class_item.emp_idd = list_vac_class[i].emp_id
    #     emp_class_item.emp_name = list_vac_class[i].emp_name
    #     emp_class_item.emp_url = list_vac_class[i].emp_url
    #     q_insert = (f"INSERT INTO tab_emp (emp_id, emp_name, emp_url) VALUES (\'{emp_class_item.emp_idd}\', "
    #                 f"\'{emp_class_item.emp_name}\', \'{emp_class_item.emp_url}\')")
    #     try:
    #         cur.execute(q_insert)
    #         ins_count += 1
    #     except:
    #         print(f"Ошибка вставки в tab_emp1 \n {q_insert}")
    #         ins_count_err += 1
    #     finally:
    #         i += 1
    # print(f"Вставлено вакансий {ins_count} записей из {i} записей \n Ошибок записи {ins_count_err} ")
    cur.close()
    conn.close()


def load_vac_from_emp(list_emp: list):
    for item_emp in list_emp:
        API_headers = {'User-Agent': 'HH-User-Agent'}
        API_params = {'page': 0, 'per_page': 100}
        # print(item_emp)
        # print(item_emp.emp_idd, item_emp.vac_url)
        print("API_URL", item_emp["vacancies_url"])
        response = requests.get(item_emp["vacancies_url"], headers=API_headers, params=API_params)
        status = response.status_code
        data_vac = response.json()
        print(data_vac)
        if status == 200:
            # print("connect 200")
            rez_load(data_vac)
        else:
            print('Ошибка при обращении к API Vac - error', item_emp["vacancies_url"])

def rez_load(vac_list):
    """Заполнение класса работодателей"""
    i = 0
    if "items" not in vac_list:
        print(f"Нет данных 'items' на странице {self._params['page']}")

    vac_items = vac_list['items']
    for vac_item in vac_items:
        print(f"vac_iteb {vac_item["id"]},{vac_item.get("vacancies_url","Без URL")},{vac_item.get("name","без назв-я")}"
              f"{vac_item["snippet"]["requirement"]},{vac_item["snippet"]["responsibility"]}\n")
    # return (emp_class_list)
