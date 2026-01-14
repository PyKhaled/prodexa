from abc import ABC, abstractmethod
from typing import Dict


class BaseAdapter(ABC):
    site: str = "*"

    @classmethod
    def matches(cls, url: str) -> bool:
        return cls.site in url

    @abstractmethod
    def fetch(self, url: str) -> str:
        """Return raw HTML"""
        raise NotImplementedError

    @abstractmethod
    def extract(self, html: str) -> Dict:
        """Return raw extracted fields"""
        raise NotImplementedError

    @abstractmethod
    def normalize(self, data: Dict) -> Dict:
        """Return normalized product"""
        raise NotImplementedError
