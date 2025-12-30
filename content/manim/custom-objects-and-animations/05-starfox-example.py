from manim import *


class ColorfulFadeIn(Animation):
    """An animation that fades in an object... but colorfully."""

    def __init__(self, mobject: Mobject, introducer=True, **kwargs):
        # we're using the introducer keyword argument
        # because the animation adds the objects to the scene

        # the original version of the object will be useful,
        # since we'll be changing it
        self.original = mobject.copy()

        super().__init__(mobject, introducer=introducer, **kwargs)

    def interpolate_mobject(self, alpha: float) -> None:
        """A function that gets called every frame, for the animation to... animate."""

        # the animation could have a custom rate function, but alpha is linear (0 to 1)
        # this means that we will have to apply it to get the appropriate behavior
        new_alpha = self.rate_func(alpha)

        colors = ["#ffd166", RED, "#06d6a0", BLUE] + [self.original.get_color()]

        for i, color in enumerate(colors):
            if i + 1 >= new_alpha * len(colors):
                new_color = interpolate_color(
                    colors[i - 1],
                    colors[i],
                    1 - (i + 1 - new_alpha * len(colors)),
                )
                break

        new_mobject = self.original.copy().set_opacity(new_alpha).set_color(new_color)

        self.mobject.become(new_mobject)


class Roll(Animation):
    """A rolling animation."""

    def __init__(self, mobject: Mobject, angle, direction, scale_ratio=0.85, **kwargs):
        # the original version of the object will be useful, since we'll be changing it
        self.original = mobject.copy()

        self.scale_ratio = scale_ratio
        self.angle = angle
        self.direction = direction

        super().__init__(mobject, **kwargs)

    def interpolate_mobject(self, alpha: float) -> None:
        """A function that gets called every frame, for the animation to... animate."""

        actual_alpha = self.rate_func(alpha)

        # each function will have scale 1 in the beginning, scale_ration in the middle
        # and 1 at the end (probably not the most elegant way to achieve this)
        scale_alpha = 1 - (1 - self.scale_ratio) * 2 * (0.5 - abs(actual_alpha - 0.5))

        # we want the object to move there and back
        direction_alpha = there_and_back(actual_alpha)

        self.mobject.become(self.original.copy()).rotate(
            actual_alpha * self.angle
        ).scale(scale_alpha).shift(self.direction * direction_alpha)


class Dissolve(AnimationGroup):
    """An animation that dissolves an object (shrinks + flashes)."""

    def __init__(self, mobject: Mobject, remover=True, **kwargs):
        # we're using the remover keyword argument, because the animation adds the
        # objects to the scene (can be seen when running self.mobjects after)

        self.original = mobject.copy()

        a1 = mobject.animate.scale(0)
        a2 = Flash(mobject, color=mobject.color)

        super().__init__(a1, a2, lag_ratio=0.75, remover=remover, **kwargs)


class StarFox(Scene):
    def construct(self):
        square = Square(color=BLUE, fill_opacity=0.75).scale(1.5)

        self.play(ColorfulFadeIn(square), run_time=3)

        self.play(Roll(square, angle=PI, direction=LEFT * 0.75))
        self.play(Roll(square, angle=-PI, direction=RIGHT * 0.75))

        self.play(Dissolve(square))
