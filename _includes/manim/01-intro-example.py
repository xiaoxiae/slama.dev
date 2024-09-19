from manim import *


class Intro(Scene):
    def construct(self):
        # create square and circle objects (and move them)
        square = Square(color=RED).shift(LEFT * 2)
        circle = Circle(color=BLUE).shift(RIGHT * 2)

        # animate writing them on screen
        self.play(Write(square), Write(circle))

        # fading them from the scene
        self.play(FadeOut(square), FadeOut(circle), run_time=2)