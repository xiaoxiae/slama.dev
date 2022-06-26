---
title: Home
layout: default
order: 0
css: index
no-heading: True
---

## Hi everyone!

I'm Tom and this is my personal website.

I am a student from the Czech Republic, currently getting a bachelor's degree at [MFF UK](https://www.mff.cuni.cz/en).
Besides programming, I also like to play computer games, [take photos](/photos/) and [rock climb](climbing/).

This website contains things I feel are interesting enough to put on the internet.
The language of the blog is English, but some posts might be written in other languages (and will be denoted as such).
Links to the periodically updated ones can be found at the top; the rest can be found below.
{% for post in site.posts %}
{% assign currentdate = post.date | date: "%Y" %}
{% if currentdate != date %}
{% if date %}
<div class="spacer"></div>
{% endif %}

### {{ currentdate }}
{% assign date = currentdate %} 
{% endif %}
{% unless post.hidden %}
<ul class="hfill">
	<li>{% if post.language == "cz" %}🇨🇿 {% endif%} <a href="{{ post.url }}">{{ post.title}}</a>{% if post.category_noslug %} [{{post.category_noslug}}]{% elsif post.category%} [{{post.category}}]{% endif%}{% if post.pdf or post.pdf-nogenerate %} [<a href="/assets/{{post.url | split: "/" | last}}.pdf">PDF</a>]{% endif%}</li>
	<li>{{ post.date  | date: "%-d. %-m. %Y"}}</li>
</ul>
{% endunless %}
{% endfor %}

<div class="spacer"></div>

---

{:.center}
Also, I'll just leave this here for the time being.

{:.no-invert}
![](assets/putin.webp)
