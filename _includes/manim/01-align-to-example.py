from manim import *


class AlignTo(Scene):
    def construct(self):
        c1, c2, c3 = [Circle(radius=1.5 - i / 3, color=WHITE)
                      for i in range(3)]

        self.play(*[Write(o) for o in [c1, c2, c3]])

        # align such that c1 < c2 < c3
        self.play(
            c1.animate.next_to(c2, LEFT),
            c3.animate.next_to(c2, RIGHT),
        )

        # align c1 and c2 such that their bottoms are the same as c2
        self.play(
            c1.animate.align_to(c2, DOWN),
            c3.animate.align_to(c2, DOWN),
        )

        point = [0, 2.5, 0]

        # align all circles such that their top touches a line going through the point
        self.play(
            c1.animate.align_to(point, UP),
            c2.animate.align_to(point, UP),
            c3.animate.align_to(point, UP),
        )