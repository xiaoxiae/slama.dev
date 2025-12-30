from manim import *


class MoveAndFade(Animation):
    def __init__(self, mobject: Mobject, path: VMobject, **kwargs):
        self.path = path
        self.original = mobject.copy()
        super().__init__(mobject, **kwargs)

    def interpolate_mobject(self, alpha: float) -> None:
        point = self.path.point_from_proportion(self.rate_func(alpha))

        # this is not entirely clean sice we're creating a new object
        # this is because obj.fade() doesn't add opaqueness but adds it
        self.mobject.become(self.original.copy()).move_to(point).fade(alpha)


class BezierExample(Scene):
    def construct(self):
        point_coordinates = [
            UP + LEFT * 3,  # starting
            UP + RIGHT * 2,  # 1. control
            DOWN + LEFT * 2,  # 2. control
            DOWN + RIGHT * 3,  # starting
        ]

        points = VGroup(
            *[Dot().move_to(position) for position in point_coordinates]
        ).scale(1.5)

        # make control points blue
        points[1].set_color(BLUE)
        points[2].set_color(BLUE)

        bezier = CubicBezier(*point_coordinates).scale(1.5)

        self.play(Write(bezier), Write(points))

        # regular moving along path
        circle = (
            Circle(fill_color=GREEN, fill_opacity=1, stroke_opacity=0)
            .scale(0.25)
            .move_to(points[0])
        )

        self.play(FadeIn(circle, shift=RIGHT * 0.5))
        self.play(MoveAlongPath(circle, bezier))

        self.play(FadeOut(circle))

        # moving along path with fading
        circle = (
            Circle(fill_color=GREEN, fill_opacity=1, stroke_opacity=0)
            .scale(0.25)
            .move_to(points[0])
        )

        self.play(FadeIn(circle, shift=RIGHT * 0.5))
        self.play(MoveAndFade(circle, bezier))

        self.play(FadeOut(bezier), FadeOut(points), FadeOut(circle))
