class Employers:
    __slots__ = ['idd', 'name', 'open_vac', 'emp_url', 'vac_url']
    """Класс работодателей"""
    idd: int
    name: str
    open_vac: int  # open_vacancies
    emp_url: str  # alternate_url
    vac_url: str  # vacancies_url

    def to_dict(self):
        return {
            "idd": self.idd,
            "name": self.name,
            "open_vac": self.open_vac,
            "emp_url": self.emp_url,
            "vac_url": self.vac_url
        }

    def __str__(self):
        return f"Класс Emp Idd:{self.idd}, name:{self.name}"
