from manim import *


class TracePathExample(Scene):
    def construct(self):
        dot = Dot().shift(LEFT)

        self.play(Write(dot))

        # TracedPath accepts a function that returns the position of the object to trace
        path = TracedPath(dot.get_center)

        # we mustn't forget to add the path to the scene for it to get updated!
        self.add(path)

        self.play(Rotate(dot, about_point=ORIGIN))

        self.play(dot.animate.shift(UP))
        self.play(dot.animate.shift(LEFT * 2))
        self.play(dot.animate.shift(DOWN))

        path.clear_updaters()

        self.play(dot.animate.shift(RIGHT * 2))
