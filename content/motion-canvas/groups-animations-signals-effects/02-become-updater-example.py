from manim import *


class BecomeUpdaterExample(Scene):
    def format_point(self, point) -> str:
        """Format the given point to look presentable."""
        return f"[{point[0]:.2f}, {point[1]:.2f}]"

    def construct(self):
        circle = Circle(color=WHITE)

        def circle_label_updater(obj):
            """An updater that displays the circle's position above it."""
            obj.become(Tex(f"p = {self.format_point(circle.get_center())}"))
            obj.next_to(circle, UP, buff=0.35)

        self.play(Write(circle))

        circle_label = Tex()

        # a bit of a hack - we're calling the updater to create the initial label
        circle_label_updater(circle_label)

        self.play(FadeIn(circle_label, shift=UP * 0.3))

        # start updating the label
        circle_label.add_updater(circle_label_updater)

        self.play(circle.animate.shift(RIGHT))
        self.play(circle.animate.shift(LEFT * 3 + UP))
        self.play(circle.animate.shift(DOWN * 2 + RIGHT * 2))
        self.play(circle.animate.shift(UP))
