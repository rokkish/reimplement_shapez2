from .schemas import *
from typing import Union, TypeGuard, Any


class Shapez2Proc:
    """primitiveな図形の加工屋さん"""

    procs: list[str] = []

    def __init__(self) -> None:
        self.callback = {
            "colorize": colorize,
            "crystarize": crystarize,
            "pin": pin,
            "rotate": rotate,
            "separate": separate,
            "swap": swap,
            "merge": merge,
            "merge_flat": merge_flat,
            "merge_laminate": merge_laminate,
        }

    def add_proc(self, *args, **kwargs) -> None:
        if isinstance(kwargs["proc"], list):
            for p in kwargs["proc"]:
                self.procs.append(p)
            if not isinstance(p, str):
                raise ValueError(f"{p} must be str")
        elif isinstance(p := kwargs["proc"], str):
            self.procs.append(p)
        else:
            raise ValueError(f"{kwargs["proc"]} must be str or list[str]")

    def run(self, *args, **kwargs) -> Shapez2Type:
        inp = kwargs["shapez_string"]
        for p in self.procs:
            inp = self.callback[p](inp)
        return inp


def colorize(inp: Any) -> TypeGuard[Shapez2Type]:
    return inp


def crystarize(inp: Any) -> TypeGuard[Shapez2Type]:
    return inp


def pin(inp: Any) -> TypeGuard[Shapez2Type]:
    return inp


def rotate(inp: Any) -> TypeGuard[Shapez2Type]:
    return inp


def separate(inp: Any) -> TypeGuard[Shapez2Type]:
    return inp


def swap(inp: Any) -> TypeGuard[Shapez2Type]:
    return inp


def merge(inp: Any) -> TypeGuard[Shapez2Type]:
    return inp


def merge_flat(inp: Any) -> TypeGuard[Shapez2Type]:
    return inp


def merge_laminate(inp: Any) -> TypeGuard[Shapez2Type]:
    return inp
