---
date: '2026-03-17'
title: "Learning German with Bilbo"
description: "Implementing an interleaver for audiobooks."
---

I have been trying to learn German without much success for a while now.
The main issue I run into is motivation -- I speak English at work, Czech at home and German... well, not many places, as most of my friends are either international, or speak English just fine.

Since I listen to audiobooks quite a bit, I thought of the following: **combine the English and the German version**, so I can hear the English part first, and thus know what the German part means!
While not a particularly revolutionary idea, I haven't been able to find a project that does this, so I implemented [**Bilbo** -- the **Bil**ingual audio**bo**ook interleaver](https://github.com/xiaoxiae/Bilbo).

Here is an example:

{{< video "bilbo" "alloy-of-law" >}}

> **EN:** The revolver was nothing fancy to look at, though the six-shot cylinder was machined with such care in the steel alloy frame that there was no play in its movement.
>
> **DE:** Der Revolver machte zwar keinen besonders ansehnlichen Eindruck, doch die sechsschüssige Trommel war mit solcher Präzision in den Rahmen aus einer Stahllegierung eingesetzt, dass in ihren Bewegungen nicht das geringste Spiel war.

> **EN:** There was no gleam to the metal or exotic material on the grip, but it fit his hand like it was meant to be there.
>
> **DE:** Das Metall schimmerte nicht und in den Griff waren keinerlei exotische Materialien eingelassen, aber die Waffe lag so gut in seiner Hand, als wäre sie eigens dafür geschaffen worden.

> **EN:** The waist-high fence was flimsy, the wood grayed with time, held together with fraying lengths of rope.
>
> **DE:** Der hüfthohe Zaun war baufällig, das Holz, mit der Zeit grau geworden, wurde von ausgefransten Seilen zusammengehalten.

---

If you want to try it out yourself, you can install Bilbo by running

```fish
pip install bilbo-audiobook
```

(pulls Torch; heavy dependencies!) and combine your audiobooks by running

```fish
bilbo process en.mp3 de.mp3
```

Then pick your favorite audiobook player (I prefer [Smart AudioBook Player](https://play.google.com/store/apps/details?id=ak.alizandro.smartaudiobookplayer&hl=en-US)) and enjoy!

### How it works

Fortunately, all of the difficult parts were already implemented: given two audio files, I use
1. [faster-whisper](https://github.com/SYSTRAN/faster-whisper) + [SileroVAD](https://github.com/snakers4/silero-vad) for transcriptions + word-level timestamps (**transcription**),
2. [pySBD](https://github.com/nipunsadvilkar/pySBD) to clean up + detect sentence boundaries (**segmentation**),
3. [LaBSE](https://huggingface.co/sentence-transformers/LaBSE) (via [sentence-transformers](https://github.com/UKPLab/sentence-transformers)) to compute sentence embeddings across languages and match them using dynamic programming via [Bertalign](https://github.com/bfsujason/bertalign) (**alignment**),
4. [ffmpeg](https://www.ffmpeg.org/) for audio normalization/extraction/interleaving (**assembly**), and
5. optionally, a local LLM via [ollama](https://ollama.com/) for cover art and text metadata merging (**metadata**).

Since we're mostly gluing things together, there isn't anything particularly interesting -- I just connected some pipes together and out comes a passive way for me to learn German, until I gaslight myself into learning it actively too.

Tschüss 🇩🇪!
