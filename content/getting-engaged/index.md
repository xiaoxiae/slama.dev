---
date: '2026-09-07'
title: Getting Engaged
categoryIcon: k
description: "She said yes!"
toc: true
---

**She said yes!**

---

and here is an article on why.

This is not a [/r/LinkedInLunatics](https://www.reddit.com/r/LinkedInLunatics/) type thing -- bear with me here.
I made a [cute video game](https://k.slama.dev). It took me many hours, I learned a lot of things, and I wanted to show it to you, in case you'd like to do something similar for a proposal (it worked; N=1 but we take those babyyy).

{{< image_section caption="**_[You can play it online!](https://k.slama.dev)_**  _To play, you need a microphone and patience._<br>Yes, there is a speedrunning leaderboard. Don't ask why." >}}
{{< image_row "shots/hub-hall/23-b1c0091.png | shots/cooking-play/10-ce5dbe7.png" >}}
{{< /image_section >}}

and also read the rest of the article if you're interested in how it was made.


### The Idea

I am a very tech-oriented person, as most of the activities that I do involve the computer -- programming and gaming being the main two.
Now, I certainly could go the easy way and do the traditional go-somewhere and propose type thing... but I feel like that's kind of boring, and doesn't reflect who I am.

What if I instead spend a hundred hours creating a 10-minute game, then hope that it doesn't crash or run into an unrecoverable bug on the big day, and...

Yeah, okay, writing this out loud, I probably should have gone for the former, but I had an idea that at the very end of the game, there would be light rays coming from the top of the monitor (like there's something there), and I would reach up there and get the ring.

A little cringe? Maybe.

But come on, you've got to give me that it's kind of cute. 

I went in the direction of Undertale, which fit all of the criteria I had in mind when first conceptualizing the idea -- easy to play, reasonable to implement, and I'll be damned if there is anything cuter than two doggos in love.

The idea I had was to split the gameplay into individual minigames inspired by things from our lives -- that way the game is flexible, and I can make sure that there will be at least something to play since each minigame is self-contained.

### Art

I used [**Aseprite**](https://www.aseprite.org/), using a [Wacom Intuos M Bluetooth](https://estore.wacom.com/en-us/wacom-intuos-m-bluetooth-black-us-ctl6100wlk0.html) tablet to draw all of the sprites.

{{< image_section caption="Creating the art with my trusty Wacom Intuos M Bluetooth. Da Vinci who?" >}}
{{< image_row "images/art-2.jpg | images/art-1.jpg" >}}
{{< /image_section >}}

An LLM was used here to help me create placeholder sprites and the corresponding sprite maps, which was very handy for testing the sizes and numbers of assets before committing to the drawing.

---

Before diving further, I want to go on a short intermezzo and address LLM usage for this project.

In my mind, **all of the assets and decisions made** have to be **mine alone.**
No sound, writing, room design, or sprite shall be made by the clanker, since I am the one proposing, and if I need an LLM to do that for me then what the fuck are we even doing here.

That being said, I heavily used it for **writing the code** and **helping with manual tasks** such as the one above (creating placeholder assets / rooms, wiring entities, implementing room logic based on my specification), since the point wasn't to learn Bevy or make a maintainable architecture.

If it bothers you that I used an LLM for these tasks, please go somewhere else.

---

You can look at [`assets/_src/sprites/sprites.yaml`](https://github.com/xiaoxiae/project-k/blob/master/assets/_src/sprites/sprites.yaml) to see how they're defined -- until I've drawn a real sprite, a placeholder is defined by its size, shape and appearance, from which a placeholder Aseprite file is generated that I can then draw.

```yaml
sprites:
  ...
  cooking-cupboard:
    shape: box
    tiles: [1, 2]
    color: "#7d6242"
    round: 2
    map: cooking-cupboards
  ...
```

{{< image_section caption="Sample placeholder sprites (left in pair), and their real counterparts (right in pair)." >}}
{{< image_row "images/sprites/cooking-fridge.png | images/sprites/cooking-oven-baking.png | images/sprites/crowd-bench.png" >}}
{{< image_row "images/sprites/player-sprint-left-f1.png | images/sprites/player-walk-down-f1.png | images/sprites/player-walk-right-f1.png" >}}
{{< /image_section >}}

This was incredibly helpful, since all of the boring work of setting up the spritemaps and their mapping onto entities was done automatically, and all I needed to do was draw.

### Sound

All of the sounds in the game are either **recordings** of real sounds or **music** that I composed.

#### Recordings

The easiest one -- just record the noise you want the game to make.

{{< image_section >}}
{{< image_row "images/sound-1.jpg | images/sound-2.jpg" >}}
{{< figcaption >}}Recording sounds from around the apartment for the cooking minigame -- {{<sound "sounds/cooking-fridge-open.ogg">}}opening the fridge{{</sound>}} (left) and {{<sound "sounds/cooking-chop-1.ogg">}}slamming the knife{{</sound>}} onto the cutting board like a maniac (right).{{< /figcaption >}}
{{< /image_section >}}

Since this is an Undertale-style game based on reality, the vast majority of the sounds are just recordings of household objects.
It was actually eyeopening to me how entirely mundane noises that I didn't think much of were a really good fit for entirely unrelated actions -- for the movie QTE specifically, I was just {{<sound "sounds/movie-hit.ogg">}}clicking a pen{{< /sound>}} (same for the {{<sound "sounds/movie-miss.ogg">}}miss{{</sound>}}); for the menu tick, it was just the {{<sound "sounds/ui-move-1.ogg">}}rolling{{</sound>}} on the selector.

Yet again, the LLM came in extremely handy for taking the raw recorded files and normalizing them + applying effects such as fading/high pass, so that I, similar to art, only needed to record them, and the boring manual work was taken care of.

```yaml
sounds:
  ...
  ui-interact:
    source: ui-interact.wav
    normalize: -19.0
    chain:
      - trim: {start: 0.892, dur: 0.060}
      - highpass: 200
      - fade: {out: 0.02}
  ...
```

Oh, and I also shamelessly stole the blabbering idea from [Animal Crossing](https://animalcrossing.nintendo.com/) (and I'm sure many other places) to make sounds of {{<sound "sounds/voice-player-1.ogg">}}her{{</sound>}} and {{<sound "sounds/voice-him-1.ogg">}}me{{</sound>}} speaking in dialogues.

#### Music

![Sheet music of the hub theme.](images/hub-score.png)
{.rightFloat .no-invert}

I composed a few bars of actual music for this in [Muse Score](https://musescore.org/en)!

When you're in the hub, you hear {{<sound "sounds/hub.ogg">}}this theme{{</sound>}}.
It is simple, sounds calming, and I had no idea what the fuck I was doing the entire time... but the game is no longer predominantly silent and it's meant to play in the background anyway, so I think it fits in well.

I feel like this is the weakest part of the project, since I truly do not possess talent for music (especially for composition), but it comes from the heart and that is what matters here.

Hopefully.

### Game

Now, onto the game itself.

If you haven't played it and made it this far... I would highly encourage you to **[go play it now](https://k.slama.dev/)**, since the rest covers each of the rooms in detail and reading through without playing it will spoil it for you.

You have been warned. Let's proceed.

#### The Hub

You start your journey in the hub.

Since the game consists of a bunch of unrelated minigames, the hub room is the thread that connects them together.
It is used to enter and move between the minigames, and enter the final room.

{{< image_section caption="The hub start (left), middle (middle) and near the end (right)." >}}
{{< image_row "shots/head/hub-spawn.png | shots/head/hub-hall.png | shots/head/hub-finale.png" >}}
{{< /image_section >}}

Since it would feel a bit barren, I've added a bunch of easter egg items that are of significance to the two of us (like a {{<sound "sounds/hub-egg-owl.ogg">}}hooting owl{{</sound>}} that definitely isn't just me making the noise, or a Kurzgesagt poster).
In my mind, details like these have always felt special when playing games like [Hollow Knight](https://www.hollowknight.com/) / [Outer Wilds](https://store.steampowered.com/app/753640/Outer_Wilds/), and so I tried to do something similar here.

#### Horse Minigame 🐎

I won't go into detail, except that this was our first date and you need to mimic horse noises to pass (I promise we're a normal couple).
The gimmick here is pretty fun, honestly, and I think the visual soundwave comparison is pretty neat since you can see how you're doing mid-take.

{{< image_section caption="The horse minigame over time." >}}
{{< image_row "shots/mimic-play/01-ba4e1ec.png | shots/mimic-play/03-d8e2c4f.png | shots/mimic-play/10-ce5dbe7.png" >}}
{{< /image_section >}}

This was the first idea, and I think it's implemented well.

#### Movie Minigame 🍿

A simple QTE minigame -- you have to hit ever-increasing QTEs to not fall asleep and lose the minigame while watching Twilight (or some random footage since I am not getting sued over a shitpost).

{{< image_section caption="The movie minigame over time." >}}
{{< image_row "shots/movie-dark/18-b27d7a7.png | shots/movie-dark/22-9b0e8a9.png | shots/movie-dark/32-b1c0091.png" >}}
{{< /image_section >}}

The one thing that makes this a bit more interesting is the shader that is used to show that the projector is projecting the light rays onto the screen, which adds a nice touch to make the scene more believable.
It's pretty simple (sample a column and stretch it towards the projector, making closer pixels brighter), but it's a touch that makes the scene more alive.

{{< image_section caption="The projector shader on two separate frames from an unspecified movie." >}}
{{< image_row "images/projector-1.png :: Projector shader :: :: 580,360,305,200 | images/projector-2.png :: Projector shader :: :: 580,360,305,200" >}}
{{< /image_section >}}


#### Cooking Minigame 🍳

A baking minigame that absolutely obliterates the poor kitchen, to be cleaned by an unspecified person at some point in the distant future.

{{< image_section caption="The cooking minigame over time." >}}
{{< image_row "shots/cooking-play/01-f3f510e.png | shots/cooking-play/04-6db47f8.png | shots/cooking-play/10-ce5dbe7.png" >}}
{{< /image_section >}}

This one was at the same time the easiest, the most annoying, and the most fun to make, since it required so many individual sounds and sprites (different steps / states of the bowls, robot swirling animation, transparent oven + sounds), but almost no annoying programming / mechanics.

The only two things of interest were the specks flying when cutting that stayed on the ground, and the milk trail that required a bunch of drawing to get all of the asset combinations; otherwise the implementation was very simple.


#### Crowd Minigame ‍‍🧑‍🤝‍🧑

I have a tendency to set off in a random direction and not look back at whether that is what we're doing, so this minigame is pretty much just that -- you have to pass through a thick crowd that I disappear into, and find me at the end.

{{< image_section caption="The crowd minigame over time." >}}
{{< image_row "shots/crowd-play/01-fbfd3eb.png | shots/crowd-play/04-1cf6a4e.png | shots/crowd-play/10-ce5dbe7.png" >}}
{{< /image_section >}}

This one was not trivial to implement, because we need the crowd to:
- be **diverse** to make it look real (without drawing ourselves to death), and
- **move organically**, not like robots.

Here are my solutions for both.

##### Drawing the crowd

All humans are different -- our skin color, height, hair (or lack thereof), and accessories.
These, while different, roughly follow a distribution that we know -- you won't get a 7-meter-tall person or someone with blue skin unless you're in Avatar.

Therefore, to make the crowd appear randomized, I created a fixed number of sprites that make up a person (male/female), stitched them together, and randomized the color within each (hue shift) on a reasonable distribution.
That way we get light/dark skin, different hair / shirt colors and heights, while only having to draw \(24 \times 2\) sprites!

{{< image_section caption="The spritesheets for the crowd randomization (left **m**ale, right **f**emale)." >}}
{{< image_row "images/crowd-m.png | images/crowd-f.png" >}}
{{< image_row "images/crowd/003.png | images/crowd/004.png | images/crowd/005.png | images/crowd/006.png | images/crowd/013.png | images/crowd/014.png | images/crowd/015.png | images/crowd/016.png | images/crowd/017.png" >}}
{{< image_row "images/crowd/023.png | images/crowd/024.png | images/crowd/025.png | images/crowd/026.png | images/crowd/033.png | images/crowd/034.png | images/crowd/035.png | images/crowd/036.png | images/crowd/037.png" >}}
{{< image_row "images/crowd/043.png | images/crowd/044.png | images/crowd/045.png | images/crowd/046.png | images/crowd/053.png | images/crowd/054.png | images/crowd/055.png | images/crowd/056.png | images/crowd/057.png" >}}
{{< /image_section >}}

It's not quite GTA V-levels of realism, but the crowd came out looking quite nice.


##### Making it walk

Making the crowd work was a bit more difficult, but it is conceptually relatively simple: the movement of a person in a crowd can be modeled by considering the following rules:
- they want to **go somewhere** (in our case down),
- they do **not** want to **bump into** other people and objects, and
- they want to **avoid crowded paths** so they can move as quickly as possible.

For the general navigation, we can use a **flow field** to direct the crowd towards the goal, giving each tile the direction the person should be pushed in when in that tile.
To simulate avoiding the crowded paths, we **add decaying weight** to the tiles people are standing on, such that when we repeatedly **recalculate** the flow field, it will avoid paths that are currently crowded.

The movement of the people is then a **current** velocity that is **smoothed** towards the **desired** one based on the aforementioned things:
- **flow field** value at their given tile, and a
- **repulsive force** from other nearby **people and obstacles**.

You can see it in action here:

{{< image_section caption="An example of the crowd in action, left in the real game and right in debug view. The flow field is recalculated every 500 ms, starting from the bottom and going up." >}}
{{< video "" "crowd" >}}
{{< /image_section >}}

I think it turned out pretty great!

#### The Finale

The finale was pretty simple -- walking up a columned room, with the footage of you playing the previous minigames as flashbacks (meant to resemble memories), until you reach the light at the very top, after which the credits roll.

{{< image_section caption="The start (left), middle (middle), and end (right) of the final room." >}}
{{< image_row "shots/finale-hall/35-ce5dbe7.png | shots/finale-hall/36-ce5dbe7.png | shots/finale-hall/37-ce5dbe7.png" >}}
{{< /image_section >}}

I recently played [Outer Wilds](https://store.steampowered.com/app/753640/Outer_Wilds/) (if you haven't done so, stop reading this article and go play it right now; it is only a tiny bit better than my game), so I can't claim that I thought of the concept of replaying memories myself, but it fits here really well, so I'll be using it, thank you very much.


### Conclusion

This was fun, and I hope I won't have to make another engagement video game in the future.

🕊️
{.right}
