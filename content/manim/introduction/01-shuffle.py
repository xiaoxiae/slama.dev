from manim import *
from random import *


class Shuffle(Scene):
    def construct(self):
        seed(0xDEADBEEF)

        # number of values to shuffle
        n = 5

        circles = [
            Circle(color=WHITE, fill_opacity=0.8, fill_color=WHITE).scale(0.6)
            for _ in range(n)
        ]

        # spacing between the circles
        spacing = 2
        for i, circle in enumerate(circles):
            circle.shift(RIGHT * (i - (len(circles) - 1) / 2) * spacing)

        self.play(*[Write(circle) for circle in circles])

        # selected circle
        selected = randint(0, n - 1)
        self.play(circles[selected].animate.set_color(RED))
        self.play(circles[selected].animate.set_color(WHITE))

        # slowly increase speed when swapping
        swaps = 13
        speed_start = 1
        speed_end = 0.2

        for i in range(swaps):
            speed = speed_start - abs(speed_start - speed_end) / swaps * i

            # pick two random circles (ensuring a != b)
            a, b = sample(range(n), 2)

            # swap with a slightly larger arc angle
            self.play(
                Swap(circles[a], circles[b]), run_time=speed, path_arc=135 * DEGREES
            )

        # highlight the initial circle again
        self.play(circles[selected].animate.set_color(RED))
        self.play(circles[selected].animate.set_color(WHITE))
