from typing import NamedTuple, Optional, NoReturn, Iterator
import contextlib
import re
from dataclasses import dataclass
import logging
from rich.logging import RichHandler

logging.basicConfig(
    level="NOTSET", format="%(message)s", datefmt="[%X]", handlers=[RichHandler()]
)  # set level=20 or logging.INFO to turn off debug
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


@dataclass
class Token:
    name: str
    text: str
    position: int


class ParserSyntaxError(Exception):
    def __init__(
        self,
        message: str,
        *,
        source: str,
        span: tuple[int, int],
    ) -> None:
        self.span = span
        self.message = message
        self.source = source
        super().__init__()

    def __str__(self) -> str:
        marker = " " * self.span[0] + "~" * (self.span[1] - self.span[0]) + "^"
        return "\n    ".join([self.message, self.source, marker])


class Tokenizer:
    def __init__(self, source: str, *, rules: dict[str, str | re.Pattern[str]]) -> None:
        self.source = source
        self.rules: dict[str, re.Pattern[str]] = {
            name: re.compile(pattern) for name, pattern in rules.items()
        }
        self.next_token: Optional[Token] = None
        self.position = 0

    def _info(self):
        logger.debug(f"{self.source=}")
        logger.debug(f"{self.rules=}")
        logger.debug(f"{self.next_token=}")
        logger.debug(f"{self.position=}")

    def consume(self, name: str) -> None:
        if self.check(name):
            _ = self.read()
            logger.debug(f"consume: {_}")

    def check(self, name: str, *, peek: bool = False) -> bool:
        assert (
            self.next_token is None
        ), f"Cannot check for {name!r}, already have {self.next_token}"
        assert name in self.rules, f"Unknown token name: {name!r}"

        expression = self.rules[name]

        match = expression.match(self.source, self.position)
        if match is None:
            return False
        if not peek:
            self.next_token = Token(name, match[0], self.position)
        return True

    def expect(self, name: str, *, expected: str) -> Token:
        if not self.check(name):
            raise self.raise_syntax_error(f"Expected {expected}")
        return self.read()

    def read(self) -> Token:
        token = self.next_token
        assert token is not None
        self.position += len(token.text)
        self.next_token = None
        return token

    def raise_syntax_error(
        self,
        message: str,
        *,
        span_start: Optional[int] = None,
        span_end: Optional[int] = None,
    ) -> NoReturn:
        span = (
            self.position if span_start is None else span_start,
            self.position if span_end is None else span_end,
        )
        raise ParserSyntaxError(
            message,
            source=self.source,
            span=span,
        )

    @contextlib.contextmanager
    def enclosing_tokens(
        self, open_token: str, close_token: str, *, around: str
    ) -> Iterator[None]:
        if self.check(open_token):
            open_position = self.position
            self.read()
        else:
            open_position = None

        yield

        if open_position is None:
            return
        if not self.check(close_token):
            self.raise_syntax_error(
                f"Expected matching {close_token} for {open_token}, after {around}",
                span_start=open_position,
            )

        self.read()


DEFAULT_RULES: dict[str, str | re.Pattern[str]] = {
    "COLON": r":",
    "COLOR": r"[bgrcypwu-]",
    "FIGURE": r"[SRCWPc-]",
    "END": r"$",
    "OPEN": r"^",
}


if __name__ == "__main__":
    # source = "SbP-P-Sb"
    # source = "SbP-P-Sb:--WbWb--:CuCuCuCu:P-CbCbP-"
    source = "RucrRucr:cbcbcbcb:CwCwCwCw"
    t = Tokenizer(source, rules=DEFAULT_RULES)

    with t.enclosing_tokens("OPEN", "END", around="."):
        while True:
            if t.check("COLON"):
                _ = t.read()
                logger.debug(_)
            if t.check("FIGURE"):
                _ = t.read()
                logger.debug(_)
                if t.check("COLOR"):
                    _ = t.read()
                    logger.debug(_)
                else:
                    t.raise_syntax_error(f"must color after figure")
            if t.check("END", peek=True):
                break
