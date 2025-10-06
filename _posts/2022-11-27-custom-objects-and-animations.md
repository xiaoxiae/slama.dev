---
title: Custom Objects and Animations
category: "Manim"
category_icon: /assets/category-icons/manim.svg
css: manim
category_part: 5
redirect_from:
- /manim/5/
- /manim/objects-animations-and-plugins/
excerpt: Custom objects and animations (and formerly plugins, but those are outdated now).
end: <a href="/manim/1/">Part 1</a>, <a href="/manim/2/">Part 2</a>, <a href="/manim/3/">Part 3</a>, <a href="/manim/4/">Part 4</a>, <strong>→ Part 5 ←</strong>, <a href="/manim/6/">Part 6</a>
---

- .
{:toc}

This part of the series covers creating custom objects and animations.

_This part used to also include plugins, but all of the original ones are broken as of v0.18.0._

### Custom objects
For more complex scenes, it might be a good idea to create custom Manim objects.
These usually reperesent more complex objects where simple primitives don't suffice.

To see how to create them, let's look at an example of a stack:

```py
{% include manim/05-stack-example.py %}
```

{% manim_video 05-stack-example %}

As the code suggests, every custom Manim object must inherit the {% manim_doc `Mobject` reference/manim.mobject.mobject.Mobject.html %} class (or {% manim_doc `VMobject` reference/manim.mobject.types.vectorized_mobject.VMobject.html %}, if it's a vector object).
The stack consists of other Manim objects, added to it via the {% manim_doc `add` reference/manim.mobject.mobject.Mobject.html#manim.mobject.mobject.Mobject.add %} method.
And, since it's a regular Manim object, we can interact with it like we would with any other Manim object.

### Custom animations
Custom animations are again very useful when you are dealing with more complex scenes or encounter the limitations of the builtin ones (like our `MoveAndFade` animation from the [previous part](/manim/4/)).

To see how to create them, it is again best to look at an example:

```py
{% include manim/05-starfox-example.py %}
```

{% manim_video 05-starfox-example %}

The example implements three new animations: `ColorfulFadeIn`, `Roll` and `Dissolve`.

The first (`ColorfulFadeIn`) inherits from the {% manim_doc `Animation` reference/manim.animation.animation.Animation.html %} class and implements an {% manim_doc `interpolate_mobject` reference/manim.animation.animation.Animation.html#manim.animation.animation.Animation.interpolate_mobject %} function, which is called every frame for the animation to play out. It is also an **introducer** (as seen from the `introducer` keyword argument), meaning that it "introduces" objects to the scene (important for animations to function properly).

The second (`Roll`) also inherits from the {% manim_doc `Animation` reference/manim.animation.animation.Animation.html %} class.

The last (`Dissolve`) inherits from the {% manim_doc `AnimationGroup` reference/manim.animation.composition.AnimationGroup.html %} (which itself inherits from the {% manim_doc `Animation` reference/manim.animation.animation.Animation.html %} class) and is used to define animations made out of subanimations. It is also a **remover** (as again seen by the `remover` keyword argument), meaning that it "removes" objects from the scene (again, quite important for everything to work).

<!--

This section has been nuked for now since all of the plugins I showcased are broken in v0.18.0 and there are some more cool new ones:
- https://github.com/GarryBGoode/Manim_CAD_Drawing_utils
- https://github.com/UnMolDeQuimica/manim-Chemistry
- https://github.com/GarryBGoode/manim-GearBox

### Plugins
Since we now know how to create custom Manim objects and animation, it is a good idea to explore [plugins](https://docs.manim.community/en/stable/plugins.html).
Plugins extend Manim's basic functionality in various ways, be it defining new classes and objects, or implementing an [editor simplifying working with Manim](https://github.com/ManimCommunity/manim_editor).
This part includes some more interesting plugins that you might find.

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

-->
