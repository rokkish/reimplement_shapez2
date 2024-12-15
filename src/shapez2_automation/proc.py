from typing import Any, Tuple, TypeAlias, Dict, Union

from .schemas import *
from .procs import proc_base, copy, colorize, crystarize, pin, rotate, separate, swap, rotate, merge


class Shapez2Proc:
    """primitiveな図形の加工屋さん"""

    procs: list[str] = []

    def __init__(self) -> None:
        self.callback_obj: list[Any] = [
            copy.Copy,
            copy.Copy1x2,
            copy.Copy2x1,
            colorize.ColorizeRED,
            colorize.ColorizeGREEN,
            colorize.ColorizeBLUE,
            colorize.ColorizePURPLE,
            colorize.ColorizeCYAN,
            colorize.ColorizeYELLOW,
            colorize.ColorizeWHITE,
            crystarize.CrystarizeRED,
            crystarize.CrystarizeGREEN,
            crystarize.CrystarizeBLUE,
            crystarize.CrystarizePURPLE,
            crystarize.CrystarizeCYAN,
            crystarize.CrystarizeYELLOW,
            crystarize.CrystarizeWHITE,
            pin.Pin,
            rotate.Rotate90,
            rotate.Rotate180,
            rotate.Rotate270,
            separate.Separate,
            swap.Swap,
            merge.Merge,
            merge.MergeFlat,
            merge.MergeLaminate,
        ]

        self.callback: Dict[str, proc_base.ProcBase] = {}
        """ callback dict. proc name for proc obj"""

        for obj in self.callback_obj:
            self.callback[obj.name] = obj()

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
            inp = self.callback[p].proc(inp)
        return inp
