from manim import *
from random import *


class Triangle(Scene):
    def construct(self):
        seed(0xDEADBEEF)

        # scale everything up a bit
        c = 2

        p1 = Dot().scale(c).shift(UP * c)
        p2 = Dot().scale(c).shift(DOWN * c + LEFT * c)
        p3 = Dot().scale(c).shift(DOWN * c + RIGHT * c)

        points = VGroup(p1, p2, p3)

        self.play(Write(points, lag_ratio=0.5), run_time=1.5)

        l1 = Line()
        l2 = Line()
        l3 = Line()

        lines = VGroup(l1, l2, l3)

        def create_line_updater(a, b):
            """Returns a function that acts as an updater for the given segment."""
            return lambda x: x.become(Line(start=a.get_center(), end=b.get_center()))

        l1.add_updater(create_line_updater(p1, p2))
        l2.add_updater(create_line_updater(p2, p3))
        l3.add_updater(create_line_updater(p3, p1))

        self.play(Write(lines, lag_ratio=0.5), run_time=1.5)

        x = Tex("x")
        y = Tex("y")
        z = Tex("z")

        x.add_updater(lambda x: x.next_to(p1, UP))
        y.add_updater(lambda x: x.next_to(p2, DOWN + LEFT))
        z.add_updater(lambda x: x.next_to(p3, DOWN + RIGHT))

        labels = VGroup(x, y, z).scale(c * 0.8)

        self.play(FadeIn(labels, shift=UP * 0.2))

        circle = Circle()
        circle.add_updater(
            lambda c: c.become(
                Circle.from_three_points(
                    p1.get_center(), p2.get_center(), p3.get_center()
                )
            )
        )

        self.play(Write(circle))

        self.play(
            p2.animate.shift(LEFT + UP),
            p1.animate.shift(RIGHT),
        )
