---
title: Manim – Groups, Transforms, Updaters
category: "Manim"
category_icon: /assets/category-icons/manim.svg
css: manim
---

In this part of the series, we'll learn a number of useful functions and classes when working with groups of objects.
We'll also learn how to transform objects into others, how updaters work and a few geometry-related things.

### Grouping objects
It is sometimes more useful to work with a group of objects as one, for example when moving them, scaling them, changing their color, etc.
This is where the {% manim_doc `VGroup` reference/manim.mobject.types.vectorized_mobject.VGroup.html %} class comes in.

```py
from manim import *


class VGroupExample(Scene):
    def construct(self):
        s1 = Square(color=RED)
        s2 = Square(color=GREEN)
        s3 = Square(color=BLUE)

        s1.next_to(s2, LEFT)
        s3.next_to(s2, RIGHT)

        self.play(Write(s1), Write(s2), Write(s3))

        group = VGroup(s1, s2, s3)

        # scale the entire group
        self.play(group.animate.scale(1.5).shift(UP))

        # only work with one of the group's objects
        self.play(group[1].animate.shift(DOWN * 2))

        # change color and fill
        self.play(group.animate.set_color(WHITE))
        self.play(group.animate.set_fill(WHITE, 1))
```

{% manim_video 2-VGroupExample %}

The {% manim_doc `VGroup` reference/manim.mobject.types.vectorized_mobject.VGroup.html %} class additionally contains functions for arranging objects.
The simplest to use is the {% manim_doc `arrange` reference/manim.mobject.mobject.Mobject.html#manim.mobject.mobject.Mobject.arrange %} function which arranges object such that they are next to one another, in the order they were passed to the constructor.

```py
from manim import *
from random import seed, uniform


class ArrangeExample(Scene):
    def construct(self):
        seed(0xDEADBEEF)

        circles = VGroup(
            *[
                Circle(radius=0.1)
                .scale(uniform(0.5, 4))
                .shift(UP * uniform(-3, 3) + RIGHT * uniform(-5, 5))
                for _ in range(12)
            ]
        )

        self.play(FadeIn(circles))

        self.play(circles.animate.arrange())

        # specify the direction of arrangement and spacing between the objects
        self.play(circles.animate.arrange(direction=DOWN, buff=0.1))
        self.play(circles.animate.arrange(buff=0.4))
```

{% manim_video 2-ArrangeExample %}

The `buff` parameter determines the spacing between the objects and can be used in most of the functions that involve positioning objects next to one another, such as the {% manim_doc `next_to` reference/manim.mobject.mobject.Mobject.html#manim.mobject.mobject.Mobject.next_to %} function that we've seen already.
The `direction` parameter determines the direction in which the objects are arranged.

A more general version of the {% manim_doc `arrange` reference/manim.mobject.mobject.Mobject.html#manim.mobject.mobject.Mobject.arrange %} function is the {% manim_doc `arrange_in_grid` reference/manim.mobject.mobject.Mobject.html#manim.mobject.mobject.Mobject.arrange_in_grid %} function, which (as the name suggests) arranges the objects of the group in a grid.

```py
from manim import *
from random import seed, uniform


class ArrangeInGridExample(Scene):
    def construct(self):
        seed(0xDEADBEEF)

        circles = VGroup(
            *[
                Circle(radius=0.1)
                .scale(uniform(0.5, 2))
                .shift(UP * uniform(-3, 3) + RIGHT * uniform(-5, 5))
                for _ in range(9 ** 2)
            ]
        )

        self.play(FadeIn(circles))

        self.play(circles.animate.arrange_in_grid())

        # different parameters for rows and columns
        self.play(circles.animate.arrange_in_grid(rows=5, buff=0))
        self.play(circles.animate.arrange_in_grid(cols=12, buff=0.3))
```

{% manim_video 2-ArrangeInGridExample %}


### Adding and removing elements
To add objects to the scene instantly (without animating), we can use the {% manim_doc `bring_to_front` reference/manim.scene.scene.Scene.html#manim.scene.scene.Scene.bring_to_front %} (or alternatively {% manim_doc `add` reference/manim.scene.scene.Scene.html#manim.scene.scene.Scene.add %}, which is the same functions) and {% manim_doc `bring_to_back` reference/manim.scene.scene.Scene.html#manim.scene.scene.Scene.bring_to_back %}  functions.
To remove them, we can use the {% manim_doc `remove` reference/manim.scene.scene.Scene.html#manim.scene.scene.Scene.remove %} function.

```py
from manim import *


class AddRemoveExample(Scene):
    def construct(self):
        square = Square(fill_color=WHITE, fill_opacity=1)
        small_scale = 0.6

        triangle = Triangle(fill_opacity=1).scale(small_scale).move_to(square)

        self.play(Write(square))

        # add a triangle behind the square
        self.bring_to_back(triangle)
        self.play(square.animate.shift(LEFT * 2))

        circle = Circle(fill_opacity=1).scale(small_scale).move_to(square)

        # add a circle behind the square
        self.bring_to_back(circle)
        self.play(square.animate.shift(RIGHT * 2))

        square2 = (
            Square(stroke_color=GREEN, fill_color=GREEN, fill_opacity=1)
            .scale(small_scale)
            .move_to(square)
        )

        self.remove(triangle)

        # add a second square in front of the square
        # looks jarring but is just to show the functionality
        self.bring_to_front(square2)

        self.play(square.animate.shift(RIGHT * 2))
```

{% manim_video 2-AddRemoveExample %}

We'll cover the scene functionality in-depth in one of the upcoming parts in the series.
For now, it's sufficient to know that the scene objects have a determined order in which they are rendered, which is determined primarily by their `z` coordinate (yes, even the 2D objects have a `z` coordinate) and secondarily by the order they were added to the scene (newer objects on top, older on the bottom).

```py
from manim import *


class ZIndexExample(Scene):
    def construct(self):
        c1 = Circle(fill_opacity=1, color=RED).shift(LEFT)
        c2 = Circle(fill_opacity=1, color=GREEN)
        c3 = Circle(fill_opacity=1, color=BLUE).shift(RIGHT)

        self.add(c1, c2, c3)

        self.wait(1)

        # we'll increase the z index of c1 and c2, which will bring to the front
        # c2 will still be in front of c1, which is the order they are in the scene
        c1.set_z_index(1)
        c2.set_z_index(1)

        self.wait(1)

        # c1 will now be in front of both c2 (z = 1) and c3 (z = 0)
        c1.set_z_index(2)

        self.wait(1)
```

{% manim_video 2-ZIndexExample %}

### Overlapping animations
We've seen how to start animations concurrently, but it is often prettier to run them with a certain overlap (especially when there is a lot of them), which makes them look smoother.
To achieve this, we'll use the {% manim_doc `AnimationGroup` reference/manim.animation.composition.AnimationGroup.html %} object with a `lag_ratio` parameter, which determins the part of a given animation when the next one is started.

```py
from manim import *


class AnimationGroupExample(Scene):
    def construct(self):
        c1 = Square(color=RED)
        c2 = Square(color=GREEN)
        c3 = Square(color=BLUE)

        VGroup(c1, c2, c3).arrange(buff=1)

        # each animation starts in the middle of the previous one
        self.play(AnimationGroup(Write(c1), Write(c2), Write(c3), lag_ratio=0.5))

        # each animation starts after the first tenth of the previous one
        self.play(AnimationGroup(FadeOut(c1), FadeOut(c2), FadeOut(c3), lag_ratio=0.1))

        # one animation can also be a group, which has different lag_ratio
        self.play(
            AnimationGroup(
                AnimationGroup(Write(c1), Write(c2), lag_ratio=0.1),
                Write(c3),
                lag_ratio=0.5,
            )
        )

        # lag_ratio can also be negative (in which case the animations run in reverse)
        # however, just because it can doesn't mean it should!
        self.play(AnimationGroup(FadeOut(c1), FadeOut(c2), FadeOut(c3), lag_ratio=-0.1))
```

{% manim_video 2-AnimationGroupExample %}

Animation overlap also works for objects in a {% manim_doc `VGroup` reference/manim.mobject.types.vectorized_mobject.VGroup.html %} when applying animations that have non-zero `lag_ratio` (such as {% manim_doc `Write` reference/manim.animation.creation.Write.html %}), in which case it is applied in the order they were added to the group.

```py
from manim import *


class VGroupLagRatioExample(Scene):
    def construct(self):
        squares = VGroup(Square(), Square(), Square()).arrange(buff=0.5).scale(1.5)

        # Write has non-zero lag_ratio by default so squares are written with overlap
        self.play(Write(squares))

        # FadeOut has zero lag_ratio by default, so all squares fade concurrently
        self.play(FadeOut(squares))

        squares.set_color(BLUE)

        self.play(Write(squares, lag_ratio=0))

        self.play(FadeOut(squares, lag_ratio=0.5))
```

{% manim_video 2-VGroupLagRatioExample %}

### Working with attention
When creating animations, it is sometimes necessary to draw attention to a certain part of the screen where the viewer's focus should be.
Manim offers a number of ways how to do this, the most common of which are {% manim_doc `Flash` reference/manim.animation.indication.Flash.html %}, {% manim_doc `Indicate` reference/manim.animation.indication.Indicate.html %}, {% manim_doc `Wiggle` reference/manim.animation.indication.Wiggle.html %}, {% manim_doc `FocusOn` reference/manim.animation.indication.FocusOn.html %} and {% manim_doc `Circumscribe` reference/manim.animation.indication.Circumscribe.html %}.

```py
from manim import *


class AttentionExample(Scene):
    def construct(self):
        c1 = Square()

        labels = [
            Tex("Flash"),
            Tex("Indicate"),
            Tex("Wiggle"),
            Tex("FocusOn"),
            Tex("Circumscribe"),
        ]

        # move labels below the square
        for label in labels:
            label.next_to(c1, DOWN).scale(1.5)

        def switch_labels(i: int):
            """Animate switching one label for another. Notice the shift parameter!"""
            return AnimationGroup(
                FadeOut(labels[i], shift=UP * 0.5),
                FadeIn(labels[i + 1], shift=UP * 0.5),
            )

        self.play(Write(c1))

        self.play(FadeIn(labels[0], shift=UP * 0.5), c1.animate.shift(UP))

        self.play(Flash(c1, flash_radius=1.6, num_lines=20))

        self.play(AnimationGroup(switch_labels(0), Indicate(c1), lag_ratio=0.7))

        self.play(AnimationGroup(switch_labels(1), Wiggle(c1), lag_ratio=0.7))

        self.play(AnimationGroup(switch_labels(2), FocusOn(c1), lag_ratio=0.7))

        self.play(AnimationGroup(switch_labels(3), Circumscribe(c1), lag_ratio=0.7))
```

{% manim_video 2-AttentionExample %}

The {% manim_doc `Flash` reference/manim.animation.indication.Flash.html %}, {% manim_doc `Indicate` reference/manim.animation.indication.Indicate.html %} and {% manim_doc `Circumscribe` reference/manim.animation.indication.Circumscribe.html %} animations have a useful optional `color` parameter, which changes the default color from yellow to whatever you prefer.
Also, notice that we used an optional `shift` parameter for {% manim_doc `FadeIn` reference/manim.animation.fading.FadeIn.html#manim.animation.fading.FadeIn %} and {% manim_doc `FadeIn` reference/manim.animation.fading.FadeOut.html#manim.animation.fading.FadeOut %}

### Transformations
Manim can animate the transformation of one object to another in a number of different ways.
The most commonly used is {% manim_doc `Transform` reference/manim.animation.transform.Transform.html %}, which smoothly transforms one object onto another.

```py
from manim import *


class BasicTransformExample(Scene):
    def construct(self):
        c = Circle().scale(2)
        s = Square().scale(2)

        self.play(Write(c))

        self.play(Transform(c, s))
```

{% manim_video 2-BasicTransformExample %}

It is, however, important to pay attention to which object we're working with when doing multiple transformations -- we still have to work with the original object or things will go wrong.

```py
from manim import *


class BadTransformExample(Scene):
    def construct(self):
        good = [Circle(color=GREEN), Square(color=GREEN), Triangle(color=GREEN)]
        bad = [Circle(color=RED), Square(color=RED), Triangle(color=RED)]

        VGroup(*(good + bad)).arrange_in_grid(rows=2, buff=1)

        self.play(Write(good[0]), Write(bad[0]))

        self.play(
            Transform(good[0], good[1]),  # o1 -> o2
            Transform(bad[0], bad[1]),    # o1 -> o2
        )

        self.play(
            Transform(good[0], good[2]),  # o1 -> o3
            Transform(bad[1], bad[2]),    # o2 -> o3 - bad!
        )
```

{% manim_video 2-BadTransformExample %}

If this behavior feels unintuitive, it is possible to use {% manim_doc `ReplacementTransform` reference/manim.animation.transform.ReplacementTransform.html %}, which swaps the behavior above (good will be bad and vice versa).

Besides these transformations, it is also possible to use {% manim_doc `TransformMatchingShapes` reference/manim.animation.transform_matching_parts.TransformMatchingShapes.html %}, which attempts to transform the objects in a manner that preserves parts that they have in common.
Note that it has the same behavior as {% manim_doc `ReplacementTransform` reference/manim.animation.transform.ReplacementTransform.html %}!

```py
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
```

{% manim_video 2-TransformMatchingShapesExample %}

### Updaters
Imagine that we would like to continually update an object during an animation (its position, scale, etc.).
This what Manim's updaters are for -- they are functions containing arbitrary code, connected to a certain object and evaluated each rendered frame.

```py
from manim import *


class SimpleUpdaterExample(Scene):
    def construct(self):
        square = Square()
        square_label = Tex("A neat square.").next_to(square, UP, buff=0.5)

        self.play(Write(square))
        self.play(FadeIn(square_label, shift=UP * 0.5))

        def label_updater(obj):
            """An updater which continually move an object above the square.

            The first parameter (obj) is always the object that is being updated."""
            obj.next_to(square, UP, buff=0.5)

        # we want the label to always reside above the square
        square_label.add_updater(label_updater)

        self.play(square.animate.shift(LEFT * 3))
        self.play(square.animate.scale(1 / 2))
        self.play(square.animate.rotate(PI / 2).shift(RIGHT * 3 + DOWN * 0.5).scale(3))

        # to pause updaters, we'll use suspend_updating()
        square_label.suspend_updating()

        self.play(square.animate.scale(1 / 3))
        self.play(square.animate.rotate(PI / 2))

        # to resume,we'll use resume__updating()
        square_label.resume_updating()

        self.play(square.animate.scale(3))
        self.play(square.animate.rotate(PI / 2))
```

{% manim_video 2-SimpleUpdaterExample %}

Besides changing certain attributes of an object, it might be useful to transform it to an entirely new one.
We'll use the {% manim_doc `become` reference/manim.mobject.mobject.Mobject.html#manim.mobject.mobject.Mobject.become %} function, which transforms an object into another one **immediately** (not like {% manim_doc `Transform` reference/manim.animation.transform.Transform.html %}, which is an animation).

```py
from manim import *


class BecomeUpdaterExample(Scene):
    def format_point(self, point) -> str:
        """Format the given point to look presentable."""
        return f"[{point[0]:.2f}, {point[1]:.2f}]"

    def construct(self):
        circle = Circle(color=WHITE)

        def circle_label_updater(obj):
            """An updater that displays the circle's position above it."""
            obj.become(Tex(f"p = {self.format_point(circle.get_center())}"))
            obj.next_to(circle, UP, buff=0.35)

        self.play(Write(circle))

        circle_label = Tex()

        # a bit of a hack - we're calling the updater to create the initial label
        circle_label_updater(circle_label)

        self.play(FadeIn(circle_label, shift=UP * 0.3))

        # start updating the label
        circle_label.add_updater(circle_label_updater)

        self.play(circle.animate.shift(RIGHT))
        self.play(circle.animate.shift(LEFT * 3 + UP))
        self.play(circle.animate.shift(DOWN * 2 + RIGHT * 2))
        self.play(circle.animate.shift(UP))
```

{% manim_video 2-BecomeUpdaterExample %}

Besides the new {% manim_doc `become` reference/manim.mobject.mobject.Mobject.html#manim.mobject.mobject.Mobject.become %} function, the code also contains the {% manim_doc `get_center` reference/manim.mobject.mobject.Mobject.html#manim.mobject.mobject.Mobject.get_center %} function, which returns a [NumPy array](https://numpy.org/doc/stable/reference/generated/numpy.ndarray.html) with the \([x, y, z]\) coordinates of the object (in our case the circle).

### Tasks

#### Triangle

Create an animation of the following triangle.

{% manim_video 2-Triangle %}

Dots and segments can be defined using the {% manim_doc `Dot` reference/manim.mobject.geometry.Dot.html %} and {% manim_doc `Line` reference/manim.mobject.geometry.Line.html %} classes.

```py
from manim import *


class LineExample(Scene):
    def construct(self):
        p1 = Dot()
        p2 = Dot()

        points = VGroup(p1, p2).arrange(buff=2.5)

        line = Line(start=p1.get_center(), end=p2.get_center())

        self.play(Write(p1), Write(p2))

        self.play(Write(line))
```

{% manim_video 2-LineExample %}

To create a circle given three of its points, the {% manim_doc `Circle.from_three_points` reference/manim.mobject.geometry.Circle.html#manim.mobject.geometry.Circle.from_three_points %} may be used.

```py
from manim import *


class CircleFromPointsExample(Scene):
    def construct(self):
        p1 = Dot().shift(LEFT + UP)
        p2 = Dot().shift(DOWN * 1.5)
        p3 = Dot().shift(RIGHT + UP)

        dots = VGroup(p1, p2, p3)

        # vytvoření kruhu ze tří bodů
        circle = Circle.from_three_points(p1.get_center(), p2.get_center(), p3.get_center(), color=WHITE)

        self.play(Write(dots), run_time=1.5)
        self.play(Write(circle))
```

{% manim_video 2-CircleFromPointsExample %}

{% manim_solution %}
from manim import *
from random import *


class Triangle(Scene):
    def construct(self):
        seed(0xDEADBEEF)

        # scale everything up a bit
        c = 2

        p1 = Dot().scale(c).shift(UP * c)
        p2 = Dot().scale(c).shift(DOWN * c + LEFT * c)
        p3 = Dot().scale(c).shift(DOWN * c + RIGHT * c)

        points = VGroup(p1, p2, p3)

        self.play(Write(points, lag_ratio=0.5), run_time=1.5)

        l1 = Line()
        l2 = Line()
        l3 = Line()

        lines = VGroup(l1, l2, l3)

        def create_line_updater(a, b):
            """Returns a function that acts as an updater for the given segment."""
            return lambda x: x.become(Line(start=a.get_center(), end=b.get_center()))

        l1.add_updater(create_line_updater(p1, p2))
        l2.add_updater(create_line_updater(p2, p3))
        l3.add_updater(create_line_updater(p3, p1))

        self.play(Write(lines, lag_ratio=0.5), run_time=1.5)

        x = Tex("x")
        y = Tex("y")
        z = Tex("z")

        x.add_updater(lambda x: x.next_to(p1, UP))
        y.add_updater(lambda x: x.next_to(p2, DOWN + LEFT))
        z.add_updater(lambda x: x.next_to(p3, DOWN + RIGHT))

        labels = VGroup(x, y, z).scale(c * 0.8)

        self.play(FadeIn(labels, shift=UP * 0.2))

        circle = Circle()
        circle.add_updater(
            lambda c: c.become(
                Circle.from_three_points(
                    p1.get_center(), p2.get_center(), p3.get_center()
                )
            )
        )

        self.play(Write(circle))

        self.play(
            p2.animate.shift(LEFT + UP),
            p1.animate.shift(RIGHT),
        )
{% endmanim_solution %}

#### Wave

Create an animation of a smooth wave running through a maze.

{% manim_video 2-Wave %}

The {% manim_doc `arrange_in_grid` reference/manim.mobject.mobject.Mobject.html#manim.mobject.mobject.Mobject.arrange_in_grid %} will be useful to position the squares.
To overlap the coloring of each layer in the maze, nested {% manim_doc `AnimationGroup` reference/manim.animation.composition.AnimationGroup.html %} can be used.
For creating a smooth gradient from the input colors, the {% manim_doc `color_gradient` reference/manim.utils.color.html#manim.utils.color.color_gradient %} utility function is quite useful.

```py
from manim import *


class ColorGradientExample(Scene):
    def construct(self):
        rows = 6
        square_count = rows * 9

        # the colors can be either the built-in constants or in hex notation
        # (the builtin ones are just strings in the hex notation too!)
        colors = [RED, "#ffd166", "#06d6a0", BLUE]
        squares = [
            Square(fill_color=WHITE, fill_opacity=1).scale(0.3)
            for _ in range(square_count)
        ]

        group = VGroup(*squares).arrange_in_grid(rows=rows)

        self.play(Write(group, lag_ratio=0.04))

        all_colors = color_gradient(colors, square_count)

        self.play(
            AnimationGroup(
                *[s.animate.set_color(all_colors[i]) for i, s in enumerate(squares)],
                lag_ratio=0.02,
            )
        )

        self.play(FadeOut(group))
```

{% manim_video 2-ColorGradientExample %}

Here is the text input that I used to generate the maze, if you wish to use it.

```
#######################################################
#  #################            ##                    #
# ##################           ####                   #
# #################            ####                   #
#  ###############             #####               # ##
#      #########               #####               ####
#         ###                  ######            ######
#          ###            ##   #####    ###       #####
#          ####      ########   ####  #####        ## #
#          #####   ##########   ###  ########       # #
#         #####   ###########        ########         #
#         ####   ###########        ##########        #
#        ##      ###########        ##########        #
#      ####     ############      #############       #
#    ######     ############     #############        #
# #########  ## ###########     #########    #        #
# ############### #########     #######               #
# ###############   ######      ######                #
# ###############    #####       ####                 #
#   #############      #                ##            #
#     #  #######                       ########### ####
#          ###         #              #################
# ##                  ####            #################
#####                ######          ##################
######                ######         ##################
# ###      ###        #######  ###   ###############  #
#         ####         ############   ####  #######   #
#        #####          ############          ###     #
#         ###            ##########                   #
#######################################################}
```

{% manim_solution %}
from manim import *
from random import *


class Wave(Scene):
    def construct(self):
        seed(0xDEADBEEF)

        maze_string = """
#######################################################
#  #################            ##                    #
# ##################           ####                   #
# #################            ####                   #
#  ###############             #####               # ##
#      #########               #####               ####
#         ###                  ######            ######
#          ###            ##   #####    ###       #####
#          ####      ########   ####  #####        ## #
#          #####   ##########   ###  ########       # #
#         #####   ###########        ########         #
#         ####   ###########        ##########        #
#        ##      ###########        ##########        #
#      ####     ############      #############       #
#    ######     ############     #############        #
# #########  ## ###########     #########    #        #
# ############### #########     #######               #
# ###############   ######      ######                #
# ###############    #####       ####                 #
#   #############      #                ##            #
#     #  #######                       ########### ####
#          ###         #              #################
# ##                  ####            #################
#####                ######          ##################
######                ######         ##################
# ###      ###        #######  ###   ###############  #
#         ####         ############   ####  #######   #
#        #####          ############          ###     #
#         ###            ##########                   #
#######################################################
"""

        maze = []  # 2D array of squares like we see it
        maze_bool = []  # 2D array of true/false values
        all_squares = VGroup()

        # go line by line
        for row in maze_string.strip().splitlines():
            maze.append([])
            maze_bool.append([])

            for char in row:
                square = Square(
                    side_length=0.23,
                    stroke_width=1,
                    fill_color=WHITE if char == "#" else BLACK,
                    fill_opacity=1,
                )

                maze[-1].append(square)
                maze_bool[-1].append(char == " ")
                all_squares.add(square)

        w = len(maze[0])
        h = len(maze)

        # arrange the squares in the grid
        all_squares.arrange_in_grid(rows=h, buff=0)

        self.play(FadeIn(all_squares), run_time=2)

        x, y = 1, 1

        colors = ["#ef476f", "#ffd166", "#06d6a0", "#118ab2"]

        # create a dictionary of distances from start to other points
        distances = {(x, y): 0}
        stack = [(x, y, 0)]

        while len(stack) != 0:
            x, y, d = stack.pop(0)

            for dx, dy in ((0, 1), (1, 0), (-1, 0), (0, -1)):
                nx, ny = dx + x, dy + y

                if nx < 0 or nx >= w or ny < 0 or ny >= h:
                   continue

                if maze_bool[ny][nx] and (nx, ny) not in distances:
                    stack.append((nx, ny, d + 1))
                    distances[(nx, ny)] = d + 1

        max_distance = max([d for d in distances.values()])

        all_colors = color_gradient(colors, max_distance + 1)

        # create animation groups for each distance from start
        groups = []
        for d in range(max_distance + 1):
            groups.append(
                AnimationGroup(
                    *[
                        maze[y][x].animate.set_fill(all_colors[d])
                        for x, y in distances
                        if distances[x, y] == d
                    ]
                )
            )

        self.play(AnimationGroup(*groups, lag_ratio=0.08))
{% endmanim_solution %}

#### Hilbert
Create an animation of the Hilbert's (or any other space-filling) curve.

{% manim_video 2-Hilbert %}

You can use this custom `Path` function, which creates a path from the given points.

```py
from manim import *


class Path(VMobject):
    def __init__(self, points, *args, **kwargs):
        super().__init__(self, *args, **kwargs)
        self.set_points_as_corners(points)

    def get_important_points(self):
        """Returns the important points of the curve."""
        # shot explanation: Manim uses quadratic Bézier curves to create paths
        # > each curve is determined by 4 points - 2 anchor and 2 control
        # > VMobject's builtin self.points returns *all* points
        # > we, however, only care about the anchors
        # > see https://en.wikipedia.org/wiki/Bézier_curve for more details
        return list(self.get_start_anchors()) + [self.get_end_anchors()[-1]]


class PathExample(Scene):
    def construct(self):
        path = Path([LEFT + UP, LEFT + DOWN, RIGHT + UP, RIGHT + DOWN])

        self.play(Write(path))

        path_points = VGroup(*[Dot().move_to(point) for point in path.get_important_points()])

        self.play(Write(path_points))

        path2 = path.copy()
        path3 = path.copy()

        self.play(
            path2.animate.next_to(path, LEFT, buff=1),
            path3.animate.next_to(path, RIGHT, buff=1),
        )

        # flip(LEFT) flips top-down, because LEFT is the axis **by which** to flip
        self.play(
            path2.animate.flip(),
            path3.animate.flip(LEFT),
        )
```

We're also using the {% manim_doc `flip` reference/manim.mobject.mobject.Mobject.html#manim.mobject.mobject.Mobject.flip %} function, which flips an object in the given axis (defaulting to flipping left-right), and the {% manim_doc `copy` reference/manim.mobject.mobject.Mobject.html#manim.mobject.mobject.Mobject.copy %} function, which copies an object.

{% manim_solution %}
from manim import *


class Path(VMobject):
    def __init__(self, points, *args, **kwargs):
        super().__init__(self, *args, **kwargs)
        self.set_points_as_corners(points)

    def get_important_points(self):
        return list(self.get_start_anchors()) + [self.get_end_anchors()[-1]]


class Hilbert(Scene):
    def construct(self):
        points = [LEFT + DOWN, LEFT + UP, RIGHT + UP, RIGHT + DOWN]

        hilbert = Path(points).scale(3)

        self.play(Write(hilbert, lag_ratio=0.5))

        for i in range(1, 6):
            # length of a single segment in the curve
            new_segment_length = 1 / (2 ** (i + 1) - 1)

            # scale the curve such that it it is centered
            new_scale = (1 - new_segment_length) / 2

            # save the previous (large) curve to align smaller ones by it
            lu = hilbert.copy()
            lu, hilbert = hilbert, lu

            self.play(
                lu.animate.scale(new_scale)
                .set_color(DARK_GRAY)
                .align_to(hilbert, points[1])
            )

            ru = lu.copy()
            self.play(ru.animate.align_to(hilbert, points[2]))

            ld, rd = lu.copy(), ru.copy()
            self.play(
                ld.animate.align_to(hilbert, points[0]).rotate(-PI / 2),
                rd.animate.align_to(hilbert, points[3]).rotate(PI / 2),
            )

            new_hilbert = Path(
                list(ld.flip(LEFT).get_important_points())
                + list(lu.get_important_points())
                + list(ru.get_important_points())
                + list(rd.flip(LEFT).get_important_points())
            )

            self.play(Write(new_hilbert))

            self.remove(lu, ru, ld, rd)

            hilbert = new_hilbert
{% endmanim_solution %}
