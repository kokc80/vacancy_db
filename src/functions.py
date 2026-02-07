from types import NoneType

import requests

from src.cl_emlpoyers import Employers
from src.cl_vacancy import Vacancy


def emp_load(emp_list: list) -> list:
    """Заполнение класса работодателей"""
    emp_class_item = Employers
    i = 0
    # print("emp_list", emp_list)

    emp_class_list = []
    for emp_list_item in emp_list:
        emp_class_item = Employers
        # emp_class_item.emp_idd = emp_list_item["id"]
        # if emp_list_item.get("employer", None) is not None:
        #     if emp_list_item.get("employer", {}).get("id", None) is not None:
        emp_class_item.emp_idd = emp_list_item["id"]
        emp_class_item.emp_name = emp_list_item["name"]
        emp_class_item.emp_url = emp_list_item["url"]
        emp_class_item.vac_url = emp_list_item.get("vacancies_url", "NONE")
        emp_class_item.open_vac = emp_list_item.get("open_vacancies", 0)
        emp_class_list.append(emp_class_item)
        i += 1
    return emp_class_list


def vac_load(vac_list: list):
    """Заполнение класса вакансий"""
    vac_class_item = Vacancy
    i = 0
    # print("Func vac_list", vac_list)
    vac_class_list = []
    while i < len(vac_list):
        vac_list_item = vac_list[i]
        vac_class_item = Vacancy
        vac_class_item.vac_idd = vac_list_item["id"]
        vac_class_item.vac_name = vac_list_item["name"]
        vac_class_item.vac_url = vac_list_item.get("url", "NONE")
        if vac_list_item.get("employer", None) is not None:
            # employers_dict = vac_list_item["employer"]
            # print("emp_dict существует",employers_dict)
            if vac_list_item.get("employer", {}).get("id", None) is not None:
                vac_class_item.emp_idd = vac_list_item["employer"]["id"]
            else:
                vac_class_item.emp_idd = 0
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
            vac_class_item.emp_idd = 0
            vac_class_item.emp_name = "Нет названия"
            vac_class_item.emp_url = "Нет ссылки"
        if vac_list_item["salary_range"] is not None:
            if vac_list_item["salary_range"]["currency"] is not None:
                vac_class_item.sal_cur = vac_list_item["salary_range"]["currency"]
            else:
                vac_class_item.sal_cur = "NON"
            if vac_list_item["salary_range"]["from"] is not None:
                vac_class_item.sal_from = vac_list_item["salary_range"]["from"]
            else:
                vac_class_item.sal_from = -1
            if vac_list_item["salary_range"]["to"] is not None:
                vac_class_item.sal_to = vac_list_item["salary_range"]["to"]
            else:
                vac_class_item.sal_mode = -1
            if vac_list_item["salary_range"]["mode"] is not None:
                vac_class_item.sal_mode = vac_list_item["salary_range"]["mode"]["id"]
            else:
                vac_class_item.sal_mode_n = ""
            if vac_list_item["salary_range"]["mode"] is not None:
                vac_class_item.sal_mode_n = vac_list_item["salary_range"]["mode"][
                    "name"
                ]
            else:
                vac_class_item.sal_mode_n = ""
        else:
            vac_class_item.sal_cur = "NON"
            vac_class_item.sal_from = -1
            vac_class_item.sal_to = -1
            vac_class_item.sal_mode = ""
            vac_class_item.sal_mode_n = ""
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
    return vac_class_list


def compile_vac_from_emp(list_emp: list):
    """Собирает вакансии работодателей"""
    i = 0
    emp_vac_list: list
    emp_vac_list = []
    for item_emp in list_emp:
        i += 1
        # сокращаем количество работодателей
        if i < 1500:
            API_headers = {"User-Agent": "HH-User-Agent"}
            API_params = {"page": 0, "per_page": 100}
            if item_emp["open_vacancies"] != 0:
                # print(f"Работодатель {i} из {i_all}\n VAC_API_URL :{item_emp["vacancies_url"]}")
                response = requests.get(
                    item_emp["vacancies_url"], headers=API_headers, params=API_params
                )
                status = response.status_code
                data_vac = response.json()
                # print("Данные вакансий", data_vac)
                if status == 200:
                    # print("connect 200")
                    emp_vac = rez_load_emp(data_vac)
                    if type(emp_vac) is not NoneType:
                        if len(emp_vac) >= 1:
                            for emp_vac_item in emp_vac:
                                emp_vac_list.append(emp_vac_item)
                else:
                    print(
                        "Ошибка при обращении к API Vac - error",
                        item_emp["vacancies_url"],
                    )
    return emp_vac_list


def rez_load_emp(vac_list):
    """Собирает вакансии работодателя по vac_url"""
    tmp_list: list
    tmp_list = []
    if "items" not in vac_list:
        result = "Нет данных 'items' на странице {self._params['page']}"
        return result
    else:
        vac_items = vac_list["items"]
        # Убираем работодателей без вакансий
        if len(vac_items) > 0:
            for vac_item in vac_items:
                # result = (
                #      f"VAC_item: {vac_item}\nVAC_print: {vac_item.get("vacancies_url", "Без URL")},"
                #      f"{vac_item.get("name", "без назв-я")}, {vac_item["snippet"]["requirement"]},"
                #      f"{vac_item["snippet"]["responsibility"]}\n"
                # )
                tmp_list.append(vac_item)
        else:
            return
    return tmp_list
