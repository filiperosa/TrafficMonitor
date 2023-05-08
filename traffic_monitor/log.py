from typing import Optional, Type
from dataclasses import dataclass, field
import re

def optional_field():
    return field(metadata={"convert_": lambda x: x if x != "-" else None})

@dataclass
class Log:
    remotehost: str
    rfc931: Optional[str] = optional_field()
    authuser: Optional[str] = optional_field()
    timestamp: int
    request: str
    status: int
    bytes: int
    section:str = field(init=False)

    def __post_init__(self):
        # init section field
        self.section = '/' + self.request.split()[1].split('/',2)[1]