from dataclasses import dataclass
from typing import Any

@dataclass
class Response:
    code: int
    message: str | None = None
    data: Any | None = None