---
date: '2023-07-12'
categoryPart: 6
title: OpenGL and Interactivity
description: Experimental OpenGL backend for faster GPU-based rendering in Manim Community.
toc: true
---

In this addition to my Manim series, we'll cover the (at the moment rather experimental) OpenGL backend for faster GPU-based rendering.

It is **heavily** based on [aquabeam's article](https://www.aquabeam.me/manim/opengl_guide/) and [Benjamin Hackl's video](https://www.youtube.com/watch?v=KeXBLPC1tns) (criminally underrated YouTube channel, by the way) about ManimCommunity's OpenGL support, so feel free to refer to them if you'd like to learn more.

### Introduction
By default, Manim uses **Cairo** for all of its rendering, which mostly utilizes the CPU.
This is usually fine, but quickly falls apart for more complex animations (especially the 3D ones) where it can take minutes or even _hours_ to render a single animation.

To greatly speed things up, we can switch the backend to **OpenGL**, which uses the GPU and thus greatly improves the rendering times, to the point that it is now possible to use the scene interactively!

To start things off, let's slightly edit one of the first scenes in the series:

```python {file="06-intro-example.py"}
```

Saving the scene to a file, we can use
```text
manim <file_name> -p --renderer=opengl
```
to render and preview the file with the OpenGL backend.

After running the command, there are a few things we can notice:
- the scene is being displayed **immediately**, not after it's rendered in its entirety
- the animation **doesn't exit** but instead stops after the last animation
- the terminal opens an [IPython](https://ipython.org/) prompt which we can use to further animate the scene

This does exactly what you think -- we now have an interactive command prompt available which we can use to further animate and interact with the scene (try mouse drag!).

Let's now issue some commands -- we can run the following command in the prompt

```py
self.play(Write(Text("This is awesome!")))
```

to write some text and

```py
self.play(square.animate.set_color(BLUE), circle.animate.set_color(RED))
```

to swap the colors of the background objects. Pretty awesome, right?

{{< video "manim" "06-intro-example" >}}

We can of course use `self.interactive_embed()` as many times as we like -- to exit the current interactive session and continue onto the next one, we can either type `exit`, or just `Ctrl+D`.

To render to file, we can additionally pass the `--write_to_movie` flag, which will render to file **but disable interactivity**, so if you want to record the interactive animations, I'd suggest to record the window/screen using software like [OBS](https://obsproject.com/).

### Mouse and Keyboard
Now this in and of itself is incredible (at least for a long-time user of Manim like me), but we can take this to a whole another level by introducing keyboard and mouse interactivity.

This comes in the form of `on_key_{press/release}` and `on_mouse_{press/motion/scroll/drag}` functions [[source code](https://github.com/ManimCommunity/manim/blob/main/manim/scene/scene.py)], which we can override in our scene and achieve further interactivity.

For example, let's create a simple scene that grows/shrinks an object based on key presses:

```python {file="06-keyboard-example.py"}
```

{{< video "manim" "06-keyboard-example" >}}

Once we get to interact with the scene, we can press `+` to grow the size of the circle on the screen and `-` to shrink it.
The interactive window uses [Pyglet](https://pyglet.org/), which is why we're importing the [`pyglet.window.key`](https://pyglet.readthedocs.io/en/latest/modules/window_key.html) constants.

We can do a similar thing for interactivity with the mouse:

```python {file="06-mouse-example.py"}
```

{{< video "manim" "06-mouse-example" >}}

### Camera
The OpenGL camera [[source code](https://github.com/ManimCommunity/manim/blob/main/manim/renderer/opengl_renderer.py)] offers quite a few functions that work really well in combination with interactivity and can be combined in a really nice way.

For example, one neat thing we can do is manually move camera into a number of positions and then smoothy interpolate among them using the following code:

```python {file="06-camera-example.py"}
```

{{< video "manim" "06-camera-example" >}}


### Mobject → OpenGLMobject

Since Cairo and OpenGL's Mobject implementations are incompatible, Manim uses [magic](https://www.aquabeam.me/manim/opengl_guide/#will-my-code-work-with-opengl) to make classes like `Square` and `Circle` usable. This means that if you wish to use the base classes like `Mobject`, `VMobject` and `Surface`, you'll have to use their OpenGL counterparts (`OpenGLVMobject` and `OpenGLSurface` respectively).

Since none of this is really documented, you'll have to look at the [source code](https://github.com/ManimCommunity/manim/tree/main/manim/mobject/opengl).

> Mobject is dead. Long live Mobject.


### More examples!
Here are some more examples of what you can do with OpenGL, mostly to inspire rather than document (since you'll have to do quite a bit of digging through the source code regardless).

_This section is ever-expanding and will contain more examples as I experiment with OpenGL!_

#### Pointcloud

```python {file="06-pointcloud-example.py"}
```

{{< video "manim" "06-pointcloud-example" >}}
