---
layout: post
---

As a university student majoring in computer science and someone who loves to ~~complicate~~ simplify everyday tasks, I wasn't really satisfied with the way I used to manage my notes while attending High School. So during the summer of 2019 (before entering college), decided to develop a handy little set of asripts to manage things regarding my education.

In this post, I'll explain how my setup works, what I use it for and why you should consider developing something similar for your personal use.

Parts of my setup are inspired by the well-written [„How I manage my LaTeX lecture notes“](https://castel.dev/post/lecture-notes-3/) article by [Gilles Castel](https://castel.dev/). Feel free to check it out if you want a different take on a similar subject!

### Overview
Running `py school.py` (or simply `school` in my Shell) yields the following:

```
A multi-purpose script for simplifying my MFF UK education.

supported options:
  {list}
    {courses}       List information about the courses.
    {finals}        List dates of all finals.
  {compile}
    {cron}          Add crontab notifications for all courses.
    {notes}         Run md_to_pdf script on all course notes.
  {open}
    {folder}        Open the course's folder in Ranger.
    {website}       Open the course's website in FireFox.
    {notes}         Open the course's notes in Xournal++.
```

Listing my finals:
```
xiaoxiae@thinkpad-e11 ~> school l c th
╭────────────────────────────◀ Finals! ▶────────────────────────────╮
│ Úvod do počítačových sítí  │  8. 1. 2020 │ 15:40 │ done │ S5  │ 2 │
│ Diskrétní matematika       │ 16. 1. 2020 │ 10:00 │ done │ S3  │ 3 │
│ Principy počítačů          │ 22. 1. 2020 │ 13:00 │ done │ S3  │ 3 │
│ Algoritmizace              │ 24. 1. 2020 │  9:00 │ done │ S9  │ - │
│ Lineární algebra 1         │ 29. 1. 2020 │  8:45 │ done │ S1  │ 4 │
│ Základy počítačové grafiky │  3. 2. 2020 │  9:00 │ done │ SW2 │ - │
╰───────────────────────────────────────────────────────────────────╯
```

Displaying my schedule for thursday:
```
xiaoxiae@thinkpad-e11 ~> school l c th
╭─────────────────◀ Čtvrtek / 6. 2. ▶──────────────────╮
│ Diskrétní matematika    │ p │ 10:40 - 12:10 │ S5 │ 2 │
│ Lineární algebra 1      │ p │ 12:20 - 13:50 │ S3 │ 3 │
│ Programování 1          │ c │ 14:00 - 15:30 │ S8 │ 1 │
│ Úvod do řešení problémů │ c │ 19:19 - 21:50 │ S3 │ 3 │
╰──────────────────────────────────────────────────────╯
```


Opening a course's website in FireFox and its folder in Ranger:
```
xiaoxiae@thinkpad-e11 ~> school o w dm-c
xiaoxiae@thinkpad-e11 ~> school o n dm-c
```


