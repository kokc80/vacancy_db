import psycopg2


def db_connect(db_name: str):
    try:
        conn = psycopg2.connect(
            host="localhost",
            # database="vacancy",
            user="postgres",
            password="678330",
            port="5432"
        )
        conn.autocommit = True
    except:
        print("Ошибка подключения")
    finally:
        print("Соединение успешно")

    db_name="vacancy_db"
    cur = conn.cursor()

    # Удаление BD
    try:
        cur.execute(f"DROP DATABASE {db_name};")
        print(f"Удаление БД '{db_name}' выполнено")
    except:
        print(f"Удаление БД не требуется, БД -'{db_name}' не существует")
    finally:
        print("OK")
    # Создание новой BD
    cur.execute(f"CREATE DATABASE {db_name};")
    print(f"Создание БД - {db_name}")

    # Закрытие курсора и соединения
    cur.close()
    conn.close()
