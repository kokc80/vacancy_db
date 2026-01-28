import psycopg2
from src.cl_emlpoyers import Employers


def db_connect(db_name: str, init_db: bool):
    """Подключение или инициализация БД"""
    if init_db is True:
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
    else:
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
                print("Таблицы созданы")
            except:
                print("Ошибка создания таблиц")
            cur.close()
            conn.close()
        except:
            print("Ошибка подключения db_connect False")
        finally:
            print(f"Соединение успешно c {db_name}")


def emp_load(emp_list: list):
    """Заполнение класса работодателей"""
    emp_class_item = Employers
    i = 0
    emp_class_list = []
    while i < len(emp_list):
        emp_list_item = emp_list[i]
        emp_class_item=Employers()
        emp_class_item.idd = emp_list_item["id"]
        emp_class_item.name = emp_list_item["name"]
        emp_class_item.emp_url = emp_list_item["url"]
        emp_class_item.vac_url = emp_list_item.get("vacancies_url","NONE")
        emp_class_item.open_vac = emp_list_item.get("open_vacancies",0)
        emp_class_list.append(emp_class_item)
        i += 1
    return (emp_class_list)


def insert_emp(db_name: str, list_emp_class: list):
    i = 0
    while i < len(list_emp_class):
        print(list_emp_class[i].idd,
              list_emp_class[i].name,
              list_emp_class[i].emp_url,
              list_emp_class[i].vac_url,
              list_emp_class[i].open_vac)
        i += 1
