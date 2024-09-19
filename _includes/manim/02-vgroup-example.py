from manim import *


class VGroupExample(Scene):
    def construct(self):
        s1 = Square(color=RED)
        s2 = Square(color=GREEN)
        s3 = Square(color=BLUE)

        s1.next_to(s2, LEFT)
        s3.next_to(s2, RIGHT)

        self.play(Write(s1), Write(s2), Write(s3))

        group = VGroup(s1, s2, s3)

        # scale the entire group
        self.play(group.animate.scale(1.5).shift(UP))

        # only work with one of the group's objects
        self.play(group[1].animate.shift(DOWN * 2))

        # change color and fill
        self.play(group.animate.set_color(WHITE))
        self.play(group.animate.set_fill(WHITE, 1))