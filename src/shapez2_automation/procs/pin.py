from .proc_base import ProcBase
from shapez2_automation.schemas import Shapez2MultiLayer
from shapez2_automation.parse import parse_shapez2


class Pin(ProcBase):
    name = "pin"
    input_size = 1
    output_size = 1

    def proc(self, inp: Shapez2MultiLayer) -> Shapez2MultiLayer:
        "入力図形の最下層にピンを追加。5層以上になる場合、最上層を捨てる"
        from copy import deepcopy

        out = deepcopy(inp)

        pin_layer = parse_shapez2("P-P-P-P-").convert_schemas().mlayer[0]
        if len(out.mlayer) > 3:
            out.mlayer = out.mlayer[1:]
        out.mlayer = [x for x in out.mlayer] + [pin_layer]
        return out