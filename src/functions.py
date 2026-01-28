import psycopg2
from src.cl_emlpoyers import Employers
from src.cl_vacancy import Vacancy


def db_connect(db_name: str):
    """Подключение или инициализация БД"""
    conn = psycopg2.connect(
        host="localhost",
        user="postgres",
        password="678330",
        port="5432"
        )
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
    except:
        print(f"Удаление БД не требуется, БД -'{db_name}' не существует")
    finally:
        print(f"Инициализация БД {db_name} прошла успешно")
    # Создание новой BD
    cur.execute(f"CREATE DATABASE {db_name};")
    print(f"Создание БД - {db_name}")
    # Закрытие курсора и соединения
    cur.close()
    conn.close()
    try:
        conn = psycopg2.connect(
            host="localhost",
            database=db_name,
            user="postgres",
            password="678330",
            port="5432"
            )
        conn.autocommit = True
        cur = conn.cursor()
        try:
            cur.execute("CREATE TABLE tab_emp (e_id int, e_name varchar, e_open_vac int,e_emp_url varchar, "
                        "e_vac_url varchar)")
            cur.execute("CREATE TABLE tab_vac (v_id int, v_name varchar, v_url varchar, snippet_req varchar, "
                        "snippet_res varchar)")
            print("Таблицы созданы")
        except:
            print("Ошибка создания таблиц")
        cur.close()
        conn.close()
    except:
        print("Ошибка подключения db_connect False")
    finally:
        print(f"Соединение и создание таблиц успешно c {db_name}")


def emp_load(emp_list: list):
    """Заполнение класса работодателей"""
    emp_class_item = Employers
    i = 0
    emp_class_list = []
    while i < len(emp_list):
        emp_list_item = emp_list[i]
        emp_class_item = Employers()
        emp_class_item.idd = emp_list_item["id"]
        emp_class_item.name = emp_list_item["name"]
        emp_class_item.emp_url = emp_list_item["url"]
        emp_class_item.vac_url = emp_list_item.get("vacancies_url", "NONE")
        emp_class_item.open_vac = emp_list_item.get("open_vacancies", 0)
        emp_class_list.append(emp_class_item)
        i += 1
    return (emp_class_list)


def vac_load(vac_list: list):
    """Заполнение класса работодателей"""
    vac_class_item = Vacancy
    i = 0
    vac_class_list = []
    while i < len(vac_list):
        vac_list_item = vac_list[i]
        vac_class_item = Vacancy()
        vac_class_item.idd = vac_list_item["id"]
        vac_class_item.name = vac_list_item["name"]
        vac_class_item.url = vac_list_item.get("url", "NONE")
        vac_class_item.emp_id = vac_list_item.get("employer",{}.get("id",0))
        vac_class_item.emp_name = vac_list_item.get("employer",{}.get("name",0))
        # if vacancy_item["salary"] is not None:
        #     if vacancy_item["salary"]["currency"] is not None:
        #         vacancy_class.salary_cur = vacancy_item["salary"]["currency"]
        #     else:
        #         vacancy_class.salary_cur = "не определено"
        #     if vacancy_item["salary"]["from"] is not None:
        #         vacancy_class.salary_from = vacancy_item["salary"]["from"]
        #     else:
        #         vacancy_class.salary_from = 0
        #     if vacancy_item["salary"]["to"] is not None:
        #         vacancy_class.salary_to = vacancy_item["salary"]["to"]
        #     else:
        #         vacancy_class.salary_to = 0
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
        vac_class_item.sn_req = vac_list_item.get("snippet",{}.get("requirement","NONE"))
        vac_class_item.sn_res = vac_list_item.get("snippet",{}.get("responsibility","NONE"))
        vac_class_list.append(vac_class_item)
        i += 1
    return (vac_class_list)

def ins_emp(db_name: str, list_emp_class: list):
    i = 0
    while i < len(list_emp_class):
        print(list_emp_class[i].idd,
              list_emp_class[i].name,
              list_emp_class[i].emp_url,
              list_emp_class[i].vac_url,
              list_emp_class[i].open_vac)
        i += 1

def ins_vac(db_name: str, list_vac_class: list):
    i = 0
    while i < len(list_vac_class):
        print(list_vac_class[i].idd,
              list_vac_class[i].name,
              list_vac_class[i].url,
              list_vac_class[i].sal_cur,
              list_vac_class[i].sal_from,
              list_vac_class[i].sal_to,
              list_vac_class[i].sn_req,
              list_vac_class[i].sn_res
              )
        i += 1
