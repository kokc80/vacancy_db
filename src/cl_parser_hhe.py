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
        """Получение списка работодателей"""
        self._params['text'] = keyword
        while self._params.get('page') != 20:
            response = requests.get(self.__url, headers=self._headers, params=self._params)
            employers_items = response.json()['items']
            # print("EMP\n", employers_items)
            self._employers.append(employers_items)
            self._params['page'] += 1
            return employers_items


if __name__ == "__main__":
    hh_api = HeadHunterEmp()
    hh_api._connect_to_api()
    api_employers = hh_api.load_employers("000")
    print("REZ parser EMPLOYERS", api_employers)
