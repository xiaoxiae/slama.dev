from manim import *
from random import *


class Wave(Scene):
    def construct(self):
        seed(0xDEADBEEF)

        maze_string = """
#######################################################
#  #################            ##                    #
# ##################           ####                   #
# #################            ####                   #
#  ###############             #####               # ##
#      #########               #####               ####
#         ###                  ######            ######
#          ###            ##   #####    ###       #####
#          ####      ########   ####  #####        ## #
#          #####   ##########   ###  ########       # #
#         #####   ###########        ########         #
#         ####   ###########        ##########        #
#        ##      ###########        ##########        #
#      ####     ############      #############       #
#    ######     ############     #############        #
# #########  ## ###########     #########    #        #
# ############### #########     #######               #
# ###############   ######      ######                #
# ###############    #####       ####                 #
#   #############      #                ##            #
#     #  #######                       ########### ####
#          ###         #              #################
# ##                  ####            #################
#####                ######          ##################
######                ######         ##################
# ###      ###        #######  ###   ###############  #
#         ####         ############   ####  #######   #
#        #####          ############          ###     #
#         ###            ##########                   #
#######################################################
"""

        maze = []  # 2D array of squares like we see it
        maze_bool = []  # 2D array of true/false values
        all_squares = VGroup()

        # go line by line
        for row in maze_string.strip().splitlines():
            maze.append([])
            maze_bool.append([])

            for char in row:
                square = Square(
                    side_length=0.23,
                    stroke_width=1,
                    fill_color=WHITE if char == "#" else BLACK,
                    fill_opacity=1,
                )

                maze[-1].append(square)
                maze_bool[-1].append(char == " ")
                all_squares.add(square)

        w = len(maze[0])
        h = len(maze)

        # arrange the squares in the grid
        all_squares.arrange_in_grid(rows=h, buff=0)

        self.play(FadeIn(all_squares), run_time=2)

        x, y = 1, 1

        colors = ["#ef476f", "#ffd166", "#06d6a0", "#118ab2"]

        # create a dictionary of distances from start to other points
        distances = {(x, y): 0}
        stack = [(x, y, 0)]

        while len(stack) != 0:
            x, y, d = stack.pop(0)

            for dx, dy in ((0, 1), (1, 0), (-1, 0), (0, -1)):
                nx, ny = dx + x, dy + y

                if nx < 0 or nx >= w or ny < 0 or ny >= h:
                   continue

                if maze_bool[ny][nx] and (nx, ny) not in distances:
                    stack.append((nx, ny, d + 1))
                    distances[(nx, ny)] = d + 1

        max_distance = max([d for d in distances.values()])

        all_colors = color_gradient(colors, max_distance + 1)

        # create animation groups for each distance from start
        groups = []
        for d in range(max_distance + 1):
            groups.append(
                AnimationGroup(
                    *[
                        maze[y][x].animate.set_fill(all_colors[d])
                        for x, y in distances
                        if distances[x, y] == d
                    ]
                )
            )

        self.play(AnimationGroup(*groups, lag_ratio=0.08))
