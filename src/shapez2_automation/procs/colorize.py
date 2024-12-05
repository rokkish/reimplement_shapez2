from .proc_base import ProcBase
from shapez2_automation.schemas import Shapez2MultiLayer, Shapez2Colors, Shapez2MultiLayers


class ColorizeBase(ProcBase):
    name = "colorize"
    input_size = 1
    output_size = 1

    def colorize(self, inp: Shapez2MultiLayer, color: Shapez2Colors) -> Shapez2MultiLayer:
        "入力図形の最上位レイヤのみ着色"
        from copy import deepcopy

        out = deepcopy(inp)
        out.mlayer[0].colorize(color)
        return out


class ColorizeRED(ColorizeBase):
    name = "colorize_RED"

    def proc(self, inp: Shapez2MultiLayer) -> Shapez2MultiLayer:
        return self.colorize(inp, Shapez2Colors.RED)


class ColorizeGREEN(ColorizeBase):
    name = "colorize_GREEN"

    def proc(self, inp: Shapez2MultiLayer) -> Shapez2MultiLayer:
        return self.colorize(inp, Shapez2Colors.GREEN)


class ColorizeBLUE(ColorizeBase):
    name = "colorize_BLUE"

    def proc(self, inp: Shapez2MultiLayer) -> Shapez2MultiLayer:
        return self.colorize(inp, Shapez2Colors.BLUE)


class ColorizePURPLE(ColorizeBase):
    name = "colorize_PURPLE"

    def proc(self, inp: Shapez2MultiLayer) -> Shapez2MultiLayer:
        return self.colorize(inp, Shapez2Colors.PURPLE)


class ColorizeCYAN(ColorizeBase):
    name = "colorize_CYAN"

    def proc(self, inp: Shapez2MultiLayer) -> Shapez2MultiLayer:
        return self.colorize(inp, Shapez2Colors.CYAN)


class ColorizeYELLOW(ColorizeBase):
    name = "colorize_YELLOW"

    def proc(self, inp: Shapez2MultiLayer) -> Shapez2MultiLayer:
        return self.colorize(inp, Shapez2Colors.YELLOW)


class ColorizeWHITE(ColorizeBase):
    name = "colorize_WHITE"

    def proc(self, inp: Shapez2MultiLayer) -> Shapez2MultiLayer:
        return self.colorize(inp, Shapez2Colors.WHITE)

