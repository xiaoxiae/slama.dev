---
date: '2024-10-13'
categoryPart: 2
title: Groups, Animations, Signals, Effects
end: <a href="/motion-canvas/1/">Part 1</a>, <strong>→ Part 2 ←</strong>, <a href="/motion-canvas/3/">Part
  3</a>
description: Groups of objects, animation flow, signals (Manim updaters on crack),
  effects.
toc: true
---

In this part of the series, we'll explore some more **layout-related animations**, explore the **animation flow** and discover **signals + effects**.

We'll also play around with colors a bit 🙂.

### Grouping objects

Motion Canvas doesn't fully support the same grouping as Manim (i.e. change the color of all objects in this particular group).
Instead, we should always be working with the [**scene hierarchy**](https://motioncanvas.io/docs/hierarchy) and layout objects, which do supports certain operations, mostly related to their position, scale/size and rotation.

In this example, we're also using the fact that Motion Canvas supports any `X11` colors names -- feel free to [browse through them](https://x11.linci.co/) and pick the ones that you like!

{{< code_toggle "vgroup.tsx" "02-vgroup-example.py" >}}

{{< video "motion-canvas" "02-vgroup" >}}

Arranging objects in Manim is usually done via the {{< doc "manim" "arrange" "reference/manim.mobject.mobject.Mobject.html#manim.mobject.mobject.Mobject.arrange" >}} function.
In Motion Canvas, we again utilize the almighty flexbox... well, kind of -- animating certain flexbox properties is [still not supported](https://github.com/motion-canvas/motion-canvas/issues/363) (but will likely be in the future):

{{< code_toggle "arrange.tsx" "02-arrange-example.py" >}}

{{< video "motion-canvas" "02-arrange" >}}

For grids, Manim's {{< doc "manim" "arrange_in_grid" "reference/manim.mobject.mobject.Mobject.html#manim.mobject.mobject.Mobject.arrange_in_grid" >}} is just a special case of Motion Canvas' flexbox shenanigans.
The only difference here is that we're newly using the `wrap` property, since the circles would otherwise be squished and not wrapped to form a grid.

To make the animation a bit more interesting, we can utilize the [**`chroma.js`**](https://gka.github.io/chroma.js/) (which Motion Canvas internally uses to work with colors) to assign colors using a color scale.

```tsx {file="arrange-in-grid.tsx"}
```

{{< video "motion-canvas" "02-arrange-in-grid" >}}

### Add, remove and ordering

The order in which the objects are rendered are based on the [scene hierarchy](https://motioncanvas.io/docs/hierarchy#modifying-the-hierarchy) -- the higher they are, the sooner they are rendered (i.e. the more _at the bottom_ they are).
However, if they differ in their z-index, the one with a higher z-index will always be drawn on top of the other:

```tsx {file="add-remove.tsx"}
```

{{< video "motion-canvas" "02-add-remove" >}}

### Animation flow

We've already seen a few of these in the [previous post](/motion-canvas/1/), but we can use different functions for working with [animation flow](https://motioncanvas.io/docs/flow).
The main difference between Manim and one of the main features of Motion Canvas is that the animation model inherently allows for a lot of concurrency, since you can have multiple threads concurrently changing different properties, even of the same object:

```tsx {file="animation-flow.tsx"}
```

{{< video "motion-canvas" "02-animation-flow" >}}

<!--
### Transformations
Unfortunately, Motion Canvas can't do this.

There is no magic {{< doc "manim" "Transform" "reference/manim.animation.transform.Transform.html" >}} function that changes one object into another one.

Objects have a way of changing into different objects of the same type by continuously changing their parameters (i.e. text, curves, etc...), and those that don't can be transformed via fading, which usually looks pretty okay.

Sorry 🤷.
-->


### Signals
**[Signals](https://motioncanvas.io/docs/signals)** are Manim's updaters on crack.

Instead of object's characteristics being static values, they are usually **signals,** which are (as the documentation describes) values that can change over time and define dependencies between objects.

This means that, as opposed to Manim's updater we **don't need to explicitly say** that an object's attribute should be set to this value at every frame -- we say that **it is that value:**

```tsx {file="simple-signal.tsx"}
```

{{< video "motion-canvas" "02-simple-signal" >}}

Note that we don't necessarily need to only assign one signal to another -- we can assign a function that takes the value of the signal and modifies it how we want, for example taking the position of an object and converting it to a text to display it:


```tsx {file="become-signal.tsx"}
```

{{< video "motion-canvas" "02-become-signal" >}}

A crucial detail is that signals are **lazy** -- assuming that the value of a signal is some complicated function that relies on other signals, it is **only calculated when the value is requested**, making it a perfect fit for creating dependencies between properties, but not so much for e.g. a simulation function that needs to change things each frame.

For that, we have **effects...**

### Effects

**[Effects](https://motioncanvas.io/docs/effects)** are functions that are run on their dependency changes, but unlike signals are **no longer lazy.** _This means that all of their dependencies are no longer lazy as well,_ so if you have many things going on at the same time, things might run a bit slow...

Effects come in two flavors; _directly quoting the documentation_:

- {{< doc "motion-canvas" "createEffect()" "core/signals#createEffect" >}} runs immediately after any of its dependencies changes.
- {{< doc "motion-canvas" "createDeferredEffect" "core/signals#createDeferredEffect" >}} runs at the end of each frame if any of its dependencies changed

For example, we could use it to create a simple particle simulation like this one:
```tsx {file="effect.tsx"}
```

{{< video "motion-canvas" "02-effect" >}}

### Tasks

#### Shuffle

{{< video "motion-canvas" "02-task-shuffle" >}}

Before trying to animate this, here are a few useful things:

1. to move a circle along a nice path, you can define a **spline** between two points and then move along it using the {{< doc "motion-canvas" "getPointAtPercentage" "2d/components/Curve#getPointAtPercentage" >}} function (see the [documentation page for splines](https://motioncanvas.io/docs/spline))
2. to animate a value from `0` to `1` that we can use for the percentage value, we can create and animate a new signal (more about what that is in the [next Motion Canvas post](/motion-canvas/2/))
3. the {{< doc "motion-canvas" "easeInOutExpo" "core/tweening#easeInOutExpo" >}} easing curve is nicer for shuffing since it's more sudden than the default

All of the above can be summarized in the following animation:

```tsx {file="shuffle-helper.tsx"}
```

{{< video "motion-canvas" "02-shuffle-helper" >}}

{{< code_toggle_details "task-shuffle.tsx" "01-shuffle.py" >}}

#### Triangle

{{< video "motion-canvas" "02-task-triangle" >}}

Unlike Manim's {{< doc "manim" "Circle.from_three_points" "reference/manim.mobject.geometry.arc.Circle.html#manim.mobject.geometry.arc.Circle.from_three_points" >}}, Motion Canvas doesn't have a utility function for doing this.
Instead, the following functions (along with a {{< doc "motion-canvas" "createDeferredEffect" "core/signals#createDeferredEffect" >}}) could be useful:

```typescript
/**
 * Cross product of two 3D points.
 */
function cross(a: [number, number, number], b: [number, number, number]): [number, number, number] {
    return [
        a[1] * b[2] - a[2] * b[1],
        a[2] * b[0] - a[0] * b[2],
        a[0] * b[1] - a[1] * b[0]
    ];
}

/**
 * Calculate intersection coordinates of two lines.
 */
function lineIntersection(p1: Vector2, p2: Vector2, p3: Vector2, p4: Vector2): Vector2 {
    const pad = (point: Vector2): [number, number, number] => [point.x, point.y, 1];

    const line1Padded = [pad(p1), pad(p2)];
    const line2Padded = [pad(p3), pad(p4)];

    const line1Cross = cross(line1Padded[0], line1Padded[1]);
    const line2Cross = cross(line2Padded[0], line2Padded[1]);

    const intersection = cross(line1Cross, line2Cross);
    const [x, y, z] = intersection;

    // Return the intersection point in the xy-plane
    return new Vector2(x / z, y / z);
}

/**
 * Calculate the bisector of a given line segment.
 */
function perpendicularBisector(p1: Vector2, p2: Vector2): [Vector2, Vector2] {
    const diff = p1.sub(p2);

    let direction = cross([diff.x, diff.y, 0], [0, 0, 1]);
    let directionVector = new Vector2(direction[0], direction[1]);

    const midpoint = p1.add(p2).div(2);

    return [midpoint.add(directionVector), midpoint.sub(directionVector)];
}
```

{{< code_toggle_details "task-triangle.tsx" "02-triangle.py" >}}

#### Wave

{{< video "motion-canvas" "02-task-wave" >}}

Noting extra here, just a BFS.

Here is the text input that I used to generate the maze, if you wish to use it.

```text
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
# ###############   ######      #####f                #
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
```

{{< code_toggle_details "task-wave.tsx" "02-wave.py" >}}

#### Hilbert

{{< video "motion-canvas" "02-task-hilbert" >}}

Here are some useful things:

- the {{< doc "motion-canvas" "clone" "2d/components/Node/#clone" >}} function will be very useful here to create copies of an object
- use the {{< doc "motion-canvas" "topLeft" "2d/components/Layout/#topLeft" >}}, {{< doc "motion-canvas" "topRight" "2d/components/Layout/#topRight" >}}, {{< doc "motion-canvas" "bottomLeft" "2d/components/Layout/#bottomLeft" >}} and {{< doc "motion-canvas" "bottomRight" "2d/components/Layout/#bottomRight" >}} cardinal directions for alignment
- you can [define the spline using `<Knot>`](https://motioncanvas.io/docs/spline#using-knot-nodes), which allows you to access their {{< doc "motion-canvas" "absolutePosition" "2d/components/Layout/#absolutePosition" >}}, which will make the code a lot simpler easier (the clones will likely be scaled + rotated at this point, which doesn't change their relative {{< doc "motion-canvas" "position" "2d/components/Node#position" >}})
- setting the smoothness of a spline to `0` will make it line segments
- you can animate drawing of a spline with the {{< doc "motion-canvas" "end" "2d/components/Curve#end" >}} signal

{{< code_toggle_details "task-hilbert.tsx" "02-hilbert.py" >}}
