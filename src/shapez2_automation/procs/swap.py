from .proc_base import ProcBase
from shapez2_automation.schemas import Shapez2MultiLayer, Shapez2MultiLayers


class Swap(ProcBase):
    name = "swap"
    input_size = 2
    output_size = 2

    def proc(self, inp: Shapez2MultiLayers) -> Shapez2MultiLayers:
        raise NotImplementedError
