from manim import *


class AttentionExample(Scene):
    def construct(self):
        c1 = Square()

        labels = [
            Tex("Flash"),
            Tex("Indicate"),
            Tex("Wiggle"),
            Tex("FocusOn"),
            Tex("Circumscribe"),
        ]

        # move labels below the square
        for label in labels:
            label.next_to(c1, DOWN).scale(1.5)

        def switch_labels(i: int):
            """Animate switching one label for another. Notice the shift parameter!"""
            return AnimationGroup(
                FadeOut(labels[i], shift=UP * 0.5),
                FadeIn(labels[i + 1], shift=UP * 0.5),
            )

        self.play(Write(c1))

        self.play(FadeIn(labels[0], shift=UP * 0.5), c1.animate.shift(UP))

        self.play(Flash(c1, flash_radius=1.6, num_lines=20))

        self.play(AnimationGroup(switch_labels(0), Indicate(c1), lag_ratio=0.7))

        self.play(AnimationGroup(switch_labels(1), Wiggle(c1), lag_ratio=0.7))

        self.play(AnimationGroup(switch_labels(2), FocusOn(c1), lag_ratio=0.7))

        self.play(AnimationGroup(switch_labels(3), Circumscribe(c1), lag_ratio=0.7))