---
title: Manim [1] – Introduction
category: "Manim"
category_icon: /assets/category-icons/manim.svg
css: manim
---

**→ Part 1 ←**, [Part 2](/manim/groups-transformations-updaters/), [Part 3](/manim/camera-and-graphs/), [Part 4](/manim/3d-and-the-other-graphs/)

_Over the course of this year, I created a well-received "Introduction to Manim" series for [KSP](https://ksp.mff.cuni.cz/) (Czech CS-oriented correspondence seminar), so it made sense to make it more accessible by translating it to English and publish it here._

- .
{:toc}

Animations are better than pictures, be it when presenting interesting ideas or visualizing algorithms.
That is why it's useful to know how to create them, ideally programmatically.
This is the main motivation behind learning **Manim** -- a Python library created by Grant Sanderson ([3b1b](https://www.youtube.com/c/3blue1brown)), which this multipart series aims to cover.

### Preface
To follow the series, basic knowledge of Python is required.
It is also useful to know the basics of \(\TeX\), which we'll use to typeset math and text, but it is not required.
You will also need to [install Manim](https://docs.manim.community/en/stable/installation.html) if you wish to try the example code yourself.

Each part of the series contain a number of tasks for the reader to implement, which use the covered concepts.
The author's solutions are always provided (you are, however, highly encouraged to try to implement them first).

The classes/methods discussed in the series are accompanied by the links to their pages on the [official Manim documentation](https://docs.manim.community/en/stable/index.html), which contains a more comprehensive description and the source code.


### First animations
The basic building block of Manim are **scenes**, which are Python classes inheriting the {% manim_doc `Scene` reference/manim.scene.scene.Scene.html %} class.
Each of the scenes must implement the {% manim_doc `construct` reference/manim.scene.scene.Scene.html#manim.scene.scene.Scene.construct %} method, which contains information about how the scene looks like (creating shapes, moving them, changing, color and size, etc.).

Here is an example of a simple scene that creates a red square and then a blue circle.

```py
from manim import *


class Intro(Scene):
    def construct(self):
        # create square and circle objects (and move them)
        square = Square(color=RED).shift(LEFT * 2)
        circle = Circle(color=BLUE).shift(RIGHT * 2)

        # animate writing them on screen
        self.play(Write(square), Write(circle))

        # fading them from the scene
        self.play(FadeOut(square), FadeOut(circle), run_time=2)
```

To render the video, we will use the `manim <file name> -pqm` command, where
- `-p` is the preview flag, telling Manim that we want to immediately view the result and
- `-qm` sets the quality to `m`edium (others being `l`ow, `h`igh and 4`k`),

yielding the following video:

{% manim_video 1-Intro %}

The method {% manim_doc `self.play` reference/manim.scene.scene.Scene.html#manim.scene.scene.Scene.play %} always expects a **non-zero** number of animations that it plays at the same time.
We're calling it with the {% manim_doc `Write` reference/manim.animation.creation.Write.html %} and {% manim_doc `FadeOut` reference/manim.animation.fading.FadeOut.html %} animations above, which create and hide objects passed to them.
The optional parameter `run_time` sets the animation duration (in seconds), defaulting to \(1\) if nothing is passed.

There are also a number of builtin constants used (`LEFT`, `RIGHT`, `RED`, `BLUE`).
These are constants that Manim uses to make the code more readable, a comprehensive list can be found {% manim_doc here reference/manim.constants.html %}.

After both of the objects are created, the {% manim_doc `shift` reference/manim.mobject.mobject.Mobject.html#manim.mobject.mobject.Mobject.shift %} method is used to move them in the given direction, **also returning them**.
This is how the vast majority of functions on Manim objects are implemented, mainly to avoid having to use the following (valid but verbose) syntax:

```py
square = Square(color=RED)
square.shift(LEFT * 2)
```

Since the direction constants are [NumPy arrays](https://numpy.org/doc/stable/reference/generated/numpy.ndarray.html), they can be added and multiplied by constants with ease -- to move to the side and slightly up, we can simply do `obj.shift(LEFT + UP * 1.5)`.

### `animate` syntax
Besides creating and hiding objects, we'd like to animate their attributes like color, position and orientation.
The {% manim_doc `shift` reference/manim.mobject.mobject.Mobject.html#manim.mobject.mobject.Mobject.shift %} function does move the object, but it doesn't do so visually.

This can be done in a number of ways, arguably the most elegant being the {% manim_doc `animate` tutorials/quickstart.html#using-animate-syntax-to-animate-methods %} syntax, which can be used via the magic `animate` word after the object:

```py
from manim import *


class Animate(Scene):
    def construct(self):
        square = Square(color=RED).shift(LEFT * 2)
        circle = Circle(color=BLUE).shift(RIGHT * 2)

        self.play(Write(square), Write(circle))

        # moving objects
        self.play(
            square.animate.shift(UP * 0.5),
            circle.animate.shift(DOWN * 0.5)
        )

        # rotating and filling the square (opacity 80%)
        # scaling and filling the circle (opacity 80%)
        self.play(
            square.animate.rotate(PI / 2).set_fill(RED, 0.8),
            circle.animate.scale(2).set_fill(BLUE, 0.8),
        )

        # change color
        self.play(
            square.animate.set_color(GREEN),
            circle.animate.set_color(ORANGE),
        )

        self.play(FadeOut(square), FadeOut(circle))
```

{% manim_video 1-Animate %}

The example shows a number of properties that each object has (position, orientation, color) and that can be animated.
As you can see from the code, the animations can be chained to change a number of them at once -- just make sure that they are not conflicting (moving both up and down at the same time, for example).

### Aligning objects
We've seen that the {% manim_doc `shift` reference/manim.mobject.mobject.Mobject.html#manim.mobject.mobject.Mobject.shift %} function moves an object in the given direction.
Sometimes, however, it might be more convenient to move it in relation to other objects in the scene.

#### `next_to`
For moving one object next to another, we'll use the {% manim_doc `next_to` reference/manim.mobject.mobject.Mobject.html#manim.mobject.mobject.Mobject.next_to %} function:

```py
from manim import *


class NextTo(Scene):
    def construct(self):
        c1, c2, c3, c4 = [Circle(radius=0.5, color=WHITE)
                          for _ in range(4)]

        rectangle = Rectangle(width=5, height=3)

        # use Python's * syntax to write the objects
        # does the following: f(*[1, 2, 3]) == f(1, 2, 3)
        self.play(*[Write(o) for o in [c1, c2, c3, c4, rectangle]])

        # move the circles such that they surround the rectangle
        self.play(
            c1.animate.next_to(rectangle, LEFT),
            c2.animate.next_to(rectangle, UP),
            c3.animate.next_to(rectangle, RIGHT),
            c4.animate.next_to(rectangle, DOWN),
        )
```

{% manim_video 1-NextTo %}

#### `move_to`
For moving one object on top of another, we'll use the {% manim_doc `move_to` reference/manim.mobject.mobject.Mobject.html#manim.mobject.mobject.Mobject.move_to %} function:

```py
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
```

{% manim_video 1-MoveTo %}

#### `align_to`
For moving one object on the "same level" as another, we'll use the {% manim_doc `align_to` reference/manim.mobject.mobject.Mobject.html#manim.mobject.mobject.Mobject.align_to %} function:

```py
from manim import *


class AlignTo(Scene):
    def construct(self):
        c1, c2, c3 = [Circle(radius=1.5 - i / 3, color=WHITE)
                      for i in range(3)]

        self.play(*[Write(o) for o in [c1, c2, c3]])

        # align such that c1 < c2 < c3
        self.play(
            c1.animate.next_to(c2, LEFT),
            c3.animate.next_to(c2, RIGHT),
        )

        # align c1 and c2 such that their bottoms are the same as c2
        self.play(
            c1.animate.align_to(c2, DOWN),
            c3.animate.align_to(c2, DOWN),
        )

        point = [0, 2.5, 0]

        # align all circles such that their top touches a line going through the point
        self.play(
            c1.animate.align_to(point, UP),
            c2.animate.align_to(point, UP),
            c3.animate.align_to(point, UP),
        )
```

{% manim_video 1-AlignTo %}


### Typesetting text and math

Manim supports setting in \(\TeX\) (including math).
To do this, we'll be using the {% manim_doc `Tex` reference/manim.mobject.text.tex_mobject.Tex.html %} for setting text and {% manim_doc `MathTex` reference/manim.mobject.text.tex_mobject.MathTex.html %} for setting math.
If you're not familiar with setting math in \(\TeX\), you can use one of many online editors (such as [this one](https://latexeditor.lagrida.com/)).

```py
from manim import *


class TextAndMath(Scene):
    def construct(self):
        text = Tex("Hello Manim!").shift(LEFT * 2.5)

        # note that we're using Python's r-strings for cleaner code
        formula = MathTex(r"\sum_{i = 0}^\infty \frac{1}{2^i} = 2").shift(RIGHT * 2.5)

        self.play(Write(formula), Write(text))

        self.play(FadeOut(formula), FadeOut(text))
```

{% manim_video 1-TextAndMath %}

An alternative to using the {% manim_doc `Tex` reference/manim.mobject.text.tex_mobject.Tex.html %} class is the {% manim_doc `Text` reference/manim.mobject.text.text_mobject.Text.html %} class, which internally doesn't use \(\TeX\) and thus renders a(n arguably) worse-looking text, but is easier to work with when dealing with non-english characters.

### Tasks

#### Shuffle

Create an animation of random shuffling.

{% manim_video 1-Shuffle %}

The {% manim_doc `Swap` reference/manim.animation.transform.Swap.html %} animation may be used for swapping the position of two objects.
Its optional parameter `path_arc`, which determines the angle under which they are swapped, might also be useful.

```py
from manim import *


class Sort(Scene):
    def construct(self):
        c11 = Circle(color=WHITE).shift(UP * 1.5 + LEFT * 2)
        c12 = Circle(color=WHITE).shift(UP * 1.5 + RIGHT * 2)
        c21 = Circle(color=WHITE).shift(DOWN * 1.5 + LEFT * 2)
        c22 = Circle(color=WHITE).shift(DOWN * 1.5 + RIGHT * 2)

        self.play(Write(c11), Write(c12), Write(c21), Write(c22))

        self.play(Swap(c11, c21))

        self.play(Swap(c12, c22, path_arc=160 * DEGREES))
```

{% manim_video 1-ShuffleExample %}

{% manim_solution %}
from manim import *
from random import *


class Shuffle(Scene):
    def construct(self):
        seed(0xDEADBEEF)

        # number of values to shuffle
        n = 5

        circles = [
            Circle(color=WHITE, fill_opacity=0.8, fill_color=WHITE).scale(0.6)
            for _ in range(n)
        ]

        # spacing between the circles
        spacing = 2
        for i, circle in enumerate(circles):
            circle.shift(RIGHT * (i - (len(circles) - 1) / 2) * spacing)

        self.play(*[Write(circle) for circle in circles])

        # selected circle
        selected = randint(0, n - 1)
        self.play(circles[selected].animate.set_color(RED))
        self.play(circles[selected].animate.set_color(WHITE))

        # slowly increase speed when swapping
        swaps = 13
        speed_start = 1
        speed_end = 0.2

        for i in range(swaps):
            speed = speed_start - abs(speed_start - speed_end) / swaps * i

            # pick two random circles (ensuring a != b)
            a, b = sample(range(n), 2)

            # swap with a slightly larger arc angle
            self.play(
                Swap(circles[a], circles[b]), run_time=speed, path_arc=135 * DEGREES
            )

        # highlight the initial circle again
        self.play(circles[selected].animate.set_color(RED))
        self.play(circles[selected].animate.set_color(WHITE))
{% endmanim_solution %}

#### Sort

Create an animation of a sequence being sorted.

{% manim_video 1-Sort %}

The {% manim_doc `stretch_to_fit_height` reference/manim.mobject.mobject.Mobject.html#manim.mobject.mobject.Mobject.stretch_to_fit_height %} function (combined with the `animate` syntax) may be useful for changing the height of the object, without scaling it proportionally.

```py
from manim import *


class StretchToFitHeightExample(Scene):
    def construct(self):
        s1 = Square().shift(LEFT * 2.5)
        s2 = Square().shift(RIGHT * 2.5)

        self.play(Write(s1), Write(s2))

        self.play(
            s1.animate.stretch_to_fit_height(3.5),
            s2.animate.set_height(3.5),
        )
```

{% manim_video 1-StretchToFitHeightExample %}

{% manim_solution %}
from manim import *
from random import *


class Sort(Scene):
    def construct(self):
        seed(0xDEADBEEF)

        n = 20
        value_min, value_max = 1, 20

        values = [randint(value_min, value_max) for _ in range(n)]

        # width of rectangles and the height of a single unit
        rectangle_width = 0.2
        unit_height = 0.2

        rectangle_spacing = 2.5

        rectangles = [
            Rectangle(
                width=rectangle_width,
                height=unit_height * v,
                fill_color=WHITE,
                fill_opacity=1,
            )
            for v in values
        ]

        # calculate the point at which to align all of the rectangles (so they're all centered)
        alignment_point = None
        max_value = 0
        for i, v in enumerate(values):
            if max_value < v:
                max_value = v
                alignment_point = Point().shift(DOWN * rectangles[i].height / 2)

        for i, rect in enumerate(rectangles):
            rect.shift(
                RIGHT
                * (i - (len(rectangles) - 1) / 2)
                * rectangle_width
                * rectangle_spacing
            ).align_to(alignment_point, DOWN)

        self.play(*[Write(r) for r in rectangles])

        def animate_at(a, b, duration):
            """Animate that we're looking at the positions a and b."""
            self.play(
                *[
                    r.animate.set_color(WHITE if i not in (a, b) else YELLOW)
                    for i, r in enumerate(rectangles)
                ],
                run_time=duration,
            )

        def animate_swap(a, b, duration):
            """Animate the swap of positions a and b."""
            self.play(
                rectangles[a]
                .animate.stretch_to_fit_height(values[a] * unit_height)
                .align_to(alignment_point, DOWN),
                rectangles[b]
                .animate.stretch_to_fit_height(values[b] * unit_height)
                .align_to(alignment_point, DOWN),
                run_time=duration,
            )

        # the first pass is slower
        speed_slow = 0.6
        speed_fast = 0.07

        for i in range(n):
            speed = speed_slow if i == 0 else speed_fast
            swapped = False
            for j in range(n - i - 1):
                animate_at(j, j + 1, speed)

                if values[j] > values[j + 1]:
                    values[j], values[j + 1] = values[j + 1], values[j]

                    animate_swap(j, j + 1, speed)
                    swapped = True

            # if the sequence is sorted, stop
            if not swapped:
                break

        self.play(*[FadeOut(r) for r in rectangles])
{% endmanim_solution %}

#### Search

Create an animation of binary searching a random sorted sequence.

{% manim_video 1-Search %}

The {% manim_doc `Arrow` reference/manim.mobject.geometry.line.Arrow.html %} object is very useful for creating the position indicators.

```py
from manim import *


class ArrowExample(Scene):
    def construct(self):
        a1 = Arrow(start=UP, end=DOWN).shift(LEFT * 2)
        a2 = Arrow(start=DOWN, end=UP).shift(RIGHT * 2)

        self.play(Write(a1), Write(a2))
```

{% manim_video 1-ArrowExample %}

{% manim_solution %}
from manim import *
from random import *


class Search(Scene):
    def construct(self):
        seed(0xDEADBEEF1)  # prettier input

        n = 10
        value_min, value_max = 1, n

        values = sorted([randint(value_min, value_max) for _ in range(n)])

        square_side_length = 0.75
        square_spacing = 1.3

        squares = [Square(side_length=square_side_length) for v in values]
        numbers = [Tex(f"${v}$") for v in values]

        # move rectangles such that they are centered
        for i, rect in enumerate(squares):
            rect.shift(
                RIGHT
                * (i - (len(squares) - 1) / 2)
                * square_side_length
                * square_spacing
            )

        # label positions
        for i, number in enumerate(numbers):
            number.move_to(squares[i])

        pointer_length = 0.4
        l_pointer = Arrow(start=DOWN * pointer_length, end=UP).next_to(squares[0], DOWN)
        r_pointer = Arrow(start=DOWN * pointer_length, end=UP).next_to(squares[-1], DOWN)

        self.play(*[Write(s) for s in squares], *[Write(n) for n in numbers])

        # print the number we're looking for
        target = randint(value_min, value_max)
        text = Tex(f"Hledáme: ${target}$").shift(UP * 1.5)
        self.play(Write(text))

        self.play(Write(l_pointer), Write(r_pointer))

        lo, hi = 0, len(values) - 1

        def color_in_range(objects, color, range):
            """Return the animation of coloring the objects in the sequence."""
            return [
                o.animate.set_color(color) for i, o in enumerate(objects) if i in range
            ]

        while lo < hi:
            avg = (lo + hi) // 2

            current_arrow = (
                Arrow(start=DOWN * pointer_length, end=UP)
                .next_to(squares[avg], DOWN)
                .set_color(ORANGE)
            )

            self.play(Write(current_arrow))

            if values[avg] < target:
                # move left pointer
                self.play(
                    FadeOut(current_arrow),
                    l_pointer.animate.next_to(squares[avg + 1], DOWN),
                    *color_in_range(squares, DARK_GRAY, range(lo, avg + 1)),
                    *color_in_range(numbers, DARK_GRAY, range(lo, avg + 1)),
                )

                lo = avg + 1
            elif values[avg] >= target:
                # move right pointer
                self.play(
                    FadeOut(current_arrow),
                    r_pointer.animate.next_to(squares[avg], DOWN),
                    *color_in_range(squares, DARK_GRAY, range(avg + 1, hi + 1)),
                    *color_in_range(numbers, DARK_GRAY, range(avg + 1, hi + 1)),
                )

                hi = avg

            # the desired value has been found
            if values[hi] == target:
                self.play(
                    *color_in_range(squares, DARK_GRAY, range(hi)),
                    *color_in_range(squares, DARK_GRAY, range(hi + 1, n)),
                    *color_in_range(numbers, DARK_GRAY, range(hi)),
                    *color_in_range(numbers, DARK_GRAY, range(hi + 1, n)),
                    numbers[hi].animate.set_color(GREEN),
                    squares[hi].animate.set_color(GREEN),
                    FadeOut(l_pointer),
                )
                break

        self.play(*[FadeOut(r) for r in numbers + squares + [r_pointer, text]])
{% endmanim_solution %}
