class Vacancy:
    """класс представляет одну вакансию"""

    __slots__ = [
        "vac_idd",
        "vac_name",
        "vac_url",
        "sal_from",
        "sal_to",
        "sal_mode",
        "sal_mode_n",
        "sal_cur",
        "sn_req",
        "sn_res",
        "emp_idd",
        "emp_name",
        "emp_url",
        "open_vac",
    ]
    vac_idd: str
    vac_name: str
    vac_url: str
    sal_from: float
    sal_to: float
    sal_mode: str
    sal_mode_n: str
    sal_cur: str
    sn_req: str
    sn_res: str
    emp_idd: str
    emp_name: str
    emp_url: str
    open_vac: int

    def to_dict(self):
        return {
            "vac_idd": self.vac_idd,
            "vac_name": self.vac_name,
            "vac_url": self.vac_url,
            "sal_from": self.sal_cur,
            "sal_to": self.sal_to,
            "sal_mode": self.sal_mode,
            "sal_mode_n": self.sal_mode_n,
            "sal_cur": self.sal_cur,
            "sn_req": self.sn_req,
            "sn_res": self.sn_res,
            "emp_idd": self.emp_idd,
            "emp_name": self.emp_name,
            "emp_url": self.emp_url,
            "open_vac": self.open_vac,
        }

    def __init__(self):
        self.vac_idd = None  # Инициализируем как None или пустую строку
        self.vac_name = ""
        self.vac_url = ""
        self.sal_from = 0
        self.sal_to = 0
        self.sal_mode = ""
        self.sal_mode_n = ""
        self.sal_cur = ""
        self.sn_req = ""
        self.sn_res = ""
        self.emp_idd = None
        self.emp_name = ""
        self.emp_url = ""

    def __str__(self):
        return f"vac_id,name: {self.vac_idd},{self.vac_name};\n   emp_id,name: {self.emp_idd},{self.emp_name}"
