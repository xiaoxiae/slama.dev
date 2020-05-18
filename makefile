.PHONY:  all clean build upload serve
.SILENT:

XOPP = $(shell find _includes/ -type f -name '*.xopp')
SVG = $(patsubst %.xopp, %.svg, $(XOPP))

all: build upload

build: $(SVG)
	scripts/katex_server/start
	bundle exec jekyll build --trace
	scripts/katex_server/stop

serve: $(SVG)
	scripts/katex_server/start
	trap "scripts/katex_server/stop; exit 0" 2
	bundle exec jekyll serve

%.svg: %.xopp
	scripts/xopp_to_svg -f $^

upload: ; scripts/upload

clean: ; bundle exec jekyll clean --trace
