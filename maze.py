import numpy
from numpy.random import random_integers as rand
import matplotlib.pyplot as pyplot
from matplotlib import animation

palettes = {
    # RGB vectors in a 0-1 format palatable to matplotlib
    # Once a palette is selected (e.g. 'maze') the boolean values in the maze are mapped to the appropriate color
    'maze':             numpy.array( [ [1.0, 1.0, 1.0],     # index 0 = paths = white
                                       [0.0, 0.0, 0.0] ] ), # index 1 = walls = black

    'known_to_player':  numpy.array( [ [0.0, 0.0, 0.0],     # index 0 = unknown territory = black
                                       [0.0, 1.0, 0.5] ] ), # index 1 = known paths = green

    'known_to_minator': numpy.array( [ [0.0, 0.0, 0.0],     # index 0 = unknown territory = black
                                       [1.0, 0.5, 0.0] ] ), # index 1 = known paths = orange

    'player_location':  numpy.array( [ [0.0, 0.0, 0.0],     # index 0 = not here = black - check this works when averaging colours
                                       [0.0, 0.0, 1.0] ] ), # index 1 = here = blue

    'minator_location': numpy.array( [ [0.0, 0.0, 0.0],     # index 0 = not here = black - check this works when averaging colours
                                       [1.0, 0.0, 0.0] ] )  # index 1 = here = red
}

#print palettes['maze']
#print palettes['known_to_player'][1]

# The idea is that we keep the maze (and maze-like things such as known territory) boolean and separate from each other
# and manage the rendering later via function CreateImage etc.

def CreateImage(boolean_array, palette_name):
    # The next statement uses an array as an index to another array.  Gotta love Python!
    # http://wiki.scipy.org/Tentative_NumPy_Tutorial#head-3f4d28139e045a442f78c5218c379af64c2c8c9e
    return palettes[palette_name][boolean_array.astype(int)]

def generate(width=81, height=51, complexity=.75, density=.75):
    # Only odd shapes
    shape = ((height // 2) * 2 + 1, (width // 2) * 2 + 1)
    # Adjust complexity and density relative to maze size
    complexity = int(complexity * (5 * (shape[0] + shape[1])))
    density    = int(density * (shape[0] // 2 * shape[1] // 2))
    # Build actual maze
    Z = numpy.zeros(shape, dtype=bool)
    # Fill borders
    Z[0, :] = Z[-1, :] = 1  # 1 (True) is a wall, 0 (False) is a path
    Z[:, 0] = Z[:, -1] = 1
    # Make isles
    for i in range(density):
        x, y = rand(0, shape[1] // 2) * 2, rand(0, shape[0] // 2) * 2
        Z[y, x] = 1
        for j in range(complexity):
            neighbours = []
            if x > 1:             neighbours.append((y, x - 2))
            if x < shape[1] - 2:  neighbours.append((y, x + 2))
            if y > 1:             neighbours.append((y - 2, x))
            if y < shape[0] - 2:  neighbours.append((y + 2, x))
            if len(neighbours):
                y_,x_ = neighbours[rand(0, len(neighbours) - 1)]
                if Z[y_, x_] == 0:
                    Z[y_, x_] = 1
                    Z[y_ + (y - y_) // 2, x_ + (x - x_) // 2] = 1
                    x, y = x_, y_
    return Z

def show_maze(maze):
    image = CreateImage(boolean_array=maze, palette_name='maze')
    pyplot.figure(figsize=(10, 5))
    pyplot.xticks([]), pyplot.yticks([])
    pyplot.imshow(image, interpolation='nearest')
    pyplot.show()

def animate_maze(maze):
    image = CreateImage(boolean_array=maze, palette_name='maze')
    fig = pyplot.figure(figsize=(10, 5))
    pyplot.xticks([]), pyplot.yticks([])
    imgplot = pyplot.imshow(image, interpolation='nearest')

    def CreateFrame(frame):
        image[1, 1 + frame] = palettes['known_to_player'][1]
        imgplot.set_data(image)
        return imgplot

    anim = animation.FuncAnimation(fig, CreateFrame, frames=maze.shape[1]-2, interval=50)
    #anim.save('myAnimatedMaze.mp4')
    pyplot.show()

#show_maze(maze = generate(80, 40, 0.9, 0.9))
animate_maze(maze = generate(80, 40, 0.9, 0.9))
