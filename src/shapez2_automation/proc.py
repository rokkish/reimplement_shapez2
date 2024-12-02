from shapez2_automation.schemas import Shapez2MultiLayer
from shapez2_automation.parse import parse_shapez2
from .schemas import *
from typing import Any, Tuple, TypeAlias, Dict, Union

Shapez2MultiLayers: TypeAlias = Tuple[Shapez2MultiLayer, Shapez2MultiLayer]


class Shapez2Proc:
    """primitiveな図形の加工屋さん"""

    procs: list[str] = []

    def __init__(self) -> None:
        self.callback: Dict[str, Dict[str, Union[function, Tuple]]] = {
            "copy_1in1out": {
                "proc": copy_1to1,
                "shape": (1, 1),
            },
            "copy_1in2out": {
                "proc": copy_1to2,
                "shape": (1, 2),
            },
            "copy_2in1out": {
                "proc": copy_2to1,
                "shape": (2, 1),
            },
            "colorize_RED": {
                "proc": colorize_RED,
                "shape": (1, 1),
            },
            "colorize_GREEN": {
                "proc": colorize_GREEN,
                "shape": (1, 1),
            },
            "colorize_BLUE": {
                "proc": colorize_BLUE,
                "shape": (1, 1),
            },
            "colorize_PURPLE": {
                "proc": colorize_PURPLE,
                "shape": (1, 1),
            },
            "colorize_CYAN": {
                "proc": colorize_CYAN,
                "shape": (1, 1),
            },
            "colorize_YELLOW": {
                "proc": colorize_YELLOW,
                "shape": (1, 1),
            },
            "colorize_WHITE": {
                "proc": colorize_WHITE,
                "shape": (1, 1),
            },
            "crystarize_RED": {
                "proc": crystarize_RED,
                "shape": (1, 1),
            },
            "crystarize_GREEN": {
                "proc": crystarize_GREEN,
                "shape": (1, 1),
            },
            "crystarize_BLUE": {
                "proc": crystarize_BLUE,
                "shape": (1, 1),
            },
            "crystarize_PURPLE": {
                "proc": crystarize_PURPLE,
                "shape": (1, 1),
            },
            "crystarize_CYAN": {
                "proc": crystarize_CYAN,
                "shape": (1, 1),
            },
            "crystarize_YELLOW": {
                "proc": crystarize_YELLOW,
                "shape": (1, 1),
            },
            "crystarize_WHITE": {
                "proc": crystarize_WHITE,
                "shape": (1, 1),
            },
            "pin": {
                "proc": pin,
                "shape": (1, 1),
            },
            "rotate_90": {
                "proc": rotate_90,
                "shape": (1, 1),
            },
            "rotate_180": {
                "proc": rotate_180,
                "shape": (1, 1),
            },
            "rotate_270": {
                "proc": rotate_270,
                "shape": (1, 1),
            },
            "separate": {
                "proc": separate,
                "shape": (1, 2),
            },
            "swap": {
                "proc": swap,
                "shape": (2, 2),
            },
            "merge": {
                "proc": merge,
                "shape": (2, 1),
            },
            "merge_flat": {
                "proc": merge_flat,
                "shape": (2, 1),
            },
            "merge_laminate": {
                "proc": merge_laminate,
                "shape": (2, 1),
            },
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
            inp = self.callback[p]["proc"](inp)
        return inp


def copy_1to1(inp: Shapez2MultiLayer) -> Shapez2MultiLayer:
    "図形操作なしで、入力図形をそのまま出力する"
    return inp


def copy_1to2(inp: Shapez2MultiLayer) -> Shapez2MultiLayers:
    "図形操作なしで、入力図形を2出力に分割する"
    return (inp, inp)


def copy_2to1(inp: Shapez2MultiLayers) -> Shapez2MultiLayer:
    "図形操作なしで、入力図形を1出力に統合する"
    raise NotImplementedError("実装できなさそう")


def colorize(inp: Shapez2MultiLayer, color: Shapez2Colors) -> Shapez2MultiLayer:
    "入力図形の最上位レイヤのみ着色"
    from copy import deepcopy

    out = deepcopy(inp)
    out.mlayer[0].colorize(color)
    return out


def colorize_RED(inp: Shapez2MultiLayer) -> Shapez2MultiLayer:
    return colorize(inp, Shapez2Colors.RED)


def colorize_GREEN(inp: Shapez2MultiLayer) -> Shapez2MultiLayer:
    return colorize(inp, Shapez2Colors.GREEN)


def colorize_BLUE(inp: Shapez2MultiLayer) -> Shapez2MultiLayer:
    return colorize(inp, Shapez2Colors.BLUE)


def colorize_PURPLE(inp: Shapez2MultiLayer) -> Shapez2MultiLayer:
    return colorize(inp, Shapez2Colors.PURPLE)


def colorize_CYAN(inp: Shapez2MultiLayer) -> Shapez2MultiLayer:
    return colorize(inp, Shapez2Colors.CYAN)


def colorize_YELLOW(inp: Shapez2MultiLayer) -> Shapez2MultiLayer:
    return colorize(inp, Shapez2Colors.YELLOW)


def colorize_WHITE(inp: Shapez2MultiLayer) -> Shapez2MultiLayer:
    return colorize(inp, Shapez2Colors.WHITE)


def crystarize(inp: Shapez2MultiLayer, color: Shapez2Colors) -> Shapez2MultiLayer:
    "入力図形のピン、隙間を円形結晶で埋める"
    raise NotImplementedError


def crystarize_RED(inp: Shapez2MultiLayer) -> Shapez2MultiLayer:
    return crystarize(inp, Shapez2Colors.RED)


def crystarize_GREEN(inp: Shapez2MultiLayer) -> Shapez2MultiLayer:
    return crystarize(inp, Shapez2Colors.GREEN)


def crystarize_BLUE(inp: Shapez2MultiLayer) -> Shapez2MultiLayer:
    return crystarize(inp, Shapez2Colors.BLUE)


def crystarize_PURPLE(inp: Shapez2MultiLayer) -> Shapez2MultiLayer:
    return crystarize(inp, Shapez2Colors.PURPLE)


def crystarize_CYAN(inp: Shapez2MultiLayer) -> Shapez2MultiLayer:
    return crystarize(inp, Shapez2Colors.CYAN)


def crystarize_YELLOW(inp: Shapez2MultiLayer) -> Shapez2MultiLayer:
    return crystarize(inp, Shapez2Colors.YELLOW)


def crystarize_WHITE(inp: Shapez2MultiLayer) -> Shapez2MultiLayer:
    return crystarize(inp, Shapez2Colors.WHITE)


def pin(inp: Shapez2MultiLayer) -> Shapez2MultiLayer:
    "入力図形の最下層にピンを追加。5層以上になる場合、最上層を捨てる"
    from copy import deepcopy

    out = deepcopy(inp)

    pin_layer = parse_shapez2("P-P-P-P-").convert_schemas().mlayer[0]
    if len(out.mlayer) > 3:
        out.mlayer = out.mlayer[1:]
    out.mlayer = [x for x in out.mlayer] + [pin_layer]
    return out


def rotate_90(inp: Shapez2MultiLayer) -> Shapez2MultiLayer:
    "時計回りに90度回転"
    ret_mlayer = []
    ret_layer = []
    for layer in inp.mlayer:
        ret_layer = [
            layer.layer[3],
            layer.layer[0],
            layer.layer[1],
            layer.layer[2],
        ]
        ret_mlayer.append(Shapez2Layer(ret_layer))
    return Shapez2MultiLayer(ret_mlayer)


def rotate_180(inp: Shapez2MultiLayer) -> Shapez2MultiLayer:
    "時計回りに180度回転"
    ret_mlayer = []
    ret_layer = []
    for layer in inp.mlayer:
        ret_layer = [
            layer.layer[2],
            layer.layer[3],
            layer.layer[0],
            layer.layer[1],
        ]
        ret_mlayer.append(Shapez2Layer(ret_layer))
    return Shapez2MultiLayer(ret_mlayer)


def rotate_270(inp: Shapez2MultiLayer) -> Shapez2MultiLayer:
    "時計回りに90度回転"
    ret_mlayer = []
    ret_layer = []
    for layer in inp.mlayer:
        ret_layer = [
            layer.layer[1],
            layer.layer[2],
            layer.layer[3],
            layer.layer[0],
        ]
        ret_mlayer.append(Shapez2Layer(ret_layer))
    return Shapez2MultiLayer(ret_mlayer)


def separate(inp: Shapez2MultiLayer) -> Shapez2MultiLayers:
    raise NotImplementedError


def swap(inp: Shapez2MultiLayers) -> Shapez2MultiLayers:
    raise NotImplementedError


def merge(inp: Shapez2MultiLayers) -> Shapez2MultiLayer:
    raise NotImplementedError


def merge_flat(inp: Shapez2MultiLayers) -> Shapez2MultiLayer:
    raise NotImplementedError


def merge_laminate(inp: Shapez2MultiLayers) -> Shapez2MultiLayer:
    raise NotImplementedError
