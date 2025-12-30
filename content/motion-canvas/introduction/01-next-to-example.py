from manim import *


class NextTo(Scene):
    def construct(self):
        c1, c2, c3, c4 = [Circle(radius=0.5, color=WHITE) for _ in range(4)]

        rectangle = Rectangle(width=5, height=3)

        # use Python's * syntax to write the objects
        # does the following: f(*[1, 2, 3]) == f(1, 2, 3)
        self.play(*[Write(o) for o in [c1, c2, c3, c4, rectangle]])

        # move the circles such that they surround the rectangle
        self.play(
            c1.animate.next_to(rectangle, LEFT),
            c2.animate.next_to(rectangle, UP),
            c3.animate.next_to(rectangle, RIGHT),
            c4.animate.next_to(rectangle, DOWN),
        )
