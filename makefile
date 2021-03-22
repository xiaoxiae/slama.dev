.PHONY:  all clean build upload serve
.SILENT:

XOPP = $(shell find _includes/ -type f -name '*.xopp')
SVG  = $(patsubst %.xopp, %.svg, $(XOPP))

all: build upload

build: $(SVG); jekyll build --trace
serve: $(SVG); jekyll serve --trace --drafts

upload:
	cd _site && git a . && git c -m "automated commit" && git push

clean:
	rm -r .katex-cache/
	jekyll clean --trace

%.svg: %.xopp
	_plugins/xopp_to_svg.py -f $^
