from manim import *
from random import *


class Search(Scene):
    def construct(self):
        seed(0xDEADBEEF1)  # prettier input

        n = 10
        value_min, value_max = 1, n

        values = sorted([randint(value_min, value_max) for _ in range(n)])

        square_side_length = 0.75
        square_spacing = 1.3

        squares = [Square(side_length=square_side_length) for v in values]
        numbers = [Tex(f"${v}$") for v in values]

        # move rectangles such that they are centered
        for i, rect in enumerate(squares):
            rect.shift(
                RIGHT
                * (i - (len(squares) - 1) / 2)
                * square_side_length
                * square_spacing
            )

        # label positions
        for i, number in enumerate(numbers):
            number.move_to(squares[i])

        pointer_length = 0.4
        l_pointer = Arrow(start=DOWN * pointer_length, end=UP).next_to(squares[0], DOWN)
        r_pointer = Arrow(start=DOWN * pointer_length, end=UP).next_to(
            squares[-1], DOWN
        )

        self.play(*[Write(s) for s in squares], *[Write(n) for n in numbers])

        # print the number we're looking for
        target = randint(value_min, value_max)
        text = Tex(f"Target: ${target}$").shift(UP * 1.5)
        self.play(Write(text))

        self.play(Write(l_pointer), Write(r_pointer))

        lo, hi = 0, len(values) - 1

        def color_in_range(objects, color, range):
            """Return the animation of coloring the objects in the sequence."""
            return [
                o.animate.set_color(color) for i, o in enumerate(objects) if i in range
            ]

        while lo < hi:
            avg = (lo + hi) // 2

            current_arrow = (
                Arrow(start=DOWN * pointer_length, end=UP)
                .next_to(squares[avg], DOWN)
                .set_color(ORANGE)
            )

            self.play(Write(current_arrow))

            if values[avg] < target:
                # move left pointer
                self.play(
                    FadeOut(current_arrow),
                    l_pointer.animate.next_to(squares[avg + 1], DOWN),
                    *color_in_range(squares, DARK_GRAY, range(lo, avg + 1)),
                    *color_in_range(numbers, DARK_GRAY, range(lo, avg + 1)),
                )

                lo = avg + 1
            elif values[avg] >= target:
                # move right pointer
                self.play(
                    FadeOut(current_arrow),
                    r_pointer.animate.next_to(squares[avg], DOWN),
                    *color_in_range(squares, DARK_GRAY, range(avg + 1, hi + 1)),
                    *color_in_range(numbers, DARK_GRAY, range(avg + 1, hi + 1)),
                )

                hi = avg

            # the desired value has been found
            if values[hi] == target:
                self.play(
                    *color_in_range(squares, DARK_GRAY, range(hi)),
                    *color_in_range(squares, DARK_GRAY, range(hi + 1, n)),
                    *color_in_range(numbers, DARK_GRAY, range(hi)),
                    *color_in_range(numbers, DARK_GRAY, range(hi + 1, n)),
                    numbers[hi].animate.set_color(GREEN),
                    squares[hi].animate.set_color(GREEN),
                    FadeOut(l_pointer),
                )
                break

        self.play(*[FadeOut(r) for r in numbers + squares + [r_pointer, text]])
