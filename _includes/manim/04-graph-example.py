from manim import *
from math import sin


class GraphExample(Scene):
    def construct(self):
        axes = Axes(x_range=[-5, 5], y_range=[-3, 7])
        labels = axes.get_axis_labels(x_label="x", y_label="y")

        def f1(x):
            return x ** 2

        def f2(x):
            return sin(x)

        g1 = axes.plot(f1, color=RED)
        g2 = axes.plot(f2, color=BLUE)

        self.play(Write(axes), Write(labels))

        self.play(AnimationGroup(Write(g1), Write(g2), lag_ratio=0.5))

        self.play(Unwrite(axes), Unwrite(labels), Unwrite(g1), Unwrite(g2))