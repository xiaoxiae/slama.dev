from manim import *
from random import *


class Sort(Scene):
    def construct(self):
        seed(0xDEADBEEF)

        n = 20
        value_min, value_max = 1, 20

        values = [randint(value_min, value_max) for _ in range(n)]

        # width of rectangles and the height of a single unit
        rectangle_width = 0.2
        unit_height = 0.2

        rectangle_spacing = 2.5

        rectangles = [
            Rectangle(
                width=rectangle_width,
                height=unit_height * v,
                fill_color=WHITE,
                fill_opacity=1,
            )
            for v in values
        ]

        # calculate the point at which to align all of the rectangles (so they're all centered)
        alignment_point = None
        max_value = 0
        for i, v in enumerate(values):
            if max_value < v:
                max_value = v
                alignment_point = Point().shift(DOWN * rectangles[i].height / 2)

        for i, rect in enumerate(rectangles):
            rect.shift(
                RIGHT
                * (i - (len(rectangles) - 1) / 2)
                * rectangle_width
                * rectangle_spacing
            ).align_to(alignment_point, DOWN)

        self.play(*[Write(r) for r in rectangles])

        def animate_at(a, b, duration):
            """Animate that we're looking at the positions a and b."""
            self.play(
                *[
                    r.animate.set_color(WHITE if i not in (a, b) else YELLOW)
                    for i, r in enumerate(rectangles)
                ],
                run_time=duration,
            )

        def animate_swap(a, b, duration):
            """Animate the swap of positions a and b."""
            self.play(
                rectangles[a]
                .animate.stretch_to_fit_height(values[a] * unit_height)
                .align_to(alignment_point, DOWN),
                rectangles[b]
                .animate.stretch_to_fit_height(values[b] * unit_height)
                .align_to(alignment_point, DOWN),
                run_time=duration,
            )

        # the first pass is slower
        speed_slow = 0.6
        speed_fast = 0.07

        for i in range(n):
            speed = speed_slow if i == 0 else speed_fast
            swapped = False
            for j in range(n - i - 1):
                animate_at(j, j + 1, speed)

                if values[j] > values[j + 1]:
                    values[j], values[j + 1] = values[j + 1], values[j]

                    animate_swap(j, j + 1, speed)
                    swapped = True

            # if the sequence is sorted, stop
            if not swapped:
                break

        self.play(*[FadeOut(r) for r in rectangles])
