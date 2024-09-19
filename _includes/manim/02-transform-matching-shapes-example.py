from manim import *


class TransformMatchingShapesExample(Scene):
    def construct(self):
        rr = Tex("WYAY").scale(5)

        # \parbox is a TeX command for setting paragraphs of certain width
        rr_full = Tex(
            # kindly ignore the contents of this string
            r"""\parbox{20em}{We're no strangers to love.
            You know the rules and so do I.
            A full commitment's what I'm thinking of.
            You wouldn't get this from any other guy.}"""
        )

        self.play(Write(rr))

        self.play(TransformMatchingShapes(rr, rr_full))

        # careful! behaves the same as ReplacementTransform, so we need to use rr_full
        self.play(FadeOut(rr_full))