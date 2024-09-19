from manim import *


class BadTransformExample(Scene):
    def construct(self):
        good = [Circle(color=GREEN), Square(color=GREEN), Triangle(color=GREEN)]
        bad = [Circle(color=RED), Square(color=RED), Triangle(color=RED)]

        VGroup(*(good + bad)).arrange_in_grid(rows=2, buff=1)

        self.play(Write(good[0]), Write(bad[0]))

        self.play(
            Transform(good[0], good[1]),  # o1 -> o2
            Transform(bad[0], bad[1]),    # o1 -> o2
        )

        self.play(
            Transform(good[0], good[2]),  # o1 -> o3
            Transform(bad[1], bad[2]),    # o2 -> o3 - bad!
        )