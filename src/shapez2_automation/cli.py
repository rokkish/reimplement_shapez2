import argparse
from dataclasses import dataclass
import logging
from rich.logging import RichHandler

from .schemas import Shapez2Type, _token_to_fig, _token_to_col
from .parse import parse_shapez2, Shapez2MultiLayer
from .proc import Shapez2Proc


logging.basicConfig(
    level="NOTSET", format="%(message)s", datefmt="[%X]", handlers=[RichHandler()]
)  # set level=20 or logging.INFO to turn off debug
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


@dataclass
class Shapez2Simulator:
    # def __init__(self, *args, **kwargs) -> None:
    #     for k in kwargs.keys():
    #         self.__dict__ = kwargs[k]

    def parse(self, *args, **kwargs) -> Shapez2MultiLayer:
        """文字列から扱いやすい形式にパース"""
        p = parse_shapez2(kwargs["shapez_string"])
        return p.convert_schemas()

    def do_proc(self, *args, **kwargs) -> Shapez2Type:
        """procsを登録し、適用する"""
        p = Shapez2Proc()
        p.add_proc(**kwargs)
        return p.run(**kwargs)

    def print(self, *args, **kwargs) -> None:
        """結果の表示"""
        logger.info(f'in:\n{kwargs["shapez_string"]}')
        logger.info(f'apply:\n{kwargs["proc"]}')
        logger.info(f'out:\n{kwargs["out"]}')


def cli() -> None:
    parser = argparse.ArgumentParser(
        description="simulator for shapez2",
    )
    parser.add_argument(
        "shapez_string",
        help=f"図形を指定する. {list(_token_to_fig.keys())} for Figure. {list(_token_to_col.keys())} for Color. Example: RucrRucr is 1layer, RucrRucr:cbcbcbcb is 2layer",
    )
    parser.add_argument(
        "proc",
        nargs="*",
        default="rotate",
        help=f"図形に適用する操作を選択する. {list(Shapez2Proc().callback.keys())} are available",
    )

    d = dict()
    args = parser.parse_args()
    for k, v in args._get_kwargs():
        d[k] = v
    simulator = Shapez2Simulator()
    d["shapez_string"] = simulator.parse(**d)
    d["out"] = simulator.do_proc(**d)
    simulator.print(**d)


if __name__ == "__main__":
    cli()
