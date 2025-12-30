---
date: '2024-12-30'
title: "Jekyll to Hugo Migration: A Comprehensive Comparison"
description: "A detailed breakdown of all the differences encountered when migrating slama.dev from Jekyll to Hugo."
draft: true
toc: true
---

## 1. Directory Structure

| Aspect | Jekyll | Hugo |
|--------|--------|------|
| Posts | `_posts/YYYY-MM-DD-slug.md` (flat files) | `content/slug/index.md` (page bundles) |
| Layouts | `_layouts/` | `layouts/_default/` |
| Includes/Partials | `_includes/` | `layouts/partials/` |
| Styles | `_sass/` | `assets/scss/` |
| Plugins | `_plugins/` (Ruby + Python) | `scripts/` (Python only) |
| Static files | `assets/` | `static/` + `assets/` |
| Data | Inline YAML / generated markdown | `data/` directory (YAML files) |
| Config | `_config.yml` + `_config-local.yml` | `config/_default/hugo.toml` + `config/development/` |
| Output | `_site/` | `public/` |
| i18n | None (custom Ruby logic) | `i18n/en.yaml`, `i18n/cs.yaml` |

---

## 2. Frontmatter Changes

| Field | Jekyll | Hugo |
|-------|--------|------|
| Date | In filename (`2021-01-07-slug.md`) | Explicit `date: '2021-01-07'` |
| Title | Derived from filename or explicit | Always explicit `title:` |
| Excerpt | `excerpt:` | `description:` |
| TOC | Inline `{:toc}` (Kramdown) | Frontmatter `toc: true` |
| Custom fields | Same (`end:`, `css:`, etc.) | Same (accessed via `.Params.`) |

---

## 3. Template Syntax

| Feature | Jekyll (Liquid) | Hugo (Go templates) |
|---------|-----------------|---------------------|
| Variable access | `{{ page.title }}` | `{{ .Title }}` or `{{ .Params.title }}` |
| Site config | `{{ site.title }}` | `{{ site.Title }}` |
| Conditionals | `{% if %}...{% elsif %}...{% endif %}` | `{{ if }}...{{ else if }}...{{ end }}` |
| Loops | `{% for x in y %}...{% endfor %}` | `{{ range y }}...{{ end }}` |
| Assignment | `{% assign x = y %}` | `{{ $x := y }}` |
| Filters | `{{ x \| filter_name }}` | `{{ x \| functionName }}` |
| Includes | `{% include "file" %}` | `{{ partial "file" . }}` |
| Comments | `{% comment %}...{% endcomment %}` | `{{/* ... */}}` |
| Null check | `{% if x %}` | `{{ with x }}...{{ end }}` |
| String contains | `contains` | `strings.Contains` |
| Absolute URL | `\| absolute_url` | `\| absURL` |

---

## 4. Custom Tags → Shortcodes

| Tag | Jekyll Syntax | Hugo Syntax |
|-----|---------------|-------------|
| Math blocks | `{% math theorem "name" %}...{% endmath %}` | `{{</* math "theorem" "name" */>}}...{{</* /math */>}}` |
| Photo row | `{% photorow %}img1\|img2{% endphotorow %}` | `{{</* photo_row "img1\|img2" */>}}` |
| Inline highlight | `{% ihighlight python %}...{% endihighlight %}` | `{{</* inline_highlight "python" */>}}...{{</* /inline_highlight */>}}` |
| Video embed | `{% manim_video name %}` | `{{</* video "manim" "name" */>}}` |
| Chess | `{% chess %}...{% endchess %}` | `{{</* chess */>}}...{{</* /chess */>}}` |

### Implementation differences

- **Jekyll:** Ruby classes extending `Liquid::Tag` or `Liquid::Block`
- **Hugo:** Go template files in `layouts/shortcodes/`
- Hugo unified `manim_video` and `motion_canvas_video` into single `video` shortcode with type parameter

---

## 5. Build Process

| Step | Jekyll | Hugo |
|------|--------|------|
| Pre-build | Ruby hooks execute Python scripts | Direct Python calls via `uv run` |
| Main build | `bundle exec jekyll build` | `hugo --minify --cleanDestinationDir` |
| Post-build | PDF generation (per-post hook) | Honeypot generation (`secrets.py`) |
| Dev server | `jekyll serve --incremental --livereload` | `hugo server --buildDrafts` |
| Dev port | 4000 | 1313 |

### Hook system

- **Jekyll:** `Jekyll::Hooks.register :site, :after_init` and `:posts, :post_render`
- **Hugo:** No hooks - Python scripts called before/after Hugo in shell script

---

## 6. Plugin/Script Migration

| Script | Jekyll Location | Hugo Location | Status |
|--------|-----------------|---------------|--------|
| climbing_journal.py | `_plugins/` → `_includes/diary.md` | `scripts/` → `data/climbing/journal.yaml` | Ported (data-driven) |
| climbing_videos.py | `_plugins/` | `scripts/` | Ported |
| photos.py | `_plugins/` → `_includes/photos.md` | Not ported | Missing |
| pdf.py | `_plugins/` (post_render hook) | Not ported | Missing |
| compress_images.py | `_plugins/` | Not needed (Hugo image processing) | Replaced |
| resize.py | `_plugins/` | Not needed (Hugo image processing) | Replaced |
| aoc.py | `_plugins/` | Not ported | Missing |
| secrets.py | N/A | `scripts/` | New in Hugo |
| cv generation | `_plugins/cv/` submodule | Not ported | Missing |

---

## 7. Asset Handling

| Aspect | Jekyll | Hugo |
|--------|--------|------|
| SCSS compilation | Jekyll built-in Sass | Hugo Pipes (`toCSS`) |
| CSS output | Multiple files (per-page CSS) | Single minified `main.css` |
| Image processing | Manual (Python scripts) | Built-in (`resources.GetMatch`, WebP conversion) |
| Cache busting | None | Content hashes on processed images |
| Minification | Not automatic | `--minify` flag |
| Source maps | Generated | None (production-focused) |

---

## 8. Content Organization Pattern

**Jekyll:** Generated markdown files in `_includes/`
```
Python script → _includes/diary.md → {% include diary.md %}
```

**Hugo:** Data files consumed by templates
```
Python script → data/climbing/journal.yaml → {{ range .Site.Data.climbing.journal }}
```

---

## 9. Internationalization

| Aspect | Jekyll | Hugo |
|--------|--------|------|
| Language detection | `page.language` check in Ruby | `.Language.Lang` in templates |
| Translations | Hardcoded in Ruby tag classes | `i18n/en.yaml`, `i18n/cs.yaml` |
| Usage | Custom `TAG_MAPPINGS` hash | Hugo's `T` function: `{{ T "theorem" }}` |

---

## 10. Navigation

| Aspect | Jekyll | Hugo |
|--------|--------|------|
| Menu source | `site.documents \| concat: site.pages \| sort: 'order'` | `site.Menus.main` |
| Current page | `p.title == page.title` | `$.IsMenuCurrent "main" .` |
| Order | Frontmatter `order:` field | Menu weight in config |

---

## 11. Features Not Yet Ported to Hugo

1. **PDF generation** - Posts with `pdf: true` don't generate PDFs
2. **Photo gallery generation** - `photos.py` script
3. **CV generation** - Git submodule with LaTeX
4. **MA2 course** - LaTeX submodule
5. **Advent of Code content** - `aoc.py`
6. **TBOI content** - `tboi.py`
7. **Link spider** - `spider.py`

---

## 12. New in Hugo (Not in Jekyll)

1. **Honeypot files** - `secrets.py` generates fake credentials to catch bots
2. **Built-in i18n** - Proper translation system
3. **Image processing pipeline** - Automatic WebP, resizing
4. **Page bundles** - Resources co-located with content
5. **Unified video shortcode** - Single shortcode for multiple video types

---

## 13. Configuration Differences

**Jekyll `_config.yml`:**
```yaml
url: "https://slama.dev"
permalink: /:slugified_categories/:title/
plugins: [jektex, jekyll-sitemap]
kramdown:
  syntax_highlighter: rouge
halloween:
  enabled: true
```

**Hugo `hugo.toml`:**
```toml
baseURL = "https://slama.dev"
[permalinks]
  posts = "/:slug/"
[markup.goldmark.extensions.passthrough]
  delimiters.block = [['\[', '\]'], ['$$', '$$']]
[params]
  halloween = true
```

---

## 14. Math Rendering

| Aspect | Jekyll | Hugo |
|--------|--------|------|
| Plugin | Jektex (custom gem) | Goldmark passthrough extension |
| Block delimiters | `\[...\]` or `$$...$$` | Same |
| Inline delimiters | `\(...\)` | Same |
| Rendering | Server-side KaTeX | Server-side KaTeX |
