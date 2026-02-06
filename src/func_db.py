import psycopg2


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
    except Exception as e:
        print("Ошибка подключения db_connect:", {e})
    finally:
        print("Соединение успешно")
    # Удаление BD
    try:
        cur.execute(f"DROP DATABASE {db_name};")
        print(f"Удаление БД '{db_name}' выполнено")
        cur.execute(f"CREATE DATABASE {db_name};")
        print(f"Создание БД - {db_name}")
    except Exception as e:
        print("Ошибка подключения db_connect:", {e})
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
            cur.execute(f"CREATE TABLE tab_vac (vac_id varchar, vac_name varchar, vac_url varchar, "
                        f"sal_from float, sal_to float, sal_mode varchar, sal_mode_n varchar, sal_cur varchar, "
                        f"sn_requirement varchar, sn_responsibility varchar, emp_id varchar, emp_name varchar)")
            print("Таблица tab_vac создана")
        except Exception as e:
            print("Ошибка создания tab_vac:", {e})
        try:
            cur.execute(f"CREATE TABLE tab_emp (emp_id varchar, emp_name varchar, emp_url varchar,emp_vac_url "
                        f"varchar, open_vac int)")
            print("Таблица tab_emp создана")
        except Exception as e:
            print("Ошибка создания tab_emp:", {e})
        cur.close()
        conn.close()
    except Exception as e:
        print("Ошибка подключения db_connect False", {e})
    finally:
        print(f"Соединение и создание таблиц успешно c {db_name}")


def exec_query(db_name: str, query_tmp):
    """Выполнение запроса к БД"""
    conn = psycopg2.connect(
        host="localhost",
        database=db_name,
        user="postgres",
        password="678330",
        port="5432"
    )
    conn.autocommit = True
    cur = conn.cursor()
    cur.execute(query_tmp)
    cur.close()
    conn.close()
