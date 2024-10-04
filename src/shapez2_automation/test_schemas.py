import itertools
import pytest

from .schemas import *


@pytest.mark.parametrize(["figure"], ([[v] for v in Shapez2Figures]))
@pytest.mark.parametrize(["color"], ([[v] for v in Shapez2Colors]))
@pytest.mark.parametrize(["ispin"], ([[v] for v in [True, False]]))
@pytest.mark.parametrize(["iscrystal"], ([[v] for v in [True, False]]))
def test_Shapez2Quarter(figure, color, ispin, iscrystal):
    should_raised = Shapez2Quarter.prohibit_pairs(figure, color, ispin, iscrystal)
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


def quarter_args_pairs():
    _iter = itertools.product(
        Shapez2Figures,
        Shapez2Colors,
        [True],  # , False],
        [True],  # , False]
    )
    for combo in itertools.combinations(_iter, 4):
        yield combo


def gen_args():
    yield from quarter_args_pairs()


@pytest.mark.parametrize(
    ["q1", "q2", "q3", "q4"],
    gen_args(),
)
def test_Shapez2Layer(q1, q2, q3, q4):
    quarters = []
    for q in [q1, q2, q3, q4]:
        fig, col, sp, cr = q
        if Shapez2Quarter.prohibit_pairs(fig, col, sp, cr):
            return
        quarter = Shapez2Quarter(fig, col, sp, cr)
        quarters.append(quarter)

    l = Shapez2Layer(quarters)

    assert l.layer
