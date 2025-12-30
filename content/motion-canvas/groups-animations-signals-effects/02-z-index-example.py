from manim import *


class ZIndexExample(Scene):
    def construct(self):
        c1 = Circle(
            fill_opacity=1, fill_color=RED, stroke_width=5, stroke_color=WHITE
        ).shift(LEFT)
        c2 = Circle(
            fill_opacity=1, fill_color=GREEN, stroke_width=5, stroke_color=WHITE
        )
        c3 = Circle(
            fill_opacity=1, fill_color=BLUE, stroke_width=5, stroke_color=WHITE
        ).shift(RIGHT)

        self.add(c1, c2, c3)

        self.wait(1)

        # we'll increase the z index of c1 and c2, which will bring to the front
        # c2 will still be in front of c1, which is the order they are in the scene
        c1.set_z_index(1)
        c2.set_z_index(1)

        self.wait(1)

        # c1 will now be in front of both c2 (z = 1) and c3 (z = 0)
        c1.set_z_index(2)

        self.wait(1)
