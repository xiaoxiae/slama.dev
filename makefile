.PHONY:  all clean build upload serve
.SILENT:

XOPP = $(shell find _includes/ -type f -name '*.xopp')
SVG  = $(patsubst %.xopp, %.svg, $(XOPP))

all: build upload

xopp: $(SVG);
build: $(SVG); jekyll build --trace
serve: $(SVG); jekyll serve --trace --drafts --config _config.yml,_config-local.yml

upload:
	cd _site && git a . && git c -m "automated commit" && git push -f

clean:
	jekyll clean --trace

%.svg: %.xopp
	_plugins/xopp_to_svg.py -f $^
