---
title: Manim [4] – 3D and the Other Graphs
category: "Manim"
category_icon: /assets/category-icons/manim.svg
css: manim
---

[Part 1](/manim/introduction/), [Part 2](/manim/groups-transformations-updaters/), [Part 3](/manim/camera-and-graphs/), **→ Part 4 ←**

- .
{:toc}

In this part of the series, we'll take a look at Manim's tools for 3D animations and also at plotting all sorts of graphs.

### Binary operations
We'll briefly take a look at binary operations on Manim objects, since they might come in handy for more advanced animations.
We'll use the builtin classes from the {% manim_doc `boolean_ops` reference/manim.mobject.geometry.boolean_ops.html %} file, namely {% manim_doc `Difference` reference/manim.mobject.geometry.boolean_ops.Difference.html %}, {% manim_doc `Intersection` reference/manim.mobject.geometry.boolean_ops.Intersection.html %} and {% manim_doc `Union` reference/manim.mobject.geometry.boolean_ops.Union.html %}.

```py
from manim import *


class BooleanOperations(Scene):
    def construct(self):

        circle = Circle(fill_opacity=0.75, color=RED).scale(2).shift(LEFT * 1.5)
        square = Square(fill_opacity=0.75, color=GREEN).scale(2).shift(RIGHT * 1.5)

        group = VGroup(circle, square)

        self.play(Write(group))

        self.play(group.animate.scale(0.5).shift(UP * 1.6))

        union = Union(circle, square, fill_opacity=1, color=BLUE)

        for operation, position, name in zip(
            [Intersection, Union, Difference],
            [LEFT * 4.5, ORIGIN, RIGHT * 4.5],
            ["Intersection", "Union", "Difference"],
        ):
            result = operation(circle, square, fill_opacity=1, color=DARK_BLUE)
            result_position = DOWN * 1.3 + position

            label = Tex(name).move_to(result_position).scale(0.8)

            self.play(FadeIn(result))

            self.play(
                AnimationGroup(
                    result.animate.move_to(result_position),
                    Write(label, run_time=0.5),
                    lag_ratio=0.8,
                )
            )
```

{% manim_video 4-BooleanOperations %}

When using the aforementioned classes, it is important to keep in mind that they are restricted to vector objects (the {% manim_doc `VMobject` reference/manim.mobject.types.vectorized_mobject.VMobject.html %} class) with **non-zero area**, meaning that intersecting two intersecting lines **does not** produce a point (although it geometrically should).


### Graphs (the other ones)
Graphs are an essential part of any math/CS-oriented graphical tool.
The ones we'll be covering in this part of the series are the ones you plot (as opposed to the combinatorial ones covered in the [previous part](/manim/camera-and-graphs/)).
We'll be mainly using the {% manim_doc `Axes` reference/manim.mobject.graphing.coordinate_systems.Axes.html %} class and its parent {% manim_doc `CoordinateSystem` reference/manim.mobject.graphing.coordinate_systems.CoordinateSystem.html %}.

#### Using expressions

The simplest way to plot a graph of a function using an expression.

```py
from manim import *
from math import sin


class GraphExample(Scene):
    def construct(self):
        axes = Axes(x_range=[-5, 5], y_range=[-3, 7])
        labels = axes.get_axis_labels(x_label="x", y_label="y")

        def f1(x):
            return x ** 2

        def f2(x):
            return sin(x)

        g1 = axes.plot(f1, color=RED)
        g2 = axes.plot(f2, color=BLUE)

        self.play(Write(axes), Write(labels))

        self.play(AnimationGroup(Write(g1), Write(g2), lag_ratio=0.5))

        self.play(Unwrite(axes), Unwrite(labels), Unwrite(g1), Unwrite(g2))
```

{% manim_video 4-GraphExample %}

When drawing this way, it is important for the functions to be **continuous** (and when they are not, draw them by part).
This is due to the fact that Manim draws them by sampling their function values which it then interpolates via a curve (a polynomial passing through the sampled points) and thus cannot know about the discontinuity.

```py
from manim import *
from math import sin


class DiscontinuousGraphExample(Scene):
    def construct(self):
        axes = Axes(x_range=[-5, 5], y_range=[-3, 7])
        labels = axes.get_axis_labels(x_label="x", y_label="y")

        def f(x):
            return 1 / x

        g_bad = axes.plot(f, color=RED)

        g_left = axes.plot(f, x_range=[-5, -0.1], color=GREEN)
        g_right = axes.plot(f, x_range=[0.1, 5], color=GREEN)

        self.play(Write(axes), Write(labels))

        self.play(Write(g_bad))
        self.play(FadeOut(g_bad))

        self.play(AnimationGroup(Write(g_left), Write(g_right), lag_ratio=0.5))

        self.play(Unwrite(axes), Unwrite(labels), Unwrite(g_left), Unwrite(g_right))
```

{% manim_video 4-DiscontinuousGraphExample %}

#### Parametric graphs

The other, more general way to define a graph is parametrically -- we're also defining the function using an expression, but it is a single parameter function returning the corresponding pair of coordinates.

```py
from manim import *
from math import sin, cos


class ParametricGraphExample(Scene):
    def construct(self):
        axes = Axes(x_range=[-10, 10], y_range=[-5, 5])
        labels = axes.get_axis_labels(x_label="x", y_label="y")

        def f1(t):
            """Parametric function of a circle."""
            return (cos(t) * 3 - 4.5, sin(t) * 3)

        def f2(t):
            """Parametric function of <3."""
            return (
                0.2 * (16 * (sin(t)) ** 3) + 4.5,
                0.2 * (13 * cos(t) - 5 * cos(2 * t) - 2 * cos(3 * t) - cos(4 * t)),
            )

        # the t_range parameter determines the range of the parametric function parameter
        g1 = axes.plot_parametric_curve(f1, color=RED, t_range=[0, 2 * PI])
        g2 = axes.plot_parametric_curve(f2, color=BLUE, t_range=[-PI, PI])

        self.play(Write(axes), Write(labels))

        self.play(AnimationGroup(Write(g1), Write(g2), lag_ratio=0.5))

        self.play(Unwrite(axes), Unwrite(labels), Unwrite(g1), Unwrite(g2))
```

{% manim_video 4-ParametricGraphExample %}

#### Line graphs

Besides defining the graph in terms of expressions, it is also possible to define it using the raw values themselves.

```py
from manim import *
from random import random, seed


class LineGraphExample(Scene):
    def construct(self):
        seed(0xDEADBEEF2)  # prettier input :P

        # value to graph (x, y);  np.arange(l, r, step) returns a list
        # from l (inclusive) do r (non-inclusive) with steps of size step
        x_values = np.arange(-1, 1 + 0.25, 0.25)
        y_values = [random() for _ in x_values]

        # include axis numbers this time
        axes = Axes(
            x_range=[-1, 1, 0.25],
            y_range=[-0.1, 1, 0.25],
            x_axis_config={"numbers_to_include": x_values},
            y_axis_config={"numbers_to_include": np.arange(0, 1, 0.25)},
            axis_config={"decimal_number_config": {"num_decimal_places": 2}},
        )

        labels = axes.get_axis_labels(x_label="x", y_label="y")

        graph = axes.plot_line_graph(x_values=x_values, y_values=y_values)

        self.play(Write(axes), Write(labels))

        self.play(Write(graph), run_time=2)

        self.play(Unwrite(axes), Unwrite(labels), Unwrite(graph))
```

{% manim_video 4-LineGraphExample %}

### Introduction to 3D
Let's finally explore the world of 3D in Manim!

#### Basics

The most important thing is that we get a new dimension which we'll call \(z\).
We also get two new constants for this dimension which we can use to move objects in it: `OUT` (positive) and `IN` (negative).
To render the scene in 3D, we'll have to use {% manim_doc `ThreeDScene` reference/manim.scene.three_d_scene.ThreeDScene.html %}.

```py
from manim import *


class Axes3DExample(ThreeDScene):
    def construct(self):
        axes = ThreeDAxes()

        x_label = axes.get_x_axis_label(Tex("x"))
        y_label = axes.get_y_axis_label(Tex("y")).shift(UP * 1.8)

        # 3D variant of the Dot() object
        dot = Dot3D()

        # zoom out so we see the axes
        self.set_camera_orientation(zoom=0.5)

        self.play(FadeIn(axes), FadeIn(dot), FadeIn(x_label), FadeIn(y_label))

        self.wait(0.5)

        # animate the move of the camera to properly see the axes
        self.move_camera(phi=75 * DEGREES, theta=30 * DEGREES, zoom=1, run_time=1.5)

        # built-in updater which begins camera rotation
        self.begin_ambient_camera_rotation(rate=0.15)

        # one dot for each direction
        upDot = dot.copy().set_color(RED)
        rightDot = dot.copy().set_color(BLUE)
        outDot = dot.copy().set_color(GREEN)

        self.wait(1)

        self.play(
            upDot.animate.shift(UP),
            rightDot.animate.shift(RIGHT),
            outDot.animate.shift(OUT),
        )

        self.wait(2)
```

{% manim_video 4-Axes3DExample %}

As you can see, the initial camera position assumes that we're working in 2D.
To control it, we used the {% manim_doc `set_camera_orientation` reference/manim.scene.three_d_scene.ThreeDScene.html#manim.scene.three_d_scene.ThreeDScene.set_camera_orientation %} to set its position and {% manim_doc `begin_ambient_camera_rotation` reference/manim.scene.three_d_scene.ThreeDScene.html#manim.scene.three_d_scene.ThreeDScene.move_camera %} to begin an ambient rotation.
The used arguments `phi` (\(\varphi\)) a `theta` (\(\vartheta\)) determine the position like so.

![Meaning of the phi and theta arguments for 3D camera positioning.](/assets/manim/4-Camera.svg)

Besides the {% manim_doc `ThreeDAxes` reference/manim.mobject.graphing.coordinate_systems.ThreeDAxes.html %} object used to work with the 3D axes, Manim also contains a number of 3D {% manim_doc primitives reference/manim.mobject.three_d.three_dimensions.html %} that you can use to create more complex 3D scenes.

```py
from manim import *


class Rotation3DExample(ThreeDScene):
    def construct(self):
        cube = Cube(side_length=3, fill_opacity=1)

        self.begin_ambient_camera_rotation(rate=0.3)

        self.set_camera_orientation(phi=75 * DEGREES, theta=30 * DEGREES)

        self.play(Write(cube), run_time=2)

        self.wait(3)

        self.play(Unwrite(cube), run_time=2)
```

{% manim_video 4-Rotation3DExample %}

#### Operations

Translating and rotating objects in 3D behaves just like you would expect (again using {% manim_doc `shift` reference/manim.mobject.mobject.Mobject.html#manim.mobject.mobject.Mobject.shift %} and {% manim_doc `scale` reference/manim.mobject.mobject.Mobject.html#manim.mobject.mobject.Mobject.scale %}).
Rotation is a bit trickier, since it isn't entirely clear what should happen when rotating an object by a certain amount of degrees.
It is quite an interesting topic and has a number of solutions (see [Euler angles](https://en.wikipedia.org/wiki/Euler_angles) and [Quaternions](https://en.wikipedia.org/wiki/Quaternion)) if you're interested, we'll however use the most simple one: specify an axis that the object will rotate about.

```py
from manim import *


class Basic3DExample(ThreeDScene):
    def construct(self):
        cube = Cube(side_length=3, fill_opacity=0.5)

        self.set_camera_orientation(phi=75 * DEGREES, theta=30 * DEGREES)

        self.play(FadeIn(cube))

        for axis in [RIGHT, UP, OUT]:
            self.play(Rotate(cube, PI / 2, about_point=ORIGIN, axis=axis))

        self.play(FadeOut(cube))
```

{% manim_video 4-Basic3DExample %}

### Tasks

#### Binomic Distribution Simulation
Create an animation of the [Galton board](https://en.wikipedia.org/wiki/Galton_board).

{% manim_video 4-BinomialDistributionSimulation %}

There are a number of new classes that will be useful for creating the movement of the marble.
The main one is the {% manim_doc `CubicBezier` reference/manim.mobject.geometry.arc.CubicBezier.html %}, which can be used to model the path and animated by {% manim_doc `MoveAlongPath` reference/manim.animation.movement.MoveAlongPath.html %}.
To create the moving and fading animation, you can use the custom `MoveAndFade` animation, the functionality of which will be covered in the upcoming series part.

Also, the rate functions from the [previous part](/manim/camera-and-graphs/) will come in handy to make the movement look believable.

```py
from manim import *
from random import choice, seed


class MoveAndFade(Animation):
    def __init__(self, mobject: Mobject, path: VMobject, **kwargs):
        self.path = path
        self.original = mobject.copy()
        super().__init__(mobject, **kwargs)

    def interpolate_mobject(self, alpha: float) -> None:
        point = self.path.point_from_proportion(self.rate_func(alpha))

        # this is not entirely clean sice we're creating a new object
        # this is because obj.fade() doesn't add opaqueness but adds it
        self.mobject.become(self.original.copy()).move_to(point).fade(alpha)


class BezierExample(Scene):
    def construct(self):
        point_coordinates = [
            UP + LEFT * 3,  # starting
            UP + RIGHT * 2,  # 1. control
            DOWN + LEFT * 2,  # 2. control
            DOWN + RIGHT * 3,  # starting
        ]

        points = VGroup(*[Dot().move_to(position) for position in point_coordinates]).scale(1.5)

        # make control points blue
        points[1].set_color(BLUE)
        points[2].set_color(BLUE)

        bezier = CubicBezier(*point_coordinates).scale(1.5)

        self.play(Write(bezier), Write(points))

        # regular moving along path
        circle = Circle(fill_color=GREEN, fill_opacity=1, stroke_opacity=0).scale(0.25).move_to(points[0])

        self.play(FadeIn(circle, shift=RIGHT * 0.5))
        self.play(MoveAlongPath(circle, bezier))

        self.play(FadeOut(circle))

        # moving along path with fading
        circle = Circle(fill_color=GREEN, fill_opacity=1, stroke_opacity=0).scale(0.25).move_to(points[0])

        self.play(FadeIn(circle, shift=RIGHT * 0.5))
        self.play(MoveAndFade(circle, bezier))

        self.play(FadeOut(bezier), FadeOut(points), FadeOut(circle))
```

{% manim_video 4-BezierExample %}

For additional information about the behavior of Bézier curves, I highly recommend Jason Davies' incredible [interactive website](https://www.jasondavies.com/animated-bezier/), which explains everything very elegantly.

{% manim_solution %}
from manim import *
from random import choice, seed


class MoveAndFade(Animation):
    def __init__(self, mobject: Mobject, path: VMobject, **kwargs):
        self.path = path
        self.original = mobject.copy()
        super().__init__(mobject, **kwargs)

    def interpolate_mobject(self, alpha: float) -> None:
        point = self.path.point_from_proportion(self.rate_func(alpha))

        # this is not entirely clean sice we're creating a new object
        # this is because obj.fade() doesn't add opaqueness but adds it
        self.mobject.become(self.original.copy()).move_to(point).fade(alpha)


class BinomialDistributionSimulation(Scene):
    def create_graph(x_values, y_values):
        """Build a graph with the given values."""
        y_values_all = list(range(0, (max(y_values) or 1) + 1))

        axes = (
            Axes(
                x_range=[-n // 2 + 1, n // 2, 1],
                y_range=[0, max(y_values) or 1, 1],
                x_axis_config={"numbers_to_include": x_values},
                tips=False,
            )
            .scale(0.45)
            .shift(LEFT * 3.0)
        )

        graph = axes.plot_line_graph(x_values=x_values, y_values=y_values)

        return graph, axes

    def construct(self):
        seed(0xDEADBEEF2)  # hezčí vstupy :)

        radius = 0.13
        x_spacing = radius * 1.5
        y_spacing = 4 * radius

        n = 9
        pyramid = VGroup()
        pyramid_values = []  # how many marbles fell where

        # build the pyramid
        for i in range(1, n + 1):
            row = VGroup()

            for j in range(i):
                obj = Dot()

                # if it's the last row, make the rows numbers instead
                if i == n:
                    obj = Tex("0")
                    pyramid_values.append(0)

                row.add(obj)

            row.arrange(buff=2 * x_spacing)

            if len(pyramid) != 0:
                row.move_to(pyramid[-1]).shift(DOWN * y_spacing)

            pyramid.add(row)

        pyramid.move_to(RIGHT * 3.4)

        x_values = np.arange(-n // 2 + 1, n // 2 + 1, 1)

        graph, axes = create_graph(x_values, pyramid_values)

        self.play(Write(axes), Write(pyramid), Write(graph), run_time=1.5)

        for iteration in range(120):
            circle = (
                Circle(fill_opacity=1, stroke_opacity=0)
                .scale(radius)
                .next_to(pyramid[0][0], UP, buff=0)
            )

            # go faster and faster
            run_time = (
                0.5
                if iteration == 0
                else 0.1
                if iteration == 1
                else 0.02
                if iteration < 20
                else 0.003
            )

            self.play(FadeIn(circle, shift=DOWN * 0.5), run_time=run_time * 2)

            x = 0
            for i in range(1, n):
                next_position = choice([0, 1])
                x += next_position

                dir = LEFT if next_position == 0 else RIGHT

                circle_center = circle.get_center()

                # behave normally when it's not the last row
                if i != n - 1:
                    b = CubicBezier(
                        circle_center,
                        circle_center + dir * x_spacing,
                        circle_center + dir * x_spacing + DOWN * y_spacing / 2,
                        circle.copy().next_to(pyramid[i][x], UP, buff=0).get_center(),
                    )

                    self.play(
                        MoveAlongPath(circle, b, rate_func=rate_functions.ease_in_quad),
                        run_time=run_time,
                    )

                # if it is, animate fadeout and add
                else:
                    b = CubicBezier(
                        circle_center,
                        circle_center + dir * x_spacing,
                        circle_center + dir * x_spacing + DOWN * y_spacing / 2,
                        pyramid[i][x].get_center(),
                    )

                    pyramid_values[x] += 1

                    n_graph, n_axes = create_graph(x_values, pyramid_values)

                    self.play(
                        AnimationGroup(
                            AnimationGroup(
                                MoveAndFade(
                                    circle, b, rate_func=rate_functions.ease_in_quad
                                ),
                                run_time=run_time,
                            ),
                            AnimationGroup(
                                pyramid[i][x]
                                .animate(run_time=run_time)
                                .become(
                                    Tex(str(pyramid_values[x])).move_to(pyramid[i][x])
                                ),
                                graph.animate.become(n_graph),
                                axes.animate.become(n_axes),
                                run_time=run_time,
                            ),
                            lag_ratio=0.3,
                        )
                    )

        self.play(FadeOut(axes), FadeOut(pyramid), FadeOut(graph), run_time=1)
{% endmanim_solution %}


#### 3D Game of Life
Create an animation of a 3D variant of [Conway's Game of Life](https://en.wikipedia.org/wiki/Conway's_Game_of_Life).

The rules are simple: we start in an initial state where some cells are dead and some are alive.
Each (besides the corner ones) has 26 neighbours (all cells 1 away in space).
For each game, we define sets of rules \(X\) and \(Y\), which determine when cells live and die.
In each step of the game, **all cells at once** change by the following rules:

- if cell is **alive** and its number of alive neighbours is in \(X\), it **survives**, otherwise it **dies**
- if cell is **dead** and its number of alive neighbours is in \(Y\), it gets **revived**, otherwise it **stays dead**


##### Basic variant
Implement a game with rules \(X = \left\{4, 5\right\}, Y = \left\{5\right\}\).
Simulate it on a \(16^3\) board with a random initial state (\(p = 0.2\) for cells to be a live) and colors determining the position in 3D space.

{% manim_video 4-GOL-first %}

To check the correctness of rules, you can use this [awesome interactive editor](https://kodub.itch.io/game-of-life-3d) by Kodub.

I very much recommend rendering smaller areas first (say \(8^3\)) on lower quality (`l` or `m`).
While the community version of Manim supports 3D rendering, it is not optimized for it and only uses the processor to render the frames.
If you're interested in faster rendering, I would suggest you take a look at [ManimGL](https://github.com/3b1b/manim), which is actively developed by Grant Sanderson and supports interactive animations, but its documentation is practically non-existent and will differ from the code covered in this series in a lot of ways.


##### Cell age
We'll define a new parameter \(Z\), which determines the "liveness" of a cell.
The liveness of a new cell is \(Z\) and gets decremented each step of the simulation.
The cell can now only die when its liveness is \(1\), otherwise it is considered alive.
If it survives with liveness \(1\), its liveness stays at \(1\).

{% manim_video 4-GOL-second %}

Implement a game with rules \(X = \{2, 6, 9\}\), \(Y = \{4, 6, 8, 9\}\) and \(Z = 10\).
The colors are determined by the age of the cells.

{% manim_solution %}
from manim import *
from random import random, seed
from enum import Enum

# inspired by https://softologyblog.wordpress.com/2019/12/28/3d-cellular-automata-3/


class Grid:
    class ColorType(Enum):
        FROM_COORDINATES = 0
        FROM_PALETTE = 1

    def __init__(
        self,
        scene,
        grid_size,
        survives_when,
        revives_when,
        state_count=2,
        size=1,
        palette=["#000b5e", "#001eff"],
        color_type=ColorType.FROM_PALETTE,
    ):
        self.grid = {}
        self.scene = scene
        self.grid_size = grid_size
        self.size = size
        self.survives_when = survives_when
        self.revives_when = revives_when
        self.state_count = state_count
        self.palette = palette
        self.color_type = color_type

        self.bounding_box = Cube(side_length=self.size, color=GRAY, fill_opacity=0.05)
        self.scene.add(self.bounding_box)

    def fadeOut(self):
        self.scene.play(
            FadeOut(self.bounding_box),
            *[FadeOut(self.grid[index][0]) for index in self.grid],
        )

    def __index_to_position(self, index):
        """Convert the index of a cell to its position in 3D."""
        dirs = [RIGHT, UP, OUT]

        # be careful!
        # we can't just add stuff to ORIGIN, since it doesn't create new objects,
        # meaning we would be moving the origin, which messes with the animations
        result = list(ORIGIN)
        for dir, value in zip(dirs, index):
            result += ((value - (self.grid_size - 1) / 2) / self.grid_size) * dir * self.size

        return result

    def __get_new_cell(self, index):
        """Create a new cell"""
        cell = (
            Cube(
                side_length=1 / self.grid_size * self.size, color=BLUE, fill_opacity=1
            ).move_to(self.__index_to_position(index)),
            self.state_count - 1,
        )

        self.__update_cell_color(index, *cell)

        return cell

    def __return_neighbouring_cell_coordinates(self, index):
        """Return the coordinates of the neighbourhood of a given index."""
        neighbourhood = set()
        for dx in range(-1, 1 + 1):
            for dy in range(-1, 1 + 1):
                for dz in range(-1, 1 + 1):
                    if dx == 0 and dy == 0 and dz == 0:
                        continue

                    nx = index[0] + dx
                    ny = index[1] + dy
                    nz = index[2] + dz

                    # don't loop around (although we could)
                    if (
                        nx < 0
                        or nx >= self.grid_size
                        or ny < 0
                        or ny >= self.grid_size
                        or nz < 0
                        or nz >= self.grid_size
                    ):
                        continue

                    neighbourhood.add((nx, ny, nz))

        return neighbourhood

    def __count_neighbours(self, index):
        """Return the number of neighbouring cells for a given index (excluding itself)."""
        total = 0
        for neighbour_index in self.__return_neighbouring_cell_coordinates(index):
            if neighbour_index in self.grid:
                total += 1

        return total

    def __return_possible_cell_change_indexes(self):
        """Return the indexes of all possible cells that could change."""
        changes = set()
        for index in self.grid:
            changes |= self.__return_neighbouring_cell_coordinates(index).union({index})
        return changes

    def toggle(self, index):
        """Toggle a given cell."""
        if index in self.grid:
            self.scene.remove(self.grid[index][0])
            del self.grid[index]
        else:
            self.grid[index] = self.__get_new_cell(index)
            self.scene.add(self.grid[index][0])

    def __update_cell_color(self, index, cell, age):
        """Update the color of the specified cell."""
        if self.color_type == self.ColorType.FROM_PALETTE:
            state_colors = color_gradient(self.palette, self.state_count - 1)

            cell.set_color(state_colors[age - 1])
        else:

            def coordToHex(n):
                return hex(int(n * (256 / self.grid_size)))[2:].ljust(2, "0")

            cell.set_color(
                f"#{coordToHex(index[0])}{coordToHex(index[1])}{coordToHex(index[2])}"
            )

    def do_iteration(self):
        """Perform the automata generation, returning True if a state of any cell changed."""
        new_grid = {}
        something_changed = False

        for index in self.__return_possible_cell_change_indexes():
            neighbours = self.__count_neighbours(index)

            # alive rules
            if index in self.grid:
                cell, age = self.grid[index]

                # always decrease age
                if age != 1:
                    age -= 1
                    something_changed = True

                # survive if within range or age isn't 1
                if neighbours in self.survives_when or age != 1:
                    self.__update_cell_color(index, cell, age)
                    new_grid[index] = (cell, age)
                else:
                    self.scene.remove(self.grid[index][0])
                    something_changed = True

            # dead rules
            else:
                # revive if within range
                if neighbours in self.revives_when:
                    new_grid[index] = self.__get_new_cell(index)
                    self.scene.add(new_grid[index][0])
                    something_changed = True

        self.grid = new_grid

        return something_changed


class GOLFirst(ThreeDScene):
    def construct(self):
        seed(0xDEADBEEF)

        self.set_camera_orientation(phi=75 * DEGREES, theta=30 * DEGREES)
        self.begin_ambient_camera_rotation(rate=-0.20)

        grid_size = 16
        size = 3.5

        grid = Grid(
            self,
            grid_size,
            [4, 5],
            [5],
            state_count=2,
            size=size,
            color_type=Grid.ColorType.FROM_COORDINATES,
        )

        for i in range(grid_size):
            for j in range(grid_size):
                for k in range(grid_size):
                    if random() < 0.2:
                        grid.toggle((i, j, k))

        grid.fadeIn()

        self.wait(1)

        for i in range(50):
            something_changed = grid.do_iteration()

            if not something_changed:
                break

            self.wait(0.2)

        self.wait(2)

        grid.fadeOut()


class GOLSecond(ThreeDScene):
    def construct(self):
        seed(0xDEADBEEF)

        self.set_camera_orientation(phi=75 * DEGREES, theta=30 * DEGREES)
        self.begin_ambient_camera_rotation(rate=0.15)

        grid_size = 16
        size = 3.5

        grid = Grid(
            self,
            grid_size,
            [2, 6, 9],
            [4, 6, 8, 9],
            state_count=10,
            size=size,
            color_type=Grid.ColorType.FROM_PALETTE,
        )

        for i in range(grid_size):
            for j in range(grid_size):
                for k in range(grid_size):
                    if random() < 0.3:
                        grid.toggle((i, j, k))

        self.wait(2)

        for i in range(70):
            something_changed = grid.do_iteration()

            if not something_changed:
                break

            self.wait(0.1)

        self.wait(2)

        grid.fadeOut()
{% endmanim_solution %}
