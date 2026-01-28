class Vacancy:
    """ класс представляет одну вакансию аттрибуты класса - части вакансии из разметки"""
    __slots__ = ['idd', 'name', 'url', 'company', 'title', 'employment_form', 'salary_cur', 'salary_from', 'salary_to',
                 'required_skills', 'location', 'description']
    idd: int
    name: str
    url: str
    company: str
    title: str
    employment_form: str
    sal_cur: str
    sal_from: float
    sal_to: float
    required_skills: str
    location: str
    description: str
