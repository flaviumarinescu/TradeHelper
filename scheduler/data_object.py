import pandas as pd


class Data(object):
    def __init__(self, name: str):
        self._name = name
        self._hourly = None
        self._quaterly = None
        self._daily = None
        self._levels = None

    def _check(self, value) -> bool:
        return True if isinstance(value, pd.DataFrame) else False

    def integrity(self) -> str:
        return "incomplete" if None in self.__dict__.values() else "complete"

    @property
    def name(self):
        return self._name

    @property
    def hourly(self):
        return self._hourly

    @hourly.setter
    def hourly(self, value):
        if self._check(value):
            self._hourly = value
        else:
            raise RuntimeError("Faulty hourly data for {self._name}")

    @property
    def quaterly(self):
        return self._quaterly

    @quaterly.setter
    def quaterly(self, value):
        if self._check(value):
            self._quaterly = value
        else:
            raise RuntimeError("Faulty quaterly data {self._name}")

    @property
    def daily(self):
        return self._daily

    @daily.setter
    def daily(self, value):
        if self._check(value):
            self._daily = value
        else:
            raise RuntimeError("Faulty daily data {self._name}")

    @property
    def levels(self):
        return self._levels

    @daily.setter
    def levels(self, value):
        if self._check(value):
            self._levels = value
        else:
            raise RuntimeError("Faulty levels data {self._name}")

    def __str__(self):
        print(f"{self._name}'s data is {self.integrity()}")
