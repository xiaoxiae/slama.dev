from manim import *
from random import *
import networkx as nx


class GraphGenerationExample(Scene):
    def construct(self):
        seed(0xDEADBEEF)

        n = 12  # number of vertices
        p = 3 / n  # probability that there is an edge between a pair

        # generate until our graph is not connected (so it looks nicer)
        graph = None
        while graph is None or not nx.is_connected(graph):
            graph = nx.generators.random_graphs.gnp_random_graph(n, p)

        g = (
            Graph.from_networkx(graph, layout_config={"seed": 0})
            .scale(2.2)
            .rotate(-PI / 2)
        )

        self.play(Write(g))
