from dataclasses import dataclass

@dataclass
class IRequest:
    id: str
    url: str
    param: dict
    expiration_date: int
    method: str
    wait: float = 1.1
    jscript: str = ""

@dataclass
class IPageResult:
    id: str
    method: str
