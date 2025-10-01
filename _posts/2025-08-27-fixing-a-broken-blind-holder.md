---
title: Fixing a Broken Blind Holder
excerpt: "How 3D reconstruction and 3D printing can fix broken things."
css: photos
bluesky_url: https://bsky.app/profile/tomas.slama.dev/post/3lxfbgjnk5k26
category_icon: /assets/category-icons/3d-print.webp
---

- .
{:toc}

A blind holder, as pictured on the image below, recently broke in our appartment.
Naturally, the only reasonable thing to do was to ~~go to Obi and buy a new one for 3 euros~~
- take ~80 images of the working one from various angles,
- use [`colmap`](https://colmap.github.io/) to reconstruct the 3D model,
- use [Blender](https://www.blender.org/) and [MeshLab](https://www.meshlab.net/) to clean it up, and
- use Prusa to 3D print an exact replica.

Suddenly, something that would take other people **minutes** and **very little money** to purchase and solve, took me only 2 hours on a Sunday, and all I needed was relatively expensive specialized equipment. 😎

<div class='photo-section'>
<figure>
    <div class="row">
        <div class="photos2-0">
            <img src="/assets/fixing-a-broken-blind-holder/working-and-broken.webp" alt="A working holder, and the broken one.">
        </div>
        <div class="photos2-1">
            <img src="/assets/fixing-a-broken-blind-holder/working-in-action.webp" alt="The working holder in action.">
        </div>
    </div>
    <figcaption>The working/broken holders (top left), and the working one in action (top right).</figcaption>
</figure>
<figure>
    <div class="row">
        <div class="photos1-0">
            <img src="/assets/fixing-a-broken-blind-holder/mosaic.webp" alt="A working holder, and the broken one.">
        </div>
    </div>
    <div class="row">
        <div class="photos2-0">
            <img src="/assets/fixing-a-broken-blind-holder/pointcloud.webp" alt="A working holder, and the broken one.">
        </div>
        <div class="photos2-1">
            <img src="/assets/fixing-a-broken-blind-holder/mesh.webp" alt="The working holder in action.">
        </div>
    </div>
    <figcaption>The dense pointcloud (left) and its corresponding 3D mesh (right), created from 76 images via <a href="https://colmap.github.io/" markdown="1">`colmap`</a> (top).</figcaption>
</figure>
</div>

Initially, I tried to print with PLA, but unfortunately it is too rigid to work well for situations like these.
Instead, I opted for TPU, which is significantly more elastic and thus more suitable for this use case; it is still a bit too elastic, but I don't own any other filament types, so this will have to do.

<div class='photo-section'>
<figure>
    <div class="row">
        <div class="photos2-0">
            <img src="/assets/fixing-a-broken-blind-holder/3d-print-pla.webp" alt="A working holder, and the broken one.">
        </div>
        <div class="photos2-1">
            <img src="/assets/fixing-a-broken-blind-holder/3d-print-tpu.webp" alt="The working holder in action.">
        </div>
    </div>
    <figcaption>The first print attempt with PLA (left), and the second with TPU (right).</figcaption>
</figure>
</div>

While the model itself could be cleaner (the Meshlab/Blender post-processing was rather hasty), the important part is that the component functions as it should, and that this approach works really well if small things around the house break.

Stay tuned for the next post, where I 3D print a **blind holder holder,** which will hold up to **7 additional blind holders,** in case we decide to obtain more blinds. 🙃
