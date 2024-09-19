from manim import *


# example from https://github.com/Matheart/manim-physics
class ElectricFieldExample(Scene):
    def construct(self):
        charge1 = Charge(-1, LEFT + DOWN)
        charge2 = Charge(2, RIGHT + DOWN)
        charge3 = Charge(-1, UP)

        def rebuild(field):
            """Funkce která přestaví elektrické pole."""
            field.become(ElectricField(charge1, charge2, charge3))

        field = ElectricField(charge1, charge2, charge3)

        self.add(field, charge1, charge2, charge3)

        self.play(Write(field), FadeIn(charge1), FadeIn(charge2), FadeIn(charge3))

        field.add_updater(rebuild)

        self.play(
            charge1.animate.shift(LEFT),
            charge2.animate.shift(RIGHT),
            charge3.animate.shift(DOWN * 0.5),
            run_time=2,
        )