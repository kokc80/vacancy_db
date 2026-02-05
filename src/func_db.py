import psycopg2
from src.cl_vacancy import Vacancy


def db_connect(db_name: str):
    """Подключение или инициализация БД и таблиц"""
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
            cur.execute("CREATE TABLE tab_vac (vac_id varchar, vac_name varchar, vac_url varchar, "
                        "sal_from float, sal_to float, sal_mode varchar, sal_mode_n varchar, sal_cur varchar"
                        "sn_requirement varchar, sn_responsibility varchar, "
                        "emp_id varchar, emp_name varchar,")
            print("Таблица tab_vac создана")
        except:
            print("Ошибка создания таблицы tab_vac")
        try:
            cur.execute("CREATE TABLE tab_emp (emp_id int, emp_name varchar, emp_url varchar, emp_vac_url varchar, "
                        "open_vac int")
            print("Таблица tab_emp создана")
        except:
            print("Ошибка создания таблицы tab_emp")
        cur.close()
        conn.close()
    except:
        print("Ошибка подключения db_connect False")
    finally:
        print(f"Соединение и создание таблиц успешно c {db_name}")


def ins_tab_vac(db_name: str, list_vac_class: Vacancy()):
    """"""
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
