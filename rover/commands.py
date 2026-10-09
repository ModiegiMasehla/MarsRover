import math
from dataclasses import dataclass
from typing import Optional, Union


class InvalidInstruction(ValueError):
    """Raised when a line cannot be understood."""


@dataclass(frozen=True)
class MoveCommand:
    distance: float
    direction: str  # "forward" or "backward"

    @property
    def signed_distance(self) -> float:
        return self.distance if self.direction == "forward" else -self.distance

    def describe(self) -> str:
        return f"Moving {self.distance} meters {self.direction}"


@dataclass(frozen=True)
class TurnCommand:
    degrees: float
    direction: str  # "clockwise" or "counterclockwise"

    @property
    def signed_degrees(self) -> float:
        return self.degrees if self.direction == "clockwise" else -self.degrees

    def describe(self) -> str:
        return f"Turning {self.degrees} degrees {self.direction}"


Command = Union[MoveCommand, TurnCommand]


def _number(token: str) -> float:
    try:
        value = float(token)
    except ValueError:
        raise InvalidInstruction(f"not a number: {token!r}") from None
    if not math.isfinite(value) or value < 0:
        raise InvalidInstruction(f"must be a non-negative number: {token!r}")
    return value


def parse_line(line: str) -> Optional[Command]:
    """Parse one instruction line. Returns None for blank lines."""
    parts = line.lower().split()
    if not parts:
        return None

    if len(parts) != 4:
        raise InvalidInstruction("expected 4 words")

    verb, amount, unit, direction = parts

    if verb == "move":
        if unit != "meters" or direction not in ("forward", "backward"):
            raise InvalidInstruction("expected 'move <n> meters forward|backward'")
        return MoveCommand(_number(amount), direction)

    if verb == "turn":
        if unit != "degrees" or direction not in ("clockwise", "counterclockwise"):
            raise InvalidInstruction("expected 'turn <n> degrees clockwise|counterclockwise'")
        return TurnCommand(_number(amount), direction)

    raise InvalidInstruction(f"unknown command: {verb!r}")
