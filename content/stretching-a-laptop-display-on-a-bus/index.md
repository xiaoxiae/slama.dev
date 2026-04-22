---
date: '2026-04-22'
title: "Stretching a Laptop Display on a Bus"
draft: true
---

We've all been there -- you find yourself sitting on a bus with an hour to spare.
You pull out your laptop, eager to finish that one blog post you didn't have time for, but -- oh no! -- there is **not enough room to work comfortably!**

You can either 
1. **fold the monitor** to have a comfortable arm position, distorting the display 🤏, or
2. **bring the laptop closer** and raise your arms like Dracula to be able to type 🧛

What the global elites are not telling your is that there is a **third option:** combine the comfort of a non-vampiric hand position and an undistorted dispaly by folding it and **stretching it** to accomodate for the distortion -- all for the low low price of a single magical `xrandr` incantation:

```fish
xrandr --output <your monitor> --transform 1,0,0,0,0.6,0,0,0,1
```

{{< image_section caption="**(left)** Ugly. Shrunk. Does not spark joy.<br>**(right)**: Nice. Readable. Sparks joy." >}}
{{< image_row "unstretched.jpg :: Laptop that does not spark joy. | stretched.jpg :: Laptop that sparks joy." >}}
{{< /image_section >}}

Beautiful. Pristine. Like bus rides were always meant to be experienced.
