from .proc_base import ProcBase
from shapez2_automation.schemas import Shapez2MultiLayer, Shapez2MultiLayers


class Copy(ProcBase):
    name = "copy_1x1"
    input_size = 1
    output_size = 1

    def proc(self, inp: Shapez2MultiLayer) -> Shapez2MultiLayer:
        "図形操作なしで、入力図形をそのまま出力する"
        return inp


class Copy1x2(ProcBase):
    name = "copy_1x2"
    input_size = 1
    output_size = 2

    def proc(self, inp: Shapez2MultiLayer) -> Shapez2MultiLayers:
        "図形操作なしで、入力図形を2出力に分割する"
        return (inp, inp)


class Copy2x1(ProcBase):
    name = "copy_2x1"
    input_size = 2
    output_size = 1

    def proc(self, inp: Shapez2MultiLayers) -> Shapez2MultiLayer:
        "図形操作なしで、入力図形を1出力に統合する"
        raise NotImplementedError("実装できなさそう")
