from manim import *


class BooleanOperations(Scene):
    def construct(self):
        circle = Circle(fill_opacity=0.75, color=RED).scale(2).shift(LEFT * 1.5)
        square = Square(fill_opacity=0.75, color=GREEN).scale(2).shift(RIGHT * 1.5)

        group = VGroup(circle, square)

        self.play(Write(group))

        self.play(group.animate.scale(0.4).shift(UP * 1.6))

        union = Union(circle, square, fill_opacity=1, color=BLUE)

        for operation, position in zip(
            [Intersection, Union, Exclusion, Difference],
            [LEFT * 5, LEFT * 1.7, RIGHT * 1.7, RIGHT * 5],
        ):
            result = operation(circle, square, fill_opacity=1, color=DARK_BLUE)
            result_position = DOWN * 1.3 + position

            label = Tex(str(operation.__name__)).move_to(result_position).scale(0.8)

            self.play(FadeIn(result))

            self.play(
                AnimationGroup(
                    result.animate.move_to(result_position),
                    Write(label, run_time=0.5),
                    lag_ratio=0.8,
                )
            )
