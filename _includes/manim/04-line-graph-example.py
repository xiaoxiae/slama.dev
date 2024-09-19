from manim import *
from random import random, seed


class LineGraphExample(Scene):
    def construct(self):
        seed(0xDEADBEEF2)  # prettier input :P

        # value to graph (x, y);  np.arange(l, r, step) returns a list
        # from l (inclusive) do r (non-inclusive) with steps of size step
        x_values = np.arange(-1, 1 + 0.25, 0.25)
        y_values = [random() for _ in x_values]

        # include axis numbers this time
        axes = Axes(
            x_range=[-1, 1, 0.25],
            y_range=[-0.1, 1, 0.25],
            x_axis_config={"numbers_to_include": x_values},
            y_axis_config={"numbers_to_include": np.arange(0, 1, 0.25)},
            axis_config={"decimal_number_config": {"num_decimal_places": 2}},
        )

        labels = axes.get_axis_labels(x_label="x", y_label="y")

        graph = axes.plot_line_graph(x_values=x_values, y_values=y_values)

        self.play(Write(axes), Write(labels))

        self.play(Write(graph), run_time=2)

        self.play(Unwrite(axes), Unwrite(labels), Unwrite(graph))