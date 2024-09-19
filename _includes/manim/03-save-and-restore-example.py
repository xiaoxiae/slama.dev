from manim import *

class SaveAndRestoreExample(Scene):
    def construct(self):
        square = Square()

        square.save_state()

        self.play(Write(square))

        self.play(square.animate.set_fill(WHITE, 1))
        self.play(square.animate.scale(1.5).rotate(PI / 4))
        self.play(square.animate.set_color(BLUE))

        self.play(square.animate.restore())

        self.play(Unwrite(square))