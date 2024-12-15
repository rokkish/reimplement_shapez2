from .proc_base import ProcBase
from shapez2_automation.schemas import Shapez2MultiLayer, Shapez2MultiLayers



class Separate(ProcBase):
    name = "separate"
    input_size = 1
    output_size = 2

    def proc(self, inp: Shapez2MultiLayer) -> Shapez2MultiLayers:
        raise NotImplementedError
