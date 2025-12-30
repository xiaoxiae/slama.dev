from manim import *


class Basic3DExample(ThreeDScene):
    def construct(self):
        cube = Cube(side_length=3, fill_opacity=0.5)

        self.set_camera_orientation(phi=75 * DEGREES, theta=30 * DEGREES)

        self.play(FadeIn(cube))

        for axis in [RIGHT, UP, OUT]:
            self.play(Rotate(cube, PI / 2, about_point=ORIGIN, axis=axis))

        self.play(FadeOut(cube))
