from typing import Optional, Type
from dataclasses import dataclass, field
import re

@dataclass
class Log:
    """ log of HTTP request """

    remotehost: str
    rfc931: Optional[str]
    authuser: Optional[str]
    timestamp: int
    request: str
    status: int
    bytes: int
    section:str = field(init=False)

    def __post_init__(self):
        # init section field
        self.section = '/' + self.request.split()[1].split('/',2)[1]