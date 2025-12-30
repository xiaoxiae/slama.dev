from manim import *


class WriteVsCreate(Scene):
    def construct(self):
        s1 = Square(stroke_width=5)
        t1 = Tex("Write")

        s2 = Square(stroke_width=5)
        t2 = Tex("Create")

        VGroup(
            VGroup(s1, t1).arrange(DOWN),
            VGroup(s2, t2).arrange(DOWN),
        ).arrange(buff=1)

        # write also animates the outline
        self.play(FadeIn(t1))
        self.play(Write(s1, run_time=2))
        self.play(s1.animate.set_color(DARK_GRAY))

        # create does not and is therefore better suited
        # the rate_func parameter is magic for now and is covered in the next part
        self.play(FadeIn(t2))
        self.play(Create(s2, run_time=2, rate_func=linear))
        self.play(s2.animate.set_color(DARK_GRAY))

        self.wait()
