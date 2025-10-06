---
title: Introduction
category: "Manim"
category_icon: /assets/category-icons/manim.svg
css: manim
category_part: 1
redirect_from:
- /manim/1/
- /manim/
excerpt: An introduction to Manim, originally translated from a Czech CS-oriented correspondence seminar.
end: <strong>→ Part 1 ←</strong>, <a href="/manim/2/">Part 2</a>, <a href="/manim/3/">Part 3</a>, <a href="/manim/4/">Part 4</a>, <a href="/manim/5/">Part 5</a>, <a href="/manim/6/">Part 6</a>
---

_**15/10/2024 update:**_
- I got fed up with Manim and **[switched to Motion Canvas](/motion-canvas/introduction/)** and I think you should too 🙂

_**27/12/2023 update:**_
- fixed to be up-to-date with **Manim v0.18.0**
- the code snippets can be selected by **triple clicking on the code window**

---

_Over the course of this year (2021/2022), I created a well-received "Introduction to Manim" series for [KSP](https://ksp.mff.cuni.cz/) (Czech CS-oriented correspondence seminar), so it made sense to make it more accessible by translating it to English and publish it here._

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

Here is an example of a simple scene that creates a red {% manim_doc `Square` reference/manim.mobject.geometry.polygram.Square.html %} and then a blue {% manim_doc `Circle` reference/manim.mobject.geometry.arc.Circle.html %}.

```py
{% include manim/01-intro-example.py %}
```

To render the video, we will use the `manim <file_name> -pqm` command, where
- `-p` is the preview flag, telling Manim that we want to immediately view the result and
- `-qm` sets the quality to `m`edium (others being `l`ow, `h`igh and 4`k`),

yielding the following video:

{% manim_video 01-intro-example %}

The method {% manim_doc `self.play` reference/manim.scene.scene.Scene.html#manim.scene.scene.Scene.play %} always expects a **non-zero** number of animations that it plays at the same time.
We're calling it with the {% manim_doc `Write` reference/manim.animation.creation.Write.html %} and {% manim_doc `FadeOut` reference/manim.animation.fading.FadeOut.html %} animations above, which create and hide objects passed to them.
The optional parameter `run_time` sets the animation duration (in seconds), defaulting to \(1\) if nothing is passed.

There are also a number of builtin constants used (`LEFT`, `RIGHT`, `RED`, `BLUE`).
These are constants that Manim uses to make the code more readable.
For a more comprehensive list, here are the {% manim_doc colors reference/manim.utils.color.manim_colors.html %} and here are {% manim_doc other reference/manim.constants.html %} constants.

After both of the objects are created, the {% manim_doc `shift` reference/manim.mobject.mobject.Mobject.html#manim.mobject.mobject.Mobject.shift %} method is used to move them in the given direction, **also returning them**.
This is how the vast majority of functions on Manim objects are implemented, mainly to avoid having to use the following (valid but verbose) syntax:

```py
# this
square = Square(color=RED)
square.shift(LEFT * 2)

# is the same as this
square = Square(color=RED).shift(LEFT * 2)
```

Since the direction constants are [NumPy arrays](https://numpy.org/doc/stable/reference/generated/numpy.ndarray.html), they can be added and multiplied by constants with ease -- to move to the side and slightly up, we can simply do `obj.shift(LEFT + UP * 1.5)`.

### `animate` syntax
Besides creating and hiding objects, we'd like to animate their attributes like color, position and orientation.
The {% manim_doc `shift` reference/manim.mobject.mobject.Mobject.html#manim.mobject.mobject.Mobject.shift %} function does move the object, but it doesn't do so visually.

This can be done in a number of ways, arguably the most elegant being the {% manim_doc `animate` tutorials/quickstart.html#using-animate-syntax-to-animate-methods %} syntax, which can be used via the magic `animate` word after the object:

```py
{% include manim/01-animate-example.py %}
```

{% manim_video 01-animate-example %}

The example shows a number of properties that each object has (position, orientation, color) and that can be animated.
As you can see from the code, the animations can be chained to change a number of them at once -- just make sure that they are not conflicting (moving both up and down at the same time, for example).

### Aligning objects
We've seen that the {% manim_doc `shift` reference/manim.mobject.mobject.Mobject.html#manim.mobject.mobject.Mobject.shift %} function moves an object in the given direction.
Sometimes, however, it might be more convenient to move it in relation to other objects in the scene.

#### `next_to`
For moving one object next to another, we'll use the {% manim_doc `next_to` reference/manim.mobject.mobject.Mobject.html#manim.mobject.mobject.Mobject.next_to %} function:

```py
{% include manim/01-next-to-example.py %}
```

{% manim_video 01-next-to-example %}

#### `move_to`
For moving one object on top of another, we'll use the {% manim_doc `move_to` reference/manim.mobject.mobject.Mobject.html#manim.mobject.mobject.Mobject.move_to %} function:

```py
{% include manim/01-move-to-example.py %}
```

{% manim_video 01-move-to-example %}

#### `align_to`
For moving one object on the "same level" as another, we'll use the {% manim_doc `align_to` reference/manim.mobject.mobject.Mobject.html#manim.mobject.mobject.Mobject.align_to %} function:

```py
{% include manim/01-align-to-example.py %}
```

{% manim_video 01-align-to-example %}


### Typesetting text and math

Manim supports setting in \(\TeX\) (including math).
To do this, we'll be using the {% manim_doc `Tex` reference/manim.mobject.text.tex_mobject.Tex.html %} for setting text and {% manim_doc `MathTex` reference/manim.mobject.text.tex_mobject.MathTex.html %} for setting math.
If you're not familiar with setting math in \(\TeX\), you can use one of many online editors (such as [this one](https://latexeditor.lagrida.com/)).

```py
{% include manim/01-text-and-math-example.py %}
```

{% manim_video 01-text-and-math-example %}

An alternative to using the {% manim_doc `Tex` reference/manim.mobject.text.tex_mobject.Tex.html %} class is the {% manim_doc `Text` reference/manim.mobject.text.text_mobject.Text.html %} class, which internally doesn't use \(\TeX\) and thus renders a(n arguably) worse-looking text, but is easier to work with when dealing with non-english characters.

### Tasks

#### Shuffle

Create an animation of random shuffling.

{% manim_video 01-shuffle %}

The {% manim_doc `Swap` reference/manim.animation.transform.Swap.html %} animation may be used for swapping the position of two objects.
Its optional parameter `path_arc`, which determines the angle under which they are swapped, might also be useful.

```py
{% include manim/01-shuffle-example.py %}
```

{% manim_video 01-shuffle-example %}

{% manim_solution %}
{% include manim/01-shuffle.py %}
{% endmanim_solution %}

#### Sort

Create an animation of a sequence being sorted.

{% manim_video 01-sort %}

The {% manim_doc `stretch_to_fit_height` reference/manim.mobject.mobject.Mobject.html#manim.mobject.mobject.Mobject.stretch_to_fit_height %} function (combined with the `animate` syntax) may be useful for changing the height of the object, without scaling it proportionally.

```py
{% include manim/01-stretch-to-fit-height-example.py %}
```

{% manim_video 01-stretch-to-fit-height-example %}

{% manim_solution %}
{% include manim/01-sort.py %}
{% endmanim_solution %}

#### Search

Create an animation of binary searching a random sorted sequence.

{% manim_video 01-search %}

The {% manim_doc `Arrow` reference/manim.mobject.geometry.line.Arrow.html %} object is very useful for creating the position indicators.

```py
{% include manim/01-arrow-example.py %}
```

{% manim_video 01-arrow-example %}

{% manim_solution %}
{% include manim/01-search.py %}
{% endmanim_solution %}
