from manim import *


class Path(VMobject):
    def __init__(self, points, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_points_as_corners(points)

    def get_important_points(self):
        return list(self.get_start_anchors()) + [self.get_end_anchors()[-1]]


class Hilbert(Scene):
    def construct(self):
        points = [LEFT + DOWN, LEFT + UP, RIGHT + UP, RIGHT + DOWN]

        hilbert = Path(points).scale(3)

        self.play(Create(hilbert), rate_func=linear)

        for i in range(1, 6):
            # length of a single segment in the curve
            new_segment_length = 1 / (2 ** (i + 1) - 1)

            # scale the curve such that it it is centered
            new_scale = (1 - new_segment_length) / 2

            # save the previous (large) curve to align smaller ones by it
            lu = hilbert.copy()
            lu, hilbert = hilbert, lu

            self.play(
                lu.animate.scale(new_scale)
                .set_color(DARK_GRAY)
                .align_to(hilbert, points[1])
            )

            ru = lu.copy()
            self.play(ru.animate.align_to(hilbert, points[2]))

            ld, rd = lu.copy(), ru.copy()
            self.play(
                ld.animate.align_to(hilbert, points[0]).rotate(-PI / 2),
                rd.animate.align_to(hilbert, points[3]).rotate(PI / 2),
            )

            new_hilbert = Path(
                list(ld.flip(LEFT).get_important_points())
                + list(lu.get_important_points())
                + list(ru.get_important_points())
                + list(rd.flip(LEFT).get_important_points())
            )

            # Create will be exponentially longer so it looks nice
            self.play(Create(new_hilbert, run_time=1.5 ** (i - 1)), rate_func=linear)

            self.remove(lu, ru, ld, rd)

            hilbert = new_hilbert
