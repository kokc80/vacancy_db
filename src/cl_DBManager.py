class DBManager:

    def get_companies_and_vacancies_count(self):
        """получает список всех компаний и количество вакансий у каждой компании."""
        conn = psycopg2.connect(host="localhost", database=db_name, user="postgres", password="678330", port="5432")
        conn.autocommit = True
        cur = conn.cursor()
        tmp_quwery = "SELECT count(*) tab_emp"
        # cur.execute(tmp_quwery)

        tmp_quwery = "SELECT count(*) from tab_emp"
        # cur.execute(tmp_quwery)

    def get_all_vacancies(self):
        """получает список всех вакансий с указанием наз-я компании, наз-я вакансии и зарплаты и ссылки на вакансию."""
        pass

    def get_avg_salary(self):
        """получает среднюю зарплату по вакансиям."""
        pass

    def get_vacancies_with_higher_salary(self):
        """получает список всех вакансий, у которых зарплата выше средней по всем вакансиям."""
        pass

    def get_vacancies_with_keyword(self):
        """получает список всех вакансий, в названии которых содержатся переданные в метод слова, например python."""
        pass
