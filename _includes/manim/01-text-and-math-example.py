from manim import *


class TextAndMath(Scene):
    def construct(self):
        text = Tex("Hello Manim!").shift(LEFT * 2.5)

        # note that we're using Python's r-strings for cleaner code
        formula = MathTex(r"\sum_{i = 0}^\infty \frac{1}{2^i} = 2").shift(RIGHT * 2.5)

        self.play(Write(formula), Write(text))

        self.play(FadeOut(formula), FadeOut(text))