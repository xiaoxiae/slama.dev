from manim import *


class VGroupLagRatioExample(Scene):
    def construct(self):
        squares = VGroup(Square(), Square(), Square()).arrange(buff=0.5).scale(1.5)

        # Write has non-zero lag_ratio by default so squares are written with overlap
        self.play(Write(squares))

        # FadeOut has zero lag_ratio by default, so all squares fade concurrently
        self.play(FadeOut(squares))

        squares.set_color(BLUE)

        self.play(Write(squares, lag_ratio=0))

        self.play(FadeOut(squares, lag_ratio=0.5))