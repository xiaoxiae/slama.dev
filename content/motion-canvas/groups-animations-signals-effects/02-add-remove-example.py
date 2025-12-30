from manim import *


class AddRemoveExample(Scene):
    def construct(self):
        square = Square(fill_color=WHITE, fill_opacity=1)
        small_scale = 0.6

        triangle = Triangle(fill_opacity=1).scale(small_scale).move_to(square)

        self.play(Write(square))

        # add a triangle behind the square
        self.bring_to_back(triangle)
        self.play(square.animate.shift(LEFT * 2))

        circle = Circle(fill_opacity=1).scale(small_scale).move_to(square)

        # add a circle behind the square
        self.bring_to_back(circle)
        self.play(square.animate.shift(RIGHT * 2))

        square2 = (
            Square(stroke_color=GREEN, fill_color=GREEN, fill_opacity=1)
            .scale(small_scale)
            .move_to(square)
        )

        self.remove(triangle)

        # add a second square in front of the square
        # looks jarring but is just to show the functionality
        self.bring_to_front(square2)

        self.play(square.animate.shift(RIGHT * 2))
