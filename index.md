---
title: Home
layout: default
order: 0
css: index
no-heading: True
icon: fa-house
---

<a href="https://protab.cz/" class="promo-banner protab-banner">
	<span class="promo-text"><strong>ProTab 2025</strong> – Letní <strong>programátorský tábor</strong> pro středoškoláky, který každým rokem organizuji s partou fajn lidí. Pojeďte na super akci! ️❤️ </span>
	<span class="promo-cta">Více info →</span>
</a>

## Hi everyone!

I'm Tom and this is my personal website.

I'm a full-stack developer at **[Freya Voice](https://freyavoice.ai/)**, working on **[Climbuddy](https://climbuddy.com)** in my spare time.

Besides programming, I like to play <a class='secret' href='/assets/nolife.webp'>video games</a>, [take photos](/photos/), [make videos](/videos/) and [rock climb](/climbing/).

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

<div class="spacer">
{% assign date = currentdate %}
{% endif %}
{% unless post.hidden %}
<div class="post-item">
	<div class="post-header">
		<div class="post-title-row">
    	{% if post.category_icon %}<img class='icon' src='{{post.category_icon}}' alt="Category icon"/>{% endif %}
			{% if post.pdf or post.pdf-nogenerate %}<a href="/assets/{{post.url | split: "/" | last}}.pdf" class="post-icon" aria-label="Download PDF"><i class="fa-solid fa-file-pdf" aria-hidden="true"></i></a>{% endif %}
			{% if post.language == "cz" %}<span class="language-flag">🇨🇿</span>{% endif %}
			<span class="post-title-link">
			{% if post.redirect.to %}
				{% if post.draft %}
					<a href="{{ post.redirect.to }}" class="red main-link"><strong>{{ post.title}}</strong> <i class="fa-solid fa-arrow-up-right-from-square" aria-hidden="true"></i></a>
				{% else %}
					<a href="{{ post.redirect.to }}" class="main-link"><strong>{{ post.title}}</strong> <i class="fa-solid fa-arrow-up-right-from-square" aria-hidden="true"></i></a>
				{% endif %}
			{% else %}
				{% if post.draft %}
					<a href="{{ post.url }}" class="red main-link"><strong>{{ post.title}}</strong></a>
				{% else %}
					<a href="{{ post.url }}" class="main-link"><strong>{{ post.title}}</strong></a>
				{% endif %}
			{% endif %}
			</span>
			{% if post.category %}<span class='category-tag'>[{{ post.category }}{% if post.category_part %} <span class='mono'>{{post.category_part}}</span>{% endif %}]</span>{% elsif post.category_part %}<span class='category-tag'>[<span class='mono'>{{post.category_part}}</span>]</span>{% endif %}
		</div>
		<div class="post-date">
			<span markdown="1">{{ post.date  | date: "%-d. %-m."}}</span>
		</div>
	</div>
	{% if post.excerpt %}
	<div class="post-excerpt">
		{{ post.excerpt | strip_html }}
	</div>
	{% endif %}
</div>
{% endunless %}
{% endfor %}

<div class="spacer"></div>
