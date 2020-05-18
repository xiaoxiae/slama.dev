.PHONY: all clean build upload serve

XOPP = $(shell find _includes/ -type f -name '*.xopp')
SVG = $(patsubst %.xopp, %.svg, $(XOPP))

.PHONY: all
all: $(MP3_FILES)

%.svg: %.xopp
	scripts/xopp_to_svg -f $^

all: $(SVG) build upload 

build:
	scripts/katex_server/start
	bundle exec jekyll build --trace
	scripts/katex_server/stop

serve:
	scripts/katex_server/start
	bundle exec jekyll serve
	scripts/katex_server/stop

upload:
	scripts/upload

clean:
	rm (find _includes/ -type f -name "*.svg")
	bundle exec jekyll clean --trace

