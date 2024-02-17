---
title: A tale of 3D Printing
excerpt: "A story of doing some 3D printing and failing miserably."
css: photos
---

- .
{:toc}

I recently got back to hangboarding after eating several tons of potato salad during the Christmas holidays (spoiler alert: it's been rough).
Since I use liquid chalk for friction, I wanted to design and 3D print a holder for the chalk and also for the brush.
Easy, right?

And so the adventure begins.


### The Holder

I own a [Prusa i3 MK3S+](https://www.prusa3d.com/category/original-prusa-i3-mk3s/) (great product, great company) and know my way around [Fusion 360](https://www.autodesk.com/products/fusion-360/free-trial) (great product, [fuck the company](https://hackaday.com/2022/08/12/local-simulation-feature-to-be-removed-from-all-autodesk-fusion-360-versions/)), so designing something to hold my liquid chalk and a brush was pretty simple.
This is what I came up with:

<div class='photo-section'>
<figure>
    <div class="row">
        <div class="photos2-0">
            <a href="/assets/a-tale-of-3d-printing/holder.zip"><img src="/assets/a-tale-of-3d-printing/holder-render.webp" alt="Render of the Holder."></a>
        </div>
        <div class="photos2-1">
            <img src="/assets/a-tale-of-3d-printing/holder-photo.webp" alt="Photo of the Holder.">
        </div>
    </div>
    <figcaption>The Holder (left render, right image) <a href="/assets/a-tale-of-3d-printing/holder.zip">[.STL model]</a>.</figcaption>
</figure>
</div>

It is meant to be hooked around something (in my case the door frame) and carry a reasonably-sized brush and bottled liquid chalk.

Although I made the hook too thin on the first go, resulting in it snapping and me updating it to make it thicker, this was a pretty fun experience.
Since it only took about 30 minutes, I was motivated to continue with designing and printing more things.


### The Salt and Pepper

Since we were missing a stand for salt and pepper in our kitchen, this was the next logical target.
While not necessary, it would be a nice addition to our otherwise barren table.
Here it is:

<div class='photo-section'>
<figure>
    <div class="row">
        <div class="photos2-0">
            <a href="/assets/a-tale-of-3d-printing/salt-and-pepper.zip"><img src="/assets/a-tale-of-3d-printing/salt-and-pepper-render.webp" alt="Render of the Salt and Pepper."></a>
        </div>
        <div class="photos2-1">
            <img src="/assets/a-tale-of-3d-printing/salt-and-pepper-photo.webp" alt="Photo of the Salt and Pepper.">
        </div>
    </div>
    <figcaption>The Salt and Pepper (left render, right image) <a href="/assets/a-tale-of-3d-printing/salt-and-pepper.zip">[.STL model]</a>.</figcaption>
</figure>
</div>

There again isn't much to comment on here -- the design is pretty simple and works fine.
Designing the hex pattern was the only non-trivial part (but was still pretty easy) and could prove useful in the future.

The only bad thing is that the letters are facing away from the center of the table (i.e. from our point of view), which is only a minor issue and didn't warrant a reprint.

### The Box

Having basically no time today, <a class='secret' href='/assets/kacka.webp'>my girlfriend</a> suggested I print a small box to keep her jewelry in when she needs to remove it in her lab:

<div class='photo-section'>
<figure>
    <div class="row">
        <div class="photos2-0">
            <a href="/assets/a-tale-of-3d-printing/tank.zip"><img src="/assets/a-tale-of-3d-printing/tank-render.webp" alt="Render of the Bank."></a>
        </div>
        <div class="photos2-1">
            <img src="/assets/a-tale-of-3d-printing/tank-photo.webp" alt="Photo of the Box.">
        </div>
    </div>
    <figcaption>The Box (left render, right image) <a href="/assets/a-tale-of-3d-printing/tank.zip">[.STL model]</a>.</figcaption>
</figure>
</div>

Tank god it was simple.

<pre class="vanilla">
    .--._____,
 .-='=='==-, "
(O_o_o_o_o_O)
</pre>


### The Disaster

Since the last one was a really simple design, I wanted today to be a little more complicated and so I designed a mini replica of the [Kilter Board](https://settercloset.com/pages/the-kilter-board), dubbing it the Bilter Koard (creative, I know; they can't sue me, right?).

<div class='photo-section'>
<figure>
    <div class="row">
        <div class="photos1-0">
            <a href="/assets/a-tale-of-3d-printing/board.zip"><img src="/assets/a-tale-of-3d-printing/board-render.webp" alt="A render of the Bilter Koard."></a>
        </div>
    </div>
    <figcaption>The Bilter Koard™© render <a href="/assets/a-tale-of-3d-printing/board.zip">[.STL model]</a>.</figcaption>
</figure>
</div>

First, I printed the base, which holds the board in place.
The first print produced an extreme amount of fuzz, which I solved by reducing the temperature from 215°C down to 180°C:

<div class='photo-section'>
<figure>
    <div class="row">
        <div class="photos1-0">
            <img src="/assets/a-tale-of-3d-printing/stringing-photo.webp" alt="A photo of the stringing problem.">
        </div>
    </div>
    <figcaption>Stringing reduction for 180°C (left) from 215°C (right). </figcaption>
</figure>
</div>

And here is where the fuck-up happens.

Right after the print, I noticed that the bottom wasn't connected to the printing board... like at all.
Usually, there is a bit of pressure I have to exert to get it off, but this time it was entirely free.

Thinking it strange but blaming it on the reduced temperature, I repeated the step with for the top part and **w̸͇̱̑̃͜e̴̛̜n̸͍̳̐͊͑t̷̳̰̗͗ ̸̡̼̔̽t̸͖̭͖̽̄o̴͕̰͒ ̴̦̜̪͂̈́͝b̴̘̥̒̀͜ȅ̴̗́͛͜d̵̜̀̑̍**, waking up to this sight.


<div class='photo-section'>
<figure>
    <div class="row">
        <div class="photos3-0">
            <img src="/assets/a-tale-of-3d-printing/fucky-wucky-photo-5.webp" alt="A photo of a fucked-up extruder [1].">
        </div>
        <div class="photos3-1">
            <img src="/assets/a-tale-of-3d-printing/fucky-wucky-photo-1.webp" alt="A photo of a fucked-up extruder [2].">
        </div>
        <div class="photos3-2">
            <img src="/assets/a-tale-of-3d-printing/fucky-wucky-photo-2.webp" alt="A photo of a fucked-up extruder [3].">
        </div>
    </div>
    <div class="row">
        <div class="photos2-0">
            <img src="/assets/a-tale-of-3d-printing/fucky-wucky-photo-3.webp" alt="A photo of a fucked-up extruder [4].">
        </div>
        <div class="photos2-1">
            <img src="/assets/a-tale-of-3d-printing/fucky-wucky-photo-4.webp" alt="A photo of a fucked-up extruder [5].">
        </div>
    </div>
    <figcaption>ALL I​S LOST the pon̷y he comes he c̶̮omes he comes the ich​or permeates all MY FACE MY FACE ᵒh god no NO NOO̼O​O NΘ stop the an​*̶͑̾̾​̅ͫ͏̙̤g͇̫͛͆̾ͫ̑͆l͖͉̗̩̳̟̍ͫͥͨe̠̅s ͎a̧͈͖r̽̾̈́͒͑e n​ot rè̑ͧ̌aͨl̘̝̙̃ͤ͂̾̆ ZA̡͊͠͝LGΌ ISͮ̂҉̯͈͕̹̘̱ TO͇̹̺ͅƝ̴ȳ̳ TH̘Ë͖́̉ ͠P̯͍̭O̚​N̐Y̡ H̸̡̪̯ͨ͊̽̅̾̎Ȩ̬̩̾͛ͪ̈́̀́͘ ̶̧̨̱̹̭̯ͧ̾ͬC̷̙̲̝͖ͭ̏ͥͮ͟Oͮ͏̮̪̝͍M̲̖͊̒ͪͩͬ̚̚͜Ȇ̴̟̟͙̞ͩ͌͝S̨̥̫͎̭ͯ̿̔̀ͅ</figcaption>
</figure>
</div>

Sigh.

This is entirely my bad -- not making sure that the first layer sticks and going to bed instead is pretty irresponsible (although this has never happened to me for the first layer of this size).

To fix this self-induced fuck-up, I
1. I heated the nozzle again to 230°C and left it be for a while, eventually loosening the blob enough so I could get it off,
2. followed these two manuals [[1]](https://help.prusa3d.com/guide/2a-mk3s-extruder-disassembly_188397) [[2]](https://help.prusa3d.com/guide/2b-mk3s-extruder-disassembly_181561) to take the extruder apart, clean it up and put it back,
3. tried printing something, which resulted in filament leaking from the top of the heater block ([this video](https://www.youtube.com/watch?v=OzRAVkXjw3I) explains what happened quite well)
4. went back to step **2** but did it properly this time (_only once; no infinite loops here!_),

**It works now.** _\*Happy Tom noises\*._

### ~~The~~ We Are So Back (Bilter Koard)

Due to reasons, I happen to have a large dataset of 3D-scanned climbing holds.
This is nice, but just dragging them into the Prusa Slicer won't work due to them not being watertight.
To clean up the dataset, I used Python and the [`trimesh` library](https://trimesh.org/) to voxelize+smoothen+decimate the objects:

<details closed>
	<summary class="code-summary">The clean-up code (click to show).</summary>
	<div markdown="1">
```py
"""Must be run from the folder with the hold files!"""

import trimesh
import trimesh.voxel.creation
from pathlib import Path


RESOLUTION = 0.001
FACE_COUNT = 10_000


# Convert all object files in the current directory
for file in Path(".").iterdir():
    if file.suffix != ".obj":
        continue

    print(f"Voxelizing {file}...", end=" ", flush=True)

    # Voxelize
    mesh = trimesh.load(file)
    mesh = trimesh.voxel.creation.voxelize(mesh, RESOLUTION).fill().marching_cubes

    # Smoothen (we're not playing Minecraft)
    smoothened = trimesh.smoothing.filter_laplacian(mesh)

    # Decimate so it's of reasonable size
    decimated = smoothened.simplify_quadric_decimation(FACE_COUNT)

    trimesh.exchange.export.export_mesh(decimated, f"voxelized_{file.with_suffix('.stl').name}")
    print("done!", flush=True)
```
</div>
</details>

<div class='photo-section'>
<figure>
    <div class="row">
        <div class="photos1-0">
            <img src="/assets/a-tale-of-3d-printing/holds.webp" alt="Photo of the holds.">
        </div>
    </div>
    <figcaption>The Holds <a href="/assets/a-tale-of-3d-printing/holds.zip">[.STL models]</a>.</figcaption>
</figure>
</div>

The board design isn't anything too exciting -- it consists of the board the holds attach to, bottom part that holds the board in place and two stick on each that hold it at the desired angle (35°/45°/55°).

<div class='photo-section'>
<figure>
    <div class="row">
        <div class="photos2-0">
            <img src="/assets/a-tale-of-3d-printing/board-photo.webp" alt="A photo of the board, along with a sample route.">
        </div>
        <div class="photos2-1">
            <img src="/assets/a-tale-of-3d-printing/board-parts.webp" alt="A photo of the parts of the board, along with a sample route.">
        </div>
    </div>
    <figcaption>The Bilter Koard™© (left assembled, right disassembled) <a href="/assets/a-tale-of-3d-printing/board.zip">[.STL model]</a>.</figcaption>
</figure>
</div>

To attach the holds to the board, I made sure to bevel the holes so I can use M3.5 screws superglued to the holds.
I experimented with printing thin plastic sticks so the build would be plastic-only (no extra parts) but it didn't work super well.

<div class='photo-section'>
<figure>
    <div class="row">
        <div class="photos2-0">
            <img src="/assets/a-tale-of-3d-printing/screws-1.webp" alt="Photo of how the screws are done [1].">
        </div>
        <div class="photos2-1">
            <img src="/assets/a-tale-of-3d-printing/screws-2.webp" alt="Photo of how the screws are done [2].">
        </div>
    </div>
    <figcaption>How the screws are superglued to the holds (left) and connected to the board (right).</figcaption>
</figure>
</div>

I'm happy with how it turned out but what I would really like is to make the holds' first few layers semi-transparent, put individually addressable RPi-controlled LEDs behind it, add a servo or two and make a proper Kilter Board miniature.
That would, however, turn it from something made in ~4 hours to a summer project so maybe some other time.

### The Conclusion
Knowing basic CAD and owning a 3D printer is a truly potent combination.
It's very satisfying to be able to think of something cool and actually be able to design and create it.

It also comes with its own set of issues (if you're not being really careful) and it can be truly frustrating to spend 2 hours taking apart/putting back the extruder, only to have to do it all over again because you did something wrong at some point in the process.

My hope with writing this article is that you either don't know much CAD/3D printing and found it interesting, or you know it and found it funny (I'm much more motivated than skilled).
