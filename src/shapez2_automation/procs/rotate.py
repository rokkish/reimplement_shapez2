from .proc_base import ProcBase
from shapez2_automation.schemas import Shapez2MultiLayer, Shapez2Layer, Shapez2MultiLayers


class Rotate90(ProcBase):
    name = "rotate_90"
    input_size = 1
    output_size = 1

    def proc(self, inp: Shapez2MultiLayer) -> Shapez2MultiLayer:
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


class Rotate180(ProcBase):
    name = "rotate_180"
    input_size = 1
    output_size = 1

    def proc(self, inp: Shapez2MultiLayer) -> Shapez2MultiLayer:
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


class Rotate270(ProcBase):
    name = "rotate_270"
    input_size = 1
    output_size = 1

    def proc(self, inp: Shapez2MultiLayer) -> Shapez2MultiLayer:
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

