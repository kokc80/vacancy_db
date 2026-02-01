from abc import ABC, abstractmethod

import requests


class ParserHHE(ABC):
    """
    Класс Parser является абстрактным родительским классом
    """
    @abstractmethod
    def load_employers(self, keyword) -> None:
        pass

    @abstractmethod
    def _connect_to_api(self):
        pass


class HeadHunterEmp(ParserHHE):
    """Класс для получения работодателй с API HeadHunter"""
    def __init__(self):
        self.__url = 'https://api.hh.ru/employers'
        self._headers = {'User-Agent': 'HH-User-Agent'}
        self._params = {'text': '', 'page': 0, 'per_page': 100}
        self._employers = []

    def _connect_to_api(self):
        """Метод подключения к API"""
        # print ("connect")
        response = requests.get(self.__url, headers=self._headers, params=self._params)
        status = response.status_code
        if status == 200:
            # print("connect 200")
            return response
        else:
            return 'Ошибка при обращении к API Emp - error'

    def load_employers(self, keyword):
        """Получение списка вакансий с API"""
        self._params['text'] = keyword
        self._params['page'] = 0  # Инициализируем страницу
        all_employers = []  # Временный список для всех вакансий

        while self._params['page'] <= 200:
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
                employers_items = data['items']
                # Добавляем каждую вакансию отдельно
                for employers in employers_items:
                    all_employers.append(employers)
                # print(f"VACs page {self._params['page']}: {len(employers_items)} вакансий")
                # Если на странице нет вакансий — заканчиваем
                if len(employers_items) == 0:
                    break
                self._params['page'] += 1
            except requests.exceptions.RequestException as e:
                print(f"Ошибка запроса на странице {self._params['page']}: {e}")
                break
            except KeyError as e:
                print(f"Ошибка парсинга JSON на странице {self._params['page']}: {e}")
                break

        # Сохраняем все вакансии в атрибут класса
        self._vacancies = all_employers

        return all_employers


if __name__ == "__main__":
    hh_api = HeadHunterEmp()
    hh_api._connect_to_api()
    api_employers = hh_api.load_employers("Python")
    print("REZ parser EMPLOYERS", api_employers)
