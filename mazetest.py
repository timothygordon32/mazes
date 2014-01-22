import unittest

# Lifted from http://www.openp2p.com/pub/a/python/2004/12/02/tdd_pyunit.html

import numpy


NORTH = 0
EAST = 1
SOUTH = 2
WEST = 3

def visible_from(position, maze, max_distance):
    y = position[0]
    x = position[1]
    distances = [0, 0, 0, 0]

    for cy in reversed(range(y)):
        distances[NORTH] = y - cy - 1
        if maze[cy, x]:
            break

    for cy in range(y + 1, maze.shape[0]):
        distances[SOUTH] = cy - y - 1
        if maze[cy, x]:
            break

    for cx in reversed(range(x)):
        distances[WEST] = x - cx - 1
        if maze[y, cx]:
            break

    for cx in range(x + 1, maze.shape[1]):
        distances[EAST] = cx - x - 1
        if maze[y, cx]:
            break

    return distances


class VisibilityTests(unittest.TestCase):
    def testCannotSeeAnythingWhenBoxedIn(self):
        # +++  Maze with a hole
        # +X+
        # +++
        M = numpy.ones((3, 3), dtype=bool)
        M[1, 1] = 0

        V = visible_from((1, 1), M, 1)
        self.failUnless(V == [0, 0, 0, 0])

    def testCanSeeAShortWayNorth(self):
        # +++  Maze with a NS hole
        # + +
        # +X+
        # +++
        M = numpy.ones((4, 3), dtype=bool)
        M[1, 1] = 0
        M[2, 1] = 0
        V = visible_from((2, 1), M, 1)
        self.failUnless(V == [1, 0, 0, 0])

    def testCanSeeAShortWaySouth(self):
        # +++  Maze with a NS hole
        # +X+
        # + +
        # +++
        M = numpy.ones((4, 3), dtype=bool)
        M[1, 1] = 0
        M[2, 1] = 0
        V = visible_from((1, 1), M, 1)
        self.failUnless(V == [0, 0, 1, 0])

    def testCanSeeAShortWayWest(self):
        # ++++ Maze with a EW hole
        # + X+
        # ++++
        M = numpy.ones((3, 4), dtype=bool)
        M[1, 1] = 0
        M[1, 2] = 0
        V = visible_from((1, 2), M, 1)
        self.failUnless(V == [0, 0, 0, 1])

    def testCanSeeAShortWayEast(self):
        # ++++ Maze with a EW hole
        # +X +
        # ++++
        M = numpy.ones((3, 4), dtype=bool)
        M[1, 1] = 0
        M[1, 2] = 0
        V = visible_from((1, 1), M, 1)
        self.failUnless(V == [0, 1, 0, 0])


def main():
    unittest.main()


if __name__ == '__main__':
    main()