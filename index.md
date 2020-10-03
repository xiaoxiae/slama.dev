---
title: Home
layout: default
order: 0
---

## Hi everyone!

I'm Tom and this is my personal website.

I am a student from the Czech Republic, currently getting a bachelor's degree at [MFF UK](https://www.mff.cuni.cz/en).
Besides programming, I also like to play the viola, dance, [take photos](/photography/) and [rock climb](climbing/).

This website contains things I feel are interesting enough to put on the internet.
The language of the blog is English, but some posts might be written in other languages.
Links to the periodically updated ones can be found at the top; the rest can be found below.
{% for post in site.posts %}
{% assign currentdate = post.date | date: "%Y" %}
{% if currentdate != date %}
### {{ currentdate }}
{% assign date = currentdate %} 
{% endif %}
{% if post.category != 'TIL' %}
- {% if post.language %}[{{post.language | upcase}}] {% endif%}[{{ post.title}}]({{ post.url }}) ({{ post.date  | date: "%-d. %-m. %Y"}}{% if post.category %}; {{post.category}}{% endif%})
{% endif %}
{% endfor %}

### Tom's Intro to Linux
{% for post in site.posts %}
{% if post.category == 'TIL' %}
- [{{ post.title}}]({{ post.url }}) ({{ post.date  | date: "%-d. %-m. %Y"}})
{% endif %}
{% endfor %}
