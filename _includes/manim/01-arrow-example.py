from manim import *


class ArrowExample(Scene):
    def construct(self):
        a1 = Arrow(start=UP, end=DOWN).shift(LEFT * 2)
        a2 = Arrow(start=DOWN, end=UP).shift(RIGHT * 2)

        self.play(Write(a1), Write(a2))