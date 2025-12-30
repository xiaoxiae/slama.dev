from manim import *


class MoveTo(Scene):
    def construct(self):
        s1, s2, s3 = [Square() for _ in range(3)]

        self.play(*[Write(o) for o in [s1, s2, s3]])

        # align squares next to one another
        self.play(
            s1.animate.next_to(s2, LEFT),
            s3.animate.next_to(s2, RIGHT),
        )

        # create numbers for each of them
        # the Tex class will be discussed below
        t1, t2, t3 = [Tex(f"${i}$").scale(3) for i in range(3)]

        # move the numbers on top of the squares
        t1.move_to(s1)
        t2.move_to(s2)
        t3.move_to(s3)

        self.play(*[Write(o) for o in [t1, t2, t3]])
