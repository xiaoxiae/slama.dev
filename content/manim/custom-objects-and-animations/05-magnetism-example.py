from manim import *


# example from https://github.com/Matheart/manim-physics
class MagnetismExample(Scene):
    def construct(self):
        current1 = Current(LEFT * 2.5)
        current2 = Current(RIGHT * 2.5, direction=IN)

        def rebuild(field):
            """Funkce která přestaví magnetické pole."""
            field.become(MagneticField(current1, current2))

        field = MagneticField(current1, current2)

        self.play(Write(field), FadeIn(current1), FadeIn(current2))

        field.add_updater(rebuild)

        self.play(
            Rotate(current1, about_point=ORIGIN, angle=PI),
            Rotate(current2, about_point=ORIGIN, angle=PI),
            run_time=2,
        )
