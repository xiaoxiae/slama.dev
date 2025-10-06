---
title: Groups, Transforms, Updaters
category: "Manim"
category_icon: /assets/category-icons/manim.svg
css: manim
category_part: 2
redirect_from:
- /manim/2/
excerpt: Functions and classes for working with groups of objects, object transforms and updaters.
end: <a href="/manim/1/">Part 1</a>, <strong>→ Part 2 ←</strong>, <a href="/manim/3/">Part 3</a>, <a href="/manim/4/">Part 4</a>, <a href="/manim/5/">Part 5</a>, <a href="/manim/6/">Part 6</a>
---

- .
{:toc}

In this part of the series, we'll learn a number of useful functions and classes when working with groups of objects.
We'll also learn how to transform objects into others, how updaters work and a few geometry-related things.

### Grouping objects
It is sometimes more useful to work with a group of objects as one, for example when moving them, scaling them, changing their color, etc.
This is where the {% manim_doc `VGroup` reference/manim.mobject.types.vectorized_mobject.VGroup.html %} class comes in.

```py
{% include manim/02-vgroup-example.py %}
```

{% manim_video 02-vgroup-example %}

The {% manim_doc `VGroup` reference/manim.mobject.types.vectorized_mobject.VGroup.html %} class additionally contains functions for arranging objects.
The simplest to use is the {% manim_doc `arrange` reference/manim.mobject.mobject.Mobject.html#manim.mobject.mobject.Mobject.arrange %} function which arranges object such that they are next to one another, in the order they were passed to the constructor (left to right).

```py
{% include manim/02-arrange-example.py %}
```

{% manim_video 02-arrange-example %}

The `buff` parameter determines the spacing between the objects and can be used in most of the functions that involve positioning objects next to one another, such as the {% manim_doc `next_to` reference/manim.mobject.mobject.Mobject.html#manim.mobject.mobject.Mobject.next_to %} function that we've seen already.
The `direction` parameter determines the direction in which the objects are arranged.

A more general version of the {% manim_doc `arrange` reference/manim.mobject.mobject.Mobject.html#manim.mobject.mobject.Mobject.arrange %} function is the {% manim_doc `arrange_in_grid` reference/manim.mobject.mobject.Mobject.html#manim.mobject.mobject.Mobject.arrange_in_grid %} function, which (as the name suggests) arranges the objects of the group in a grid. By default, it attempts to make the grid as square as possible.

```py
{% include manim/02-arrange-in-grid-example.py %}
```

{% manim_video 02-arrange-in-grid-example %}


### Adding and removing elements
To add objects to the scene instantly (without animating), we can use the {% manim_doc `bring_to_front` reference/manim.scene.scene.Scene.html#manim.scene.scene.Scene.bring_to_front %} (or alternatively {% manim_doc `add` reference/manim.scene.scene.Scene.html#manim.scene.scene.Scene.add %}, which is the same) and {% manim_doc `bring_to_back` reference/manim.scene.scene.Scene.html#manim.scene.scene.Scene.bring_to_back %}  functions.
To remove them, we can use the {% manim_doc `remove` reference/manim.scene.scene.Scene.html#manim.scene.scene.Scene.remove %} function.

```py
{% include manim/02-add-remove-example.py %}
```

{% manim_video 02-add-remove-example %}

We'll cover the scene functionality in-depth in one of the upcoming parts in the series.
For now, it's sufficient to know that the scene objects have a set order in which they are rendered, which is determined primarily by their `z_index` (something different than their \(z\) coordinate) and secondarily by the order they were added to the scene (newer objects on top, older on the bottom).

```py
{% include manim/02-z-index-example.py %}
```

{% manim_video 02-z-index-example %}

### Overlapping animations
We've seen how to start animations concurrently, but it is often prettier to run them with a certain overlap (especially when there is a lot of them), which makes them look smoother.
To achieve this, we'll use the {% manim_doc `AnimationGroup` reference/manim.animation.composition.AnimationGroup.html %} object with a `lag_ratio` parameter, which determines the part of a given animation when the next one is started.

```py
{% include manim/02-animation-group-example.py %}
```

{% manim_video 02-animation-group-example %}

Animation overlap also works for objects in a {% manim_doc `VGroup` reference/manim.mobject.types.vectorized_mobject.VGroup.html %} when applying animations that have non-zero `lag_ratio` (such as {% manim_doc `Write` reference/manim.animation.creation.Write.html %}), in which case it is applied in the order they were added to the group.

```py
{% include manim/02-vgroup-lag-ratio-example.py %}
```

{% manim_video 02-vgroup-lag-ratio-example %}

### Working with attention
When creating animations, it is sometimes necessary to draw attention to a certain part of the screen where the viewer's focus should be.
Manim offers a number of ways how to do this, the most common of which are {% manim_doc `Flash` reference/manim.animation.indication.Flash.html %}, {% manim_doc `Indicate` reference/manim.animation.indication.Indicate.html %}, {% manim_doc `Wiggle` reference/manim.animation.indication.Wiggle.html %}, {% manim_doc `FocusOn` reference/manim.animation.indication.FocusOn.html %} and {% manim_doc `Circumscribe` reference/manim.animation.indication.Circumscribe.html %}.

```py
{% include manim/02-attention-example.py %}
```

{% manim_video 02-attention-example %}

The {% manim_doc `Flash` reference/manim.animation.indication.Flash.html %}, {% manim_doc `Indicate` reference/manim.animation.indication.Indicate.html %} and {% manim_doc `Circumscribe` reference/manim.animation.indication.Circumscribe.html %} animations have a useful optional `color` parameter, which changes the default color from yellow to whatever you prefer.
Also, notice that we used an optional `shift` parameter for {% manim_doc `FadeIn` reference/manim.animation.fading.FadeIn.html#manim.animation.fading.FadeIn %} and {% manim_doc `FadeOut` reference/manim.animation.fading.FadeOut.html#manim.animation.fading.FadeOut %} which specify the direction in which the fade should occur.

### Transformations
Manim can animate the transformation of one object to another in a number of different ways.
The most commonly used is {% manim_doc `Transform` reference/manim.animation.transform.Transform.html %}, which smoothly transforms one object onto another.

```py
{% include manim/02-basic-transform-example.py %}
```

{% manim_video 02-basic-transform-example %}

It is, however, important to pay attention to which object we're working with when doing multiple transformations -- we still have to work with the original object or things will go wrong.

```py
{% include manim/02-bad-transform-example.py %}
```

{% manim_video 02-bad-transform-example %}

If this behavior feels unintuitive, it is possible to use {% manim_doc `ReplacementTransform` reference/manim.animation.transform.ReplacementTransform.html %}, which swaps the behavior above (good will be bad and vice versa).

Besides these transformations, it is also possible to use {% manim_doc `TransformMatchingShapes` reference/manim.animation.transform_matching_parts.TransformMatchingShapes.html %}, which attempts to transform the objects in a manner that preserves parts that they have in common.
Note that it has the same behavior as {% manim_doc `ReplacementTransform` reference/manim.animation.transform.ReplacementTransform.html %}!

```py
{% include manim/02-transform-matching-shapes-example.py %}
```

{% manim_video 02-transform-matching-shapes-example %}

### Updaters
Imagine that we would like to continually update an object during an animation (its position, scale, etc.).
This what Manim's updaters are for -- they are functions containing arbitrary code, connected to a certain object and evaluated each rendered frame.

```py
{% include manim/02-simple-updater-example.py %}
```

{% manim_video 02-simple-updater-example %}

Besides changing certain attributes of an object, it might be useful to transform it to an entirely new one.
We'll use the {% manim_doc `become` reference/manim.mobject.mobject.Mobject.html#manim.mobject.mobject.Mobject.become %} function, which transforms an object into another one **immediately** (not like {% manim_doc `Transform` reference/manim.animation.transform.Transform.html %}, which is an animation).

```py
{% include manim/02-become-updater-example.py %}
```

{% manim_video 02-become-updater-example %}

Besides the new {% manim_doc `become` reference/manim.mobject.mobject.Mobject.html#manim.mobject.mobject.Mobject.become %} function, the code also contains the {% manim_doc `get_center` reference/manim.mobject.mobject.Mobject.html#manim.mobject.mobject.Mobject.get_center %} function, which returns a [NumPy array](https://numpy.org/doc/stable/reference/generated/numpy.ndarray.html) with the \((x, y, z)\) coordinates of the object (in our case the circle).

### Tasks

#### Triangle

Create an animation of the following triangle.

{% manim_video 02-triangle %}

Dots and segments can be defined using the {% manim_doc `Dot` reference/manim.mobject.geometry.arc.Dot.html %} and {% manim_doc `Line` reference/manim.mobject.geometry.line.Line.html %} classes.

```py
{% include manim/02-line-example.py %}
```

{% manim_video 02-line-example %}

To create a circle given three of its points, the {% manim_doc `Circle.from_three_points` reference/manim.mobject.geometry.arc.Circle.html#manim.mobject.geometry.arc.Circle.from_three_points %} may be used.

```py
{% include manim/02-circle-from-points-example.py %}
```

{% manim_video 02-circle-from-points-example %}

{% manim_solution %}
{% include manim/02-triangle.py %}
{% endmanim_solution %}

#### Wave

Create an animation of a smooth wave running through a maze.

{% manim_video 02-wave %}

The {% manim_doc `arrange_in_grid` reference/manim.mobject.mobject.Mobject.html#manim.mobject.mobject.Mobject.arrange_in_grid %} will be useful to position the squares.
To overlap the coloring of each layer in the maze, nested {% manim_doc `AnimationGroup` reference/manim.animation.composition.AnimationGroup.html %} can be used.
For creating a smooth gradient from the input colors, the {% manim_doc `color_gradient` reference/manim.utils.color.html#manim.utils.color.color_gradient %} utility function is quite useful.

```py
{% include manim/02-color-gradient-example.py %}
```

{% manim_video 02-color-gradient-example %}

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
#######################################################
```

{% manim_solution %}
{% include manim/02-wave.py %}
{% endmanim_solution %}

#### Hilbert
Create an animation of the Hilbert's (or any other space-filling) curve.

{% manim_video 02-hilbert %}

You can use this custom `Path` function, which creates a path from the given points.

```py
{% include manim/02-path-example.py %}
```

{% manim_video 02-path-example %}

We're also using the {% manim_doc `flip` reference/manim.mobject.mobject.Mobject.html#manim.mobject.mobject.Mobject.flip %} function, which flips an object in the given axis (defaulting to flipping left-right), and the {% manim_doc `copy` reference/manim.mobject.mobject.Mobject.html#manim.mobject.mobject.Mobject.copy %} function, which copies an object.

Furthermore, the {% manim_doc `Create` reference/manim.animation.creation.Create.html %} animation is more appropriate than {% manim_doc `Write` reference/manim.animation.creation.Write.html %} since we're not interested in the outline of the curve we're drawing, only its shape.

```py
{% include manim/02-write-vs-create-example.py %}
```

{% manim_video 02-write-vs-create-example %}

{% manim_solution %}
{% include manim/02-hilbert.py %}
{% endmanim_solution %}
