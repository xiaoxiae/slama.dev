.PHONY:  all clean build upload serve
.SILENT:

XOPP = $(shell find _includes/ -type f -name '*.xopp')
SVG  = $(patsubst %.xopp, %.svg, $(XOPP))

all: build upload

build: $(SVG) bundle exec jekyll build --trace
serve: $(SVG) bundle exec jekyll serve --trace --drafts

upload: ; scripts/upload

clean:
	rm -r .katex-cache/
	bundle exec jekyll clean --trace

%.svg: %.xopp
	scripts/xopp_to_svg -f $^
