from dataclasses import dataclass
from enum import StrEnum, auto
from typing import Sequence


class Shapez2Figures(StrEnum):
    """形状タイプ"""

    CIRCLE = auto()
    SQUARE = auto()
    SHURIKEN = auto()
    DIAMOND = auto()
    EMPTY = auto()  # 空図形


class Shapez2Colors(StrEnum):
    """色タイプ"""

    RED = auto()
    GREEN = auto()
    BLUE = auto()
    MAGENDA = auto()
    CYAN = auto()
    YELLOW = auto()
    EMPTY = auto()  # 素材の灰色


class Shapez21ColorPattern(StrEnum):
    """使いやすい組み合わせのパターン.色はすべて等しい"""

    DIVERCITY = auto()  # 4パーツ, 全部違う
    ALL_SAME = auto()  # 4パーツ, 全部等しい
    DIAGONAL_SAME = auto()  # 4or2パーツのみ, 対角線パーツが等しい
    NEIGHBOR_SAME = auto()  # 4or2パーツのみ, 隣接パーツが等しい

    OTHERS = auto()  # 上記に該当しない


@dataclass
class Shapez2Quarter:
    """1層,1/4の型"""

    figure: Shapez2Figures
    color: Shapez2Colors
    ispin: bool  # ピンの有無
    iscrystal: bool  # 結晶状態の是非

    @staticmethod
    def prohibit_pairs(figure, color, ispin, iscrystal) -> bool:
        return (
            figure == Shapez2Figures.EMPTY
            and (color != Shapez2Colors.EMPTY or iscrystal)
        ) or (figure != Shapez2Figures.EMPTY and ispin)

    def __post_init__(self) -> None:
        if self.figure == Shapez2Figures.EMPTY:
            if self.color != Shapez2Colors.EMPTY or self.iscrystal:
                raise ValueError("図形が空なら、colorは必ず空であり、クリスタルは禁止")
            else:
                pass
        else:
            if self.ispin:
                raise ValueError("図形なら、ピンは禁止")


@dataclass
class Shapez2Layer:
    """1層の型"""

    layer: Sequence[Shapez2Quarter]

    def __post_init__(self) -> None:
        self.__validate_layer(self.layer)

    def __validate_layer(self, v: Sequence[Shapez2Quarter]) -> None:
        if len(v) != 4:
            raise ValueError(f"layers must have 4 parts, but {len(v)}")
        if (
            len(set([v.figure for v in self.layer])) == 1
            and self.layer[0] == Shapez2Figures.EMPTY
            and not self.layer[0].ispin
        ):
            raise ValueError(f"すべての figure が空は禁止. pin ならOK")

    def is_neighbor_same(self, figures: Sequence[Shapez2Figures]) -> bool:
        ret = False
        for i in range(-1, len(figures) - 1):
            ret |= figures[i] == figures[i + 1]
        return ret

    def get_pattern(self) -> Sequence[Shapez21ColorPattern]:
        colors = [v.color for v in self.layer]
        if len(set(colors)) > 1:
            return [Shapez21ColorPattern.OTHERS]

        figures = [v.figure for v in self.layer]
        exist_neighbor_same = self.is_neighbor_same(figures)

        n_empty = 0
        for v in figures:
            if v == Shapez2Figures.EMPTY:
                n_empty += 1

        match len(set(figures)):
            case 1:
                return [Shapez21ColorPattern.ALL_SAME]
            case 2:
                # NOTE: 空の図形の数に応じて Shapez21ColorPattern を最大2つとりうる
                if n_empty in [1, 2]:
                    if exist_neighbor_same:
                        return [Shapez21ColorPattern.NEIGHBOR_SAME]
                    return [Shapez21ColorPattern.DIAGONAL_SAME]
                elif n_empty == 0:
                    if exist_neighbor_same:
                        return [Shapez21ColorPattern.NEIGHBOR_SAME] * 2
                    return [Shapez21ColorPattern.DIAGONAL_SAME] * 2
                else:
                    raise ValueError(f"figure 2種類で{n_empty=}は想定外")
            case 3:
                if n_empty == 0:
                    if exist_neighbor_same:
                        return [Shapez21ColorPattern.NEIGHBOR_SAME]
                    return [Shapez21ColorPattern.DIAGONAL_SAME]
                return [Shapez21ColorPattern.OTHERS]
            case 4:
                return [Shapez21ColorPattern.DIVERCITY]
            case _:
                raise ValueError(f"1層の図形は最大4種類が前提")


@dataclass
class Shapez2MultiLayer:
    """多層の型"""

    mlayer: Sequence[Shapez2Layer]

    def __post_init__(self) -> None:
        self.__validate_mlayer(self.mlayer)

    def __validate_mlayer(self, v: Sequence[Shapez2Layer]) -> None:
        if len(v) < 5:
            raise ValueError(f"mlayers must have 1~4 layers, but {len(v)}")
        if False:
            # 多層の禁止事項
            raise ValueError(f"crystalの下は空禁止.落下するので")
            raise ValueError(f"pin の重なりはおそらく禁止")
