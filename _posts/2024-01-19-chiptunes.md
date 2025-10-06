---
title: Chiptunes
excerpt: "An experiment in making chiptune music."
category: "music"
category_icon: /assets/category-icons/music.svg
---

As a part of the holiday brake (mostly to prevent me from playing Factorio), I decided to get into making chip music.
The goal is to, at the very least, grasp the concepts and produce an original piece of music that sounds.
_No qualifier, just sounds._

This (short) post is both a write-up and a place for notes as I learn.
Since I am a complete beginner, take everything written here with a huge grain of salt.

---

1. **day:** spent comfortable with Furnace; playing around with inputting notes
    - _the target device is the NES since it's channels are pretty limited_
2. **day:** figured out a simple progression that sounds interesting
3. **day:** fleshed out the progression and added fluff around to make it interesting
    - **here are the results** (it's pretty bad): [First.wav](/assets/chiptunes/First.wav) (10 seconds), [First.fur](/assets/chiptunes/First.fur) (Furnace file)
    - also thinking about the next, longer song I'd like to work on
4. **day:** work on the second song, which will be a Waltz
5. **day:** again some more work, this is pretty hard

<div class="force-spacing" markdown="1">
_A long time ellapsed here, during which I did nothing. The work during days 4. and 5. gave me a good idea of how much work it actually is to create a good-sounding chiptune (which, to some extent, was the goal of the project), so I'm going to leave it here for now. Who knows, maybe I'll return to make more chiptunes some other time_ 🙂.<br>
</div>

<ol>
  <li value="99"><strong>day:</strong> finishing touches on the (start of the) Waltz</li>
    <ul>
      <li><strong>here are the results</strong> (still pretty bad): <a href="/assets/chiptunes/Second.wav">Second.wav</a> (20 seconds), <a href="/assets/chiptunes/Second.fur">Second.fur</a> (Furnace file)</li>
    </ul>
</ol>

---

### Terms and definitions

**Chiptune music** [[wikipedia](https://en.wikipedia.org/wiki/Chiptune)]:
- music created using **PSG**s (programmable sound generators)
    - chips that create/synthesize audio waves from basic waveforms
    - usually a basic wave like **square/triangle/saw-tooth/sin/noise**
        - [here is what some of them sound like](https://www.youtube.com/watch?v=VRD9Uj2YTBk)
    - can be used in **FM synthesis** to create more general sounds by _modulating waves with one another_ ([neatly explained in this video](https://www.youtube.com/watch?v=vvBl3YUBUyY))

**Tracker** [[wikipedia](https://en.wikipedia.org/wiki/Music_tracker)]:
- generally software for creating music
- music presented as musical notes positioned in several channels (top to bottom)
- here is a [gigantic video](https://www.youtube.com/watch?v=roBkg-iPrbw&t=1226s) that dives into trackers in great detail

### Using the [Furnace](https://github.com/tildearrow/furnace) tracker

- here is a great [[YouTube video](https://www.youtube.com/watch?v=Q37XuOLz0jw)] from which I learned most of the introductory stuff

**Pattern window** (bottom left) is where we'll be doing the sequencing
- channels have the following columns:
    - **note** -- defining the _pitch_ and the _octave_
    - **instrument** -- selecting pre-made instruments from the instrument window
    - **volume** -- the volume of the note
    - **effects** (multiple) -- things like vibratos, pitch slides (see right side)
- notes always play indefinitely (until another note / note cut)

**Tempo** (top right) is determined by the `tick rate`, which determines TPS
- `speed` -- how many ticks a row lasts for
- `highlight` -- highlights row multiples (i.e. determines beat/measure length)
- `pattern length` -- number of measures in the **current pattern**

**Pattern window** (top left) determines the order the patterns in the song are played

**Edit window** (top left-ish) has things for editing the composition
- `octave` -- the octave that will be input
- `step` -- the length of a step after a note is input

**Chip manager window** can be used to define the PSGs used in the composition

#### Controls
- `F4`/`F5` -- stop/play (the stop was configured)
- `Ctrl+Enter`/`Shift+Enter` -- step/play from cursor

- `Ctrl+F1`/`Ctrl+F2` -- Transpose -1/+1 note
- `Ctrl+F3`/`Ctrl+F4` -- Transpose -1/+1 octave

- **notes** can be input either with a MIDI controller (oof) or via a the keyboard:
    - `space` -- disable/enable note input
    - `1` -- note cut (`OFF`)
    - `zsxdcvgbhnmq` (first octave)
    - `q2w3er5t6yui` (second octave)

- **effects** can be input by writing their code in the rightmost two columns
    - these are _not tied to one note_ but to the _whole channel_!
    - certain individual effects have to be turned off!
    - `ECxx` -- note cut
    - `F3xx`/`F4xx` -- volume slide up/down
