# Mars Rover

A command-line simulator that reads a file of instructions and moves a rover around a 2D plane.

The rover starts at `(0, 0)` facing north (`0` degrees). Clockwise turns increase the heading, so `90` is east, `180` south and `270` west.

## Usage

Requires Python 3.8+. No third-party packages.

```
python simulate_rover.py instructions.txt
```

Exit code is `0` on success, `1` if an instruction was rejected or the file could not be read, `2` on wrong usage.

## Instruction format

One instruction per line, case-insensitive. Blank lines are skipped but still count toward the instruction number.

```
Move <n> meters forward|backward
Turn <n> degrees clockwise|counterclockwise
```

`<n>` may be a decimal and must be a non-negative, finite number. Anything else aborts the run at that line.

## Example

`instructions.txt`:

```
Move 10 meters forward
Turn 90 degrees clockwise
```

Output:

```
I'm at (0.00, 0.00) facing 0.00 degrees
Moving 10.0 meters forward (instruction 1.0)
I'm at (0.00, 10.00) facing 0.00 degrees
Turning 90.0 degrees clockwise (instruction 2.0)
I'm at (0.00, 10.00) facing 90.00 degrees
```

More samples are in `examples/`. The bundled `instructions.txt` has an invalid third line on purpose, so it shows the abort message.

## Project layout

```
simulate_rover.py     entry point
rover/model.py        Rover state, turning and moving
rover/commands.py     parsing and validation of instruction lines
rover/simulator.py    runs instructions and prints progress
rover/cli.py          argument handling and file errors
tests/                unit tests
```

## Tests

```
python -m unittest discover -v
```
