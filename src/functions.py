import psycopg2
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
            cur.execute("CREATE TABLE tab_emp (e_id int, e_name varchar, e_open_vac int,e_emp_url varchar, "
                        "e_vac_url varchar)")
            cur.execute("CREATE TABLE tab_vac (v_id int, v_name varchar, v_url varchar, emp_id int, "
                        "snippet_req varchar, snippet_res varchar, sal_cur varchar, sal_from float, sal_to float)")
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
    # print(emp_list)
    emp_class_list = []
    while i < len(emp_list):
        emp_list_item = emp_list[i]
        emp_class_item = Employers()
        emp_class_item.idd = emp_list_item["id"]
        emp_class_item.name = emp_list_item["name"]
        emp_class_item.emp_url = emp_list_item.get("employer",{}.get("url", "NONE"))
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
        #print(f"\n vac_load  vac_id {vac_class_item.idd}")
        vac_list_item = vac_list[i]
        vac_class_item = Vacancy()
        vac_class_item.idd = vac_list_item["id"]
        vac_class_item.name = vac_list_item["name"]
        vac_class_item.url = vac_list_item.get("url", "NONE")
        if vac_list_item.get("employer",{}.get("id", "NONE" )) is not None:
            vac_class_item.emp_id = vac_list_item.get("employer",{}.get("id", "NONE" ))
        else:
            vac_class_item.emp_id = "NONE"
        if vac_list_item.get("employer",{}.get("name", "NOne")) is not None:
            vac_class_item.emp_name = vac_list_item["employer"]["name"]
        else:
            vac_class_item.emp_name = "None"
        if vac_list_item["salary"] is not None:
            if vac_list_item.get("salary",{}.get("currency", "NON")) is not None:
                vac_class_item.sal_cur = vac_list_item.get("salary",{}.get("currency","NON"))
            else:
                vac_class_item.sal_cur = "NON"
            if vac_list_item.get("salary",{}.get("from",0)) is not None:
                vac_class_item.sal_from = vac_list_item.get("salary",{}.get("from",0))
            else:
                vac_class_item.sal_from = -1
            if vac_list_item.get("salary",{}.get("to",0)) is not None:
                vac_class_item.sal_to = vac_list_item.get("salary",{}.get("to",0))
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


def ins_tab(db_name: str, list_emp_class: list, list_vac_class: list):
    conn = psycopg2.connect(
        host="localhost",
        database=db_name,
        user="postgres",
        password="678330",
        port="5432"
    )
    conn.autocommit = True
    cur = conn.cursor()
    i = 0
    ins_count = 0
    while i < len(list_emp_class):
        try:
            q_insert = (f"INSERT INTO tab_emp (e_id, e_name, e_open_vac, e_emp_url, e_vac_url) "
                        f"VALUES ({list_emp_class[i].idd}, \'{list_emp_class[i].name}\' ,{list_emp_class[i].open_vac},"
                        f"\'{list_emp_class[i].emp_url}\', \'{list_emp_class[i].vac_url}\')")
            cur.execute(q_insert)
        except:
            print(f"{q_insert}")
            print("Ошибка вставки в tab_emp")
        finally:
            ins_count += 1
        i += 1
    print(f"Вставлено работодателей {ins_count} из {i} записей")

    i = 0
    ins_count = 0
    while i < len(list_vac_class):
        try:
            q_insert = (f"INSERT INTO tab_vac (v_id, v_name, v_url, emp_id, snippet_req, snippet_res, sal_cur, "
                        f"sal_from, sal_to) "
                        f"VALUES ({list_vac_class[i].idd}, \'{list_vac_class[i].name}\', \'{list_vac_class[i].url}\', "
                        f"{list_vac_class[i].emp_id}, \'{list_vac_class[i].sn_req}\', \'{list_vac_class[i].sn_res}\', "
                        f"\'{list_vac_class[i].sal_cur}\', {list_vac_class[i].sal_from}, {list_vac_class[i].sal_to})")
            print("emp_id", list_vac_class[i].emp_id,"\n",list_vac_class[i].name)
            emp_id_tmp = cur.execute(q_insert)
        except:
            print("Ошибка вставки в tab_vac")
            print(f"{q_insert}\n {emp_id_tmp}")
        finally:
            ins_count += 1
        i += 1
    cur.close()
    conn.close()
    print(f"Вставлено вакансий {ins_count} из {i} записей")
