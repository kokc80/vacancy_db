import pytest

from src.cl_emlpoyers import Employers
from src.cl_vacancy import Vacancy
from src.functions import emp_load, vac_load, rez_load_emp


def test_emp_load():
    # Входные данные
    mock_data = [
        {
            "id": "991",
            "name": "Name_1",
            "open_vacancies": 0,
            "url": "e_url1",
            "vacancies_url": "v_url1",
        },
        {
            "id": "992",
            "name": "Name_2",
            "open_vacancies": 5,
            "url": "e_url2",
            "vacancies_url": "v_url2",
        },
    ]

    # Ожидаемые объекты (с заполненными полями)
    expected_objects = []
    for item in mock_data:
        emp = Employers()
        emp.emp_idd = item["id"]
        emp.emp_name = item["name"]
        emp.emp_url = item["url"]
        emp.vac_url = item.get("vacancies_url", "NONE")
        emp.open_vac = item.get("open_vacancies", 0)
        expected_objects.append(emp)

    # Вызов функции
    result = emp_load(mock_data)

    # Проверка: количество объектов
    assert len(result) == len(expected_objects)

    # Проверка полей каждого объекта
    for i, obj in enumerate(result):
        assert obj.emp_idd == expected_objects[i].emp_idd
        assert obj.emp_name == expected_objects[i].emp_name
        assert obj.emp_url == expected_objects[i].emp_url
        assert obj.vac_url == expected_objects[i].vac_url
        assert obj.open_vac == expected_objects[i].open_vac


test_vac1 = Vacancy
test_vac1.vac_idd = "129559101"
test_vac1.vac_name = "vac_name_101"
test_vac1.vac_url = "vac_url_101"
test_vac1.sal_cur = "RUR"
test_vac1.sal_from = -1
test_vac1.sal_mode = "MONTH"
test_vac1.sal_mode_n = "За месяц"
test_vac1.sal_to = 90000
test_vac1.sn_req = "sn_req_101"
test_vac1.sn_res = "sn_res_101"
test_vac1.emp_idd = "129559101"
test_vac1.emp_name = "Аэропорт Якутск1"
test_vac1.emp_url = "emp_url_101"

def test_vac_load():
    # Входные данные
    mock_data = [
        {
            "id": "129559101", "name": "vac_name_101", "url": "vac_url_101",
            "salary_range": {"currency": "RUR", "from": 0, "mode": {"id": "MONTH", "name": "За месяц"}, "to": 1000},
            "snippet": {"requirement": "sn_req_101", "responsibility": "sn_res_101"},
            "employer": {"id": "101", "name": "ООО Якутск1", "url": "emp_url_101", "vacancies_url": "emp_vacurl_101"},
        },
    ]

    # Ожидаемые объекты (с заполненными полями)
    expected_objects = []
    for item in mock_data:
        vac = Vacancy
        vac.vac_idd = item["id"]
        vac.vac_name = item["name"]
        vac.vac_url = item["url"]
        vac.sal_cur = item["salary_range"]["currency"]
        vac.sal_from = item["salary_range"]["from"]
        vac.sal_mode = item["salary_range"]["mode"]["id"]
        vac.sal_mode_n = item["salary_range"]["mode"]["name"]
        vac.sal_to = item["salary_range"]["to"]
        vac.emp_idd = item["employer"]["id"]
        vac.emp_name = item["employer"]["name"]
        vac.emp_url = item["employer"]["url"]
        expected_objects.append(vac)

    # Вызов функции
    result = vac_load(mock_data)

    # Проверка: количество объектов
    assert len(result) == len(expected_objects)

    # Проверка полей каждого объекта
    for i, obj in enumerate(result):
        assert obj.emp_idd == expected_objects[i].emp_idd
        assert obj.vac_name == expected_objects[i].vac_name
        assert obj.vac_url == expected_objects[i].vac_url
        assert obj.open_vac == expected_objects[i].open_vac


class TestRezLoadEmp:
    def test_missing_items_key(self):
        """Тест: отсутствует ключ 'items' в входном словаре"""
        vac_list = {"other_key": "value"}
        result = rez_load_emp(vac_list)

        assert isinstance(result, str)
        assert "Нет данных 'items'" in result

    def test_empty_items_list(self):
        """Тест: 'items' присутствует, но список пуст"""
        vac_list = {"items": []}
        result = rez_load_emp(vac_list)

        assert result is None

    def test_single_vacancy_item(self):
        """Тест: один элемент в 'items'"""
        vac_list = {
            "items": [
                {
                    "vacancies_url": "https://example.com/vac/1",
                    "name": "Python Developer",
                    "snippet": {
                        "requirement": "Опыт 3+ года",
                        "responsibility": "Разработка API"
                    }
                }
            ]
        }

        result = rez_load_emp(vac_list)

        assert isinstance(result, list)
        assert len(result) == 1
        assert result[0] == vac_list["items"][0]

    def test_multiple_vacancy_items(self):
        """Тест: несколько элементов в 'items'"""
        vac_list = {
            "items": [
                {
                    "vacancies_url": "https://example.com/vac/1",
                    "name": "Python Developer",
                    "snippet": {
                        "requirement": "Опыт 3+ года",
                        "responsibility": "Разработка API"
                    }
                },
                {
                    "vacancies_url": "https://example.com/vac/2",
                    "name": "QA Engineer",
                    "snippet": {
                        "requirement": "Знание SQL",
                        "responsibility": "Тестирование API"
                    }
                }
            ]
        }

        result = rez_load_emp(vac_list)

        assert isinstance(result, list)
        assert len(result) == 2
        assert result[0] == vac_list["items"][0]
        assert result[1] == vac_list["items"][1]

    def test_missing_vacancies_url(self):
        """Тест: отсутствует 'vacancies_url' в item"""
        vac_list = {
            "items": [
                {
                    "name": "Python Developer",
                    "snippet": {
                        "requirement": "Опыт 3+ года",
                        "responsibility": "Разработка API"
                    }
                }
            ]
        }

        result = rez_load_emp(vac_list)

        assert isinstance(result, list)
        assert len(result) == 1
        # Проверяем, что item добавлен, несмотря на отсутствие vacancies_url
        assert "vacancies_url" not in result[0]

    def test_missing_name(self):
        """Тест: отсутствует 'name' в item"""
        vac_list = {
            "items": [
                {
                    "vacancies_url": "https://example.com/vac/1",
                    "snippet": {
                        "requirement": "Опыт 3+ года",
                        "responsibility": "Разработка API"
                    }
                }
            ]
        }

        result = rez_load_emp(vac_list)

        assert isinstance(result, list)
        assert len(result) == 1
        # Проверяем, что item добавлен, несмотря на отсутствие name
        assert "name" not in result[0]

    def test_missing_snippet(self):
        """Тест: отсутствует 'snippet' в item"""
        vac_list = {
            "items": [
                {
                    "vacancies_url": "https://example.com/vac/1",
                    "name": "Python Developer"
                }
            ]
        }
        result = rez_load_emp(vac_list)
        assert isinstance(result, list)
        assert len(result) == 1
        # Проверяем, что item добавлен, несмотря на отсутствие snippet
        assert "snippet" not in result[0]

    def test_none_input(self):
        """Тест: входной аргумент None"""
        with pytest.raises(TypeError):
            rez_load_emp(None)

    def test_deep_nested_structure(self):
        """Тест: сложная вложенная структура внутри items"""
        vac_list = {
			"items": [
				{
					"vacancies_url": "https://example.com/vac/1",
					"name": "Python Developer",
					"snippet": {
						"requirement": "Глубокие знания Python",
						"responsibility": "Архитектура микросервисов",
						"additional": {
							"stack": ["FastAPI", "PostgreSQL"],
							"team": "5 человек"
						}
					},
					"metadata": {
						"created": "2023-01-01",
						"updated": "2023-01-15"
					}
				}
			]
		}

        result = rez_load_emp(vac_list)

        assert isinstance(result, list)
        assert len(result) == 1
        assert result[0] == vac_list["items"][0]
