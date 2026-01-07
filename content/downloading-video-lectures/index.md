---
date: '2021-02-19'
title: Downloading video lectures
description: A short post about how to download video lectures from various websites.
toc: true
---

### Preface
This post is **not** about how to illegally download lectures to share them online, since it's something you obviously shouldn't do (for both moral and legal reasons).

It is instead meant for people who would like to download videos for offline viewing, when the sites they're viewing them on don't support this by default. They usually do this for reasons mentioned above, which is frustrating for people who:
- would rather use a video player of their choice
- have a bad internet connection and so can't view the video without lagging
- want to view it later when they won't have an internet connection

#### Regular websites
When you start viewing a video on a website's media player and don't see an obvious way to download it, there is a high chance that it plays the video using a [`.m3u`](https://en.wikipedia.org/wiki/M3U) file that it first downloads. You can check this by going to the `Network` tab of your browser (`F12` for Firefox/Chrome), refreshing the page and looking for a file that ends with `m3u8`.

If it does, then downloading it is easy -- use [`ffmpeg`](https://ffmpeg.org/) with the following parameters:

```bash
ffmpeg -i "<URL of the .m3u8 file>" <output file name>.mp4
```

#### YouTube (and [a few others](https://ytdl-org.github.io/youtube-dl/supportedsites.html))
The steps above don't work on YouTube, because it uses its own methods for displaying the video in your browser. Luckily, you can use [`yt-dlp`](https://github.com/yt-dlp/yt-dlp) (formally `youtube-dl`):

```bash
yt-dlp "<URL of the YouTube video>"
```

#### Microsoft Stream
Same problem as with YouTube, different program -- use [`destreamer`](https://github.com/snobu/destreamer):

```bash
destreamer -i "<URL of the Microsoft Stream video>"
```
