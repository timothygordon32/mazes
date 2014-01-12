import numpy
from numpy.random import random_integers as rand
import matplotlib.pyplot as pyplot
import matplotlib.colors as colors
from matplotlib import animation

maze_start = 2
maze_finish = 3
maze_player = 4

def generate(width=81, height=51, complexity=.75, density=.75):
    # Only odd shapes
    shape = ((height // 2) * 2 + 1, (width // 2) * 2 + 1)
    # Adjust complexity and density relative to maze size
    complexity = int(complexity * (5 * (shape[0] + shape[1])))
    density    = int(density * (shape[0] // 2 * shape[1] // 2))
    # Build actual maze
    Z = numpy.zeros(shape, dtype=bool)
    # Fill borders
    Z[0, :] = Z[-1, :] = 1
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

def show(maze):

    render = maze.astype(numpy.int)

    render[1, 1] = maze_start
    render[-2, -2] = maze_finish

    pyplot.figure(figsize=(10, 5))
    pyplot.xticks([]), pyplot.yticks([])
    pyplot.imshow(render, cmap=colors.ListedColormap(['black', 'white', 'red', 'green', 'yellow'], 'indexed'), interpolation='nearest')
    pyplot.show()

def show2(maze):

    render = maze.astype(numpy.int)

    render[1, 1] = maze_start
    render[-2, -2] = maze_finish

    fig = pyplot.figure(figsize=(10, 5))
    pyplot.xticks([]), pyplot.yticks([])
    im = pyplot.imshow(render, cmap=colors.ListedColormap(['black', 'white', 'red', 'green', 'yellow'], 'indexed'), interpolation='nearest')

    def animate(i):
        render[1, 1 + i] = maze_player
        im.set_data(render)
        return im

    anim = animation.FuncAnimation(fig, animate, frames=79, interval=200)

    # anim.save('basic_animation.mp4', fps=1)

    pyplot.show()

show2(maze = generate(80, 40, 0.9, 0.9))