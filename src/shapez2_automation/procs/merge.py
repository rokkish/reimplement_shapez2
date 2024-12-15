from .proc_base import ProcBase
from shapez2_automation.schemas import Shapez2MultiLayer, Shapez2MultiLayers


class Merge(ProcBase):
    name = "merge"
    input_size = 2
    output_size = 1

    def proc(self, inp: Shapez2MultiLayers) -> Shapez2MultiLayer:
        raise NotImplementedError


class MergeFlat(ProcBase):
    name = "merge_flat"
    input_size = 2
    output_size = 1

    def proc(self, inp: Shapez2MultiLayers) -> Shapez2MultiLayer:
        raise NotImplementedError


class MergeLaminate(ProcBase):
    name = "merge_laminate"
    input_size = 2
    output_size = 1

    def proc(self, inp: Shapez2MultiLayers) -> Shapez2MultiLayer:
        raise NotImplementedError
