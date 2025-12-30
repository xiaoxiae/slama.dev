from manim import *
from random import seed, uniform


class ArrangeInGridExample(Scene):
    def construct(self):
        seed(0xDEADBEEF)

        circles = VGroup(
            *[
                Circle(radius=0.1)
                .scale(uniform(0.5, 2))
                .shift(UP * uniform(-3, 3) + RIGHT * uniform(-5, 5))
                for _ in range(9**2)
            ]
        )

        self.play(FadeIn(circles))

        # square grid (or as close as possible)
        self.play(circles.animate.arrange_in_grid())

        # different parameters for rows and columns
        self.play(circles.animate.arrange_in_grid(rows=5, buff=0))
        self.play(circles.animate.arrange_in_grid(cols=12, buff=0.3))
