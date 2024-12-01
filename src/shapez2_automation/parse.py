from typing import NamedTuple, Optional, Sequence, Union, Tuple
import logging
from rich.logging import RichHandler

from .tokenizer import Tokenizer, DEFAULT_RULES
from .schemas import (
    _token_to_fig,
    _token_to_col,
    Shapez2Quarter,
    Shapez2Layer,
    Shapez2MultiLayer,
    Shapez2Figures,
    Shapez2Colors,
)

logging.basicConfig(
    level="NOTSET", format="%(message)s", datefmt="[%X]", handlers=[RichHandler()]
)  # set level=20 or logging.INFO to turn off debug
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# <Color> := b | g | r | c | y | p | w | u | -
# blue, green, red, cyan, yellow, purple, white, uncolor, empty
# <Figure> := S | R | C | W | P | c | -
# Star, Rect, Circle, Windmill, Pin, crystal, -(empty)
# <Layer> := <Figure><Color>
# <Shapez> := <Shapez>:<Layer>

# Example.
# SbP-P-Sb:--WbWb--:CuCuCuCu:P-CbCbP-
# RbCbCbCb:RuCuCuCu:WgWrWgWr


class Node:
    def __init__(self, v: str) -> None:
        self.v = v

    def __str__(self) -> str:
        return self.v

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}('{self}')"

    def serialize(self) -> str:
        raise NotImplementedError


class Figure(Node):
    def serialize(self) -> str:
        return str(self)


class Color(Node):
    def serialize(self) -> str:
        return str(self)


MarkerQuarter = Tuple[Figure, Color]
MarkerLayer = Union[Sequence["MarkerQuarter"]]
MarkerLayerList = Sequence[MarkerLayer]


class ParsedShapez2(NamedTuple):
    shapez2: Optional[MarkerLayerList]

    def __repr__(self) -> str:
        if self.shapez2 is None:
            return "none"
        ret = ""
        for i, l in enumerate(self.shapez2):
            ret += f"{i}: {l}\n"
        return ret

    def convert_schemas(self) -> Shapez2MultiLayer:
        """素のobjectリストから制約をもつschemaに変換"""
        l_convs = []
        if self.shapez2 is None:
            raise ValueError("self.shapez2 not found")

        for layer in self.shapez2:
            q_convs = []
            for quarter in layer:
                (fig, col) = quarter
                q_cov = Shapez2Quarter(
                    _fig := _token_to_fig[str(fig)],
                    _token_to_col[str(col).upper()],
                    _fig == Shapez2Figures.PIN,
                    _fig == Shapez2Figures.CRYSTAL,
                )
                q_convs.append(q_cov)
            l_conv = Shapez2Layer(q_convs)
            l_convs.append(l_conv)
        ml = Shapez2MultiLayer(l_convs)
        return ml


def _parse_shapez2(tokenizer: Tokenizer) -> ParsedShapez2:
    """token文字列から素のobjectにパース"""
    # parse all tokens
    layers: list[MarkerLayer] = []
    quarters: list[MarkerQuarter] = []

    with tokenizer.enclosing_tokens("OPEN", "END", around="."):
        while True:
            if tokenizer.check("COLON"):
                _ = tokenizer.read()
                logger.debug(_)
                layers.append(quarters)
                quarters = []
            elif tokenizer.check("FIGURE"):
                f = tokenizer.read()
                logger.debug(f)
                if tokenizer.check("COLOR"):
                    c = tokenizer.read()
                    logger.debug(c)
                    quarters.append((Figure(f.text), Color(c.text)))
                else:
                    tokenizer.raise_syntax_error(
                        "can not parse. must be color after figure"
                    )
            elif tokenizer.check("END", peek=True):
                layers.append(quarters)
                break
            else:
                tokenizer.raise_syntax_error(
                    f"Unexpected string, not in {DEFAULT_RULES}"
                )

    v = ParsedShapez2(layers)
    return v


def parse_shapez2(inp: str) -> ParsedShapez2:
    return _parse_shapez2(Tokenizer(inp, rules=DEFAULT_RULES))
