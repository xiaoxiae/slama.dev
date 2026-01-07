---
date: '2022-07-03'
categoryPart: 3
title: Camera and Graphs
end: <a href="/manim/1/">Part 1</a>, <a href="/manim/2/">Part 2</a>, <strong>→ Part
  3 ←</strong>, <a href="/manim/4/">Part 4</a>, <a href="/manim/5/">Part 5</a>, <a
  href="/manim/6/">Part 6</a>
description: Camera controls, (combinatorial) graphs and rate functions.
toc: true
---

This part of the series covers mainly two topics -- the camera and (combinatorial) graphs.
Besides this, it also includes some useful concepts for more advanced animations.

### `save` and `restore`
Each Manim object ({{< doc "manim" "MObject" "reference/manim.mobject.mobject.Mobject.html" >}}) contains the {{< doc "manim" "save_state" "reference/manim.mobject.mobject.Mobject.html#manim.mobject.mobject.Mobject.save_state" >}} function that allows to save the current state of the object, which it can later go back to using the {{< doc "manim" "restore" "reference/manim.mobject.mobject.Mobject.html#manim.mobject.mobject.Mobject.restore" >}} function (possibly using the animate syntax).
This makes the code, in certain situations, much more compact and readable.

```python {file="03-save-and-restore-example.py"}
```

{{< video "manim" "03-save-and-restore-example" >}}

One animation that we used here but haven't seen yet is the {{< doc "manim" "Unwrite" "reference/manim.animation.creation.Unwrite.html" >}}, which is {{< doc "manim" "Write" "reference/manim.animation.creation.Write.html" >}} in reverse.

### Graphs

#### Introduction
Combinatorial graphs are a necessary component of any mathematical library and Manim is no exception.
They are implemented using the {{< doc "manim" "Graph" "reference/manim.mobject.graph.Graph.html" >}} class.

```python {file="03-graph-example.py"}
```

{{< video "manim" "03-graph-example" >}}

As you can see from the code, the {{< doc "manim" "Graph" "reference/manim.mobject.graph.Graph.html" >}} expects a list of vertices and edges as the input.
To access them, we will use the `graph.vertices` and `graph.edges` dictionaries -- just be careful that edges of type \((u, v)\) can't be accessed by using \((v, u)\) (something quite unintuitive for undirected graphs).

The default algorithm for vertex positioning is [Fruchterman-Reingold](https://networkx.org/documentation/stable/reference/generated/networkx.drawing.layout.spring_layout.html) and works in a simple way -- vertices have a repulsing force and edges have an attracting one.
Besides the `seed` parameter, the algorithm has a number of other parameters for adjusting its behavior, which you can read about in the link above.

#### Custom vertices and edges
Note that vertices and edges need not be circles and segments -- we can use custom Manim objects and functions for creating more exotic graphs.

```python {file="03-starry-sky-example.py"}
```

{{< video "manim" "03-starry-sky-example" >}}

As the code suggests, the current implementation expects both `vertex_type` and `edge_type` to be functions returning a {{< doc "manim" "MObject" "reference/manim.mobject.mobject.html" >}}. Besides this, the `edge_type` function must have an optional `z_index` parameter, since the graph implementation sets it to a negative number to push the edges behind the vertices. Additionally, the edges must have a `put_start_and_end_on` function (which {{< doc "manim" "DashedLine" "reference/manim.mobject.geometry.line.DashedLine.html" >}} does), since this is what edge udaters call when vertices move.

#### Random graphs
If we don't want to create random graphs manually, we can use the popular [`networkx`](https://networkx.org/documentation/stable/reference/introduction.html) library, which contains a number of useful graph generators and graph-related functions.

```python {file="03-graph-generation-example.py"}
```

{{< video "manim" "03-graph-generation-example" >}}

### Camera
In Manim, each camera scene contains a camera object (implemented via the {{< doc "manim" "Camera" "reference/manim.camera.camera.Camera.html" >}}).
So far, it wasn't very useful, because we've implemented all object transformations by changing the objects themselves.
In certain cases, however, it is much more convenient to just move/zoom the camera to achieve the same result.

This is not as simple as it seems, because the default {{< doc "manim" "Scene" "reference/manim.scene.scene.Scene.html" >}} class isn't equipped to deal with a moving camera.
That's why we'll use the {{< doc "manim" "MovingCameraScene" "reference/manim.scene.moving_camera_scene.MovingCameraScene.html" >}}, which contains a `frame` object that we can animate.

```python {file="03-moving-camera-example.py"}
```

{{< video "manim" "03-moving-camera-example" >}}

As the example suggests, the `self.camera.frame` object behaves just like all of the animated objects we've seen -- we can set its height, scale it, move it, etc.
This also means that we can use updaters exactly how one would expect.

```python {file="03-moving-camera-updater-example.py"}
```

{{< video "manim" "03-moving-camera-updater-example" >}}

As the code mentions, it is very important to pay attention to whether the updated object has been added to the scene.
In this case, the updater hasn't been animated yet (which implicitly adds it to the scene), meaning that we had to add it manually.

Besides moving and zooming, we can also do things like changing the color of the background.

```python {file="03-background-color-example.py"}
```

{{< video "manim" "03-background-color-example" >}}


### Rate functions
For fine-tuning animations, it is sometimes desirable to change the functions that time them.
We've already seen

```python {file="03-rate-functions-example.py"}
```

{{< video "manim" "03-rate-functions-example" >}}

Below is the (almost) complete list of curves that are frequently used in animations.
There also exists a [wonderful website](https://easings.net/) which contains a number of these functions, including an interactive visualisation of their progress, if you want to experiment with them outside of Manim.

<!--
```py
from manim import *


class RateFuncExample(Scene):
    def construct(self):
        x = VGroup()
        for k, v in rate_functions.__dict__.items():
            if "function" in str(v):
                if (
                    not k.startswith("__")
                    and not k.startswith("sqrt")
                    and not k.startswith("bezier")
                ):
                    try:
                        rate_func = v
                        plot = (
                            ParametricFunction(
                                lambda x: [x, rate_func(x), 0],
                                t_range=[0, 1, .01],
                                use_smoothing=False,
                                color=YELLOW,
                            )
                            .stretch_to_fit_width(1.5)
                            .stretch_to_fit_height(1)
                        )
                        plot_bg = SurroundingRectangle(plot).set_color(WHITE)
                        plot_title = (
                            Text(rate_func.__name__, weight=BOLD)
                            .scale(0.5)
                            .next_to(plot_bg, UP, buff=0.1)
                        )
                        x.add(VGroup(plot_bg, plot, plot_title))
                    except: # because functions `not_quite_there`, `function squish_rate_func` are not working.
                        pass
        x.arrange_in_grid(cols=8)
        x.height = config.frame_height
        x.width = config.frame_width
        x.move_to(ORIGIN).scale(0.95)

        self.add(VGroup(Tex("Manim Rate Funtions").scale(1.25), x).arrange(DOWN, buff=0.75))
```
-->

![A list of Manim easing curves](03-rate-function-list.webp)
{.inverse-invert}

### Tasks

#### Graph algorithm
Create an animation of DFS (or some other neat graph algorithm).

{{< video "manim" "03-graph-algorithm" >}}

Note that the solution to this task might suffer from a bug in Manim's graph class implementation in the ordering of vertices and edges in {{< doc "manim" "AnimationGroup" "reference/manim.animation.composition.AnimationGroup.html" >}} (at least from what I can gather, I haven't been able to debug what exactly the issue is), which can be solved by manually setting a higher `z_index` for the graph's vertices.

```py
# quickfix for a bug in AnimationGroup's handling of z_index
for v in graph.vertices:
    graph.vertices[v].set_z_index(1)
```

{{< details "Author's Solution" "03-graph-algorithm.py" >}}{{< /details >}}

#### Fibonacci sequence
Create animation of the Fibonacci sequence (or some other similar sequence like [Pell](https://en.wikipedia.org/wiki/Pell_number)'s numbers or [Lucas](https://en.wikipedia.org/wiki/Lucas_number)' numbers).

{{< video "manim" "03-fibonacci-sequence" >}}

Updaters from the previous part will be very handy.
Additionally, the {{< doc "manim" "TracedPath" "reference/manim.animation.changing.TracedPath.html" >}} class can be used to create the path traced by the dot traveling around the spiral.
The animation of the dot travel can be implemented via the {{< doc "manim" "Rotate" "reference/manim.animation.rotation.Rotate.html" >}} animation, which can be used to rotate one object around another.

```python {file="03-trace-path-example.py"}
```

{{< video "manim" "03-trace-path-example" >}}

There is, however, a slight catch: using {{< doc "manim" "TracedPath" "reference/manim.animation.changing.TracedPath.html" >}} runs into a [well-known Manim bug](https://github.com/ManimCommunity/manim/issues/550) with caching -- that's why we need to use the `--disable_caching` flag which fixes this bug by not caching the animations.

{{< details "Author's Solution" "03-fibonacci-sequence.py" >}}{{< /details >}}

#### Langton's ant
Create an animation of [Langton's ant](https://en.wikipedia.org/wiki/Langton%27s_ant) (or one of it's color variants).

{{< video "manim" "03-langton-ant" >}}

In each step, the ant moves in the following manner:
- if it's on a black space, turns right; else turns left
- inverts the color of the space it's standing on
- moves forward

To create the ant object, you can use the {{< doc "manim" "SVGMobject" "reference/manim.mobject.svg.svg_mobject.SVGMobject.html" >}} class to render an SVG image ([this one](03-ant.svg), for example, which the author's solution uses).

```python {file="03-svg-example.py"}
```

{{< video "manim" "03-svg-example" >}}

There is one trap in this task, which is using updaters on the ant to track it while moving.
This won't move due to how a center of an object is calculated -- by default, it is simply the center of the bounding rectangle of the object, which fails for shapes like the ant.

{{< video "manim" "03-get-center-example" >}}

{{< details "Author's Solution" "03-langton-ant.py" >}}{{< /details >}}
