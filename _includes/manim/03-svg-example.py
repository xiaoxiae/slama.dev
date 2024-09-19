from manim import *


class SVGExample(Scene):
    def construct(self):
        image = SVGMobject("ant.svg")

        self.play(Write(image))

        self.play(image.animate.set_color(RED).scale(1.75))

        self.play(Rotate(image, TAU))  # tau = 2 pi

        self.play(FadeOut(image))