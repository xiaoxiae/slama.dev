.PHONY:  all clean build upload
.SILENT:

XOPP = $(shell find _includes/ -type f -name '*.xopp')
SVG = $(patsubst %.xopp, %.svg, $(XOPP))

all: build upload

_includes/cv.md: ; scripts/generate_cv

build: $(SVG) _includes/cv.md
	bundle exec jekyll build --trace

%.svg: %.xopp
	scripts/xopp_to_svg -f $^

upload: ; scripts/upload

clean: ; bundle exec jekyll clean --trace
