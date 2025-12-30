from manim import *


class DiscontinuousGraphExample(Scene):
    def construct(self):
        axes = Axes(x_range=[-5, 5], y_range=[-3, 7])
        labels = axes.get_axis_labels(x_label="x", y_label="y")

        def f(x):
            return 1 / x

        g_bad = axes.plot(f, color=RED)

        g_left = axes.plot(f, x_range=[-5, -0.1], color=GREEN)
        g_right = axes.plot(f, x_range=[0.1, 5], color=GREEN)

        self.play(Write(axes), Write(labels))

        self.play(Write(g_bad))
        self.play(FadeOut(g_bad))

        self.play(AnimationGroup(Write(g_left), Write(g_right), lag_ratio=0.5))

        self.play(Unwrite(axes), Unwrite(labels), Unwrite(g_left), Unwrite(g_right))
