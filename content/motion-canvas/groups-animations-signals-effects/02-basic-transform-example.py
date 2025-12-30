from manim import *


class BasicTransformExample(Scene):
    def construct(self):
        c = Circle().scale(2)
        s = Square().scale(2)

        self.play(Write(c))

        self.play(Transform(c, s))
