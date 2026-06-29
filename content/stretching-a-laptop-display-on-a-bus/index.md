---
date: '2026-05-13'
title: "Stretching a Laptop Display on a Bus"
description: A surprisingly effective solution to an unsurprisingly uncommon problem.
---

We've all been there -- you find yourself sitting on a bus with an hour or two to spare.
You pull out your laptop, eager to finish that one blog post you didn't have time for, but -- oh no! -- there is **not enough room in front of you to work comfortably!**

You can either 
1. **fold the monitor** to have a comfortable arm position, distorting the display 🤏, or
2. **bring the laptop closer** and raise your arms like Dracula to be able to type 🧛

What the global elites are not telling you is that there is a **third option:** combine the comfort of a non-vampiric hand position and an undistorted display by folding it and **stretching the screen** to compensate for the distortion -- all for the low low price of a single magical `xrandr` incantation:

```fish
xrandr --output <your monitor> --transform 1,0,0,0,0.6,0,0,0,1
```

{{< image_section caption="**(left)** Ugly. Shrunk. Does not spark joy.<br>**(right)** Nice. Readable. Sparks joy." >}}
{{< image_row "unstretched.jpg :: Laptop that does not spark joy. | stretched.jpg :: Laptop that sparks joy." >}}
{{< /image_section >}}

Beautiful. Pristine. Like bus rides were always meant to be experienced.

<!--

Leaving a note for future follow-up: I think it would be super cool to make a project that tracks where your eyes are, calculates what the transformation of the display should be in order to see a perfect rectangle, and then apply it; a few things:
- should only transform to nearest multiples of the angle, so we don't keep jittering as the eye tracking stabilizes
- if we go off the screen, it should stay there, since it was likely because we went too high

Math-wise:
- detection gives you a line, but you need distance for the rectangle to know where to project itself to; can just be estimated from eye distance?
- we can also rotate so the screen is level with the eyes
- when we know the point + rotation about it, we have our transformation
- the only difficult part is fitting the transform into the infinite triangle that goes through the point -- can this even be calculated algebraically? When we rotate towards the origin and move it to fit within the rectangle, this already changes the transform to look somewhere slightly else; an iterative method should be fine?

Now that I think of it, that has to already exist... but maybe not on the level of the display?

-->
