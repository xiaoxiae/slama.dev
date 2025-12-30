from manim import *


class ShuffleExample(Scene):
    def construct(self):
        c11 = Circle(color=WHITE).shift(UP * 1.5 + LEFT * 2)
        c12 = Circle(color=WHITE).shift(UP * 1.5 + RIGHT * 2)
        c21 = Circle(color=WHITE).shift(DOWN * 1.5 + LEFT * 2)
        c22 = Circle(color=WHITE).shift(DOWN * 1.5 + RIGHT * 2)

        self.play(Write(c11), Write(c12), Write(c21), Write(c22))

        self.play(Swap(c11, c21))

        self.play(Swap(c12, c22, path_arc=160 * DEGREES))
