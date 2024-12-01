import itertools
import pytest

from .schemas import *


@pytest.mark.parametrize(["figure"], ([[v] for v in Shapez2Figures]))
@pytest.mark.parametrize(["color"], ([[v] for v in Shapez2Colors]))
@pytest.mark.parametrize(["ispin"], ([[v] for v in [True, False]]))
@pytest.mark.parametrize(["iscrystal"], ([[v] for v in [True, False]]))
def test_Shapez2Quarter(
    figure: Shapez2Figures, color: Shapez2Colors, ispin: bool, iscrystal: bool
) -> None:
    should_raised = Shapez2Quarter.prohibit_pairs(figure, color)
    raised = False
    try:
        _ = Shapez2Quarter(
            figure,
            color,
            ispin,
            iscrystal,
        )
    except ValueError:
        raised = True
    assert raised == should_raised


def quarter_args_pairs():  # type: ignore
    _iter = itertools.product(
        Shapez2Figures,
        Shapez2Colors,
        [True],  # , False],
        [True],  # , False]
    )
    for combo in itertools.combinations(_iter, 4):
        yield combo


def gen_args():  # type: ignore
    yield from quarter_args_pairs()  # type: ignore


@pytest.mark.parametrize(
    ["q1", "q2", "q3", "q4"],
    gen_args(),  # type: ignore
)
def test_Shapez2Layer(q1, q2, q3, q4) -> None:
    quarters = []
    for q in [q1, q2, q3, q4]:
        fig, col, sp, cr = q
        if Shapez2Quarter.prohibit_pairs(fig, col):
            return
        quarter = Shapez2Quarter(fig, col, sp, cr)
        quarters.append(quarter)

    l = Shapez2Layer(quarters)

    assert l.layer
