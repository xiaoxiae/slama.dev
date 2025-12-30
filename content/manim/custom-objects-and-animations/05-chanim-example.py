from manim import *


class ChanimExample(Scene):
    def construct(self):
        # internally uses ChemFig syntax (https://www.ctan.org/pkg/chemfig)
        chem = ChemWithName(
            "*6((=O)-N(-CH_3)-*5(-N=-N(-CH_3)-=)--(=O)-N(-H_3C)-)", "Caffeine"
        )

        chem.move_to(ORIGIN)

        self.play(chem.creation_anim())
