from manim import *


class BackgroundColorExample(MovingCameraScene):
    def construct(self):
        self.camera.background_color = WHITE
        self.camera.frame.scale(0.6)

        square = Square(color=BLACK)

        self.play(Write(square))

        circle = Circle(color=BLACK).next_to(square, LEFT)
        triangle = Triangle(color=BLACK).next_to(square, RIGHT)

        self.play(FadeIn(triangle, shift=RIGHT * 0.2), FadeIn(circle, shift=LEFT * 0.2))
