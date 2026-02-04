class Employers:
    __slots__ = ['emp_idd', 'emp_name', 'emp_url', 'vac_url', 'open_vac','descr']
    """Класс работодателей"""
    emp_idd: str
    emp_name: str
    emp_url: str  # alternate_url
    vac_url: str  # vacancies_url
    open_vac: int  # open_vacancies
    descr: str

    def to_dict(self):
        return {
            "emp_idd": self.emp_idd,
            "emp_name": self.emp_name,
            "emp_url": self.emp_url,
            "vac_url": self.vac_url,
            "open_vac": self.open_vac,
            "descr": self.descr
        }

    def __str__(self):
        return f"Класс Emp Idd:{self.emp_idd}, name:{self.emp_name}, URL:{self.vac_url}"

    def __init__(self):
        self.emp_idd = None      # Инициализируем как None или пустую строку
        self.emp_name = ""
        self.emp_url = ""
        self.vac_url = ""
        self.open_vac = 0
        self.descr = ""