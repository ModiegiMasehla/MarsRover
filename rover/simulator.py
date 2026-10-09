from typing import Callable, Iterable, Optional

from rover.commands import InvalidInstruction, MoveCommand, parse_line
from rover.model import Rover


def run_instructions(
    lines: Iterable[str],
    rover: Optional[Rover] = None,
    output: Callable[[str], None] = print,
) -> bool:
    """Execute instructions line by line.

    Returns True if every instruction ran, False if it aborted on a bad one.
    Instruction numbers follow the line number in the file (blank lines count).
    """
    rover = rover if rover is not None else Rover()
    output(rover.status())

    for number, line in enumerate(lines, start=1):
        try:
            command = parse_line(line)
        except InvalidInstruction:
            output(
                "I've encountered an instruction I don't understand, "
                f"aborting (instruction {float(number)})"
            )
            return False

        if command is None:
            continue

        output(f"{command.describe()} (instruction {float(number)})")
        if isinstance(command, MoveCommand):
            rover.move(command.signed_distance)
        else:
            rover.turn(command.signed_degrees)
        output(rover.status())

    return True
