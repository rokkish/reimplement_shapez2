import argparse
from dataclasses import dataclass
import logging
from rich.logging import RichHandler

from .schemas import Shapez2Type, _token_to_fig, _token_to_col, Shapez2MultiLayer
from .parse import parse_shapez2
from .proc import Shapez2Proc
from .solver import Shapez2Solver
from .viewer2d import Viewer2d


logging.basicConfig(
    level="NOTSET", format="%(message)s", datefmt="[%X]", handlers=[RichHandler()]
)  # set level=20 or logging.INFO to turn off debug
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


@dataclass
class Shapez2Simulator:
    """Shapze2シミュレータ.
    - 図形を表す文字列をもとにパース
    - 回転、切断などの処理を実行
    - 図形を作成するための処理を求める
    - 処理結果の表示
    """

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

    def get_required_proc(self, *args, **kwargs):
        """与えられた図形を0から作成するprocsを返す"""
        s = Shapez2Solver(kwargs["shapez_string"])
        return s.solve()

    def print(self, *args, **kwargs) -> None:
        """結果の表示"""
        if kwargs["invert"]:
            logger.info(f'in:\n{kwargs["shapez_string"]}')
            logger.info(f'solution:\n{kwargs["out"]}')
        else:
            # logger.info(f'in:\n{kwargs["shapez_string"]}')
            # logger.info(f'apply:\n{kwargs["proc"]}')
            # logger.info(f'out:\n{kwargs["out"]}')
            Viewer2d(kwargs["shapez_string"]).print()
            Viewer2d(kwargs["out"]).print()


def cli() -> None:
    parser = argparse.ArgumentParser(
        description="simulator for shapez2",
    )
    parser.add_argument(
        "shapez_string",
        help=f"図形を指定する",
    )
    parser.add_argument(
        "proc",
        nargs="*",
        choices=list(Shapez2Proc().callback.keys()),
        default="copy",
        help=f"図形に適用する操作を選択する",
    )
    parser.add_argument(
        "--invert",
        action="store_true",
        help=Shapez2Simulator().get_required_proc.__doc__,
    )

    # 引数のparse
    d = dict()
    args = parser.parse_args()
    for k, v in args._get_kwargs():
        d[k] = v

    # インスタンスの生成
    simulator = Shapez2Simulator()

    # 入力文字列をobjectにパース
    d["shapez_string"] = simulator.parse(**d)

    # モードに応じてmainの処理を実行
    if d["invert"]:
        d["out"] = simulator.get_required_proc(**d)
    else:
        d["out"] = simulator.do_proc(**d)

    # 結果の表示
    simulator.print(**d)


if __name__ == "__main__":
    cli()
