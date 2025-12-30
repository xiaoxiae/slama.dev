from manim import *
from manim.opengl import *


class BunnyScene(Scene):
    def construct(self):
        pointcloud = OpenGLPMobject()

        # one side of the Stanford bunny
        # https://slama.dev/assets/manim/bunny.txt
        points = []
        with open("bunny.txt") as f:
            for line in f.read().splitlines():
                points.append(list(map(float, line.split())))

        pointcloud.add_points(points)

        # scale + color
        pointcloud.scale(20)
        pointcloud.set_color_by_gradient((RED, GREEN, BLUE))

        self.play(Create(pointcloud))

        self.interactive_embed()
