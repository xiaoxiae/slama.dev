from manim import *


class SimpleUpdaterExample(Scene):
    def construct(self):
        square = Square()
        square_label = Tex("A neat square.").next_to(square, UP, buff=0.5)

        self.play(Write(square))
        self.play(FadeIn(square_label, shift=UP * 0.5))

        def label_updater(obj):
            """An updater which continually move an object above the square.

            The first parameter (obj) is always the object that is being updated."""
            obj.next_to(square, UP, buff=0.5)

        # we want the label to always reside above the square
        square_label.add_updater(label_updater)

        self.play(square.animate.shift(LEFT * 3))
        self.play(square.animate.scale(1 / 2))
        self.play(square.animate.rotate(PI / 2).shift(RIGHT * 3 + DOWN * 0.5).scale(3))

        # to pause updaters, we'll use suspend_updating()
        square_label.suspend_updating()

        self.play(square.animate.scale(1 / 3))
        self.play(square.animate.rotate(PI / 2))

        # to resume,we'll use resume__updating()
        square_label.resume_updating()

        self.play(square.animate.scale(3))
        self.play(square.animate.rotate(PI / 2))
