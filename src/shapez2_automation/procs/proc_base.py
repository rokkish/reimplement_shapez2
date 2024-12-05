from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class ProcBase:
    name: str = "base"
    input_size: int = 0
    output_size: int = 0

    def proc(self, inp: Any) -> Any:
        raise NotImplementedError
