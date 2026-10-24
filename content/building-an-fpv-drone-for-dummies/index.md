---
date: '2026-10-25'
title: "Building an FPV Drone (for dummies)"
description: "What I wish I knew, but had to learn in the process of building a drone."
toc: true
hidden: true
---

Over the past few months, I have gotten quite a bit into [FPV drones](/drone).
Starting out with an [Air75 II](https://betafpv.com/products/air75-ii-brushless-whoop-quadcopter) (**Syl <i class='fa-solid fa-drone-syl' aria-hidden='true'></i>**), I spent endless afternoons learning to fly on the simulator ([The Zone](https://store.steampowered.com/app/3491280/) is the best one!), and then endless more flying the whoop outside.
However, it seems inevitable that, as an FPV pilot, you start yearning for something a bit faster and more powerful.

Hence my journey of building an FPV drone began.

My requirements were as follows: I wanted something that
- I **built myself**, since I'll break it anyway at some point and I want to know how to fix it, 
- weighs **under 250 grams** (because of [EU regulations](https://www.easa.europa.eu/en/domains/drones-air-mobility/operating-drone/open-category-low-risk-civil-drones)), and
- can fly comfortably with an **action camera** mounted on top (my trusty [Osmo Nano](https://www.dji.com/osmo-nano)).

The goal of this article is to document the entire process, from shopping to flying, since it might be useful to people who are in the same position as I was, and to highlight **things that I did not know but should have**.

## Selecting Parts

Generally speaking, a drone consists of the following parts:

- <i class='fa-solid fa-part-frame' aria-hidden='true'></i> **frame** -- what holds the components of the drone together,
- <i class='fa-solid fa-part-stack' aria-hidden='true'></i> **stack** -- the FC (flight controller) and ESC (electronic speed controller),
- <i class='fa-solid fa-part-motor' aria-hidden='true'></i> **motors** and their <i class='fa-solid fa-part-propeller' aria-hidden='true'></i> **propellers**,
- radio <i class='fa-solid fa-part-receiver' aria-hidden='true'></i> **receiver** so the drone listens to your controller,
- <i class='fa-solid fa-part-camera' aria-hidden='true'></i> **camera** + <i class='fa-solid fa-part-vtx' aria-hidden='true'></i> **video transmitter** so you see what's happening, and
- <i class='fa-solid fa-part-battery' aria-hidden='true'></i> **batteries** so all of the things above have the ~~nutrients~~ electrons they need.

Selecting parts can be quite overwhelming (where do you even begin?), so it is best to start with parts that are constrained by your requirements, since the others can then be more easily selected.
This was my list of parts, and my reasons for picking them, with footnotes going more in depth on some of these since I wanted to keep the table clear and concise.

| Part | Model | Price | Why |
| :-- | :-- | --: | :-- |
| <i class='fa-solid fa-part-camera' aria-hidden='true'></i> Camera + <i class='fa-solid fa-part-vtx' aria-hidden='true'></i> VTX | **[Nano 90 V2](https://n-factory.de/HDZero-Nano-90-V2-Cam-162-720p-60-90-FPS)** + **[HDZero Race V3](https://n-factory.de/HDZero-Race-V3-VTX-en)** | €149.90 | I wanted to use the [HDZero](https://www.hd-zero.com/) protocol, since I've got the [BoxPro goggles](https://www.hd-zero.com/product-page/hdzero-boxpro-boxpro), and I think the company is cool. |
| <i class='fa-solid fa-part-frame' aria-hidden='true'></i> Frame | **[DeepSpace Seeker 3 DC (3")](https://n-factory.de/DeepSpace-Seeker-3-DC-3-inch-Freestyle-Frame-Kit)** | €46.90 | Since I wanted sub-250 grams, we're in the 3" territory. This was a frame that was decently priced, light, and had a separate 20x20mm mount at the back for the video stack. |
| <i class='fa-solid fa-part-propeller' aria-hidden='true'></i> Propellers | \(5\times\) **[HQ Durable T3x3x3](https://www.fpv24.com/en/hqprop/hq-durable-prop-3030-dreiblatt-t3x3x3-schwarz-4-stueck-pc-fpv-propeller)** | €14.45 | Matches the frame (3"). |
| <i class='fa-solid fa-part-motor' aria-hidden='true'></i> Motors | \(6\times\) **[T-Motor F1404 4600KV](https://n-factory.de/T-Motor-F1404-4600KV-Ultra-Light-Motor)** | €113.40 |  They match the frame (9x9 mm), the propellers (3"), and should have a sufficient thrust-to-weight ratio for the drone to fly well[^motor]. |
| <i class='fa-solid fa-part-battery' aria-hidden='true'></i> Battery | \(4\times\) **[CNHL MiniStar 650 mAh 4S 70C XT30U](https://www.fpv24.com/en/cnhl/cnhl-ministar-lipo-akku-650mah-148v-4s-70c-xt30u)** | €50.00 | Induced by the KV of the motor; 4S is the standard cell count for 3" builds, and this one was not too heavy and not too expensive. |
| <i class='fa-solid fa-part-stack' aria-hidden='true'></i> FC + ESC | **[OddityRC F405 Mini AM32 40A](https://www.fpv24.com/en/oddityrc/oddityrc-f405-mini-am32-40a-stack)** | €52.90 | Decently small + cheap stack. Needed to fit the 20x20 mm mount of the Seeker frame and have a 9V output for the camera setup. Handles the motors fine (rated for 40A per motor, ours do 20A max). Costlier ones add features that I don't really need, so I went for this one[^stack]. |
| <i class='fa-solid fa-part-antenna' aria-hidden='true'></i> VTX antenna | **[TBS VAS Airscrew u.FL RHCP](https://n-factory.de/TBS-VAS-Airscrew-UFL-RHCP-FPV-Antenna)** | €22.90 | The camera stack has a u.FL connector for the antenna. Otherwise arbitrary; should be tougher than the whoop variants, and should stick out sufficiently above the drone so the coverage from different angles is better[^vtx]. |
| <i class='fa-solid fa-part-receiver' aria-hidden='true'></i> Receiver | **[RadioMaster XR1 Nano ELRS](https://www.fpv24.com/en/radiomaster/radiomaster-xr1-nano-multi-frequency-24ghz-elrs-empfaenger)** | €15.90 | The stack doesn't have a built-in ELRS, so we needed one. No particular reason for this one except being reasonably cheap, and the video will drop much sooner than the receiver ever will. |
| **Total** | | **€466.35** | €379.49 for the drone itself (\(4\times\) motors, \(1\times\) battery, \(1\times\) propellers); the rest are spares. |
{narrow="{1} – {2} ({3})"}

[^motor]: From what I've generally read, it seems that **~4–5:1 thrust-to-weight ratio** (how much motors generate vs how much the drone weighs) makes the drone feel good. I will come entirely clean and tell you that an LLM told me this (I suck at physics, but reading it through, it looks right), but going by [the motors' bench test](https://www.ligpower.com/product/f1404-kv4600-fpv-motor.html) (full throttle, \(15.64\,\text{V}\)), the drone weighing \(\approx 228\,\text{g}\) (\(\approx 298\,\text{g}\) with the Osmo Nano), the battery dropping to \(13.0\,\text{V}\) when full-throttling, and thrust scaling with \(\text{RPM}^2 \propto V^2\), we get
    \[\begin{aligned}
        T_\text{max} &= 4 \cdot 310.6\,\text{g} \approx 1242\,\text{g} \\
        T_\text{worst} &\approx T_\text{max} \cdot \left(\frac{13.0\,\text{V}}{15.64\,\text{V}}\right)^2 \approx 860\,\text{g} \\
        \frac{T_\text{max}}{228\,\text{g}} &\approx 5.4 \qquad \frac{T_\text{max}}{298\,\text{g}} \approx \boxed{4.2} \\
        \frac{T_\text{worst}}{228\,\text{g}} &\approx 3.8 \qquad \frac{T_\text{worst}}{298\,\text{g}} \approx \boxed{2.9}
    \end{aligned}\]
  so flying without the camera should feel pretty good, and if I want to make some cool / cinematic shots it won't fly that terribly either.

[^stack]: Some of these features include faster processors, more ports and memory, built-in ELRS, a barometer, solder-free setups... all of which I didn't really see a need for an everyday 3" that's also my first build.

[^vtx]: This is actually really important -- before, I didn't really understand why we have antennas sticking out so far from the drones, so I tried it with the antenna from my Air75 II because there was a mix-up in delivery. The reason is that **you will lose video when the drone turns towards you**, and will have to reverse-fly back in shame because you're dumb and don't understand how physics works.

I did exclude a bunch of additional equipment that I bought, such as the battery charger, soldering equipment that I previously did not possess, and black TPU filament that I used to print a few [custom parts](#the-custom-parts), but those are more interchangeable and less important for the purposes of this article, so I'm not including them.

## Building

At this point I'll pretty much defer the entire build part to Oscar Liang's awesome [How to Build an FPV Drone](https://oscarliang.com/how-to-build-fpv-drone/) tutorial, which I followed religiously and it helped me a lot during the actual build and gave me a lot of confidence when doing many of the more destructive operations (fitting wires, soldering).

### The Fuckups

What I will mention are some fuckups during the build process that Oscar's article either didn't mention, or I can't read (honestly probably the latter); specifically:
1. **buy soldering flux** -- a bunch of my solders are pretty bad, and flux would have saved them
2. **do not route the wires** from the **outside** -- it might look natural that the wires will go from the side of the ESC, but that's where you'll be holding the drone from and it is on the outside of the drone -- things should not be poking out when looking at the drone from above
3. **battery wires yearn for the propellers** -- if you can manually move either the **main** or the **balance leads** from the battery to the propellers such that they touch, **they will**; my solution was zipties, [Oscar used rubber bands](https://oscarliang.com/secure-lipo-balance-lead/); both work fine

{{< image_section caption="Battery wires meeting the propellers." >}}
{{< image_row "wires-battery-leads.webp :: The battery leads and balance plug, chewed through. | wires-whoop-xt30.webp :: The XT30 pigtail, cut down to the strands." >}}
{{< image_row "wires-battery-zip-tie.jpg :: The battery leads, zip-tied to the battery. | wires-zip-tie-mounted.jpg :: The zip-tied leads on the drone, kept away from the propellers." >}}
{{< /image_section >}}

4. **do NOT leave your drone running for long without flying unless you configured it to do that**, and **definitely not without the antenna plugged in** -- the VTX chip generates power that it sends to the antenna, and if the power has nowhere to go, it... won't; you **will fry your VTX** (I fortunately did not, but not for lack of trying)
5. **get a practice soldering board** and **practice** -- it is much harder than one might think, and it's better to mess up wires that don't lead to the expensive component you bought for the drone, since a cut wire will be forever shorter
6. **get a multimeter** and a **smokestopper** -- the peace of mind knowing that your leads aren't shorted and that the drone will (probably) not catch on fire is worth the few extra bucks

### The Custom Parts

Now, for my pride and joy -- the **custom parts!**

The frame came with a [few stock 3D-printed parts](https://www.deepspacefpv.com/3D-Printed-Printing-Accessories-for-FPV-SEEKER-3-HD-5inch-Drone-Frame-p6688973.html).
Omitting the Osmo Nano, which I couldn't mount at all, most of the pre-made parts were technically functional, but very much did not fit the exact component configuration I had (the ELRS was too floppy and the VTX didn't fit).

So I designed my own!
All three are also on MakerWorld: the [camera mount](https://makerworld.com/en/models/3488265-deepspace-seeker-3-hdzero-nano-90-camera-mount), the [Osmo Nano mount](https://makerworld.com/en/models/3488246-deepspace-seeker-3-dji-osmo-nano-top-mount) and the [antenna mounts](https://makerworld.com/en/models/3488297-seeker-3-airscrew-vtx-elrs-antenna-mounts).

The design process was essentially LLM-assisted CAD design with [build123d](https://github.com/gumyr/build123d), calipers to measure proportions, and a touch of [COLMAP](https://colmap.github.io/index.html) for 3D reconstruction of the camera mount profile.
You can do `uv run <source.py>` and it will create the `out/*.stl` files.

I'll go more in depth in the subsequent sections, but I just wanted to say that I feel both excited and depressed that something that would take me days in Onshape can be done in an hour with Opus 5.5.
I do not know what this means for the field of CAD/engineering as a whole and if/when it will disrupt it the same way as it did for others, but turbulent times lie ahead.

Enough introspection, let's look at some sick renders.

#### Camera Mount

So it turns out that I kind of got the wrong camera.

It was not wrong in the sense that it wouldn't send video correctly to my goggles; it's just that neither the Seeker frame nor the camera came with any sort of mount that would bridge the gap between the 14mm camera and the 23mm gap in the frame.

Since the frame was rather complex, I opted to go for a 3D reconstruction (scaled to real proportions by measuring the circle with calipers).
This yielded a reconstruction that you could then project to 2D, and trace the edges via brightness, as seen in the images below.

{{< image_section caption="Getting the side plate's profile with COLMAP." >}}
{{< image_row "cam-mount-scan-photos.webp :: The photos of the side plate fed into COLMAP." >}}
{{< image_row "cam-mount-scan-pointcloud.webp :: The reconstructed point cloud. | cam-mount-scan-ortho.webp :: A top-down view of the plate, merged from all of the photos. | cam-mount-scan-profile.webp :: The traced profile, overlaid on the plate." >}}
{{< /image_section >}}

Finally, I caliper-measured the important parts of the camera, and designed the part by 
- starting on the **outer parts**, which just followed the contours,
- getting the **inner** part to pretty much be extruded contours minus the camera (rotated 30 degrees based on the top edge), and
- iterating on cutting out and chamfering parts so it's light and 3D-printable

{{< image_section caption="The Nano 90 camera mount [[right plate](cam-mount-outer-right.stl)] [[cradle](cam-mount-cradle.stl)] [[left plate](cam-mount-outer-left.stl)] [[source](cam-mount.py)] [[MakerWorld](https://makerworld.com/en/models/3488265-deepspace-seeker-3-hdzero-nano-90-camera-mount)]" >}}
{{< image_row "cam-mount-iso.webp :: The camera mount from an angle. | cam-mount-real.webp :: The printed camera mount on the drone." >}}
{{< image_row "cam-mount-outer-right.webp :: The camera mount's right plate. | cam-mount-cradle.webp :: The camera mount's cradle. | cam-mount-outer-left.webp :: The camera mount's left plate." >}}
{{< /image_section >}}

#### Osmo Nano Mount

This one was pretty easy.

For the top side, I took an existing 3D model of the Osmo Nano, rotated it 30 degrees, subtracted it from a rectangle, cut out the front, chamfered a bit and we're done!

For the mount on the top and bottom itself, I wanted the mount to slide in, so I added a center and a sides 45-degree cutout, as well as a small 1.5mm channel to not hit the screws (didn't want them to be sunken since everything would need to be taller).

Now I can do those sick dives I see on Instagram!

{{< image_section caption="The Osmo Nano top mount [[base](nano-mount-base.stl)] [[cradle](nano-mount-cradle.stl)] [[source](nano-mount.py)] [[MakerWorld](https://makerworld.com/en/models/3488246-deepspace-seeker-3-dji-osmo-nano-top-mount)]" >}}
{{< image_row "nano-mount-iso.webp :: The Osmo Nano mount from an angle. | nano-mount-real.webp :: The printed Osmo Nano mount on the drone." >}}
{{< image_row "nano-mount-base.webp :: The Osmo Nano mount's base. | nano-mount-cradle.webp :: The Osmo Nano mount's cradle. | nano-mount-cradle-front.webp :: The Osmo Nano mount's cradle from the front." >}}
{{< /image_section >}}

#### Antenna Mounts

These were genuinely the easiest.

The VTX antenna mount is simply a [small cylinder](https://www.reddit.com/r/AskReddit/comments/zdv5gv/how_would_you_get_a_small_cylinder_51in_length/); the only relevant part here is that the cylinder section is connected to the body at the same angle as the antenna goes up, so it handles force better.

The ELRS antenna mount is split into two parts, because otherwise the antenna wouldn't be held in place.
The intended setup is that these go on the antenna, get attached to the frame, and then the VTX antenna mount slides down to hold them in place and prevent them from rotating.

{{< image_section caption="The VTX and RX antenna mounts [[VTX mount](antenna-mounts-vtx.stl)] [[left RX holder](antenna-mounts-rx-left.stl)] [[right RX holder](antenna-mounts-rx-right.stl)] [[source](antenna-mounts.py)] [[MakerWorld](https://makerworld.com/en/models/3488297-seeker-3-airscrew-vtx-elrs-antenna-mounts)]" >}}
{{< image_row "antenna-mounts-iso.webp :: The antenna mounts from an angle. | antenna-mounts-real.webp :: The printed antenna mounts on the drone." >}}
{{< image_row "antenna-mounts-vtx.webp :: The VTX antenna mount. | antenna-mounts-rx-left.webp :: The left RX antenna holder. | antenna-mounts-rx-right.webp :: The right RX antenna holder." >}}
{{< /image_section >}}

### The Result

Behold, my child.

The red+black motor+frame colors fit really well, with the custom 3D-printed TPU parts blending seamlessly into the build.
You can view the [recent drone journal entries](/drone) to see the footage, but I'll be writing a separate blog post about those, since getting footage to look good turns out to not be easy.

{{< image_section caption="**Kaladin <i class='fa-solid fa-drone-kaladin' aria-hidden='true'></i>**, the finished build. I'm happy every time I look at it." >}}
{{< image_row "drone.webp :: The finished drone with the Osmo Nano on top." >}}
{{< image_row "drone-fpv-camera.webp :: The HDZero Nano 90 in its printed mount. | drone-osmo-nano.webp :: The Osmo Nano in its printed top mount." >}}
{{< image_row "drone-battery.webp :: The CNHL 650 mAh battery strapped on top. | drone-motor.webp :: A T-Motor F1404 with an HQ T3x3x3 prop. | drone-stack-closeup.webp :: A close-up of the stack." >}}
{{< /image_section >}}
