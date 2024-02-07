---
title: The Thinkpad Haunting of '24
excerpt: "When strange things happen to laptops."
---

- .
{:toc}

Over the course of last year, my laptop has been experiencing strange issues.
An occasional app crash here, a failed command there.
Some bits were simply not bitting.

All of these issues had a common source and are all gone now.
You can [skip to the end](#the-culprit--solution) if you want to find out what caused it, but I thought it would be more interesting to write it in the way I experienced it (i.e. only describing the issues) so you can try to figure it out just like I did.

### 1. App Crashes
Certain apps (Firefox, Beeper, Thunderbird) would occasionally crash.
This was especially annoying and frequent for Firefox, since it most often happened when opening a new tab for certain more demanding websites (i.e. YouTube).
Furthermore, re-launching the app would sometimes make it crash again and again, whereas other times it would start without any issues.

For FireFox, my first thought was that it had something to do with the large collection of add-ons I've accumulated over the years, but disabling them made no difference -- it kept crashing.
Looking through other general fixes (you can't find very many quality answers when the question is _"Firefox keeps crashing"_) didn't help either.

Since Beeper is still in beta, I chalked its crashes to this fact and left it at.

### 2. Can't Pull a Docker Image
Pulling a Docker image from Docker Hub would fail every time, for various different (yet equally strange) reasons.
The two major ones were
1. `archive/tar: invalid tar header` (after the entire image is pulled)
2. `corrupt input before offset` from `zlib` (individual layers)

Looking at the specific errors in question yielded answers where this happened due to other circumstances (like an image being actually corrupted since it was saved incorrectly), but once again weren't too helpful.

### 3. Corrupted Website Files
When making this website, certain images would, from time to time, **contain flipped bits.**
This was extremely strange since (theoretically) they should have just been copied straight from the source without any modification, yet this was clearly not happening.

I almost cried when trying to debug this, since there was quite literally nothing to off of
- the issue would immediately go away with a rebuild (it happened very infrequently)
- nobody experienced anything even remotely close to this when using Jekyll

What the fuck.

### 4. Jupyter Kernel Crashes
Working on homework for [Generative Neural Networks](/notes/generative-neural-networks/) involved a lot of Pytorch work in Jupyter.
Doing this on my desktop was not an issue and was much faster since it was GPU-enabled, but running the same code on the laptop (with the `cpu` device) would result in the kernel frequently crashing, namely:
- after model is done training (crashes in the middle were extremely infrequent),
- when creating larger datasets (that didn't take a trivial amount of memory),
- _if I looked at it in a funny way_ 👀

Probably just my laptop not being powerful enough, I guess?

### The Culprit & Solution

Running `memtester 1G 5` revealed this very quickly:

```
memtester version 4.6.0 (64-bit)
Copyright (C) 2001-2020 Charles Cazabon.
Licensed under the GNU General Public License version 2 (only).

pagesize is 4096
pagesizemask is 0xfffffffffffff000
want 1024MB (1073741824 bytes)
got  1024MB (1073741824 bytes), trying mlock ...locked.
Loop 1/5:
  Stuck Address       : testing   0FAILURE: possible bad address line at offset 0x0000000036625be8.
Skipping to next test...
  Random Value        : FAILURE: 0xbfb51836fedf7f5a != 0xbfb51832fedf7f5a at offset 0x0000000016626098.
FAILURE: 0xfed89902dfffd66b != 0xfed89903dfffd66b at offset 0x0000000016626328.
FAILURE: 0x7fbfc604fefa8244 != 0x7fbfc605fefa8244 at offset 0x0000000016626358.
FAILURE: 0x5bf61f7ff3f39e3b != 0x5bf61f7bf3f39e3b at offset 0x0000000016626378.
FAILURE: 0x7fffc8917eaf0fed != 0x7fffc8947eaf0fed at offset 0x00000000166263b8.
FAILURE: 0xfbf4a74ff3c5ede2 != 0xfbf4a74bf3c5ede2 at offset 0x0000000016626428.
FAILURE: 0x69fe8e03db7f61ca != 0x69fe8e07db7f61ca at offset 0x0000000016626438.
FAILURE: 0xeff3736b67df00fd != 0xeff3736f67df00fd at offset 0x0000000016626448.
FAILURE: 0x77d9df21fff778ab != 0x77d9df20fff778ab at offset 0x0000000016626478.
FAILURE: 0xf2d25fe269de8478 != 0xf2d25fe669de8478 at offset 0x0000000016626730.
FAILURE: 0xe77b6981fb6f5959 != 0xe77b6980fb6f5959 at offset 0x0000000016626768.
...
```

**Dead RAM.**

I ran the command simply out of curiosity without expecting errors but, to my surprise, there were quite a few of them.
For some reason, I thought that having bad memory means that the system won't even load, not that things will just silently die, but alas I was wrong (and honestly this makes much more sense).

Hindsight is 20/20 and running memtests is free. Get tested!

---

So, what next?

The obvious solution would be to replace the RAM, since one sector being bad can be an indicator that others will go too.
However, since I have a [ThinkPad X1 Carbon](https://wiki.archlinux.org/title/Lenovo_ThinkPad_X1_Carbon_(Gen_6)) which has the RAM soldered on, this is not an option.
Since I also really didn't want to buy a new laptop, I needed a software solution.

_Many thanks to my friend [David Koňařík](https://gitlab.com/dvdkon) for help with most of this._

Luckily, memory going bad is something that usually happens after long usage and Linux supports[^1] this on the kernel level via the [`memmap`](https://www.kernel.org/doc/html/v5.4/admin-guide/kernel-parameters.html) kernel command line parameter.

To disable using the bad part of the memory, I did the following:
1. **run [MemTest86](https://www.memtest86.com/) to find the bad physical addresses**
    - you can boot it from a flash-drive or Grub also has it built-in (at least mine had)
    - I used my phone to capture the output and wrote the addresses down manually; it sounds very stupid but it works pretty well and I don't know a better solution
    - in my case, the bad addresses were all in the range `0x316C540E0 - 0x316C57F50`
2. **disable the bad sectors via kernel command line parameters;** for Grub:
    - open `/etc/default/grub`
    - add `memmap=0x10000\\\$0x316C50000` to `GRUB_CMDLINE_LINUX_DEFAULT`
        - the syntax is `size&start`, so this covers all of the bad addresses
        - note the triple escape; one is shell and one is for the argument itself
    - run `update-grub`
    - reboot
3. **run `memtester` with as much RAM as possible**
    - mostly a sanity check to make sure that the memory works fine

[^1]: From my understanding, this is not the explicit use case -- `memmap` simply marks a part of the memory as **reserved**, which tells the kernel not to use it. This means that it won't be used when the system is running, which is what we wanted, but a normal use case might be that some other device is using that part of memory and we don't want to mess with it.

