---
title: Home
layout: default
order: 0
css: index
no-heading: True
---

## Hi everyone!

I'm Tom and this is my personal website.

I am a Czech student, currently getting a master's degree at the [Heidelberg University](https://www.uni-heidelberg.de/en) in Germany.
Besides programming, I like to play computer games, [take photos](/photos/), [make videos](/videos/) and [rock climb](/climbing/).

This website contains things I feel are interesting enough to put on the internet.
The language is English, but some posts might be written in other languages (and will be denoted as such).
Links to the sections of the website can be found at the top, links to the posts can be found below.
{% for post in site.posts %}
{% assign currentdate = post.date | date: "%Y" %}
{% if currentdate != date %}
{% if date %}
</div>
{% endif %}

### {{ currentdate }}
<div class="spacer"> <!-- done to reset the (2n+1)-th child counter -->
{% assign date = currentdate %} 
{% endif %}
{% unless post.hidden %}
<ul class="hfill">
	<li>
	{% if post.language == "cz" %}🇨🇿 {% endif%}
	<a href="{{ post.url }}">{{ post.title}}</a>
	</li>
	<li>
    <span class="post-attributes">
	{% if post.pdf or post.pdf-nogenerate %} <a href="/assets/{{post.url | split: "/" | last}}.pdf">PDF</a> |{% endif %}
	{% if post.category_noslug %} {{post.category_noslug}}
	{% elsif post.category%} {{post.category}}{% if post.category_part %} [{{post.category_part}}]{% endif %}{% endif %}
    {% if post.category_icon %} <img class='category-icon' src='{{post.category_icon}}'/>{% endif %}
    </span>
	<span class="nowrap">{{ post.date  | date: "%-d. %-m."}}</span>
	</li>
</ul>
{% endunless %}
{% endfor %}

<div class="spacer"></div>
