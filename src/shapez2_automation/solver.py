from .schemas import *
from typing import TypeGuard, Any


class Shapez2Solver:
    """図形を生成するproc群を求める"""

    procs: list[str] = []

    def __init__(
        self,
        source: Shapez2Type,
    ) -> None:
        self.source = source

    def solve(self):
        return self.procs
