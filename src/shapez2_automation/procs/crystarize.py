from .proc_base import ProcBase
from shapez2_automation.schemas import Shapez2MultiLayer, Shapez2Colors, Shapez2MultiLayers


class CrystarizeBase(ProcBase):
    name = "crystarize"
    input_size = 1
    output_size = 1

    def crystarize(self, inp: Shapez2MultiLayer, color: Shapez2Colors) -> Shapez2MultiLayer:
        "入力図形のピン、隙間を円形結晶で埋める"
        raise NotImplementedError


class CrystarizeRED(CrystarizeBase):
    name = "crystarize_RED"

    def proc(self, inp: Shapez2MultiLayer) -> Shapez2MultiLayer:
        return self.crystarize(inp, Shapez2Colors.RED)


class CrystarizeGREEN(CrystarizeBase):
    name = "crystarize_GREEN"

    def proc(self, inp: Shapez2MultiLayer) -> Shapez2MultiLayer:
        return self.crystarize(inp, Shapez2Colors.GREEN)


class CrystarizeBLUE(CrystarizeBase):
    name = "crystarize_BLUE"

    def proc(self, inp: Shapez2MultiLayer) -> Shapez2MultiLayer:
        return self.crystarize(inp, Shapez2Colors.BLUE)


class CrystarizePURPLE(CrystarizeBase):
    name = "crystarize_PURPLE"

    def proc(self, inp: Shapez2MultiLayer) -> Shapez2MultiLayer:
        return self.crystarize(inp, Shapez2Colors.PURPLE)


class CrystarizeCYAN(CrystarizeBase):
    name = "crystarize_CYAN"

    def proc(self, inp: Shapez2MultiLayer) -> Shapez2MultiLayer:
        return self.crystarize(inp, Shapez2Colors.CYAN)


class CrystarizeYELLOW(CrystarizeBase):
    name = "crystarize_YELLOW"

    def proc(self, inp: Shapez2MultiLayer) -> Shapez2MultiLayer:
        return self.crystarize(inp, Shapez2Colors.YELLOW)


class CrystarizeWHITE(CrystarizeBase):
    name = "crystarize_WHITE"

    def proc(self, inp: Shapez2MultiLayer) -> Shapez2MultiLayer:
        return self.crystarize(inp, Shapez2Colors.WHITE)
