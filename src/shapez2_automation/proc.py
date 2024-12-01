from shapez2_automation.schemas import Shapez2MultiLayer
from .schemas import *
from typing import Any


class Shapez2Proc:
    """primitiveな図形の加工屋さん"""

    procs: list[str] = []

    def __init__(self) -> None:
        self.callback = {
            "copy": copy,
            "colorize": colorize,
            "crystarize": crystarize,
            "pin": pin,
            "rotate": rotate,
            "rotate_rev": rotate_rev,
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


def copy(inp: Any) -> Shapez2Type:
    "入力図形をそのまま出力する"
    return inp


def colorize(inp: Any) -> Shapez2Type:
    return inp


def crystarize(inp: Any) -> Shapez2Type:
    return inp


def pin(inp: Any) -> Shapez2Type:
    return inp


def rotate(inp: Shapez2MultiLayer) -> Shapez2Type:
    "右に90度回転"
    ret_mlayer = []
    ret_layer = []
    for layer in inp.mlayer:
        ret_layer = [
            layer.layer[2],
            layer.layer[0],
            layer.layer[3],
            layer.layer[1],
        ]
        ret_mlayer.append(Shapez2Layer(ret_layer))
    return Shapez2MultiLayer(ret_mlayer)


def rotate_rev(inp: Shapez2MultiLayer) -> Shapez2MultiLayer:
    "左に90度回転"
    ret_mlayer = []
    ret_layer = []
    for layer in inp.mlayer:
        ret_layer = [
            layer.layer[1],
            layer.layer[3],
            layer.layer[0],
            layer.layer[2],
        ]
        ret_mlayer.append(Shapez2Layer(ret_layer))
    return Shapez2MultiLayer(ret_mlayer)


def separate(inp: Any) -> Shapez2Type:
    return inp


def swap(inp: Any) -> Shapez2Type:
    return inp


def merge(inp: Any) -> Shapez2Type:
    return inp


def merge_flat(inp: Any) -> Shapez2Type:
    return inp


def merge_laminate(inp: Any) -> Shapez2Type:
    return inp
