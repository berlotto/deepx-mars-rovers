#  -*- encoding: utf-8 -*-
#
# DeepX's Code Challenge
# The Mars Rovers problem
# https://github.com/GetAmbush/code-challenge/blob/master/challenge2.md
#
import fileinput
import sys

__author__ = "Sérgio Berlotto"
__email__ = "sergio.berlotto@gmail.com"
__license__ = "GPLv3 <https://www.gnu.org/licenses/gpl-3.0-standalone.html>"


class MoveToOutOfBoundsException(Exception):
    pass


class Rover():
    def __init__(self, plateau_bounds, x, y, facing):
        """
        Create the initial data of this Rover
        plateau_bounds = tuple with max X an Y (upper-right corner) Ex. (5,5)
        x = int with initial x position of Rover
        y = int with initial y position of Rover
        facing = str initial facing of this Rover
        """
        assert isinstance(plateau_bounds, tuple), \
            "Plateau bounds must be a tuple with width and height sizes"

        assert isinstance(x, int) and isinstance(y, int), \
            "X and Y must be integer numbers"

        self.x = x
        self.y = y
        self.plateau_bounds = plateau_bounds

        self.cardinals = ["N", "E", "S", "W"]

        assert facing in self.cardinals, \
            "Facing must be one of " + str(self.cardinals)

        self.facing = facing
        self.__cardinal_index = self.cardinals.index(self.facing)

    def __next_cardinal(self):
        """
        Control what is the next cardinal point, looking to right
        """
        self.__cardinal_index += 1
        if self.__cardinal_index > 3:
            self.__cardinal_index = 0
        return self.cardinals[self.__cardinal_index]

    def __prev_cardinal(self):
        """
        Control what is the previous cardinal point, looking to left
        """
        self.__cardinal_index -= 1
        if self.__cardinal_index < 0:
            self.__cardinal_index = 3
        return self.cardinals[self.__cardinal_index]

    def __can_move(self):
        """
        Verify if the required moviment will not out of plateau bounds
        Ex:
        plateau_bounds is (5,5), index must be 0,1,2,3,4 or 5
        """
        if self.facing == "E":
            return True if self.x + 1 <= self.plateau_bounds[0] else False
        if self.facing == "W":
            return True if self.x - 1 >= 0 else False
        if self.facing == "N":
            return True if self.y + 1 <= self.plateau_bounds[1] else False
        if self.facing == "S":
            return True if self.y - 1 >= 0 else False

    def get_position(self):
        """
        Only return the current position of this Rover
        """
        return "{0} {1} {2}".format(self.x, self.y, self.facing)

    def move(self):
        """
        Moves the Rover 1pt in the current direction,
        depending where Rover facing to
        """
        if not self.__can_move():
            raise MoveToOutOfBoundsException(
                "This movement will do the Rover move to "
                "out of the plateau bounds")
        if self.facing == "E":
            self.x += 1
        if self.facing == "W":
            self.x -= 1
        if self.facing == "N":
            self.y += 1
        if self.facing == "S":
            self.y -= 1

    def rotate(self, direction):
        """
        Rotate the Rover at Right or Left, 90°, one time per call
        """
        assert direction in ["L", "R"], "Direction must be one of [R, L]"

        if direction == "L":
            self.facing = self.__prev_cardinal()
        if direction == "R":
            self.facing = self.__next_cardinal()

    def make_moviments(self, mov_codes):
        """
        Receive and execute a series of moviments in the Rover
        """
        assert all([True if x in "LRM" else False for x in mov_codes]), \
            "Movie codes must be one of [L, R, M]"

        for code in mov_codes:
            if code in ["L", "R"]:
                self.rotate(code)
            elif code == "M":
                self.move()
        return self.get_position()


if __name__ == '__main__':
    """
    This script read an input file
    It can be the filename, like:
    $ python mars.py /tmp/inputfile.txt
    or can be writed in the standard input and finished with CTRL+D, like
    $ python mars.py -
    5 5
    1 3 E
    LMLMLMLMM
    CTRL+D
    or receive the filecontent by an PIPE, like:
    $ my_other_command.sh | python mars.py
    """
    if len(sys.argv) > 2:
        print(sys.argv[0] + " requires only one parameter file")
        exit(-1)

    # Capture all lines of input file
    filelines = []
    for line in fileinput.input():
        filelines.append(line.strip())

    # The file must have an odd number of rows:
    # 1st is plateau size
    # the others, two by two, are the position and movements of the Rovers.
    if len(filelines) % 2 != 1:
        print("Wrong number of lines in the file")

    plateau_size = tuple([int(x) for x in filelines[0].split()])
    ll = filelines[1:]  # Discard 1st line

    # Read 2 by 2 lines and make Rovers walk
    for pos, mvmts in [(ll[x], ll[x + 1]) for x in range(0, len(ll) - 1, 2)]:
        x, y, f = pos.split()
        x, y = int(x), int(y)  # Convert to int
        rover = Rover(plateau_size, x, y, f)
        print(rover.make_moviments(mvmts))
