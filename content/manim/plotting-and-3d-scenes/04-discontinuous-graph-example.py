from manim import *
from math import sin, cos


class ParametricGraphExample(Scene):
    def construct(self):
        axes = Axes(x_range=[-10, 10], y_range=[-5, 5])
        labels = axes.get_axis_labels(x_label="x", y_label="y")

        def f1(t):
            """Parametric function of a circle."""
            return (cos(t) * 3 - 4.5, sin(t) * 3)

        def f2(t):
            """Parametric function of <3."""
            return (
                0.2 * (16 * (sin(t)) ** 3) + 4.5,
                0.2 * (13 * cos(t) - 5 * cos(2 * t) - 2 * cos(3 * t) - cos(4 * t)),
            )

        # the t_range parameter determines the range of the function parameter
        g1 = axes.plot_parametric_curve(f1, color=RED, t_range=[0, 2 * PI])
        g2 = axes.plot_parametric_curve(f2, color=BLUE, t_range=[-PI, PI])

        self.play(Write(axes), Write(labels))

        self.play(AnimationGroup(Write(g1), Write(g2), lag_ratio=0.5))

        self.play(Unwrite(axes), Unwrite(labels), Unwrite(g1), Unwrite(g2))
