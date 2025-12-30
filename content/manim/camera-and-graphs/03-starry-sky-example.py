from manim import *
from random import uniform, randint, seed


class StarrySkyExample(Scene):
    def construct(self):
        seed(0xDEADBEEF)

        # the graph class expects a list of vertices and edges
        vertices = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
        edges = [
            (1, 2),
            (2, 3),
            (3, 4),
            (2, 4),
            (2, 5),
            (6, 5),
            (1, 7),
            (5, 7),
            (2, 8),
            (1, 9),
            (10, 8),
            (5, 11),
        ]

        def RandomStar():
            """Create a pretty random star."""
            return Star(
                randint(5, 7), fill_opacity=1, outer_radius=0.1, color=WHITE
            ).rotate(uniform(0, 2 * PI))

        def RandomSkyLine(u, v, z_index=None):
            """Create a pretty random sky line. The z_index is necessary, since it is
            passed by the graph constructor to edges so they're behind vertices."""
            return DashedLine(u, v, dash_length=uniform(0.03, 0.07), z_index=z_index)

        # custom graph with star vertices and dashed line edges
        g = (
            Graph(
                vertices,
                edges,
                layout_config={"seed": 0},
                vertex_type=RandomStar,
                edge_type=RandomSkyLine,
            )
            .scale(2)
            .rotate(-PI / 2)
        )

        self.play(Write(g))

        self.play(FadeOut(g))
