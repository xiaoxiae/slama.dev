from manim import *

# shamelessly stolen (modulo minor changes) from the Manim documentation
# https://docs.manim.community/en/stable/reference/manim.utils.rate_functions.html


class RateFunctionsExample(Scene):
    def construct(self):
        line1 = Line(3 * LEFT, RIGHT).set_color(RED)
        line2 = Line(3 * LEFT, RIGHT).set_color(GREEN)
        line3 = Line(3 * LEFT, RIGHT).set_color(BLUE)
        line4 = Line(3 * LEFT, RIGHT).set_color(ORANGE)

        lines = (
            VGroup(line1, line2, line3, line4).arrange(DOWN, buff=0.8).move_to(LEFT * 2)
        )

        dot1 = Dot().move_to(line1.get_start())
        dot2 = Dot().move_to(line2.get_start())
        dot3 = Dot().move_to(line3.get_start())
        dot4 = Dot().move_to(line4.get_start())

        dots = VGroup(dot1, dot2, dot3, dot4)

        # care for writing _ in latex -- needs to be escaped
        label1 = Tex(r"smooth (default)").next_to(line1, RIGHT, buff=0.5)
        label2 = Tex(r"linear").next_to(line2, RIGHT, buff=0.5)
        label3 = Tex(r"there\_and\_back").next_to(line3, RIGHT, buff=0.5)
        label4 = Tex(r"rush\_into").next_to(line4, RIGHT, buff=0.5)

        labels = VGroup(label1, label2, label3, label4)

        self.play(Write(lines), FadeIn(dots), FadeIn(labels))

        # usage in animate syntax (animating moving dots)
        self.play(
            dot1.animate(rate_func=smooth).shift(RIGHT * 4),
            dot2.animate(rate_func=linear).shift(RIGHT * 4),
            dot3.animate(rate_func=there_and_back).shift(RIGHT * 4),
            dot4.animate(rate_func=rush_into).shift(RIGHT * 4),
            run_time=3,
        )

        self.play(FadeOut(lines), FadeOut(dots))

        # usage in normal animations (writing lines)
        self.play(
            Write(line1, rate_func=smooth),
            Write(line2, rate_func=linear),
            Write(line3, rate_func=there_and_back),
            Write(line4, rate_func=rush_into),
            run_time=3,
        )
