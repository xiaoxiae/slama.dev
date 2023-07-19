---
excerpt: A fun experiment on productivity using a (productivi)tree.
---

---

_Update (18. 3. 2022): the concept works quite well, but needs to be connected to some other app that automatically tracks productive time, since adding dots manually (even via a script) adds too much overhead. I'll no longer be updating the image, but the post stays up._

---


With the end of the summer holidays and the beginning of a new semester, I've been thinking about clever ways to trick myself into being productive.

There are, of course, a bazillion apps, services and techniques to help with this, some of which I've used in the past. I felt, however, that none of them captured the hours of work I put into whatever I deemed productive in a meaningful way.

That's why I came up with the concept of a productivitree. Here is mine:

![](/assets/productivitree.svg)

The idea is simple: for each productive hour, I fill in a dot, with the color depending on the type of activity I did (education-related dots are blue, others are black[^1]).

Although this might not be a groundbreaking discovery in the field of procrastination, I wanted to share it anyway, since some people might find it useful/interesting.

### Generating the image
The above image was generated using **weighted stippling**, which is a technique where a given image is converted into a set of points of varying thickness (see [this paper](https://mrl.cs.nyu.edu/~ajsecord/npar2002/npar2002_ajsecord_preprint.pdf) if you're interested in the math behind it).

I used the [StippleGen](https://www.evilmadscientist.com/2012/stipplegen-weighted-voronoi-stippling-and-tsp-paths-in-processing/) program when generating my image. It should run on any major operating system and has a pretty straightforward UI, exporting directly to SVG.

As for updating the image after being productive, I created a simple script that does this automatically, selecting the one that is closest to the center.

[^1]: If your system prefers dark theme, the dots will yellow/white, since the colors are inverted.
