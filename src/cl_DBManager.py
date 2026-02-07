from abc import ABC, abstractmethod

import psycopg2

from src.func_db import db_connect


class DBClass(ABC):
    @abstractmethod
    def get_companies_and_vacancies_count(self):
        pass

    @abstractmethod
    def get_all_vacancies(self):
        pass

    @abstractmethod
    def get_avg_salary(self):
        pass

    @abstractmethod
    def get_vacancies_with_higher_salary(self):
        pass

    @abstractmethod
    def get_vacancies_with_keyword(self):
        pass


class DBManager(DBClass):
    def get_companies_and_vacancies_count(self, db_name: str):
        """получает список всех компаний и количество вакансий у каждой компании."""
        conn = psycopg2.connect(
            host="localhost",
            database=db_name,
            user="postgres",
            password="678330",
            port="5432",
        )
        conn.autocommit = True
        cur = conn.cursor()
        tmp_query = (
            f"SELECT tv.vac_id,tv.vac_name,te.emp_id,te.emp_name FROM tab_vac as tv, tab_emp as te "
            f"where tv.emp_id = te.emp_id"
        )
        tmp_query = (
            f"SELECT tv.emp_id, te.emp_name, count(vac_id) FROM tab_vac as tv "
            f"INNER JOIN tab_emp as te ON tv.emp_id = te.emp_id "
            f"group by tv.emp_id, te.emp_name"
        )
        cur.execute(tmp_query)
        result_sql = cur.fetchall()
        cur.close()
        conn.close()
        return result_sql

    def get_all_vacancies(self, db_name: str):
        """получает список всех вакансий с указанием наз-я компании, наз-я вакансии и зарплаты и ссылки на вакансию."""
        conn = psycopg2.connect(
            host="localhost",
            database=db_name,
            user="postgres",
            password="678330",
            port="5432",
        )
        conn.autocommit = True
        cur = conn.cursor()
        tmp_query = (
            f"select tv.vac_name, te.emp_name, tv.sal_from, tv.sal_to, tv.sal_cur, tv.vac_url "
            f"from tab_vac as tv, tab_emp as te where tv.emp_id = te.emp_id"
        )
        cur.execute(tmp_query)
        result_sql = cur.fetchall()
        cur.close()
        conn.close()
        return result_sql

    def get_avg_salary(self, db_name: str):
        """получает среднюю зарплату по вакансиям."""
        conn = psycopg2.connect(
            host="localhost",
            database=db_name,
            user="postgres",
            password="678330",
            port="5432",
        )
        conn.autocommit = True
        cur = conn.cursor()
        tmp_query = "select AVG(tv.sal_to), AVG(tv.sal_from) from tab_vac as tv"
        cur.execute(tmp_query)
        result_sql = cur.fetchall()
        cur.close()
        conn.close()
        return result_sql

    def get_vacancies_with_higher_salary(self, db_name: str):
        """получает список всех вакансий, у которых зарплата выше средней по всем вакансиям."""
        conn = psycopg2.connect(
            host="localhost",
            database=db_name,
            user="postgres",
            password="678330",
            port="5432",
        )
        conn.autocommit = True
        cur = conn.cursor()
        tmp_query = (
            f"select tv.vac_name, tv.sal_from, tv.sal_to, tv.sal_cur, tv.vac_url from tab_vac as tv "
            f"where tv.sal_from > (select (AVG(atv.sal_to) + AVG(atv.sal_from))/2 from tab_vac as atv)"
        )
        cur.execute(tmp_query)
        result_sql = cur.fetchall()
        cur.close()
        conn.close()
        return result_sql

    def get_vacancies_with_keyword(self, db_name: str, keyword: str):
        """получает список всех вакансий, в названии которых содержатся переданные в метод слова, например python."""
        conn = psycopg2.connect(
            host="localhost",
            database=db_name,
            user="postgres",
            password="678330",
            port="5432",
        )
        conn.autocommit = True
        cur = conn.cursor()
        tmp_query = (
            f"select tv.vac_name, tv.sal_from, tv.sal_to, tv.sal_cur, tv.vac_url "
            f"from tab_vac as tv where lower(tv.vac_name) like '%{keyword.lower()}%'"
            ""
        )
        print(tmp_query)
        cur.execute(tmp_query)
        result_sql = cur.fetchall()
        cur.close()
        conn.close()
        return result_sql


if __name__ == "__main__":
    db_connect("vacancy_db")
    db_manage = DBManager()
    result_list = db_manage.get_companies_and_vacancies_count("vacancy_db")
    for row in result_list:
        print(row)
    print(
        f"Список всех компаний и количество вакансий Количество: {len(result_list)}\n"
    )

    result_list = db_manage.get_all_vacancies("vacancy_db")
    for row in result_list:
        print(row)
    print(f"Список всех вакансий Количество: {len(result_list)}\n")

    result_list = db_manage.get_avg_salary("vacancy_db")
    for row in result_list:
        avg_sal = round((row[0] + row[1]) / 2, 2)
    print(f"Средняя зарплата по вакансиям: {avg_sal}")

    result_list = db_manage.get_vacancies_with_higher_salary("vacancy_db")
    for row in result_list:
        print(row)
    print(
        f"Список вакансий с зарплатой больше средней Количество: {len(result_list)}\n"
    )

    result_list = db_manage.get_vacancies_with_keyword("vacancy_db", "инженер")
    for row in result_list:
        print(row)
    print(f"Список вакансий с ключ словом Количество: {len(result_list)}\n")
