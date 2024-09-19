---
title: Manim – Plotting and 3D Scenes
category: "Manim"
category_icon: /assets/category-icons/manim.svg
css: manim
category_part: 4
redirect_from:
- /manim/4/
- /manim/3d-and-the-other-graphs/
excerpt: In this part of the series, we'll take a look at Manim's tools for 3D animations and also at plotting all sorts of graphs.
end: <a href="/manim/1/">Part 1</a>, <a href="/manim/2/">Part 2</a>, <a href="/manim/3/">Part 3</a>, <strong>→ Part 4 ←</strong>, <a href="/manim/5/">Part 5</a>, <a href="/manim/6/">Part 6</a>
---

- .
{:toc}

In this part of the series, we'll take a look at Manim's tools for 3D animations and also at plotting all sorts of graphs.

### Binary operations
We'll briefly take a look at binary operations on Manim objects, since they might come in handy for more advanced animations.
We'll use the builtin classes from the {% manim_doc `boolean_ops` reference/manim.mobject.geometry.boolean_ops.html %} file, namely {% manim_doc `Difference` reference/manim.mobject.geometry.boolean_ops.Difference.html %}, {% manim_doc `Intersection` reference/manim.mobject.geometry.boolean_ops.Intersection.html %}, {% manim_doc `Union` reference/manim.mobject.geometry.boolean_ops.Union.html %} and {% manim_doc `Exclusion` reference/manim.mobject.geometry.boolean_ops.Exclusion.html %}.

```py
{% include manim/04-boolean-operations-example.py %}
```

{% manim_video 04-boolean-operations-example %}

When using the aforementioned classes, it is important to keep in mind that they are restricted to vector objects (the {% manim_doc `VMobject` reference/manim.mobject.types.vectorized_mobject.VMobject.html %} class) with **non-zero area**, meaning that intersecting two intersecting lines **does not** produce a point (although it geometrically should).


### Graphs (the other ones)
Graphs are an essential part of any math/CS-oriented graphical tool.
The ones we'll be covering in this part of the series are the ones you plot (as opposed to the combinatorial ones covered in the [previous part](/manim/camera-and-graphs/)).
We'll be mainly using the {% manim_doc `Axes` reference/manim.mobject.graphing.coordinate_systems.Axes.html %} class and its parent {% manim_doc `CoordinateSystem` reference/manim.mobject.graphing.coordinate_systems.CoordinateSystem.html %}.

#### Using expressions

The simplest way to plot a graph of a function using an expression via the {% manim_doc `plot` reference/manim.mobject.graphing.coordinate_systems.CoordinateSystem.html#manim.mobject.graphing.coordinate_systems.CoordinateSystem.plot %} function.

```py
{% include manim/04-graph-example.py %}
```

{% manim_video 04-graph-example %}

When drawing this way, it is important for the functions to be **continuous** (and when they are not, draw them by part).
This is due to the fact that Manim draws them by sampling their function values which it then interpolates via a curve (a polynomial passing through the sampled points) and thus cannot know about the discontinuity.

```py
{% include manim/04-discontinuous-graph-example.py %}
```

{% manim_video 04-discontinuous-graph-example %}

#### Parametric graphs

The other, more general way to plot a graph is parametrically via {% manim_doc `plot_parametric_curve` reference/manim.mobject.graphing.coordinate_systems.CoordinateSystem.html#manim.mobject.graphing.coordinate_systems.CoordinateSystem.plot_parametric_curve %} -- we're also defining the function using an expression, but it is a single parameter function returning the corresponding pair of coordinates.

```py
{% include manim/04-parametric-graph-example.py %}
```

{% manim_video 04-parametric-graph-example %}

#### Line graphs

Besides defining the graph in terms of expressions, it is also possible to define it using the raw values themselves via {% manim_doc `plot_line_graph` reference/manim.mobject.graphing.coordinate_systems.Axes.html#manim.mobject.graphing.coordinate_systems.Axes.plot_line_graph %}.

```py
{% include manim/04-line-graph-example.py %}
```

{% manim_video 04-line-graph-example %}

### Introduction to 3D
Let's finally explore the world of 3D in Manim!

#### Basics

The most important thing is that we get a new dimension which we'll call \(z\).
We also get two new constants for this dimension which we can use to move objects in it: `OUT` (positive) and `IN` (negative).
To render the scene in 3D, we'll have to use {% manim_doc `ThreeDScene` reference/manim.scene.three_d_scene.ThreeDScene.html %}.

```py
{% include manim/04-axes3d-example.py %}
```

{% manim_video 04-axes3d-example %}

As you can see, the initial camera position assumes that we're working in 2D.
To control it, we used the {% manim_doc `set_camera_orientation` reference/manim.scene.three_d_scene.ThreeDScene.html#manim.scene.three_d_scene.ThreeDScene.set_camera_orientation %} to set its position and {% manim_doc `begin_ambient_camera_rotation` reference/manim.scene.three_d_scene.ThreeDScene.html#manim.scene.three_d_scene.ThreeDScene.move_camera %} to begin an ambient rotation.
The used arguments `phi` (\(\varphi\)) a `theta` (\(\vartheta\)) determine the position.

![Meaning of the phi and theta arguments for 3D camera positioning.](/assets/manim/04-camera.svg)

Besides the {% manim_doc `ThreeDAxes` reference/manim.mobject.graphing.coordinate_systems.ThreeDAxes.html %} object used to work with the 3D axes, Manim also contains a number of 3D {% manim_doc primitives reference/manim.mobject.three_d.three_dimensions.html %} that you can use to create more complex 3D scenes.

```py
{% include manim/04-rotation-3d-example.py %}
```

{% manim_video 04-rotation-3d-example %}

#### Operations

Translating and rotating objects in 3D behaves just like you would expect (again using {% manim_doc `shift` reference/manim.mobject.mobject.Mobject.html#manim.mobject.mobject.Mobject.shift %} and {% manim_doc `scale` reference/manim.mobject.mobject.Mobject.html#manim.mobject.mobject.Mobject.scale %}).
Rotation is a bit trickier, since it isn't entirely clear what should happen when rotating an object by a certain amount of degrees.
It is quite an interesting topic and has a number of solutions (see [Euler angles](https://en.wikipedia.org/wiki/Euler_angles) and [Quaternions](https://en.wikipedia.org/wiki/Quaternion)) if you're interested, we'll however use the most simple one: specify an axis that the object will rotate about.

```py
{% include manim/04-basic-3d-example.py %}
```

{% manim_video 04-basic-3d-example %}

### Tasks

#### Binomial Distribution Simulation
Create an animation of the [Galton board](https://en.wikipedia.org/wiki/Galton_board).

{% manim_video 04-binomial-distribution-simulation %}

There are a number of new classes that will be useful for creating the movement of the marble.
The main one is the {% manim_doc `CubicBezier` reference/manim.mobject.geometry.arc.CubicBezier.html %}, which can be used to model the path and animated by {% manim_doc `MoveAlongPath` reference/manim.animation.movement.MoveAlongPath.html %}.
To create the moving and fading animation, you can use the custom `MoveAndFade` animation, the functionality of which will be covered in the upcoming series part.

Also, the rate functions from the [previous part](/manim/camera-and-graphs/) will come in handy to make the movement look believable.

```py
{% include manim/04-bezier-example.py %}
```

{% manim_video 04-bezier-example %}

For additional information about the behavior of Bézier curves, I highly recommend Jason Davies' incredible [interactive website](https://www.jasondavies.com/animated-bezier/), which explains everything very elegantly.

{% manim_solution %}
{% include manim/04-binomial-distribution-simulation.py %}
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

{% manim_video 04-gol-first %}

To check the correctness of rules, you can use this [awesome interactive editor](https://kodub.itch.io/game-of-life-3d) by Kodub.

I very much recommend rendering smaller areas first (say \(8^3\)) on lower quality (`l` or `m`).
While the community version of Manim supports 3D rendering, it is not optimized for it and only uses the processor to render the frames.
If you're interested in faster rendering, I would suggest you take a look at [ManimGL](https://github.com/3b1b/manim), which is actively developed by Grant Sanderson and supports interactive animations, but its documentation is practically non-existent and will differ from the code covered in this series in a lot of ways.


##### Cell age
We'll define a new parameter \(Z\), which determines the "liveness" of a cell.
The liveness of a new cell is \(Z\) and gets decremented each step of the simulation.
The cell can now only die when its liveness is \(1\), otherwise it is considered alive.
If it survives with liveness \(1\), its liveness stays at \(1\).

{% manim_video 04-gol-second %}

Implement a game with rules \(X = \{2, 6, 9\}\), \(Y = \{4, 6, 8, 9\}\) and \(Z = 10\).
The colors are determined by the age of the cells.

{% manim_solution %}
{% include manim/04-gol.py %}
{% endmanim_solution %}
