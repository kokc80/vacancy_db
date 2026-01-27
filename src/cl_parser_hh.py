# временный файл
from abc import ABC, abstractmethod

import requests


class ParserHH(ABC):
    """
    Класс Parser является абстрактным родительским классом
    """
    @abstractmethod
    def load_items(self, keyword) -> None:
        pass

    @abstractmethod
    def _connect_to_api(self):
        pass


class HeadHunterVac(ParserHH):
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
            #print("connect 200")
            return response
        else:
            return 'Ошибка при обращении к API - error'

    def load_items(self, keyword):
        """Получение списка вакансий"""
        self._params['text'] = keyword
        while self._params.get('page') != 2:
            # print("PAGE", self.params.get('page'))
            response = requests.get(self.__url, headers=self._headers, params=self._params)
            vacancies_items = response.json()['items']
            # print("VAC\n", vacancies_items)
            self._vacancies.extend(vacancies_items)
            self._params['page'] += 1
            return vacancies_items

if __name__ == "__main__":
    hh_api = HeadHunterVac()
    hh_api._connect_to_api()
    api_vacantions = hh_api.load_vacancies("Python")
    print("REZ  VACANTIONS", api_vacantions)

