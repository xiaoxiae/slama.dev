from manim import *


class AnimationGroupExample(Scene):
    def construct(self):
        c1 = Square(color=RED)
        c2 = Square(color=GREEN)
        c3 = Square(color=BLUE)

        VGroup(c1, c2, c3).arrange(buff=1)

        # each animation starts in the quarter of the previous one
        self.play(AnimationGroup(Write(c1), Write(c2), Write(c3), lag_ratio=0.25))

        # each animation starts after the first tenth of the previous one
        self.play(AnimationGroup(FadeOut(c1), FadeOut(c2), FadeOut(c3), lag_ratio=0.1))

        # one animation can also be a group, which has different lag_ratio
        self.play(
            AnimationGroup(
                AnimationGroup(Write(c1), Write(c2), lag_ratio=0.1),
                Write(c3),
                lag_ratio=0.5,
            )
        )

        # lag_ratio can also be negative (in which case the animations run in reverse)
        # however, just because it can doesn't mean it should!
        self.play(AnimationGroup(FadeOut(c1), FadeOut(c2), FadeOut(c3), lag_ratio=-0.1))
