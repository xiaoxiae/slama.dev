from manim import *


class MovingCameraExample(MovingCameraScene):
    def construct(self):
        square = Square()

        self.play(Write(square))

        self.camera.frame.save_state()

        # zoom for the square to fill in the entire view (+ a bit of space)
        self.play(self.camera.frame.animate.set_height(square.height * 1.5))

        circle = Circle().next_to(square, LEFT)

        # move the camera to the new object
        self.play(
            AnimationGroup(
                self.camera.frame.animate.move_to(circle),
                Write(circle),
                lag_ratio=0.5,
            )
        )

        self.wait(0.5)

        # zoom out (increasing frame size covers more of the screen)
        self.play(self.camera.frame.animate.scale(1.3))

        triangle = Triangle().next_to(square, RIGHT)

        # move the camera again
        self.play(
            AnimationGroup(
                self.camera.frame.animate.move_to(triangle),
                Write(triangle),
                lag_ratio=0.5,
            )
        )

        self.wait(0.5)

        self.play(self.camera.frame.animate.restore())
