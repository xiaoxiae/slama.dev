.PHONY:  all clean build upload serve
.SILENT:

XOPP = $(shell find _includes/ -type f -name '*.xopp')
SVG  = $(patsubst %.xopp, %.svg, $(XOPP))

all: build upload

build: $(SVG); bundle exec jekyll build --trace
serve: $(SVG); bundle exec jekyll serve --trace --drafts

upload: ; _plugins/smart_ftp_upload.py 89.221.213.50 w220316 `secret-tool lookup service "slama.dev"`

clean:
	rm -r .katex-cache/
	bundle exec jekyll clean --trace

%.svg: %.xopp
	_plugins/xopp_to_svg.py -f $^
