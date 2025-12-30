from manim import *
from random import *


class MovingCameraUpdaterExample(MovingCameraScene):
    def construct(self):
        seed(0xDEADBEEF)

        n = 11**2

        circles = VGroup(
            *[
                Circle(radius=0.1)
                .scale(uniform(0.5, 2))
                .shift(UP * uniform(-3, 3) + RIGHT * uniform(-5, 5))
                .set_color(WHITE)
                for _ in range(n)
            ]
        )

        # the circle we'll follow
        target = circles[n // 2]

        def follow_camera(camera):
            """An updater that makes sure the camera is on top of the target."""
            camera.move_to(target.get_center())

        self.camera.frame.add_updater(follow_camera)

        # TRIPLE CAUTION!
        # updaters only work on things added to the scene
        # since self.camera.frame is, by default, not on the scene, we need to add it
        self.add(self.camera.frame)

        self.play(FadeIn(circles))

        scale_factor = 0.7

        def arrange_and_zoom(rows, color):
            """Arrange the circles in a grid, zooming the camera in the process."""
            self.play(
                circles.animate.arrange_in_grid(rows=rows).set_color(color),
                self.camera.frame.animate.scale(scale_factor),
                run_time=1.5,
            )

        arrange_and_zoom(7, RED)
        arrange_and_zoom(5, GREEN)
        arrange_and_zoom(14, BLUE)
