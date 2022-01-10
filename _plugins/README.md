# `_plugins/`
A folder full of magical scripts that
- build and optimize parts of the website
- define tags used in the articles
- that's it

---

- `climbing.py`
	- edits new climbing videos using `ffmpeg` (see the climbing folder)
	- generates `climbing/<zone number>.md` with climbing videos for the given zone
- `compress_images.py`
	- compresses new images added to `photography.md`
- `katex.rb`
	- typesets `\(...\)` and `\[...\]` math
- `projects.py`
	- generates `_includes/projects.md` -- a select few of my project do showcase on my website
- `pyhook.rb`
	- Ruby hook for Python scripts that gets executed before the website is generated
	- runs most of the Python scripts mentioned here
- `rick_roll.py`
	- <REDACTED>
- `xopp_to_svg.py`
	- converts a Xournal++ sketch into an SVG image
- `pdf.py`
	- converts articles with `pdf: true` in their header to PDF
- `tags/`
	- `inline_highlight.rb`
		- tag for inline code highlight
	- `lecture_notes_preface.rb`
		- tag for prefacing any lecture notes
	- `math.rb`
		- tag for typesetting math
	- `photos.rb`
		- tag for typesetting photos
	- `xopp.rb`
		- tag for typesetting Xournal++ images
