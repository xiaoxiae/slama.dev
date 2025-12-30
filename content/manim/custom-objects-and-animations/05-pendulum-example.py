from manim import *


# example from https://github.com/Matheart/manim-physics
class PendulumExample(SpaceScene):
    def construct(self):
        # positions of the pendulum balls
        bob_positions = [RIGHT * 1.5 + UP, RIGHT * 1.5 + UP * 2]

        pendulum = MultiPendulum(
            *bob_positions,
            pivot_point=UP,
            bob_style={"color": WHITE, "fill_opacity": 1, "radius": 0.15},
        )

        self.make_rigid_body(pendulum.bobs)
        pendulum.start_swinging()

        self.add(pendulum)

        # we will track the movement of the pendulum balls
        for i, bob in enumerate(pendulum.bobs):
            self.bring_to_back(TracedPath(bob.get_center, stroke_color=DARK_GRAY))

        self.wait(12)
