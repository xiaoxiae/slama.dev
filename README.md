# slama.dev (Hugo)

## Prerequisites

- [Hugo](https://gohugo.io/installation/) (extended version)
- [uv](https://docs.astral.sh/uv/getting-started/installation/) (Python, ruff)
- [Node.js](https://nodejs.org/) (html-validate, pa11y, prettier)
- [lychee](https://github.com/lycheeverse/lychee) (link checking)

## Contributing

To check how changes look on the website, [install Hugo](https://gohugo.io/installation/) and run

```bash
./site serve
```

Note that while this will build the website, it will look broken since the full build requires gigabytes of static files.
However, text elements, math, and general structure will be fine, so you can check that changes you make work.
