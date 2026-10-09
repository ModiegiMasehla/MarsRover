import math
from dataclasses import dataclass


@dataclass
class Rover:
    """A rover on a 2D plane. Heading 0 is north, 90 is east."""

    x: float = 0.0
    y: float = 0.0
    heading: float = 0.0

    def turn(self, degrees: float) -> None:
        """Turn clockwise by `degrees`; use a negative value for counterclockwise."""
        self.heading = (self.heading + degrees) % 360

    def move(self, distance: float) -> None:
        """Move along the current heading; use a negative value to reverse."""
        radians = math.radians(self.heading)
        self.x += distance * math.sin(radians)
        self.y += distance * math.cos(radians)

    def status(self) -> str:
        return (
            f"I'm at ({_clean(self.x):.2f}, {_clean(self.y):.2f}) "
            f"facing {_clean(self.heading):.2f} degrees"
        )


def _clean(value: float) -> float:
    """Avoid printing -0.00 for tiny floating point residue."""
    return 0.0 if abs(value) < 0.005 else value
