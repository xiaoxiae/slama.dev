.PHONY:  all setup clean build upload serve permissions
.SILENT:

XOPP = $(shell find _includes/ -type f -name '*.xopp')
SVG  = $(patsubst %.xopp, %.svg, $(XOPP))


all: build upload

xopp: $(SVG);
build: permissions $(SVG); ! ps -aux | grep "ruby.*jekyll" | grep -v grep -q && bundle exec jekyll build --trace || (echo "ERROR: Jekyll seems to be running already." && exit 1)
serve: permissions $(SVG); ! ps -aux | grep "ruby.*jekyll" | grep -v grep -q && bundle exec jekyll serve --trace --drafts --config _config.yml,_config-local.yml || (echo "ERROR: Jekyll seems to be running already." && exit 1)

upload: check
	cd _site && git add . && git commit -m "automated commit" && git push -f

check:
	! grep -R "localhost:4000" _site/**/*.html && echo "     Check passed: No 'localhost:4000' found." || (echo "ERROR: Found 'localhost:4000' in HTML files, not uploading!" && exit 1)

clean:
	bundle exec jekyll clean --trace

%.svg: %.xopp
	_plugins/xopp_to_svg.py -f $^
