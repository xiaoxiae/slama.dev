---
date: '2024-05-06'
title: Automatic Subtitling with Python
end: <a href="/comeback/">Comeback subtitles</a>
description: How to create subtitles for videos in an effective way (essentially automatically).
toc: true
---

Growing up, [Comeback](https://www.imdb.com/title/tt1321261/) was[^1] one of my favorite Czech sitcoms.
Re-watching it recently, I wanted to show it to my friend who doesn't speak Czech, but English subtitles don't seem to exist (and, for that matter, neither do Czech ones).

Seeing as I don't have much time (master thesis), I decided to waste it by creating them.
Further seeing as I am a programmer, I am not going to do this manually and, as the title suggests, will automate the process as much as I can.

This short post covers what I did and could prove useful if case you have your own favorite movie/show that you'd like to create subtitles for.

→ [Here are the subtitles](/comeback/), if you're interested. ←
{.center}

---

The general approach for creating subtitles is the following:

1. use [OpenAI's Whisper](https://github.com/openai/whisper) to automatically create the initial subtitles & timings
2. manually fix timing & errors using [Kdenlive](https://kdenlive.org/en/)
3. use a local LLM ([Mistral 7B](https://mistral.ai/news/announcing-mistral-7b/) via [ollama](https://ollama.com/)) for _Czech → English_ translation
4. fix errors using a text editor of your choice (e.g. `vimdiff`)

### 1) Transcription

To create the initial Czech subtitles (or pretty much any other language[^2]), we'll first need to install [WhisperX](https://github.com/m-bain/whisperX), which is a faster and less memory-hungry implementation of Whisper.
Assuming you have the preliminaries (CUDA-enabled GPU & PyTorch), you can install WhisperX from source via `pip`:

```text
pip install git+https://github.com/m-bain/whisperx.git
```

To automatically create the subtitles, we can use `ffmpeg` to extract the audio, and subsequently run the `whisperx` command with appropriate parameters.
_Assuming you are in the directory with your audio files, you can run the following script:_

{{< details "Code" "transcribe.sh" >}}{{< /details >}}

Note that for the `large` WhisperX models, you need to have **at least ~8 GB of VRAM**.
If you don't have this, use `medium`, which requires ~6 GB and is quite a bit worse.

If you don't have a GPU at all, I would recommend using [Runpod](https://www.runpod.io/), which offers cheap GPU devices with custom Docker images.
_This is not a sponsored post but I am a very happy customer, and if you'd like to support me, [here is my referral link](https://runpod.io?ref=zqgj8it7)._

If you only need to transcribe a short video, you can also use [Google Colab](https://colab.research.google.com/) for free, since it offers a few hours of GPU access for free.

### 2) Manual Transcription Fixes

Since the transcription contains some errors in both contents and timing (although I have to say that the results are around 95% correct, which is insanely impressive), we need to fix those.
My tool of choice is [Kdenlive](https://kdenlive.org/en/), since it's the video editor I'm pretty comfortable with and has good tools for editing subtitles.

I don't really have much to write here -- to edit the subtitles, just drag & drop the video + subtitles and hit play, fixing mistakes along the way.
_Note that doing this for a 30-minute episode usually takes me around 1 hour, so if it takes you 10 you're doing something wrong and if it takes you 5 minutes please tell me how._

One helpful thing that I discovered after translating the first ~3 episodes is that Whisper can sometimes produce consistent incorrect results, which you can fix automatically for all future episodes -- in my case, the names of the lead characters (mainly Ivuška and Ozzák) made rise to the following replacement rules:
```text
ozák -> Ozzák
Ozák -> Ozzák
ivošk -> Ivušk
Ivošk -> Ivušk
```

Yet again, here is a Python script that automatically does this for subtitle files in all subdirectories of wherever you're launching it from:

{{< details "Code" "replacements.py" >}}{{< /details >}}


### 3) Translation
For a reasonably fast and accurate Czech to English translation, one way is to use a local LLM model for line-by-line translation.
I've experimented with Whisper's translation functionality, but it creates problems with timing (since I wanted it to be the same as the Czech subtitles), as well as not being too good.

I will be using [ollama](https://ollama.com/) with the [Mistral 7B](https://mistral.ai/news/announcing-mistral-7b/), which again requires **around ~8 GB of VRAM**.
_If you don't have this, I would again recommend using [Runpod](https://runpod.io?ref=zqgj8it7)._

To install, run the following (ideally read what the script does first before you pipe it to `sh`):
```fish
curl -fsSL https://ollama.com/install.sh | sh
```

To perform the translation, we will again run a script in the directory with the videos:

{{< details "Code" "translate.py" >}}{{< /details >}}


### 4) Manual Translation Fixes

Open the subtitles in your favorite text editor (`vim`) and fix away.


### 5) Credits

I also added a link to the page with all Comeback subtitles at the beginning of each individual subtitles, in case people obtain them from somewhere else and would like to get them for other episodes:

{{< details "Code" "credits.py" >}}{{< /details >}}


[^1]: Watching the show back, I have to admit that certain episodes are a little rough to watch and could be considered problematic in today's day and age. Watch at your own peril.

[^2]: <p>Well... almost all:</p><p class="tiny"><em>Afrikaans, Albanian, Amharic, Arabic, Armenian, Assamese, Azerbaijani, Bashkir, Basque, Belarusian, Bengali, Bosnian, Breton, Bulgarian, Burmese, Cantonese, Castilian, Catalan, Chinese, Croatian, Czech, Danish, Dutch, English, Estonian, Faroese, Finnish, Flemish, French, Galician, Georgian, German, Greek, Gujarati, Haitian, Haitian Creole, Hausa, Hawaiian, Hebrew, Hindi, Hungarian, Icelandic, Indonesian, Italian, Japanese, Javanese, Kannada, Kazakh, Khmer, Korean, Lao, Latin, Latvian, Letzeburgesch, Lingala, Lithuanian, Luxembourgish, Macedonian, Malagasy, Malay, Malayalam, Maltese, Maori, Marathi, Moldavian, Moldovan, Mongolian, Myanmar, Nepali, Norwegian, Nynorsk, Occitan, Panjabi, Pashto, Persian, Polish, Portuguese, Punjabi, Pushto, Romanian, Russian, Sanskrit, Serbian, Shona, Sindhi, Sinhala, Sinhalese, Slovak, Slovenian, Somali, Spanish, Sundanese, Swahili, Swedish, Tagalog, Tajik, Tamil, Tatar, Telugu, Thai, Tibetan, Turkish, Turkmen, Ukrainian, Urdu, Uzbek, Valencian, Vietnamese, Welsh, Yiddish, Yoruba.</em></p>
