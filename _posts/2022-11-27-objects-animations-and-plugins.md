---
title: Manim – Objects, Animations and Plugins
category: "Manim"
category_icon: /assets/category-icons/manim.svg
css: manim
category_part: 5
redirect_from:
- /manim/5/
---

[Part 1](/manim/1/), [Part 2](/manim/2/), [Part 3](/manim/3/), [Part 4](/manim/4/), **→ Part 5 ←**

- .
{:toc}

This part of the series covers creating custom objects and animations, and also showcases some interesting community-made plugins.

### Custom objects
For more complex scenes, it might be a good idea to create custom Manim objects.
These usually reperesent more complex objects where simple primitives don't suffice.

To see how to create them, let's look at an example of a stack:

```py
from manim import *


class Stack(VMobject):
    def __init__(self, size, **kwargs):
        # initialize the vmobject
        super().__init__(**kwargs)

        self.squares = VGroup()
        self.labels = VGroup()
        self.index = 0
        self.pointer = Arrow(ORIGIN, UP * 1.2)

        for _ in range(size):
            self.squares.add(Square(side_length=0.8))

        self.squares.arrange(buff=0.15)

        self.pointer.next_to(self.squares[0], DOWN)

        # IMPORTANT - we have to add all of the subobjects for them to be displayed
        self.add(self.squares, self.pointer, self.labels)

    def __peek(self) -> VMobject:
        """Return the current top element in the stack."""
        return self.squares[self.index]

    def __create_label(self, element) -> VMobject:
        """Create the label for the given element (given its color and size)."""
        return (
            Tex(str(element))
            .set_height(self.__peek().height / 2)
            .set_color(self.__peek().get_color())
            .move_to(self.__peek())
            .set_z_index(1)  # labels on top!
        )

    def __animate_indicate(self, element, increase: bool = True) -> Animation:
        """Return an animation indicating the current element."""
        return Indicate(
            element,
            color=self.__peek().get_color(),
            scale_factor=1.1 if increase else 1/1.1,
        )

    def push(self, element) -> Animation:
        """Pushes an element onto the stack, returning an appropriate animation."""
        label = self.__create_label(element)
        self.labels.add(label)

        self.index += 1

        return AnimationGroup(
            FadeIn(label),
            self.pointer.animate.next_to(self.__peek(), DOWN),
            self.__animate_indicate(self.squares[self.index - 1], increase=True),
        )

    def pop(self) -> AnimationGroup:
        """Pops an element from the stack, returning an appropriate animation."""
        label = self.labels[-1]
        self.labels.remove(label)

        self.index -= 1

        return AnimationGroup(
            FadeOut(label),
            self.pointer.animate.next_to(self.__peek(), DOWN),
            self.__animate_indicate(self.__peek(), increase=False),
        )

    def clear(self) -> AnimationGroup:
        """Clear the entire stack, returning the appropriate animation."""
        result = Succession(*[self.pop() for _ in range(self.index)])

        self.index = 0

        return result


class StackExample(Scene):
    def construct(self):
        stack = Stack(10)

        self.play(Write(stack))

        self.wait(0.5)

        for i in range(5):
            self.play(stack.push(i))

        self.play(stack.pop())

        self.wait(0.5)

        # we can even use the animate syntax!
        self.play(stack.animate.scale(1.2).set_color(BLUE))

        self.wait(0.5)

        for i in range(2):
            self.play(stack.push(i))

        self.play(stack.pop())

        self.play(stack.clear())

        self.play(FadeOut(stack))
```

{% manim_video 5-StackExample %}

As the code suggests, every custom Manim object must inherit the {% manim_doc `Mobject` reference/manim.mobject.mobject.Mobject.html %} class (or {% manim_doc `VMobject` reference/manim.mobject.types.vectorized_mobject.VMobject.html %}, if it's a vector object).
The stack consists of other Manim objects, added to it via the {% manim_doc `add` reference/manim.mobject.mobject.Mobject.html#manim.mobject.mobject.Mobject.add %} method.
And, since it's a regular Manim object, we can interact with it like we would with any other Manim object.

### Custom animations
Custom animations are again very useful when you are dealing with more complex scenes or encounter the limitations of the builtin ones (like our `MoveAndFade` animation from the [previous part](/manim/4/)).

To see how to create them, it is again best to look at an example:

```py
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

        self.mobject.become(self.original.copy())\
            .rotate(actual_alpha * self.angle)\
            .scale(scale_alpha)\
            .shift(self.direction * direction_alpha)


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
```

{% manim_video 5-StarFox %}

The example implements three new animations: `ColorfulFadeIn`, `Roll` and `Dissolve`.

The first (`ColorfulFadeIn`) inherits from the {% manim_doc `Animation` reference/manim.animation.animation.Animation.html %} class and implements an {% manim_doc `interpolate_mobject` reference/manim.animation.animation.Animation.html#manim.animation.animation.Animation.interpolate_mobject %} function, which is called every frame for the animation to play out. It is also an **introducer** (as seen from the `introducer` keyword argument), meaning that it "introduces" objects to the scene (important for animations to function properly).

The second (`Roll`) also inherits from the {% manim_doc `Animation` reference/manim.animation.animation.Animation.html %} class.

The last (`Dissolve`) inherits from the {% manim_doc `AnimationGroup` reference/manim.animation.composition.AnimationGroup.html %} (which itself inherits from the {% manim_doc `Animation` reference/manim.animation.animation.Animation.html %} class) and is used to define animations made out of subanimations. It is also a **remover** (as again seen by the `remover` keyword argument), meaning that it "removes" objects from the scene (again, quite important for everything to work).

### Plugins
Since we now know how to create custom Manim objects and animation, it is a good idea to explore [plugins](https://docs.manim.community/en/stable/plugins.html).
Plugins extend Manim's basic functionality in various ways, be it defining new classes and objects, or implementing an [editor simplifying working with Manim](https://github.com/ManimCommunity/manim_editor).
This part includes some more interesting plugins that you might find into.

#### Physics

The first plugin to look at is `manim-physics` [[GitHub](https://github.com/Matheart/manim-physics)] [[doc](https://manim-physics.readthedocs.io/en/latest/)], which (as the name suggests) adds classes to work with various branches of physics.
It can be installed by running
```
pip install manim-physics
```

Here are a few interesting examples of animations that you can create with this plugin:

```py
from manim import *


# example from https://github.com/Matheart/manim-physics
# SpaceScene is a class that supports physical interactions
class FallingObjectsExample(SpaceScene):
    def construct(self):
        circle = Circle().shift(UP)
        circle.set_fill(RED, 1)
        circle.shift(DOWN + RIGHT)

        rect = Square().shift(UP)
        rect.rotate(PI / 4)
        rect.set_fill(YELLOW_A, 1)
        rect.shift(UP * 2)
        rect.scale(0.5)

        ground = Line([-4, -3.5, 0], [4, -3.5, 0])
        wall1 = Line([-4, -3.5, 0], [-4, 3.5, 0])
        wall2 = Line([4, -3.5, 0], [4, 3.5, 0])
        walls = VGroup(ground, wall1, wall2)
        self.add(walls)

        self.play(
            DrawBorderThenFill(circle),
            DrawBorderThenFill(rect),
        )

        # it was regular Manim code until here
        self.make_rigid_body(rect, circle)  # squares are rigid (they move)
        self.make_static_body(walls)        # walls are static (they don't move)

        # now we wait for the objects to fall
        self.wait(5)
```

{% manim_video 5-FallingObjectsExample %}

```py
from manim import *


# example from https://github.com/Matheart/manim-physics
class ElectricFieldExample(Scene):
    def construct(self):
        charge1 = Charge(-1, LEFT + DOWN)
        charge2 = Charge(2, RIGHT + DOWN)
        charge3 = Charge(-1, UP)

        def rebuild(field):
            """Funkce která přestaví elektrické pole."""
            field.become(ElectricField(charge1, charge2, charge3))

        field = ElectricField(charge1, charge2, charge3)

        self.add(field, charge1, charge2, charge3)

        self.play(Write(field), FadeIn(charge1), FadeIn(charge2), FadeIn(charge3))

        field.add_updater(rebuild)

        self.play(
            charge1.animate.shift(LEFT),
            charge2.animate.shift(RIGHT),
            charge3.animate.shift(DOWN * 0.5),
            run_time=2,
        )
```

{% manim_video 5-ElectricFieldExample %}

```py
from manim import *


# example from https://github.com/Matheart/manim-physics
class MagnetismExample(Scene):
    def construct(self):
        current1 = Current(LEFT * 2.5)
        current2 = Current(RIGHT * 2.5, direction=IN)

        def rebuild(field):
            """Funkce která přestaví magnetické pole."""
            field.become(MagneticField(current1, current2))

        field = MagneticField(current1, current2)

        self.play(Write(field), FadeIn(current1), FadeIn(current2))

        field.add_updater(rebuild)

        self.play(
            Rotate(current1, about_point=ORIGIN, angle=PI),
            Rotate(current2, about_point=ORIGIN, angle=PI),
            run_time=2,
        )
```

{% manim_video 5-MagnetismExample %}

```py
from manim import *


# example from https://github.com/Matheart/manim-physics
class PendulumExample(SpaceScene):
    def construct(self):
        # positions of the pendulum balls
        bob_positions = [RIGHT * 1.5 + UP, RIGHT * 1.5 + UP * 2]

        pendulum = MultiPendulum(
            *bob_positions,
            pivot_point=UP,
            bob_style={"color": WHITE, "fill_opacity": 1, "radius": 0.15},
        )

        self.make_rigid_body(pendulum.bobs)
        pendulum.start_swinging()

        self.add(pendulum)

        # we will track the movement of the pendulum balls
        for i, bob in enumerate(pendulum.bobs):
            self.bring_to_back(TracedPath(bob.get_center, stroke_color=DARK_GRAY))

        self.wait(12)
```

{% manim_video 5-PendulumExample %}

#### Chemistry

The second plugin is `chanim` [[GitHub](https://github.com/raghavg123/chanim)], which implements classes for animating chemistry notation.

It can be installed similarly using
```
pip install chanim
```

Here are a few examples of animating chemistry compounds:

```py
from manim import *


class ChanimExample(Scene):
    def construct(self):
        # internally uses ChemFig syntax (https://www.ctan.org/pkg/chemfig)
        chem = ChemWithName(
            "*6((=O)-N(-CH_3)-*5(-N=-N(-CH_3)-=)--(=O)-N(-H_3C)-)",
            "Caffeine"
        )

        chem.move_to(ORIGIN)

        self.play(chem.creation_anim())
```

{% manim_video 5-ChanimExample %}
