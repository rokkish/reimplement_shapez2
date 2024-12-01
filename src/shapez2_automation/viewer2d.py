from typing import TypeGuard, Any, Tuple
import logging
from rich.logging import RichHandler
import numpy as np
from numpy.typing import NDArray

from .schemas import *


logging.basicConfig(
    level="NOTSET", format="%(message)s", datefmt="[%X]", handlers=[RichHandler()]
)  # set level=20 or logging.INFO to turn off debug
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class Colors(StrEnum):
    RESET = "\033[0m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    PURPLE = "\033[35m"  # MAGENTA
    CYAN = "\033[36m"
    WHITE = "\033[97m"
    # PIN = "\033[30m"  # BLACK
    UNDEFINED = "\033[90m"  # GRAY


class CanvasLayer2d:
    src: NDArray
    colors: list[Colors]

    def __init__(self):
        """9x15"""
        self.src = np.array(["*"] * 9 * 15).reshape((9, 15))
        # horizon line
        self.src[:, 6:9] = "."
        # vartical line
        self.src[4, :] = "."

        self.colors = [
            Colors.UNDEFINED,
            Colors.UNDEFINED,
            Colors.UNDEFINED,
            Colors.UNDEFINED,
        ]

    def __repr__(self) -> str:
        """保持しているsrcとcolorをもとに描画"""
        ret = ""
        H, W = self.src.shape
        for i in range(H):
            if i == H // 2:
                ret += "".join(self.src[i])
                ret += "\n"
                continue
            # 左半分の描画
            ret += self.colors[i // ((H - 1) // 2 + 1) * 2]
            ret += "".join(self.src[i][: W // 2 - 1])
            ret += Colors.RESET

            # 境界線の描画
            ret += "".join(self.src[i][W // 2 - 1 : W // 2 + 2])

            # 右半分の描画
            ret += self.colors[i // ((H - 1) // 2 + 1) * 2 + 1]
            ret += "".join(self.src[i][W // 2 + 2 :])
            ret += Colors.RESET
            ret += "\n"
        return ret

    def replace_canvas(self, fig: Shapez2Figures, col: Shapez2Colors, location: int):
        """空のcanvasに対して, 特定の位置の図形を置き換え、色を保持する"""
        # roi の決定
        match location:
            case 0:
                roc = (0, 0, 4, 6)  # top, left, bottom, right
            case 1:
                roc = (0, 0 + 9, 4, 6 + 9)
            case 2:
                roc = (0 + 5, 0, 4 + 5, 6)
            case 3:
                roc = (0 + 5, 0 + 9, 4 + 5, 6 + 9)
            case _:
                raise ValueError

        # 図形の決定
        # fmt: off
        match fig:
            case Shapez2Figures.CIRCLE:
                dst = np.array([
                    [" ", " ", "+", "+", "+", "+",],
                    [" ", "+", "+", "+", "+", "+",],
                    ["+", "+", "+", "+", "+", "+",],
                    ["+", "+", "+", "+", "+", "+",],
                ]).reshape(4,6)
            case Shapez2Figures.RECT:
                dst = np.array([
                    ["+", "+", "+", "+", "+", "+",],
                    ["+", "+", "+", "+", "+", "+",],
                    ["+", "+", "+", "+", "+", "+",],
                    ["+", "+", "+", "+", "+", "+",],
                ]).reshape(4, 6)
            case Shapez2Figures.STAR:
                dst = np.array([
                    ["+", " ", " ", " ", " ", " ",],
                    [" ", "+", "+", " ", " ", " ",],
                    [" ", " ", " ", "+", "+", "+",],
                    [" ", " ", " ", "+", "+", "+",],
                ]).reshape(4,6)
            case Shapez2Figures.WINDMILL:
                dst = np.array([
                    [" ", " ", " ", " ", " ", "+",],
                    [" ", " ", " ", " ", "+", "+",],
                    [" ", " ", "+", "+", "+", "+",],
                    ["+", "+", "+", "+", "+", "+",],
                ]).reshape(4,6)
            case Shapez2Figures.PIN:
                dst = np.array([
                    [" ", " ", " ", " ", " ", " ",],
                    [" ", " ", "+", "+", " ", " ",],
                    [" ", " ", "+", "+", " ", " ",],
                    [" ", " ", " ", " ", " ", " ",],
                ]).reshape(4,6)
            case Shapez2Figures.CRYSTAL:
                dst = np.array([
                    [" ", " ", "~", "~", "~", "~",],
                    [" ", "~", "~", "~", "~", "~",],
                    ["~", "~", "~", "~", "~", "~",],
                    ["~", "~", "~", "~", "~", "~",],
                ]).reshape(4,6)
            case Shapez2Figures.EMPTY:
                dst = np.array([
                    [" ", " ", " ", " ", " ", " ",],
                    [" ", " ", " ", " ", " ", " ",],
                    [" ", " ", " ", " ", " ", " ",],
                    [" ", " ", " ", " ", " ", " ",],
                ]).reshape(4,6)
            case _:
                raise ValueError
        # fmt: on

        # 位置に応じてreplaceするcanvasを回転
        match location:
            case 0:
                pass
            case 1:
                dst = dst[:, ::-1]
            case 2:
                dst = dst[::-1, :]
            case 3:
                dst = dst[::-1, ::-1]
            case _:
                raise ValueError

        # 図形の置き換え
        self.src[roc[0] : roc[2], roc[1] : roc[3]] = dst

        # 色objectを文字色コードに変換
        match col:
            case Shapez2Colors.RED:
                self.colors[location] = Colors.RED
            case Shapez2Colors.GREEN:
                self.colors[location] = Colors.GREEN
            case Shapez2Colors.BLUE:
                self.colors[location] = Colors.BLUE
            case Shapez2Colors.PURPLE:
                self.colors[location] = Colors.PURPLE
            case Shapez2Colors.CYAN:
                self.colors[location] = Colors.CYAN
            case Shapez2Colors.YELLOW:
                self.colors[location] = Colors.YELLOW
            case Shapez2Colors.WHITE:
                self.colors[location] = Colors.WHITE
            case Shapez2Colors.UNDEFINED:
                self.colors[location] = Colors.UNDEFINED
            case Shapez2Colors.EMPTY:
                pass
            case _:
                raise ValueError


class Viewer2d:
    def __init__(self, source: Shapez2Type) -> None:
        self.source = source

    def print(self) -> None:
        if isinstance(self.source, Shapez2MultiLayer):
            canvass: list[CanvasLayer2d] = []
            for layer in self.source.mlayer:
                canvas = CanvasLayer2d()
                for i, quarter in enumerate(layer.layer):
                    # logger.debug(f"{quarter.figure}, {quarter.color}")
                    canvas.replace_canvas(quarter.figure, quarter.color, i)
                canvass.append(canvas)
                # print(canvas) # print multi layer in vertical
                # logger.debug(canvas)

            # print multi layer in horizontal
            (l_h, l_w) = canvass[0].src.shape
            ml_w = sum([cs.src.shape[1] for cs in canvass])
            ml_canvas = np.array(["*"] * l_h * ml_w).reshape((l_h, ml_w))
            for j, c in enumerate(canvass):
                ml_canvas[:, l_w * j : l_w * (j + 1)] = c.src

            ret = ""
            # add header
            for i in range(len(canvass)):
                ret += f"Layer {i}     "
            ret += "\n"
            ret += "".join(["-"] * l_w * (i + 1)) + "\n"

            # add main shape
            for k in range(l_h):
                # 横の境界線の描画
                if k == l_h // 2:
                    # ret += ''.join(ml_canvas[k])
                    # ret += "\n"
                    continue
                for _canvas in canvass:
                    offset = l_w // 2 - 1  # 6
                    # print(f"{k//((l_h-1)//2+1)*2+1=}, {k=}")
                    # 左半分の描画
                    ret += _canvas.colors[k // ((l_h - 1) // 2 + 1) * 2]
                    ret += "".join(_canvas.src[k][:offset])  # 0...6
                    ret += Colors.RESET

                    # 縦の境界線の描画
                    # ret += ''.join(_canvas.src[k][offset:offset+3])  # 6...9

                    # 右半分の描画
                    ret += _canvas.colors[k // ((l_h - 1) // 2 + 1) * 2 + 1]
                    ret += "".join(_canvas.src[k][offset + 3 :])  # 9...15
                    ret += Colors.RESET
                ret += "\n"

            print(ret)

        else:
            for quarter in self.source.layer:
                logger.debug(f"{quarter.figure}, {quarter.color}")
