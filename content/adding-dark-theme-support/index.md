---
date: '2020-01-02'
title: Adding Dark Theme Support
description: A short post about how to add a dark website theme via CSS.
toc: true
---

I've been meaning to add dark theme support to this website for quite a while. I even made a whole CSS class, but didn't know how to actually integrate it into the website (having both the light and the dark theme, that is). All of the options that I thought about (cookie, local storage, weird CSS hacks) were ugly, complicated, involved JavaScript, and were an overall no-no for a website that aims to be as simple as possible.

After some time and a bit more research, I stumbled upon the miraculous [`prefers-color-scheme`](https://developer.mozilla.org/en-US/docs/Web/CSS/@media/prefers-color-scheme#Result) CSS media query that triggers depending on the color scheme preferences of the user's browser -- exactly what I wanted!

Here is an example that sets the background to black and text to white when the dark theme preference is specified:

```scss
@media (prefers-color-scheme: dark) {
	body {
		color: white;
		background-color: black;
	}
}
```

### Setting the browser theme
It seems that setting dark theme for a given system will set up the browser theme preference automatically, but if your system doesn't support this or you prefer to only set the browser theme, here is how:

#### FireFox (>= 67)
1. go to `about:config`
2. create a new variable `ui.systemUsesDarkTheme` and set it to `1`

#### Chrome (>= 76)
1. run with the `--force-dark-mode` flag

### Support
It seems that this CSS option has been getting attention only recently, so it might take a while for the browsers to adopt it in a more user-friendly way, since it's just so much better than having to deal with JavaScript.

That being said, if you have your browser configured accordingly, you should be seeing this website in its dark theme 🌙.
