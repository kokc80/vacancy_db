class Vacancy:
    """ класс представляет одну вакансию аттрибуты класса - части вакансии из разметки"""
    __slots__ = ['idd', 'name', 'url', 'emp_id', 'emp_name', 'sal_cur', 'sal_from', 'sal_to', 'sn_req', 'sn_res']
    idd: int
    name: str
    url: str
    emp_id: str
    emp_name: str
    sal_cur: str
    sal_from: float
    sal_to: float
    sn_req: str
    sn_res: str

    def to_dict(self):
        return {
            "idd": self.idd,
            "name": self.name,
            "url": self.url,
            "emp_id": self.emp_id,
            "emp_name": self.emp_name,
            "sal_cur": self.sal_cur,
            "sal_from": self.sal_cur,
            "sal_to": self.sal_to,
            "sn_req": self.sn_req,
            "sn_res": self.sn_res}
