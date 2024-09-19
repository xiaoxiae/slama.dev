from manim import *
from random import choice, seed


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


class BinomialDistributionSimulation(Scene):
    def create_graph(x_values, y_values):
        """Build a graph with the given values."""
        y_values_all = list(range(0, (max(y_values) or 1) + 1))

        axes = (
            Axes(
                x_range=[-n // 2 + 1, n // 2, 1],
                y_range=[0, max(y_values) or 1, 1],
                x_axis_config={"numbers_to_include": x_values},
                tips=False,
            )
            .scale(0.45)
            .shift(LEFT * 3.0)
        )

        graph = axes.plot_line_graph(x_values=x_values, y_values=y_values)

        return graph, axes

    def construct(self):
        seed(0xDEADBEEF2)  # hezčí vstupy :)

        radius = 0.13
        x_spacing = radius * 1.5
        y_spacing = 4 * radius

        n = 9
        pyramid = VGroup()
        pyramid_values = []  # how many marbles fell where

        # build the pyramid
        for i in range(1, n + 1):
            row = VGroup()

            for j in range(i):
                obj = Dot()

                # if it's the last row, make the rows numbers instead
                if i == n:
                    obj = Tex("0")
                    pyramid_values.append(0)

                row.add(obj)

            row.arrange(buff=2 * x_spacing)

            if len(pyramid) != 0:
                row.move_to(pyramid[-1]).shift(DOWN * y_spacing)

            pyramid.add(row)

        pyramid.move_to(RIGHT * 3.4)

        x_values = np.arange(-n // 2 + 1, n // 2 + 1, 1)

        graph, axes = create_graph(x_values, pyramid_values)

        self.play(Write(axes), Write(pyramid), Write(graph), run_time=1.5)

        for iteration in range(120):
            circle = (
                Circle(fill_opacity=1, stroke_opacity=0)
                .scale(radius)
                .next_to(pyramid[0][0], UP, buff=0)
            )

            # go faster and faster
            run_time = (
                0.5
                if iteration == 0
                else 0.1
                if iteration == 1
                else 0.02
                if iteration < 20
                else 0.003
            )

            self.play(FadeIn(circle, shift=DOWN * 0.5), run_time=run_time * 2)

            x = 0
            for i in range(1, n):
                next_position = choice([0, 1])
                x += next_position

                dir = LEFT if next_position == 0 else RIGHT

                circle_center = circle.get_center()

                # behave normally when it's not the last row
                if i != n - 1:
                    b = CubicBezier(
                        circle_center,
                        circle_center + dir * x_spacing,
                        circle_center + dir * x_spacing + DOWN * y_spacing / 2,
                        circle.copy().next_to(pyramid[i][x], UP, buff=0).get_center(),
                    )

                    self.play(
                        MoveAlongPath(circle, b, rate_func=rate_functions.ease_in_quad),
                        run_time=run_time,
                    )

                # if it is, animate fadeout and add
                else:
                    b = CubicBezier(
                        circle_center,
                        circle_center + dir * x_spacing,
                        circle_center + dir * x_spacing + DOWN * y_spacing / 2,
                        pyramid[i][x].get_center(),
                    )

                    pyramid_values[x] += 1

                    n_graph, n_axes = create_graph(x_values, pyramid_values)

                    self.play(
                        AnimationGroup(
                            AnimationGroup(
                                MoveAndFade(
                                    circle, b, rate_func=rate_functions.ease_in_quad
                                ),
                                run_time=run_time,
                            ),
                            AnimationGroup(
                                pyramid[i][x]
                                .animate(run_time=run_time)
                                .become(
                                    Tex(str(pyramid_values[x])).move_to(pyramid[i][x])
                                ),
                                graph.animate.become(n_graph),
                                axes.animate.become(n_axes),
                                run_time=run_time,
                            ),
                            lag_ratio=0.3,
                        )
                    )

        self.play(FadeOut(axes), FadeOut(pyramid), FadeOut(graph), run_time=1)
