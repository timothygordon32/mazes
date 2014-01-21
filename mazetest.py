import unittest

# Lifted from http://www.openp2p.com/pub/a/python/2004/12/02/tdd_pyunit.html

# Here's our "unit".
import numpy


def visible_from(position, maze, max_distance):
    y = position[0]
    x = position[1]
    distance=0
    for cy in reversed(range(y)):
        distance = y - cy - 1
        if maze[cy,x]:
            break

    return (distance, 0, 0, 0)

# Here's our "unit tests".
class VisibilityTests(unittest.TestCase):
    def testCannotSeeAnythingWhenBoxedIn(self):
        # +++  Maze with a hole
        # +X+
        # +++
        M = numpy.ones((3, 3), dtype=bool)
        M[1, 1] = 0

        V = visible_from((1, 1), M, 1)
        self.failUnless(V == (0, 0, 0, 0))

    def testCanSeeAShortWayNorth(self):
        # +++  Maze with a hole
        # + +
        # +X+
        # +++
        M = numpy.ones((4, 3), dtype=bool)
        M[1, 1] = 0
        M[2, 1] = 0
        V = visible_from((2, 1), M, 1)
        self.failUnless(V == (1, 0, 0, 0))


def main():
    unittest.main()


if __name__ == '__main__':
    main()