from manim import *


class CircleFromPointsExample(Scene):
    def construct(self):
        p1 = Dot().shift(LEFT + UP)
        p2 = Dot().shift(DOWN * 1.5)
        p3 = Dot().shift(RIGHT + UP)

        dots = VGroup(p1, p2, p3)

        # create a circle from three points
        circle = Circle.from_three_points(
            p1.get_center(), p2.get_center(), p3.get_center(), color=WHITE
        )

        self.play(Write(dots), run_time=1.5)
        self.play(Write(circle))
