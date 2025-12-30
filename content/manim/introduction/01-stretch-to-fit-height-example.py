from manim import *


class StretchToFitHeightExample(Scene):
    def construct(self):
        s1 = Square().shift(LEFT * 2.5)
        s2 = Square().shift(RIGHT * 2.5)

        self.play(Write(s1), Write(s2))

        self.play(
            s1.animate.stretch_to_fit_height(3.5),
            s2.animate.set_height(3.5),
        )
