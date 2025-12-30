---
date: '2024-10-04'
categoryPart: 1
title: From Manim to Motion Canvas
end: <strong>→ Part 1 ←</strong>, <a href="/motion-canvas/2/">Part 2</a>, <a href="/motion-canvas/3/">Part 3</a>
description: After a year-long break (master thesis + Manim burnout), I'm switching to Motion Canvas and documenting the transition for other Manim users through a series that recreates my original Manim tutorials.
toc: true
---

So... I haven't released a video in a while.
By a while, I mean **over a year** at this point.

The main reason for this is **my master thesis,** which takes essentially all of my free time.
The secondary reason is that I have severe MBS (Manim Burnout Syndrome) and therefore find it difficult to work on anything Manim-related.

The remedies to this are twofold: first off, I will be working with/joining the guys over at [**Polylog**](https://www.youtube.com/@PolylogCS) to produce the videos much faster than working alone, and will be learning (as the title of this post suggests) [**Motion Canvas**](https://motioncanvas.io/).

Since I have spent a significant amount of time in Manim (even writing a [series of Manim tutorials](/manim/introduction/) about how to use it), I think it's valuable to document the process of learning Motion Canvas as a former Manim user.

**If you are a Manim user, this series of articles is for you** -- it is a re-creation of [my Manim tutorial series](/manim/introduction/), written from a perspective of a long-time Manim user and focused on the differences between the two.

### Setting up
Follow the [quickstart](https://motioncanvas.io/docs/quickstart) page to setup your development environment.

Personally, I am using the [WebStorm](https://www.jetbrains.com/webstorm/) IDE on one monitor, with the Motion Canvas editor open on the other, allowing for instant preview of the animations that I'm currently working on (you should be writing this down, Manim; live animations!).

### First animations

After following the [quickstart](https://motioncanvas.io/docs/quickstart/) and generating the project boilerplate, we are ready to start writing animations.
I won't be explaining it since the [explanation section of quickstart](https://motioncanvas.io/docs/quickstart#explanation) does a great job at doing so -- let's write some animations!

_Whenever you see something like this, the Manim code will produce an animation that is not identical, but looks/feels/is-in-the-spirit of the Motion Canvas version. **The goal is to learn how Motion Canvas does it, not re-create Manim.**_

{{< code_toggle "intro.tsx" "01-intro-example.py" >}}

{{< video "motion-canvas" "01-intro" >}}

Instead of going through what each of the line of code does (again, the [explanation section](https://motioncanvas.io/docs/quickstart#explanation) does a great job at doing this), I'll make a few observations on how Motion Canvas differs from Manim.

`1)` we are animating **properties, not objects** -- for Manim, what we're conceptually doing is transforming an object from one state to another and things magically happen; for Motion Canvas, we are **animating individual properties.**

`2)` things are **always relative to the parent** -- when using Manim, properties of things like translation, rotation are absolute; for Motion Canvas, things are always relative to the object hierarchy.
_This will make more sense in later examples._

### No `animate` syntax!

To underline point `1)`, here is a more complex example of changing properties.
_Note that I've factored out the animation of an object appearance into the `appear` function, which I'll be using throughout the rest of the examples._

{{< code_toggle "animate.tsx" "01-animate-example.py" >}}

{{< video "motion-canvas" "01-animate" >}}

As you can see, each property is animated individually, as opposed to Manim's `animate` syntax, which performs all of the operations at the 'same time.'

Although this seems like a minor difference at first, creating animations like this one in Manim would be essentially impossible without some crazy updater shenanigans:

```tsx {file="animate-complex.tsx"}
```

{{< video "motion-canvas" "01-animate-complex" >}}


### Aligning objects
Aligning things in Motion Canvas is done with layouts, which are a powerful [flexbox](https://css-tricks.com/snippets/css/a-guide-to-flexbox/)-based approach to object positioning.
Nevertheless, I recreated Manim's {{< doc "manim" "next_to" "reference/manim.mobject.mobject.Mobject.html#manim.mobject.mobject.Mobject.next_to" >}}, {{< doc "manim" "move_to" "reference/manim.mobject.mobject.Mobject.html#manim.mobject.mobject.Mobject.move_to" >}} and {{< doc "manim" "align_to" "reference/manim.mobject.mobject.Mobject.html#manim.mobject.mobject.Mobject.align_to" >}} method examples, since they were the bread and butter of my Manim workflow.

The main things used are the {{< doc "motion-canvas" "left" "2d/components/Layout/#left" >}}, {{< doc "motion-canvas" "right" "2d/components/Layout/#right" >}}, {{< doc "motion-canvas" "top" "2d/components/Layout/#top" >}}, {{< doc "motion-canvas" "bottom" "2d/components/Layout/#bottom" >}} and {{< doc "motion-canvas" "middle" "2d/components/Layout#middle" >}} properties (referred to as the [**cardinal directions**](https://motioncanvas.io/docs/layouts#cardinal-directions)) that can be used to refer to parts of an object.

#### `next_to`

{{< code_toggle "next-to.tsx" "01-next-to-example.py" >}}

{{< video "motion-canvas" "01-next-to" >}}

#### `move_to`

{{< code_toggle "move-to.tsx" "01-move-to-example.py" >}}

{{< video "motion-canvas" "01-move-to" >}}

#### `align_to`

{{< code_toggle "align-to.tsx" "01-align-to-example.py" >}}

{{< video "motion-canvas" "01-align-to" >}}

Not pretty...

This is partly because these things are not wrapped in utility functions (unlike Manim), so you have to write them manually.
Writing these functions is not difficult, but it's also usually not something you should be using -- [we have flexbox](https://motioncanvas.io/docs/layouts)!

### Flexbox!

```tsx {file="flexbox.tsx"}
```

{{< video "motion-canvas" "01-flexbox" >}}

The example above introduces two important concepts -- the **[scene hierarchy](https://motioncanvas.io/docs/hierarchy),** which controls the way the scene is structured, and the **[layout nodes](https://motioncanvas.io/docs/layouts/)**, which facilitate the flexbox arrangement; feel free to read through these documentation pages to understand more about them.

Equipped with layouts, we can rewrite one of the examples above.

While doing so, we run into important concept `2)` mentioned above: [**positioning**](https://motioncanvas.io/docs/positioning) -- unlike Manim, an object's position (and some other attributes) is **always relative to its parent**.
This means that when we add objects to a layout, they instantly snap to their positions, and removing them snaps them back to origin (unless we changed their position in the meantime).

To create our animation, we can rely on the {{< doc "motion-canvas" "save" "2d/components/Layout/#save" >}} and {{< doc "motion-canvas" "restore" "2d/components/Layout#restore" >}} functions, which can remember the absolute positions in the layout and then return to them once we disable the layout, in order to nicely animate the objects getting to their positions:

```tsx {file="move-to-flexbox.tsx"}
```

{{< video "motion-canvas" "01-move-to-flexbox" >}}


### Typesetting text and math

For typesetting \(\LaTeX\) and regular text, we can use the {{< doc "motion-canvas" "<Txt>" "2d/components/Txt" >}} and [`<Latex>`](https://motioncanvas.io/docs/latex) nodes.
We can also rejoice, since they support diffing between different contents, which was one of my largest Manim painpoints!

{{< code_toggle "text-and-math.tsx" "01-text-and-math-example.py" >}}

{{< video "motion-canvas" "01-text-and-math" >}}

### Tasks

#### Sort

{{< video "motion-canvas" "01-task-sort" >}}

Since [TypeScript doesn't provide a way to seed its random number generator](https://stackoverflow.com/questions/521295/seeding-the-random-number-generator-in-javascript), you can use Motion Canvas' [`useRandom`](https://motioncanvas.io/docs/random-values) to create a pseudo-random generator that will provide deterministic numbers each time an animation is played (see the [randomness documentation page](https://motioncanvas.io/docs/random-values) for more).

{{< code_toggle_details "task-sort.tsx" "01-sort.py" >}}

#### Search

{{< video "motion-canvas" "01-task-search" >}}

Again, a couple of things:
- an arrow can be created via a {{< doc "motion-canvas" "Line" "2d/components/Line" >}} object (having `startArrow` value)
- we can optionally use `arrows = createRefMap<Line>()` to access the arrows in a nicer way via `arrows.left`, `arrows.right`, etc (instead of having many variables); see the [references documentation page](https://motioncanvas.io/docs/references#createrefmap-function) for more

{{< code_toggle_details "task-search.tsx" "01-search.py" >}}
