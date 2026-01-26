import psycopg2


def db_connect():
    #psql - h < хост > -p < порт > -d < имя_базы_данных > -U < имя_пользователя >
    conn = psycopg2.connect(
        host="localhost",
        # database="vacancy",
        user="postgres",
        password="678330",
        port="5432"
    )
    cur = conn.cursor()

    # Удаление BD
    cur.execute("DROP DATABASE vacancydb;")
    conn.commit()

    # Создание новой BD
    cur.execute("CREATE DATABASE vacancydb;")
    conn.commit()

    # Закрытие курсора и соединения
    cur.close()
    conn.close()
    #

    # # Подключение к базе данных postgres
    # conn = psycopg2.connect(
    #     dbname="postgres",
    #     user="postgres",
    #     password="password",
    #     host="localhost",
    #     port="5432"
    # )
    #
    # cur = conn.cursor()
    #
    # # Создание новой базы данных
    # cur.execute("CREATE DATABASE selecteldb;)
    # conn.commit()
    #
    # # Закрытие курсора и соединения
    # cur.close()
    # conn.close()

print("hjgjhj")
db_connect()