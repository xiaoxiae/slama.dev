from manim import *


class LineExample(Scene):
    def construct(self):
        p1 = Dot()
        p2 = Dot()

        points = VGroup(p1, p2).arrange(buff=2.5)

        line = Line(start=p1.get_center(), end=p2.get_center())

        self.play(Write(p1), Write(p2))

        self.play(Write(line))
