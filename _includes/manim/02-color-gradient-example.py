from manim import *


class ColorGradientExample(Scene):
    def construct(self):
        rows = 6
        square_count = rows * 9

        # the colors can be either the built-in constants or in hex notation
        # (the builtin ones are just strings in the hex notation too!)
        colors = [RED, "#ffd166", "#06d6a0", BLUE]
        squares = [
            Square(fill_color=WHITE, fill_opacity=1).scale(0.3)
            for _ in range(square_count)
        ]

        group = VGroup(*squares).arrange_in_grid(rows=rows)

        self.play(Write(group, lag_ratio=0.04))

        all_colors = color_gradient(colors, square_count)

        self.play(
            AnimationGroup(
                *[s.animate.set_color(all_colors[i]) for i, s in enumerate(squares)],
                lag_ratio=0.02,
            )
        )

        self.play(FadeOut(group))