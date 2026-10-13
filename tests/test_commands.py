import unittest

from rover import InvalidInstruction, MoveCommand, TurnCommand, parse_line


class ParseTests(unittest.TestCase):
    def test_move(self):
        self.assertEqual(parse_line("Move 10 meters forward"), MoveCommand(10.0, "forward"))

    def test_turn_counterclockwise(self):
        self.assertEqual(
            parse_line("turn 45.5 degrees COUNTERCLOCKWISE"),
            TurnCommand(45.5, "counterclockwise"),
        )

    def test_blank_line(self):
        self.assertIsNone(parse_line("   \n"))

    def test_signed_values(self):
        self.assertEqual(MoveCommand(3, "backward").signed_distance, -3)
        self.assertEqual(TurnCommand(30, "counterclockwise").signed_degrees, -30)

    def test_invalid_lines(self):
        bad = [
            "Turn Mars 90 degrees clockwise",
            "Move ten meters forward",
            "Move 10 feet forward",
            "Move 10 meters sideways",
            "Turn 90 degrees left",
            "Turn 90 meters clockwise",
            "Move 10 meters",
            "Jump 10 meters forward",
            "Move -5 meters forward",
            "Move nan meters forward",
            "Move inf meters forward",
        ]
        for line in bad:
            with self.subTest(line=line):
                with self.assertRaises(InvalidInstruction):
                    parse_line(line)


if __name__ == "__main__":
    unittest.main()
