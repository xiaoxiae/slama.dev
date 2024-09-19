from manim import *


# example from https://github.com/Matheart/manim-physics
# SpaceScene is a class that supports physical interactions
class FallingObjectsExample(SpaceScene):
    def construct(self):
        circle = Circle().shift(UP)
        circle.set_fill(RED, 1)
        circle.shift(DOWN + RIGHT)

        rect = Square().shift(UP)
        rect.rotate(PI / 4)
        rect.set_fill(YELLOW_A, 1)
        rect.shift(UP * 2)
        rect.scale(0.5)

        ground = Line([-4, -3.5, 0], [4, -3.5, 0])
        wall1 = Line([-4, -3.5, 0], [-4, 3.5, 0])
        wall2 = Line([4, -3.5, 0], [4, 3.5, 0])
        walls = VGroup(ground, wall1, wall2)
        self.add(walls)

        self.play(
            DrawBorderThenFill(circle),
            DrawBorderThenFill(rect),
        )

        # it was regular Manim code until here
        self.make_rigid_body(rect, circle)  # squares are rigid (they move)
        self.make_static_body(walls)        # walls are static (they don't move)

        # now we wait for the objects to fall
        self.wait(5)