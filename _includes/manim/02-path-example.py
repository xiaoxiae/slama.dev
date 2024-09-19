from manim import *


class Path(Polygram):
    def __init__(self, points, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_points_as_corners(points)

    def get_important_points(self):
        """Returns the important points of the curve."""
        # shot explanation: Manim uses quadratic Bézier curves to create paths
        # > each curve is determined by 4 points - 2 anchor and 2 control
        # > VMobject's builtin self.points returns *all* points
        # > we, however, only care about the anchors
        # > see https://en.wikipedia.org/wiki/Bézier_curve for more details
        return list(self.get_start_anchors()) + [self.get_end_anchors()[-1]]


class PathExample(Scene):
    def construct(self):
        path = Path([LEFT + UP, LEFT + DOWN, RIGHT + UP, RIGHT + DOWN], color=WHITE)

        self.play(Write(path))

        path_points = VGroup(*[Dot().move_to(point) for point in path.get_important_points()])

        self.play(Write(path_points))

        path2 = path.copy()
        path3 = path.copy()

        self.play(
            path2.animate.next_to(path, LEFT, buff=1),
            path3.animate.next_to(path, RIGHT, buff=1),
        )

        # flip(LEFT) flips top-down, because LEFT is the axis **by which** to flip
        self.play(
            path2.animate.flip(),
            path3.animate.flip(LEFT),
        )