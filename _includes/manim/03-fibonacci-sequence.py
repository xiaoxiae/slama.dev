from manim import *
from random import *


class FibonacciSequence(MovingCameraScene):
    def create_square(self, size):
        """Create a square of the given size."""
        return VGroup(Square(side_length=size), Tex(f"${size}^2$").scale(size))

    def get_camera_centering_animation(self, squares):
        """Center (and scale) the camera at the given square."""
        h = squares.height * 1.5
        return self.camera.frame.animate.set_height(h).move_to(squares)

    def construct(self):
        squares = VGroup(self.create_square(1))

        self.play(
            Write(squares[0]),
            self.get_camera_centering_animation(squares[0])
        )

        self.camera.frame.save_state()

        n = 7

        # create the squares
        a = 1
        b = 1
        directions = [RIGHT, UP, LEFT, DOWN]
        for i in range(n):
            b = b + a
            a = b - a

            direction = directions[i % 4]

            new_square = self.create_square(a).next_to(squares, direction, buff=0)
            squares.add(new_square)

            self.play(
                FadeIn(new_square, shift=direction * a / 3),
                self.get_camera_centering_animation(squares),
            )

        dot = Dot().move_to(squares[0].get_corner(LEFT + UP)).scale(0.5)

        path = TracedPath(dot.get_center)

        self.wait(1)

        # start the spiral
        self.play(
            squares.animate.set_color(DARK_GRAY),
            AnimationGroup(
                self.camera.frame.animate.restore().move_to(dot),
                Write(dot),
                lag_ratio=0.5,
            ),
        )

        # keep a copy of the dot at the origin
        center_dot = dot.copy()
        self.add(center_dot)

        # for scaling the dot
        starting_frame_height = self.camera.frame.height

        def update_camera_position(camera):
            """Updater k pozicování kamery nad tečkou."""
            camera.move_to(dot.get_center())

        def update_spiral(path):
            """Scale the thickness of the stroke with the zoom of the camera."""
            path.set_stroke_width(self.camera.frame.height / 1.5)

        def update_dot(dot):
            """Scale the size of the dot with the zoom of the camera."""
            dot.set_height(center_dot.height * (self.camera.frame.height / starting_frame_height))

        # don't forget to add the path to the scene so it gets animated
        self.add(path)

        path.add_updater(update_spiral)

        self.camera.frame.add_updater(update_camera_position)

        dot.add_updater(update_dot)

        a = 0
        b = 1
        for i in range(n + 1):
            # the directions are defined in a way where neighbouring directions correspond
            # to points around which we want to rotate
            direction = directions[i % 4] + directions[(i + 1) % 4]
            b = b + a
            a = b - a

            # we're zooming by about the golden ratio each rotation (a little less for
            # the animation to look smoother)
            phi = (1 + 5 ** (1 / 2)) / 2
            zoom_coefficient = phi * 0.9

            self.play(
                Rotate(
                    dot,
                    about_point=squares[i].get_corner(direction),
                    angle=PI / 2,
                ),
                self.camera.frame.animate.scale(zoom_coefficient),
                rate_func=linear,
            )

        # cleanup
        self.camera.frame.clear_updaters()
        path.clear_updaters()
        dot.clear_updaters()

        self.play(self.get_camera_centering_animation(squares))

        self.wait(1)

        self.play(
            FadeOut(squares),
            FadeOut(dot),
            AnimationGroup(
                Unwrite(path, run_time=2),
                AnimationGroup(Flash(center_dot, color=WHITE), FadeOut(center_dot)),
                lag_ratio=0.9,
            ),
        )
