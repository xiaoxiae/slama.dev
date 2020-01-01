---
title: Home
layout: default
order: 0
---

## Hi everyone!

My name is Tom and this is my personal website.

I am a student from the Czech Republic, currently getting a bachelor's degree at [MFF UK](https://www.mff.cuni.cz/en).
Besides programming, I also like to play the viola, chess and [take photos](https://www.instagram.com/tomas.slama/).
As for sports, I really enjoy climbing, slacklining and snowboarding.

This website contains posts about things I feel are interesting enough to put on the internet.
Links to the periodically updated ones can be found at the top; the rest can be found here: 
{% assign posts = site.posts | sorted %}
{% for post in posts %}
- [{{ post.title}}]({{ post.url }}) ({{ post.date  | date: "%-d. %-m. %Y"}})
{% endfor %}

{: .right}
Enjoy! ❤️
