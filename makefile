.PHONY: all clean build upload

all: build upload

build:
	bundle exec jekyll build --trace

upload:
	scripts/upload

clean:
	bundle exec jekyll clean --trace
