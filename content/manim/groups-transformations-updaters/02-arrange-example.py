from manim import *
from random import seed, uniform


class ArrangeExample(Scene):
    def construct(self):
        seed(0xDEADBEEF)

        circles = VGroup(
            *[
                Circle(radius=0.1)
                .scale(uniform(0.5, 4))
                .shift(UP * uniform(-3, 3) + RIGHT * uniform(-5, 5))
                for _ in range(12)
            ]
        )

        self.play(FadeIn(circles))

        # left-to-right arrangement
        self.play(circles.animate.arrange())

        # specify the direction of arrangement and spacing between the objects
        self.play(circles.animate.arrange(direction=DOWN, buff=0.3))
        self.play(circles.animate.arrange(direction=LEFT + DOWN, buff=0.1))
