---
date: '2024-10-28'
categoryPart: 3
title: Camera and Shaders
description: Camera controls, and a glimpse into the wonderful world of shaders.
toc: true
---

The following part of the series briefly covers **camera controls** and then delves into the wonderful world of **shaders** -- something that I had absolutely no experience with before Motion Canvas and am very sad that that's the case.

The [3rd part of the Manim series](/manim/camera-and-graphs/) that this series aims to follow had a section on graphs (the computer science ones), but since Motion Canvas doesn't have native support for those, I decided to replace them with shaders instead (which Manim doesn't have).

_Special thanks for my friend Jakub Pelc for helpful pointers to shader resources.
If you happen to speak Czech, his **[series about shaders](https://ksp.mff.cuni.cz/h/ulohy/33/zadani1.html#task-33-1-S)** from [KSP](https://ksp.mff.cuni.cz/) is a great read._

### Camera

Just like Manim, setting up a camera in Motion Canvas requires setting up the scene in a particular way.
Specifically, we need to use the {{< doc "motion-canvas" "Camera" "2d/components/Camera/" >}} node and make whatever we want to view using it its children.

#### Controlling

```tsx {file="moving-camera.tsx"}
```

{{< video "motion-canvas" "03-moving-camera" >}}

Additionally, just like any {{< doc "motion-canvas" "Node" "2d/components/Node" >}}, we can use signals to create more complicated animations, such as the following, which tracks a circle within a changing grid:

```tsx {file="moving-camera-follower.tsx"}
```

{{< video "motion-canvas" "03-moving-camera-follower" >}}

#### Multi-camera

For more complicated animations, we might be interested in using multiple cameras showing the same thing, e.g. for main/side camera setups.
To achieve this, we need to store everything we want to display in a single {{< doc "motion-canvas" "Node" "2d/components/Node" >}} that **has to be on the top level** of the scene hierarchy, which we will feed to {{< doc "motion-canvas" "Camera.Stage" "2d/components/Camera/#static-Stage" >}} components:

```tsx {file="multi-camera.tsx"}
```

{{< video "motion-canvas" "03-multi-camera" >}}

### Shaders

#### Basics

[Shaders](https://developer.mozilla.org/en-US/docs/Games/Techniques/3D_on_the_web/GLSL_Shaders#fragment_shaders) are (broadly speaking) tiny programs that are designed to run in a massively parallel way, and (in our case) have the following properties:
- run on **each pixel** of the canvas/object/node/whatever we're applying the shader to
- can only communicate by taking **inputs** and producing **outputs** (no cross-communication!)

For Motion Canvas, they are written in `glsl`, which is a C-like shader language.
If you aren't familiar with it, I'd suggest to [read the following short tutorial](https://learnopengl.com/Getting-started/Shaders), but you should be able to read through the examples here without issues since the language is very simple.

_Also, if you find the following examples interesting, make sure to read the incredible [**Book of Shaders**](https://thebookofshaders.com/examples/) -- an online book that dives deep into the world of pixel shaders, and is a must-read for anyone with eyes._

Getting back to Motion Canvas, here is a simple example that creates a gradient shine effect on a circle:

```glsl {file="shader.glsl"}
```

```tsx {file="shader.tsx"}
```

{{< video "motion-canvas" "03-shader" >}}

The code should be quite straightforward, but let's comment on a few things, mainly for those who are learning about shaders for the first time (just like me when writing this example).

First of, each Motion Canvas shader will receive a set of the following `in`puts:

```glsl
in vec2 screenUV;
in vec2 sourceUV;
in vec2 destinationUV;
```

and expect the following `out`put, representing the color of the pixel:
```glsl
out vec4 outColor;
```

#### Uniforms

Each shader also receives a set of values called `uniforms` (since their value stays the same for all shaders in a single render) of a number of useful things:

```glsl
uniform float time;
uniform float deltaTime;
uniform float framerate;
uniform int frame;
uniform vec2 resolution;
uniform sampler2D sourceTexture;
uniform sampler2D destinationTexture;
uniform mat4 sourceMatrix;
uniform mat4 destinationMatrix;
```

Fortunately, we are not limited to the default `uniform`s -- we can provide any we want from Motion Canvas.
Here is a more complex example that does exactly that to create a dynamic background effect by using uniforms to provide values of the object positions, opacities and scales:

```glsl {file="shader-advanced.glsl"}
```

```tsx {file="shader-advanced.tsx"}
```

{{< video "motion-canvas" "03-shader-advanced" >}}
