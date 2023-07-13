---
title: Manim – OpenGL and Interactivity
category: "Manim"
category_icon: /assets/category-icons/manim.svg
css: manim
category_part: 6
redirect_from:
- /manim/6/
---

[Part 1](/manim/1/), [Part 2](/manim/2/), [Part 3](/manim/3/), [Part 4](/manim/4/), [Part 5](/manim/5/), **→ Part 6 ←**

- .
{:toc}

In this addition to my Manim series, we'll cover the (at the moment rather experimental) OpenGL backend for faster GPU-based rendering.

It is **heavily** based on [aquabeam's article](https://www.aquabeam.me/manim/opengl_guide/) and [Benjamin Hackl's video](https://www.youtube.com/watch?v=KeXBLPC1tns) (criminally underrated YouTube channel, by the way) about ManimCommunity's OpenGL support, so feel free to refer to them if you'd like to learn more.

### Introduction
By default, Manim uses **Cairo** for all of its rendering, which mostly utilizes the CPU.
This is usually fine, but quickly falls apart for more complex animations (especially the 3D ones) where it can take minutes or even _hours_ to render a single animation.

To greatly speed things up, we can switch the backend to **OpenGL**, which uses the GPU and thus greatly improves the rendering times, to the point that it is now possible to use the scene interactively!

To start things of, let's slightly edit one of the first scenes in the series:

```py
from manim import *
from manim.opengl import *


class IntroScene(Scene):
    def construct(self):
        square = Square(color=RED).shift(LEFT * 2)
        circle = Circle(color=BLUE).shift(RIGHT * 2)

        self.play(Write(square), Write(circle))

        # moving objects
        self.play(
            square.animate.shift(UP * 0.5),
            circle.animate.shift(DOWN * 0.5)
        )

        # rotating and filling the square (opacity 80%)
        # scaling and filling the circle (opacity 80%)
        self.play(
            square.animate.rotate(PI / 2).set_fill(RED, 0.8),
            circle.animate.scale(2).set_fill(BLUE, 0.8),
        )

        # this is new!
        self.interactive_embed()
```

Saving the scene to a file, we can use 
```
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

{% manim_video 6-Intro %}

We can of course use `self.interactive_embed()` as many times as we like -- to exit the current interactive session and continue onto the next one, we can either type `exit`, or just `Ctrl+D`.

To render to file, we can additionally pass the `--write_to_movie` flag, which will render to file **but disable interactivity**, so if you want to record the interactive animations, I'd suggest to record the window/screen using software like [OBS](https://obsproject.com/).

### Mouse and Keyboard
Now this in and of itself is incredible (at least for a long-time user of Manim like me), but we can take this to a whole another level by introducing keyboard and mouse interactivity.

This comes in the form of `on_key_{press/release}` and `on_mouse_{press/motion/scroll/drag}` functions [[source code](https://github.com/ManimCommunity/manim/blob/main/manim/scene/scene.py)], which we can override in our scene and achieve further interactivity.

For example, let's create a simple scene that grows/shrinks an object based on key presses:

```py
from manim import *
from manim.opengl import *

# Pyglet key constants
from pyglet.window import key


class KeyboardScene(Scene):
    def construct(self):
        # we're using self so it's available throughout the scene
        self.circle = Circle(color=BLUE)

        self.play(Write(self.circle))

        self.interactive_embed()

    def on_key_press(self, symbol, modifiers):
        """Called each time a key is pressed."""
        # grow the circle when plus is pressed
        if symbol == key.PLUS:
            self.play(self.circle.animate.scale(2))

        # shrink it when minus is pressed
        elif symbol == key.MINUS:
            self.play(self.circle.animate.scale(1 / 2))

        # so we can still use the default controls
        super().on_key_press(symbol, modifiers)
```

{% manim_video 6-Keyboard %}

Once we get to interact with the scene, we can press `+` to grow the size of the circle on the screen and `-` to shrink it.
The interactive window uses [Pyglet](https://pyglet.org/), which is why we're importing the [`pyglet.window.key`](https://pyglet.readthedocs.io/en/latest/modules/window_key.html) constants.

We can do a similar thing for interactivity with the mouse:

```py
from manim import *
from manim.opengl import *

from pyglet.window import key


class MouseScene(Scene):
    def construct(self):
        self.circle = Circle(color=BLUE)

        self.play(Write(self.circle))

        self.interactive_embed()

    def on_mouse_drag(self, point, d_point, buttons, modifiers):
        """Called each time the mouse is dragged (moves pressed across the windows)."""
        # resize the circle to where the mouse cursor currently is
        new_radius = np.linalg.norm(point)

        # no animations (the object is already in the scene), only changes!
        self.circle.become(
            Circle(
                color=BLUE,
                radius=new_radius,
                fill_opacity=0.5 * abs(np.sin(new_radius)),  # for some spark ;)
            )
        )

        # here we DON'T want to use the default controls since dragging moves the camera
```

{% manim_video 6-Mouse %}

### Camera
The OpenGL camera [[source code](https://github.com/ManimCommunity/manim/blob/main/manim/renderer/opengl_renderer.py)] offers quite a few functions that work really well in combination with interactivity and can be combined in a really nice way.

For example, one neat thing we can do is manually move camera into a number of positions and then smoothy interpolate among them using the following code:

```py
from manim import *
from manim.opengl import *

from pyglet.window import key


class CameraScene(Scene):
    def construct(self):
        square = Square(color=RED).shift(LEFT * 2)
        circle = Circle(color=BLUE).shift(RIGHT * 2)

        self.play(Write(square), Write(circle))

        # moving objects
        self.play(
            square.animate.shift(UP * 0.5),
            circle.animate.shift(DOWN * 0.5)
        )

        # rotating and filling the square (opacity 80%)
        # scaling and filling the circle (opacity 80%)
        self.play(
            square.animate.rotate(PI / 2).set_fill(RED, 0.8),
            circle.animate.scale(2).set_fill(BLUE, 0.8),
        )

        self.camera_states = []

        self.interactive_embed()


    def on_key_press(self, symbol, modifiers):
        # + adds a new camera position to interpolate
        if symbol == key.PLUS:
            print("New position added!")
            self.camera_states.append(
                (
                    self.camera.get_position(),
                    np.array(self.camera.euler_angles),
                )
            )

        # P plays the animations, one by one
        elif symbol == key.P:
            print("Replaying!")
            for pos, ang in self.camera_states:
                self.play(
                    self.camera.animate.set_position(pos) \
                                       .set_euler_angles(*ang)
                )

        super().on_key_press(symbol, modifiers)

```

{% manim_video 6-Camera %}


### Mobject → OpenGLMobject

Since Cairo and OpenGL's Mobject implementations are incompatible, Manim uses [magic](https://www.aquabeam.me/manim/opengl_guide/#will-my-code-work-with-opengl) to make classes like `Square` and `Circle` usable. This means that if you wish to use the base classes like `Mobject`, `VMobject` and `Surface`, you'll have to use their OpenGL counterparts (`OpenGLVMobject` and `OpenGLSurface` respectively).

Since none of this is really documented, you'll have to look at the [source code](https://github.com/ManimCommunity/manim/tree/main/manim/mobject/opengl).

> Mobject is dead. Long live Mobject.


### More examples!
Here are some more examples of what you can do with OpenGL, mostly to inspire rather then document (since you'll have to do quite a bit of digging through the source code regardless).

_This section is ever-expanding and will contain more examples as I experiment with OpenGL!_

```py
from manim import *
from manim.opengl import *


class BunnyScene(Scene):
    def construct(self):
        pointcloud = OpenGLPMobject()

        # one side of the Stanford bunny
        # https://slama.dev/assets/manim/bunny.txt
        points = []
        with open("bunny.txt") as f:
            for line in f.read().splitlines():
                points.append(list(map(float, line.split())))

        pointcloud.add_points(points)

        # scale + color
        pointcloud.scale(20)
        pointcloud.set_color_by_gradient((RED, GREEN, BLUE))

        self.play(Create(pointcloud))

        self.interactive_embed()
```

{% manim_video 6-PointCloud %}
