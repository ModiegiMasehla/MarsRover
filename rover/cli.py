import sys
from typing import List, Optional

from rover.simulator import run_instructions


def main(argv: Optional[List[str]] = None) -> int:
    args = sys.argv[1:] if argv is None else argv
    if len(args) != 1:
        print("Usage: python simulate_rover.py <instructions-file>", file=sys.stderr)
        return 2

    try:
        with open(args[0], "r", encoding="utf-8") as file:
            ok = run_instructions(file)
    except OSError as error:
        print(f"Could not read '{args[0]}': {error.strerror}", file=sys.stderr)
        return 1

    return 0 if ok else 1
