from manim import *
from random import *


class Ant:
    deltas = [(-1, 0), (0, -1), (1, 0), (0, 1)]

    def __init__(self, position):
        self.position = position
        self.orientation = 0

    def __get_orientation_delta(self):
        """By how much should the ant move in the current orientation."""
        return self.deltas[self.orientation]

    def __rotate_by_delta(self, delta):
        """Turn the ant in a multiple of 90 degrees."""
        self.orientation = (self.orientation + delta) % len(self.deltas)

    def rotate_left(self):
        """Turn the ant left."""
        self.__rotate_by_delta(-1)

    def rotate_right(self):
        """Turn the ant right."""
        self.__rotate_by_delta(1)

    def move_forward(self):
        """Move the ant forward."""
        dx, dy = self.__get_orientation_delta()
        self.position[0] += dx
        self.position[1] += dy

    def update(self, states):
        """Move and turn the ant, updating its state."""
        x, y = self.position

        states[y][x] = not states[y][x]

        if states[y][x]:
            self.rotate_right()
        else:
            self.rotate_left()

        self.move_forward()


class LangtonAnt(MovingCameraScene):
    def construct(self):
        n = 15
        state = [[False for _ in range(n)] for _ in range(n)]
        squares = [[Square() for _ in range(n)] for _ in range(n)]
        squares_vgroup = VGroup(*[*sum(squares, [])]).arrange_in_grid(columns=n, buff=0)

        ant = Ant([n // 2, n // 2])
        ant_object = (
            SVGMobject("ant.svg")
            .set_height(squares_vgroup[0].height * 0.7)
            .rotate(PI / 2)
        )

        self.play(FadeIn(squares_vgroup), Write(ant_object))

        self.wait(1)

        step_count = 100

        slow_start_iterations = 5
        slow_end_iterations = 3

        slow_run_time = 1
        fast_run_time = 0.07

        for i in range(step_count):
            x, y = ant.position

            new_color = state[y][x]
            rect = squares[y][x]

            running_time = (
                fast_run_time
                if slow_start_iterations < i < step_count - slow_end_iterations
                else slow_run_time
            )

            self.play(
                Rotate(ant_object, PI / 2 * (1 if new_color else -1)),
                run_time=running_time,
            )

            ant.update(state)
            nx, ny = ant.position

            self.play(
                rect.animate.set_fill(BLACK if new_color else WHITE, 1),
                ant_object.animate.move_to(squares[ny][nx]),
                self.camera.frame.animate.move_to(squares[ny][nx]),
                run_time=running_time,
            )

        self.wait(1)

        # determine the currently filled squares to move to them
        white_squares = VGroup()
        for i in range(n):
            for j in range(n):
                if state[i][j]:
                    white_squares.add(squares[i][j])

        self.play(
            self.camera.frame.animate.move_to(white_squares).set_height(
                white_squares.height * 1.2
            )
        )

        self.play(FadeOut(squares_vgroup), FadeOut(ant_object))
