---
date: '2026-09-07'
title: Getting Engaged
description: "She said yes!"
---

**She said yes!**

---

and here is an article on why.

This is not a [/r/LinkedInLunatics](https://www.reddit.com/r/LinkedInLunatics/) type thing, bear with me here.
I made a cute video game, it took me many hours, I learned a lot of things, and I wanted to show it to you, in case you'd like to do something similar for a proposal (it worked; N=1 but we take those babyyy).

{{< image_section caption="**_[You can play it here!](https://k.slama.dev)_**" >}}
{{< image_row "shots/hub-hall/23-b1c0091.png | shots/cooking-play/10-ce5dbe7.png" >}}
{{< /image_section >}}




and also read the rest of the article if you're interested in how it was made.


### The Idea

I am a very tech-oriented person, as most of the activities that I do involve the computer -- programming and gaming being the main two.
Now I certainly could go the easy way and do the traditional go-somewhere and propose type thing... but I feel like that's kind of boring, and doesn't reflect on who I am.

What if I instead spend a hundred hours creating a 10-minute game, then hoping that it doesn't crash or run into an unrecoverable bug on the big day, and...

Yeah, okay, writing this out loud, I should have probably gone for the former, but I had an idea that at the very end of the game, there would be lightrays coming from the top of the monitor (like there's something there), and I would reach there and get the ring.

A little cringe? Maybe.

But come on, you've got to give me that it's kind of cute. 

Let's get to implementing.


### The Game

For the game to be playable and enjoyable, it 
- shouldn't have any difficult mechanics,
- should be within my capabilities to implement, and
- must be **cute**!

I went in the direction of Undertale, which fits all of the three above -- easy to play, reasonable to implement, and I'll be damned if there is something cuter than two doggos in love.

The idea I had is to split the gameplay into individual minigames inspired by things from our lives -- that way the game is flexible, and I can make sure that there will be at least something to play since each minigame is self-contained.

These are minigames that made it into the final game.

#### 1) Horse Minigame

{{< image_section caption="The horse minigame over time." >}}
{{< image_row "shots/mimic-play/01-ba4e1ec.png | shots/mimic-play/03-d8e2c4f.png" >}}
{{< image_row "shots/mimic-play/05-1cf6a4e.png | shots/mimic-play/10-ce5dbe7.png" >}}
{{< /image_section >}}

Won't go into any details except that this was our first date and you need to mimic horse noises to pass (I promise we're a normal couple).
The gimmick here is pretty fun, honestly, and I think the visual soundwave comparison is pretty neat since you can see how you're doing mid-take

This was the first idea and I think it's implemented well.

#### 2) Movie Minigame

{{< image_section caption="The movie minigame over time." >}}
{{< image_row "shots/movie-dark/18-b27d7a7.png | shots/movie-dark/22-9b0e8a9.png" >}}
{{< image_row "shots/movie-dark/26-e5fbdfa.png | shots/movie-dark/27-a28a22c.png" >}}
{{< /image_section >}}

A simple QTE minigame -- you have to hit ever-increasing QTEs to not fall asleep and lose the minigame while watching Twilight (or some random footage since I am not getting sued over a shitpost).

The one thing that makes this a bit more interesting is the shader that is used to show that the projector is projecting the right rays onto the screen, which adds a nice touch to make the scene more believable.
It's pretty simple (sample column and stretch it towards the projector, making closer pixels brighter), but it's a touch that makes the scene more alive.


#### 3) Cooking Minigame

{{< image_section caption="The cooking minigame over time." >}}
{{< image_row "shots/cooking-play/01-f3f510e.png | shots/cooking-play/04-6db47f8.png" >}}
{{< image_row "shots/cooking-play/06-ad96090.png | shots/cooking-play/10-ce5dbe7.png" >}}
{{< /image_section >}}

A baking minigame that absolutely obliterates the poor kitchen, to be cleaned by an unspecified person at some point in the distant future.

This one was, at the same time the easiest, the most annoying, and the most fun to make, since it required so many individual sounds and sprites (different steps / states of the bowls, robot swirling animation, transparent owen + sounds), but almost no annoying programming / mechanics.

The only two things of interest were the specs flying when cutting that stayed on the ground, and the milk trail that required a bunch of drawing to get all of the asset combinations; otherwise very simple.


#### 4) Crowd Minigame

{{< image_section caption="The crowd minigame over time." >}}
{{< image_row "shots/crowd-play/01-fbfd3eb.png | shots/crowd-play/04-1cf6a4e.png" >}}
{{< image_row "shots/crowd-play/07-f510a1d.png | shots/crowd-play/10-ce5dbe7.png" >}}
{{< /image_section >}}

I have a tendency to embark in some unspecified direction and not look back at whether that is what we're doing, so this minigame is pretty much just that -- you have to pass through a thick crowd that I disappear in and find me in the end.

This one was not trivial to implement, because of two facts:
- we need **diversity** to make the crowd look like a crowd (without drawing 1000 assets), and
- make it **move organically** and not like robots.

Here are my solutions for both.

##### Drawing the crowd

All humans are different -- our skin color, height, hair (or the lack of), accessories.
These, while different, are somewhat on a distribution that we know -- you'll not get a 7-meter-tall person or someone with blue skin unless you're in Avatar.

Therefore, to make the crowd appear randomized, I created a fixed number of sprites that make up a person (male/female), stitch them together, and randomized the color within each (hue shift) on a reasonable distribution.
That way we get light/dark skin, different hair / shirt colors and heights, while only having to draw \(24 \times 2\) sprites!

{{< image_section caption="The spritesheets for the crowd randomization (left **m**ale, right **f**emale)" >}}
{{< image_row "images/crowd-m.png | images/crowd-f.png" >}}
{{< /image_section >}}

It's not quite GTA 5-levels of realism, but the crowd came out looking quite nice.


##### Making it walk



--- 



### Implementation

When it comes to the implementation, I had one clear goal in mind: **all game assets must be my original work** -- any sound / piece of writing / room design / sprite will not be touched by an LLM.
This does not mean that I won't use LLM for coding, which is what I did for 


### Art

{{< image_section caption="Creating the art with my trusty Wacom Intuos M Bluetooth. Mona Lisa who?" >}}
{{< image_row "images/art-2.jpg | images/art-1.jpg" >}}
{{< /image_section >}}

- have LLM manage sheets / placeholder sprites
- use a tablet to do the drawing
- I sucked a LOT at the beginning, just iterate until it doesn't look awful


### Sound Design

_\*cricket noises\*_

{{< image_section caption="Recording sounds from around the apartment for the cooking minigame." >}}
{{< image_row "images/sound-1.jpg | images/sound-2.jpg" >}}
{{< /image_section >}}

- raw files, YAML files that encompas the transformations required from RAW to that fo game (normalizatiopn, cutting,e etc...)
- put exapmles here
- for music, just Muse I guess>
