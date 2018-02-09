#  -*- encoding: utf-8 -*-
#
# DeepX's Code Challenge
# The Mars Rovers problem
# https://github.com/GetAmbush/code-challenge/blob/master/challenge2.md
#
# To execute the tests, run:
# > python -m unittest
# or
# > python tests.py
#
import unittest

from mars import MoveToOutOfBoundsException, Rover

class TestRoverMethods(unittest.TestCase):

    def test_movement_error(self):
        with self.assertRaises(MoveToOutOfBoundsException):
            plateau_size = (5, 5)
            rover = Rover(plateau_size, 5, 5, "N")
            print(rover.make_moviments("M"))  # Movement error

    def test_code_error(self):
        with self.assertRaises(AssertionError):
            plateau_size = (5, 5)
            rover = Rover(plateau_size, 5, 5, "S")
            print(rover.make_moviments("F"))

    def test_wrong_initial_parameters(self):
        with self.assertRaises(AssertionError):
            rover = Rover(5,5,3,"F")

        with self.assertRaises(AssertionError):
            rover = Rover((5,5),"2","3","F")

    def test_movement1(self):
        plateau_size = (5, 5)
        rover = Rover(plateau_size, 1, 2, "N")
        position = rover.make_moviments("LMLMLMLMM")

        self.assertEqual(position, "1 3 N")

    def test_movement2(self):
        plateau_size = (5, 5)
        rover = Rover(plateau_size, 3, 3, "E")
        position = rover.make_moviments("MMRMMRMRRM")

        self.assertEqual(position, "5 1 E")

    def test_get_position(self):
        plateau_size = (5, 5)
        rover = Rover(plateau_size, 3, 3, "E")
        rover.make_moviments("MMRMMRMRRM")
        position = rover.get_position()

        self.assertEqual(position, "5 1 E")

    def test_min_size(self):
        plateau_size = (1, 1)
        rover = Rover(plateau_size, 1, 1, "E")
        rover.make_moviments("R")
        position = rover.get_position()

        self.assertEqual(position, "1 1 S")

    def test_min_size_with_mov(self):
        plateau_size = (1, 1)
        rover = Rover(plateau_size, 1, 1, "E")
        rover.make_moviments("RM")
        position = rover.get_position()

        self.assertEqual(position, "1 0 S")

    def test_one_pt_size(self):
        plateau_size = (0, 0)
        rover = Rover(plateau_size, 0, 0, "E")
        rover.make_moviments("RRR")
        position = rover.get_position()

        self.assertEqual(position, "0 0 N")

    def test_big_size(self):
        plateau_size = (200, 200)
        rover = Rover(plateau_size, 50, 22, "E")
        rover.make_moviments("M" * 150)
        position = rover.get_position()

        self.assertEqual(position, "200 22 E")


if __name__ == '__main__':
    unittest.main()
