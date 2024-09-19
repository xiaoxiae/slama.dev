from manim import *
from random import *
import networkx as nx


class GraphAlgorithm(Scene):
    def construct(self):
        seed(0xDEADBEEF)

        n = 14
        p = 3 / n

        VISITED_COLOR = GREEN
        NEIGHBOUR_COLOR = BLUE

        graph = None
        while graph is None or not nx.is_connected(graph):
            graph = nx.generators.random_graphs.gnp_random_graph(n, p)

        g = (
            Graph(graph.nodes, graph.edges, layout_config={"seed": 0})
            .scale(2.7)
            .rotate(PI / 12)
        )

        # quickfix for a bug in AnimationGroup's handling of z_index
        for v in g.vertices:
            g.vertices[v].set_z_index(1)

        explored = set()

        def dfs(v, position_object):
            """Recursive DFS which moves the position_object."""
            neighbours = list(graph.neighbors(v))

            for w in neighbours:
                if w in explored:
                    continue

                edge = (v, w) if (v, w) in g.edges else (w, v)

                unexplored_neighbours = [w for w in neighbours if w not in explored]
                unexplored_neighbour_edges = [
                    (a, b)
                    for a, b in g.edges
                    if (a == v and b in unexplored_neighbours)
                    or (b == v and a in unexplored_neighbours)
                ]

                # while there exist unexplored neighbours, explore
                if len(unexplored_neighbours) != 0:
                    self.play(
                        *[
                            g.vertices[q].animate.set_color(NEIGHBOUR_COLOR)
                            for q in unexplored_neighbours
                        ],
                        *[
                            g.edges[e].animate.set_color(NEIGHBOUR_COLOR)
                            for e in unexplored_neighbour_edges
                        ],
                    )

                explored.add(w)

                # animation of transitioning to neighbouring vertex
                # has two parts - first initialize the move and then change color (+ flash)
                self.play(
                    AnimationGroup(
                        position_object.animate.move_to(g.vertices[w]),
                        AnimationGroup(
                            Flash(g.vertices[w], color=VISITED_COLOR, flash_radius=0.3),
                            g.edges[edge].animate.set_color(VISITED_COLOR),
                            g.vertices[w].animate.set_color(VISITED_COLOR),
                            *[
                                g.vertices[q].animate.set_color(WHITE)
                                for q in unexplored_neighbours
                                if q != w
                            ],
                            *[
                                g.edges[(a, b)].animate.set_color(WHITE)
                                for (a, b) in unexplored_neighbour_edges
                                if (a, b) != edge
                            ],
                        ),
                        lag_ratio=0.45,
                    )
                )

                dfs(w, position_object)
                self.play(position_object.animate.move_to(g.vertices[v]))

        self.play(Write(g))

        start_vertex = 0

        position_object = (
            Circle(fill_color=VISITED_COLOR, fill_opacity=1, stroke_color=VISITED_COLOR)
            .move_to(g.vertices[start_vertex])
            .scale(0.15)
        )

        self.play(
            Flash(g.vertices[start_vertex], color=VISITED_COLOR, flash_radius=0.3),
            g.vertices[start_vertex].animate.set_color(VISITED_COLOR),
        )

        self.add(position_object)

        # run DFS
        explored.add(start_vertex)
        dfs(start_vertex, position_object)

        self.remove(position_object)
        self.play(Unwrite(g))
