---
date: '2026-03-11'
title: "Hollow Knight Raspberry Pi 4 Case"
description: "Making a Hollow Knight (Silksong) Raspberry Pi 4 case."
categoryIcon: /assets/category-icons/hollow-knight.ico
---

I am a big fan of [Hollow Knight: Silksong](https://store.steampowered.com/app/1030300/Hollow_Knight_Silksong/). I've 100%ed the game and trying Steel Soul attempts when I have time (so not very much), and I think the design of the main characters leads itself to nice-looking art / posters.

Since I recently set up an OctoPrint server on a Raspberry Pi 4, I had an opportunity to print a case.
I found **[this awesome modular one by Malolo](https://www.thingiverse.com/thing:3723561)**, which contained OpenSCAD source files, making it extremely easy to modify them to cut an SVG of my choice.

{{< image_section caption="3D renders of Malolo's customizable case. [[Thingiverse](https://www.thingiverse.com/thing:3723561)]" >}}
{{< image_row "example-1.jpg | example-2.webp | example-3.jpg" >}}
{{< /image_section >}}

I came up with two designs: one for **Hollow Knight** ([shade](https://hollowknight.fandom.com/wiki/Shade?file=Char_shade.png)), and the other for **Hollow Knight: Silksong** ([faydown cloak](https://hollowknightsilksong.wiki.fextralife.com/Faydown+Cloak)), both etched into the top as seen on the images below:

{{< image_section caption="The two designs for the case (Hollow Knight on the left, Hollow Knight: Silksong on the right).<br>**Bottom** [STL](Case_Bottom.stl)/[OpenSCAD](Case_Bottom.scad) \(\cdot\) **Left Top** [STL](Case_Top_HK1.stl)/[OpenSCAD](Case_Top_HK1.scad)+[SVG](hk-1.svg) \(\cdot\) **Right Top** [STL](Case_Top_HK2.stl)/[OpenSCAD](Case_Top_HK2.scad)+[SVG](hk-2.svg)" >}}
{{< image_row "hk1.png | hk2.png" >}}
{{< /image_section >}}

Although there are other awesome and SVG-able images from both games, the issue is that we **can't nest holes** -- you might notice that the eyes in the first design (left) are connected to the rest of the case via 'tears', and the eyes in the other one are missing altogether.

Regardless of this limitation, I think they turned out pretty nice 🙂.
