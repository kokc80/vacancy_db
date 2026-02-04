from abc import ABC, abstractmethod

import requests


class ParserHHV(ABC):
    """
    Класс Parser является абстрактным родительским классом
    """
    @abstractmethod
    def load_vacancies(self, keyword) -> None:
        pass

    @abstractmethod
    def _connect_to_api(self):
        pass


class HeadHunterVac(ParserHHV):
    """Класс для получения вакансий с API HeadHunter"""
    def __init__(self):
        self.__url = 'https://api.hh.ru/vacancies'
        self._headers = {'User-Agent': 'HH-User-Agent'}
        self._params = {'text': '', 'page': 0, 'per_page': 100}
        self._vacancies = []

    def _connect_to_api(self):
        """Метод подключения к API"""
        # print ("connect")
        response = requests.get(self.__url, headers=self._headers, params=self._params)
        status = response.status_code
        if status == 200:
            # print("connect 200")
            return response
        else:
            return 'Ошибка при обращении к API Vac - error'

    def load_vacancies(self, keyword):
        """Получение списка вакансий с API"""
        self._params['text'] = keyword
        self._params['page'] = 0  # Инициализируем страницу
        all_vacancies = []  # Временный список для всех вакансий

        while self._params['page'] < 2:
            try:
                response = requests.get(
                    self.__url,
                    headers=self._headers,
                    params=self._params
                )
                response.raise_for_status()  # Проверяем HTTP-статус
                data = response.json()
                # Проверяем наличие 'items' в ответе
                if 'items' not in data:
                    print(f"Нет данных 'items' на странице {self._params['page']}")
                    break
                vacancies_items = data['items']
                # Добавляем каждую вакансию отдельно
                for vacancy in vacancies_items:
                    all_vacancies.append(vacancy)
                # print(f"VACs page {self._params['page']}: {len(vacancies_items)} вакансий")
                # Если на странице нет вакансий — заканчиваем
                if len(vacancies_items) == 0:
                    break
                self._params['page'] += 1
            except requests.exceptions.RequestException as e:
                print(f"Ошибка запроса на странице {self._params['page']}: {e}")
                break
            except KeyError as e:
                print(f"Ошибка парсинга JSON на странице {self._params['page']}: {e}")
                break
        # Сохраняем все вакансии в атрибут класса
        self._vacancies = all_vacancies
        return self._vacancies

if __name__ == "__main__":
    hh_api = HeadHunterVac()
    hh_api._connect_to_api()
    api_vacantions = hh_api.load_vacancies("Python")
    print("REZ parser  VACANTIONS", api_vacantions)

