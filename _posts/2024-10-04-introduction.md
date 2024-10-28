---
title: From Manim to Motion Canvas
category: "Motion Canvas"
category_icon: /assets/category-icons/motion-canvas.svg
category_part: 1
css: motioncanvas photos manim
redirect_from:
- /motion-canvas/
- /motion-canvas/1/
- /motion-canvas/from-manim-to-motion-canvas/
excerpt: "So... I haven't released a video in a while. By a while, I mean over a year at this point. The main reason for this is my master thesis, which takes essentially all of my free time. The secondary reason is that I have severe MBS (Manim Burnout Syndrome) and therefore find it difficult to work on anything Manim-related. The remedies to this are twofold: first off, I will be working with/joining the guys over at Polylog to produce the videos much faster than working alone, and will be learning (as the title of this post suggests) Motion Canvas."
end: <strong>→ Part 1 ←</strong>
---

- .
{:toc}

So... I haven't released a video in a while.
By a while, I mean **over a year** at this point.

The main reason for this is **[my master thesis](https://blog.climbuddy.com/),** which takes essentially all of my free time.
The secondary reason is that I have severe MBS (Manim Burnout Syndrome) and therefore find it difficult to work on anything Manim-related.

The remedies to this are twofold: first off, I will be working with/joining the guys over at [**Polylog**](https://www.youtube.com/@PolylogCS) to produce the videos much faster than working alone, and will be learning (as the title of this post suggests) [**Motion Canvas**](https://motioncanvas.io/).

Since I have spent a significant amount of time in Manim (even writing a [series of Manim tutorials](/manim/introduction/) about how to use it), I think it's valuable to document the process of learning Motion Canvas as a former Manim user.

**If you are a Manim user, this series of articles is for you** -- it is a re-creation of [my Manim tutorial series](/manim/introduction/), written from a perspective of a long-time Manim user and focused on the differences between the two.

<div class='photo-section'>
<figure>
    <div class="row">
        <div class="photos1-0">
            <img src="/assets/motion-canvas/friendship-ended.webp" alt="TODO">
        </div>
    </div>
</figure>
</div>

### Setting up
Follow the [quickstart](https://motioncanvas.io/docs/quickstart) page to setup your development environment.

Personally, I am using the [WebStorm](https://www.jetbrains.com/webstorm/) IDE on one monitor, with the Motion Canvas editor open on the other, allowing for instant preview of the animations that I'm currently working on (you should be writing this down, Manim; live animations!).

### First animations

After following the [quickstart](https://motioncanvas.io/docs/quickstart/) and generating the project boilerplate, we are ready to start writing animations.
I won't be explaining it since the [explanation section of quickstart](https://motioncanvas.io/docs/quickstart#explanation) does a great job at doing so -- let's write some animations!

_Whenever you see something like this, the Manim code will produce an animation that is not identical, but looks/feels/is-in-the-spirit of the Motion Canvas version. **The goal is to learn how Motion Canvas does it, not re-create Manim.**_

<div class="code-toggle">
<button class="bt" >Switch to Manim <i class="fa-brands fa-python"></i></button>
<button class="bt" style="display:none;">Switch to Motion Canvas <i class="fa-brands fa-js"></i></button>
<div class="lang-spacer"></div>
<div class="ct" markdown="1">
```typescript
{% include motion-canvas/01/intro.tsx %}
```
</div>
<div class="ct" style="display:none;" markdown="1">
```py
{% include manim/01-intro-example.py %}
```
</div>
</div>

{% motion_canvas_video 01-intro %}

Instead of going through what each of the line of code does (again, the [explanation section](https://motioncanvas.io/docs/quickstart#explanation) does a great job at doing this), I'll make a few observations on how Motion Canvas differs from Manim.

`1)` we are animating **properties, not objects** -- for Manim, what we're conceptually doing is transforming an object from one state to another and things magically happen; for Motion Canvas, we are **animating individual properties.**

`2)` things are **always relative to the parent** -- when using Manim, properties of things like translation, rotation are absolute; for Motion Canvas, things are always relative to the object hierarchy.
_This will make more sense in later examples._

### No `animate` syntax!

To underline point `1)`, here is a more complex example of changing properties.
_Note that I've factored out the animation of an object appearance into the `appear` function, which I'll be using throughout the rest of the examples._

<div class="code-toggle">
<button class="bt" >Switch to Manim <i class="fa-brands fa-python"></i></button>
<button class="bt" style="display:none;">Switch to Motion Canvas <i class="fa-brands fa-js"></i></button>
<div class="lang-spacer"></div>
<div class="ct" markdown="1">
```typescript
{% include motion-canvas/01/animate.tsx %}
```
</div>
<div class="ct" style="display:none;" markdown="1">
```py
{% include manim/01-animate-example.py %}
```
</div>
</div>

{% motion_canvas_video 01-animate %}

As you can see, each property is animated individually, as opposed to Manim's `animate` syntax, which performs all of the operations at the 'same time.'

Although this seems like a minor difference at first, creating animations like this one in Manim would be essentially impossible without some crazy updater shenanigans:

```typescript
{% include motion-canvas/01/animate-complex.tsx %}
```

{% motion_canvas_video 01-animate-complex %}


### Aligning objects
Aligning things in Motion Canvas is done with layouts, which are a powerful [flexbox](https://css-tricks.com/snippets/css/a-guide-to-flexbox/)-based approach to object positioning.
Nevertheless, I recreated Manim's {% manim_doc `next_to` reference/manim.mobject.mobject.Mobject.html#manim.mobject.mobject.Mobject.next_to %}, {% manim_doc `move_to` reference/manim.mobject.mobject.Mobject.html#manim.mobject.mobject.Mobject.move_to %} and {% manim_doc `align_to` reference/manim.mobject.mobject.Mobject.html#manim.mobject.mobject.Mobject.align_to %} method examples, since they were the bread and butter of my Manim workflow.

The main things used are the [`left`](https://motioncanvas.io/api/2d/components/Layout/#left), [`right`](https://motioncanvas.io/api/2d/components/Layout/#right), [`top`](https://motioncanvas.io/api/2d/components/Layout/#top), [`bottom`](https://motioncanvas.io/api/2d/components/Layout/#bottom) and [`middle`](https://motioncanvas.io/api/2d/components/Layout#middle) properties (referred to as the [**cardinal directions**](https://motioncanvas.io/docs/layouts#cardinal-directions)) that can be used to refer to parts of an object.

#### `next_to`

<div class="code-toggle">
<button class="bt" >Switch to Manim <i class="fa-brands fa-python"></i></button>
<button class="bt" style="display:none;">Switch to Motion Canvas <i class="fa-brands fa-js"></i></button>
<div class="lang-spacer"></div>
<div class="ct" markdown="1">
```typescript
{% include motion-canvas/01/next-to.tsx %}
```
</div>
<div class="ct" style="display:none;" markdown="1">
```py
{% include manim/01-next-to-example.py %}
```
</div>
</div>

{% motion_canvas_video 01-next-to %}

#### `move_to`

<div class="code-toggle">
<button class="bt" >Switch to Manim <i class="fa-brands fa-python"></i></button>
<button class="bt" style="display:none;">Switch to Motion Canvas <i class="fa-brands fa-js"></i></button>
<div class="lang-spacer"></div>
<div class="ct" markdown="1">
```typescript
{% include motion-canvas/01/move-to.tsx %}
```
</div>
<div class="ct" style="display:none;" markdown="1">
```py
{% include manim/01-move-to-example.py %}
```
</div>
</div>

{% motion_canvas_video 01-move-to %}

#### `align_to`

<div class="code-toggle">
<button class="bt" >Switch to Manim <i class="fa-brands fa-python"></i></button>
<button class="bt" style="display:none;">Switch to Motion Canvas <i class="fa-brands fa-js"></i></button>
<div class="lang-spacer"></div>
<div class="ct" markdown="1">
```typescript
{% include motion-canvas/01/align-to.tsx %}
```
</div>
<div class="ct" style="display:none;" markdown="1">
```py
{% include manim/01-align-to-example.py %}
```
</div>
</div>

{% motion_canvas_video 01-align-to %}

Not pretty...

This is partly because these things are not wrapped in utility functions (unlike Manim), so you have to write them manually.
Writing these functions is not difficult, but it's also usually not something you should be using -- [we have flexbox](https://motioncanvas.io/docs/layouts)!

### Flexbox!

```typescript
{% include motion-canvas/01/flexbox.tsx %}
```

{% motion_canvas_video 01-flexbox %}

The example above introduces two important concepts -- the **[scene hierarchy](https://motioncanvas.io/docs/hierarchy),** which controls the way the scene is structured, and the **[layout nodes](https://motioncanvas.io/docs/layouts/)**, which facilitate the flexbox arrangement; feel free to read through these documentation pages to understand more about them.

Equipped with layouts, we can rewrite one of the examples above.

While doing so, we run into important concept `2)` mentioned above: [**positioning**](https://motioncanvas.io/docs/positioning) -- unlike Manim, an object's position (and some other attributes) is **always relative to its parent**.
This means that when we add objects to a layout, they instantly snap to their positions, and removing them snaps them back to origin (unless we changed their position in the meantime).

To create our animation, we can rely on the [`save`](https://motioncanvas.io/api/2d/components/Layout/#save) and [`restore`](https://motioncanvas.io/api/2d/components/Layout#restore) functions, which can remember the absolute positions in the layout and then return to them once we disable the layout, in order to nicely animate the objects getting to their positions:

```typescript
{% include motion-canvas/01/move-to-flexbox.tsx %}
```

{% motion_canvas_video 01-move-to-flexbox %}


### Typesetting text and math

For typesetting \(\LaTeX\) and regular text, we can use the [`<Txt>`](https://motioncanvas.io/api/2d/components/Txt) and [`<Latex>`](https://motioncanvas.io/docs/latex) nodes.
We can also rejoice, since they support diffing between different contents, which was one of my largest Manim painpoints!

<div class="code-toggle">
<button class="bt" >Switch to Manim <i class="fa-brands fa-python"></i></button>
<button class="bt" style="display:none;">Switch to Motion Canvas <i class="fa-brands fa-js"></i></button>
<div class="lang-spacer"></div>
<div class="ct" markdown="1">
```typescript
{% raw %}import {Latex, makeScene2D, Txt} from '@motion-canvas/2d';
import {all, createRef} from '@motion-canvas/core';
import {appear} from "../../utilities";

export default makeScene2D(function* (view) {
    const text = createRef<Txt>();
    const math = createRef<Latex>();

    view.add(<>
        // text is empty for now since we're animating writing it
        <Txt ref={text} fill={"white"} x={-300}></Txt>

        // we're separating things to be diffed with {{...}}
        <Latex ref={math} fill={"white"} x={300} tex={"{{\\sum_{i = 0}}}{{^\\infty}} {{\\frac{1}{2^i}}} = {{2}}"}></Latex>
    </>)

    yield* all(
        text().text("Hello Motion Canvas!", 1),
        appear(math(), 1),
    );

    // can be diffed!
    yield* all(
        text().text("Hello everyone!", 1),
        math().tex("{{\\sum_{i = 0}}}{{^{42}}} {{\\frac{1}{2^i}}} = {{13}}", 1),
    );
});{% endraw %}
```
</div>
<div class="ct" style="display:none;" markdown="1">
```py
{% include manim/01-text-and-math-example.py %}
```
</div>
</div>

{% motion_canvas_video 01-text-and-math %}

### Tasks

#### Sort

{% motion_canvas_video 01-task-sort %}

Since [TypeScript doesn't provide a way to seed its random number generator](https://stackoverflow.com/questions/521295/seeding-the-random-number-generator-in-javascript), you can use Motion Canvas' [`useRandom`](https://motioncanvas.io/docs/random-values) to create a pseudo-random generator that will provide deterministic numbers each time an animation is played (see the [randomness documentation page](https://motioncanvas.io/docs/random-values) for more).

<div class="code-toggle">
<button class="bt" >Switch to Manim <i class="fa-brands fa-python"></i></button>
<button class="bt" style="display:none;">Switch to Motion Canvas <i class="fa-brands fa-js"></i></button>
<div class="lang-spacer"></div>
<div class="ct" markdown="1">
{% motion_canvas_solution %}
{% include motion-canvas/01/task-sort.tsx %}
{% endmotion_canvas_solution %}
</div>
<div class="ct" style="display:none;" markdown="1">
{% manim_solution %}
{% include manim/01-sort.py %}
{% endmanim_solution %}
</div>
</div>

#### Search

{% motion_canvas_video 01-task-search %}

Again, a couple of things:
- an arrow can be created via a [`Line`](https://motioncanvas.io/api/2d/components/Line) object (having `startArrow` value)
- we can optionally use `arrows = createRefMap<Line>()` to access the arrows in a nicer way via `arrows.left`, `arrows.right`, etc (instead of having many variables); see the [references documentation page](https://motioncanvas.io/docs/references#createrefmap-function) for more

<div class="code-toggle">
<button class="bt" >Switch to Manim <i class="fa-brands fa-python"></i></button>
<button class="bt" style="display:none;">Switch to Motion Canvas <i class="fa-brands fa-js"></i></button>
<div class="lang-spacer"></div>
<div class="ct" markdown="1">
{% motion_canvas_solution %}
{% include motion-canvas/01/task-search.tsx %}
{% endmotion_canvas_solution %}
</div>
<div class="ct" style="display:none;" markdown="1">
{% manim_solution %}
{% include manim/01-search.py %}
{% endmanim_solution %}
</div>
</div>

<script>
const toggleButtons = document.querySelectorAll('button');

toggleButtons.forEach(button => {
  button.addEventListener('click', function() {
    const parentSection = this.parentElement;

    let childDivs = parentSection.querySelectorAll('.ct');

    if (childDivs[0].style.display === 'none') {
      childDivs[0].style.display = 'block';
      childDivs[1].style.display = 'none';
    } else {
      childDivs[0].style.display = 'none';
      childDivs[1].style.display = 'block';
    }

    childDivs = parentSection.querySelectorAll('.bt');

    if (childDivs[0].style.display === 'none') {
      childDivs[0].style.display = 'block';
      childDivs[1].style.display = 'none';
    } else {
      childDivs[0].style.display = 'none';
      childDivs[1].style.display = 'block';
    }
  });
});
</script>
