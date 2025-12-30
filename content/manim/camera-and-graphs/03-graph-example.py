from manim import *


class GraphExample(Scene):
    def construct(self):
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

        # we're using the layout_config's seed parameter to deterministically set the
        # vertex positions (it is otherwise set randomly)
        g = Graph(vertices, edges, layout_config={"seed": 0}).scale(1.6)

        self.play(Write(g))

        # the graph contains updaters that align edges with their vertices
        self.play(g.vertices[6].animate.shift((LEFT + DOWN) * 0.5))

        self.play(g.animate.shift(LEFT * 3))

        # the graphs can also contain labels and be organized into specific layouts
        # (see the Graph class documentation for the list of all possible layouts)
        h = Graph(vertices, edges, labels=True, layout="circular").shift(RIGHT * 3)

        self.play(Write(h))

        # color the vertex 5 and all of its neighbours
        v = 5
        self.play(
            Flash(g.vertices[v], color=RED, flash_radius=0.5),
            g.vertices[v].animate.set_color(RED),
            *[g.edges[e].animate.set_color(RED) for e in g.edges if v in e],
        )
