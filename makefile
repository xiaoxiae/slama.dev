.PHONY:  all clean build upload serve
.SILENT:

XOPP = $(shell find _includes/ -type f -name '*.xopp')
SVG  = $(patsubst %.xopp, %.svg, $(XOPP))

all: build upload

build: $(SVG) _includes/cv.html _includes/songs.md; bundle exec jekyll build --trace
serve: $(SVG) _includes/cv.html _includes/songs.md; bundle exec jekyll serve --trace --drafts

upload: ; scripts/upload

clean:
	rm -r .katex-cache/
	bundle exec jekyll clean --trace

%.svg: %.xopp
	scripts/xopp_to_svg -f $^

_includes/cv.html: scripts/generate_cv; scripts/generate_cv
_includes/songs.md: scripts/rick_roll; scripts/rick_roll
