import unittest

from rover import Rover


class RoverTests(unittest.TestCase):
    def test_starts_at_origin_facing_north(self):
        self.assertEqual(Rover().status(), "I'm at (0.00, 0.00) facing 0.00 degrees")

    def test_move_forward_north(self):
        r = Rover()
        r.move(10)
        self.assertEqual(r.status(), "I'm at (0.00, 10.00) facing 0.00 degrees")

    def test_move_backward(self):
        r = Rover()
        r.move(-10)
        self.assertEqual(r.status(), "I'm at (0.00, -10.00) facing 0.00 degrees")

    def test_turn_then_move_east(self):
        r = Rover()
        r.turn(90)
        r.move(5)
        self.assertEqual(r.status(), "I'm at (5.00, 0.00) facing 90.00 degrees")

    def test_heading_wraps(self):
        r = Rover()
        r.turn(450)
        self.assertEqual(r.heading, 90)
        r.turn(-180)
        self.assertEqual(r.heading, 270)

    def test_no_negative_zero(self):
        r = Rover()
        r.turn(180)
        r.move(1e-9)
        self.assertNotIn("-0.00", r.status())


if __name__ == "__main__":
    unittest.main()
