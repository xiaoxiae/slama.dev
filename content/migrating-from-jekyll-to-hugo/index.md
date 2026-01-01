---
date: '2024-12-30'
title: "Migrating from Jekyll to Hugo"
description: "A detailed breakdown of all the differences encountered when migrating slama.dev from Jekyll to Hugo."
draft: true
toc: true
---

I've been working on this website for a few years now.

Looking at the [Wayback machine](https://web.archive.org/web/20250101000000*/slama.dev), the oldest available snapshot is from **[23. 10. 2019](https://web.archive.org/web/20191023024113/http://slama.dev/)**, which itself is not far off from the [initial commit](https://github.com/xiaoxiae/slama.dev/commit/b7e9db8), which was 4. 5. 2019 -- **over 6 years ago**.

Over time, I've added lecture notes ([Czech](/poznamky)/[English](/notes)), a [climbing diary](/climbing), some [pretty neat photos](/photos), and much more.
While I'm really happy how the website grew, it was like building a ship as it's sailing the ocean -- add a sail here, patch the hull there, sprinkle some duct tape and hope it holds.

{{< image_section caption="The evolution of [slama.dev](/) over the years (click to enlarge). <br> (2021 is missing since it's not on wayback)" >}}
{{< image_row "2019.png :: 2019 :: **2019** | 2020.png :: 2020 :: **2020** | 2022.png :: 2022 :: **2022** " >}}
{{< image_row "2023.png :: 2023 :: **2023** | 2024.png :: 2024 :: **2024** | 2025.png :: 2025 :: **2025**" >}}
{{< /image_section >}}

Although tech debt is something that could be addressed by refactoring the codebase, what could not be addressed are Jekyll (the SSG this website uses)'s [terrible build times](#build-times), the [glacial pace of new updates](https://jekyllrb.com/news/releases/) the lack of useful features like [image transformations](https://talk.jekyllrb.com/t/good-way-to-handle-images-on-websites/8689) and [overriding markdown to HTML conversions](https://stackoverflow.com/questions/67475956/jekyll-change-the-markdown-blockquote-html-output), and my [personal dislike of Ruby](ruby.jpg) (that one's on me though).

Ultimately, I decided that a migration was warranted, and decided on [**Hugo**](https://gohugo.io/) since it's fast, feature-rich, and in active development.

This post will mainly cover the changes that address the painpoints that this blog developed over time, since that will be useful for both people interested in converting from Jekyll, and those that are interested in seeing what Hugo is about.

Let's do some rewriting!

---

### Build Times

This was arguably the biggest painpoint for me when deciding to migrate from Jekyll, since a work on an article meant taking a small coffee break to begin to see the rendered results.
You could argue that seeing the article is not needed for writing the content, but this is absolutely not the case for me -- I like to see how the paragraphs look, how the images appear align, how the code gets highlighted.

Cutting to the chase, here are the cold/hot build times for both the Jekyll and the Hugo version[^jekyll].

[^jekyll]: Technically, the Jekyll hot speed time was around 2.5 seconds if we run multiple builds in a row, but this doesn't represent the actual use case -- if we ever run a server in between (i.e. work on a post and want to see how it looks), the build goes back to ~71 seconds.

![Build Times](build_times.svg "Cold / hot build times for Jekyll and Hugo, achieving a 4.9x / 20.6x speedup respectively. Cold build time occurs when the **build folder is empty**, while hot build time is every subsequent build.")

### [Page Bundles](https://gohugo.io/content-management/page-bundles/)

As the introduction aludes to, the iterative way in which this blog developed meant that a lot of assets were placed where there was room for them -- most were in `/assets/<post_name>`, some were just in `/assets/`, a few (especially climbing) were in `/climbing`, the `cv.pdf` was crying in the `/` corner... it was a mess.

While some of this is admittedly a personal skill issue, but Jekyll does not make this any easier, as the `/assets` convention is the [official way](https://jekyllrb.com/docs/assets/) to store assets like images.

Hugo makes things much easier by using **[page bundles](https://gohugo.io/content-management/page-bundles/)** -- the assets of a post can live in `content/<post_name>/` and be referenced via a relative path, and things will just work.
This means that all of the post assets can be moved to where they belong, and structures like these

```text {caption="**Jekyll** file structure -- two different places"}
_posts/
  2024-01-15-chess-...md

assets/
└── images/
    └── chess-.../
        ├── benchmark.png
        └── cpw.webp
```

with usage like `![](/assets/images/chess-.../benchmark.png)` can be rewritten as

```text {caption="**Hugo** file structure -- all in a [page bundle](https://gohugo.io/content-management/page-bundles/)"}
content/                         
└── chess-.../           
    ├── index.md
    ├── benchmark.png            
    └── cpw.webp                 
```

and a nice relative path like `![](benchmark.png)`.

This makes writing posts significantly easier, as you just plop the image in the given directory and reference it via a relative path -- no careful typing of the absolute path necessary.

### [Image Processing](https://gohugo.io/content-management/image-processing/)

Working with images in Jekyll is absolutely attrocious.
Besides the [aforementioned path shenanigans](#page-bundles), I try to keep my website relatively lean, clocking in at a little over `500 kB` for the home page, which I think is reasonable in the current age of JavaScript monstrosities.

![](time.png)
{.inverse-invert}

While this is easy to achieve for CSS/HTML-only pages, it becomes much harder when images get introduced into the picture[^pun].
The Jekyll version handled this via a [custom automated script](https://github.com/xiaoxiae/slama.dev/blob/1b3247748ff722dd403707fd269e38cd57c8e3e3/_plugins/resize.py) that looked for images on the website and resized them, and [another one](https://github.com/xiaoxiae/slama.dev/blob/1b3247748ff722dd403707fd269e38cd57c8e3e3/_plugins/compress_images.py) that did something similar for the photo gallery.

This was absolutely unmaintainable.

[^pun]: Pun intended.

Fortunately, Hugo has built-in [image processing](https://gohugo.io/content-management/image-processing/), which allows you to resize, crop, and manipulate images automatically.
This, in combination with a [render hook](https://gohugo.io/render-hooks/) that overwrites what HTML gets generated from Markdown's `![image](syntax)` means that we can automatically convert and resize **all images** on the **entire website** without the need for custom scripts, with something as simple as this:

```go
{{- $img = $img.Process "resize 800x webp" -}}
````

Here is a nice [blog post](https://blog.nathanv.me/posts/hugo-resources/) by [Nathan Vaughn](https://blog.nathanv.me/) that goes into greater detail on how Hugo handles resources and some good practices, definitely recommend a read if you're interested implementing this on your own website.

### [Data Files]()

---

The fundamental organization of the project changed significantly:

| Aspect | Jekyll | Hugo |
|--------|--------|------|
| Posts | `_posts/YYYY-MM-DD-slug.md` (flat files) | `content/slug/index.md` (page bundles) |
| Layouts | `_layouts/` | `layouts/_default/` |
| Includes/Partials | `_includes/` | `layouts/partials/` |
| Styles | `_sass/` | `assets/scss/` |
| Plugins | `_plugins/` (Ruby + Python mixed) | `scripts/` (Python only) |
| Static files | `assets/` | `static/` + `assets/` |
| Data | Inline YAML / generated markdown in `_includes/` | `data/` directory (YAML files) |
| Config | `_config.yml` + `_config-local.yml` | `config/_default/hugo.toml` + `config/development/` |
| Output | `_site/` | `public/` |
| i18n | Hardcoded in Ruby tag classes | `data/i18n/en.yaml`, `data/i18n/cs.yaml` |
| Custom tags | `_plugins/tags/*.rb` | `layouts/shortcodes/*.html` |
| Render hooks | Not available | `layouts/_default/_markup/` |

### Page Bundles

The biggest conceptual shift is Hugo's **page bundles**. In Jekyll, posts are flat files with the date in the filename:

```
_posts/
  2021-01-07-a-cheeky-python-quine.md
  2022-06-25-introduction.md
```

In Hugo, each piece of content gets its own directory with co-located resources:

```
content/
  a-cheeky-python-quine/
    index.md
    image.png      # Resources accessed via .Page.Resources
    video.mp4
  introduction/
    index.md
```

This makes resource management much cleaner - images and videos live alongside their content rather than in a separate `assets/` directory.

---

## 2. Frontmatter Changes

| Field | Jekyll | Hugo |
|-------|--------|------|
| Date | In filename (`2021-01-07-slug.md`) | Explicit `date: '2021-01-07'` |
| Title | Derived from filename or explicit | Always explicit `title:` |
| Excerpt | `excerpt:` | `description:` |
| TOC | Inline `{:toc}` (Kramdown) | Frontmatter `toc: true` |
| Categories | In filename path or frontmatter | Page section or explicit |
| Custom fields | Accessed via `page.field` | Accessed via `.Params.field` |

### Example Comparison

**Jekyll (`_posts/2021-01-07-a-cheeky-python-quine.md`):**
```yaml
---
excerpt: A fun Python quine that I stumbled upon...
---
```

**Hugo (`content/a-cheeky-python-quine/index.md`):**
```yaml
---
date: '2021-01-07'
title: A Cheeky Python Quine
description: A fun Python quine that I stumbled upon...
---
```

Note: Hugo requires explicit dates and titles since they're no longer derivable from the filename.

---

## 3. Template Syntax

This is where the learning curve is steepest. Jekyll uses Liquid; Hugo uses Go templates.

| Feature | Jekyll (Liquid) | Hugo (Go templates) |
|---------|-----------------|---------------------|
| Variable access | `{{ page.title }}` | `{{ .Title }}` or `{{ .Params.title }}` |
| Site config | `{{ site.title }}` | `{{ site.Title }}` |
| Conditionals | `{% if %}...{% elsif %}...{% endif %}` | `{{ if }}...{{ else if }}...{{ end }}` |
| Negation | `{% unless x %}` | `{{ if not x }}` |
| Loops | `{% for x in y %}...{% endfor %}` | `{{ range y }}...{{ end }}` |
| Loop variable | `{{ x }}` | `{{ . }}` (or `{{ $x := . }}`) |
| Assignment | `{% assign x = y %}` | `{{ $x := y }}` |
| Capture | `{% capture x %}...{% endcapture %}` | `{{ $x := ... }}` |
| Filters | `{{ x \| filter }}` | `{{ x \| function }}` |
| Includes | `{% include "file" %}` | `{{ partial "file" . }}` |
| Comments | `{% comment %}...{% endcomment %}` | `{{/* ... */}}` |
| Null check | `{% if x %}` | `{{ with x }}...{{ end }}` |
| String contains | `{% if x contains "y" %}` | `{{ if strings.Contains x "y" }}` |
| Absolute URL | `{{ x \| absolute_url }}` | `{{ x \| absURL }}` |
| Array concatenation | `{{ a \| concat: b }}` | `{{ $a \| append $b }}` |
| Sort | `{{ x \| sort: 'field' }}` | `{{ sort x "field" }}` |

### Context and Scope

The trickiest part of Go templates is the **context** (`.`). Inside a `range` or `with` block, `.` changes meaning:

```go-html-template
{{ range .Site.Menus.main }}
    {{/* Here . is the menu item, not the page */}}
    {{ .Name }}

    {{/* To access the page, use $ */}}
    {{ $.Title }}
{{ end }}
```

### Real Example: Navigation

**Jekyll:**
```liquid
{% assign sections = site.documents | concat: site.pages | sort: 'order' %}
{% for p in sections %}
    {% if p.title and p.order %}
        <li>
        {% if p.title == page.title %}
            <span class="current">{{ p.title }}</span>
        {% else %}
            <a href="{{ p.url }}">{{ p.title }}</a>
        {% endif %}
        </li>
    {% endif %}
{% endfor %}
```

**Hugo:**
```go-html-template
{{- range site.Menus.main -}}
    <li>
    {{- $isCurrent := or ($.IsMenuCurrent "main" .) (eq $.RelPermalink .URL) -}}
    {{- if $isCurrent }}
        <span class="current">{{ .Name }}</span>
    {{- else }}
        <a href="{{ .URL }}">{{ .Name }}</a>
    {{- end }}
    </li>
{{- end -}}
```

---

## 4. Custom Tags → Shortcodes

Jekyll has custom Liquid tags (Ruby classes); Hugo has shortcodes (Go template files).

### Tag Mapping

| Tag | Jekyll Syntax | Hugo Syntax |
|-----|---------------|-------------|
| Math blocks | `{% math theorem "name" %}...{% endmath %}` | `{{</* math "theorem" "name" */>}}...{{</* /math */>}}` |
| Photo row | `{% photos img1\|img2 %}` | `{{</* image_row "img1\|img2" */>}}` |
| Inline highlight | `{% ihighlight python %}...{% endihighlight %}` | `{{</* inline_highlight "python" */>}}...{{</* /inline_highlight */>}}` |
| Manim video | `{% manim_video name %}` | `{{</* video "manim" "name" */>}}` |
| Motion Canvas video | `{% motion_canvas_video name %}` | `{{</* video "motion-canvas" "name" */>}}` |
| Chess | `{% chess %}...{% endchess %}` | `{{</* chess */>}}...{{</* /chess */>}}` |
| Figure | Markdown `![](img)` | `{{</* figure src="img" caption="..." */>}}` |
| Details | Custom HTML | `{{</* details "summary" */>}}...{{</* /details */>}}` |
| Statnice | `{% statnice %}` | `{{</* statnice */>}}` |
| Lecture preface | `{% lecture_notes_preface %}` | `{{</* lecture_notes_preface */>}}` |

### Implementation Comparison

**Jekyll Ruby class (`_plugins/tags/math.rb`, 68 lines):**
```ruby
module Jekyll
  module Tags
    class Math < Liquid::Block
      TAG_MAPPINGS = {
        "definition" => ["Definition", "Definice"],
        "theorem" => ["Theorem", "Věta", true],
        # ... more mappings
      }.freeze

      def render(context)
        parts = @type.split(/\s(?=(?:[^"]|"[^"]*")*$)/)
        tag, name = parts[0], parts[1]&.strip&.[](1..-2)
        contents = super.strip

        language = lookup(context, 'page.language')
        tag_type = TAG_MAPPINGS[tag][language ? 1 : 0]
        # ... formatting logic
      end
    end
  end
end
```

**Hugo shortcode (`layouts/shortcodes/math.html`, 33 lines):**
```go-html-template
{{- $type := .Get 0 -}}
{{- $name := .Get 1 -}}
{{- $content := .Inner | strings.TrimSpace -}}

{{- $lang := .Page.Params.language | default "en" -}}
{{- $tagText := partial "t.html" (dict "key" $cleanType "lang" $lang) -}}
{{- $italic := or (eq $cleanType "lemma") (eq $cleanType "claim") (eq $cleanType "theorem") -}}

<p><strong>{{ $tagText }}{{ $nameStr | safeHTML }}{{ $colon }}</strong>
{{ if $italic }}<em>{{ end }}{{ $rendered | safeHTML }}{{ if $italic }}</em>{{ end }}</p>
```

The Hugo version is shorter and uses the i18n system for translations instead of hardcoded mappings.

### Shortcode Consolidation

Hugo allows consolidating similar tags. The separate `manim_video` and `motion_canvas_video` Jekyll tags became a single `video` shortcode with a type parameter:

**Jekyll (two separate tags):**
```ruby
# manim.rb
class ManimVideoTag < Liquid::Tag
  def render(context)
    "<video poster='/assets/manim/#{@name}.webp'>..."
  end
end

# motion_canvas.rb
class MotionCanvasVideoTag < Liquid::Tag
  def render(context)
    "<video poster='/assets/motion-canvas/#{@name}.webp'>..."
  end
end
```

**Hugo (one shortcode):**
```go-html-template
{{- $type := .Get 0 -}}
{{- $name := strings.TrimSpace (.Get 1) -}}
<figure>
  <video poster='/assets/{{ $type }}/{{ $name }}.webp' controls preload='none'>
    <source src='/assets/{{ $type }}/{{ $name }}.mp4' type='video/mp4'>
  </video>
</figure>
```

### Complete Shortcode List

Hugo version has these shortcodes in `layouts/shortcodes/`:

| Shortcode | Description |
|-----------|-------------|
| `aoc.html` | Advent of Code progress grid |
| `chess.html` | Chess notation with colored highlighting |
| `code_toggle.html` | Expandable code blocks |
| `code_toggle_details.html` | Details-based code toggle |
| `details.html` | Collapsible details element |
| `doc.html` | Documentation links |
| `embed.html` | HTML embeds |
| `figure.html` | Figures with captions |
| `float_box.html` | Floating content boxes |
| `inline_highlight.html` | Inline code highlighting |
| `lecture_notes_preface.html` | Standard lecture notes intro |
| `math.html` | Mathematical statements (theorem, lemma, etc.) |
| `photo_gallery.html` | Photo gallery rendering |
| `image_row.html` | Row of photos |
| `image_section.html` | Photo section with title |
| `statnice.html` | State exam preparation content |
| `tboi.html` | Binding of Isaac runs display |
| `video.html` | Unified video player |

---

## 5. Build Process

The build process simplified significantly.

### Jekyll Build Flow

```
./site build
    │
    ├── bundle exec jekyll build
    │       │
    │       ├── hooks.rb :after_init
    │       │     ├── compress_images.py
    │       │     ├── photos.py → _includes/photos.md
    │       │     ├── videos.py
    │       │     ├── climbing_videos.py
    │       │     ├── climbing_journal.py → _includes/diary.md
    │       │     ├── resize.py
    │       │     ├── aoc.py
    │       │     ├── git submodule fetch
    │       │     ├── ma2 LaTeX build → assets/matematicka-analyza-ii.pdf
    │       │     └── cv submodule → cv.pdf + _includes/cv/
    │       │
    │       ├── Jekyll processes Liquid templates
    │       │
    │       └── hooks.rb :post_render (per post)
    │             └── pdf.py (for posts with pdf: true)
    │
    └── Output in _site/
```

### Hugo Build Flow

```
./site build
    │
    ├── uv run python scripts/climbing.py build
    │     └── Generates data/climbing/*.yaml
    │
    ├── hugo --minify --cleanDestinationDir
    │     ├── Processes Go templates
    │     ├── Compiles SCSS via Hugo Pipes
    │     ├── Processes images (WebP conversion, resizing)
    │     └── Generates sitemap, RSS
    │
    ├── uv run python scripts/secrets.py
    │     └── Generates honeypot files
    │
    └── Output in public/
```

### Build Script Comparison

**Jekyll (`site` Fish script):**
```fish
function build
    bundle exec jekyll build --trace
end

function serve
    bundle exec jekyll serve --incremental --livereload \
        --drafts --future --config _config.yml,_config-local.yml
end
```

**Hugo (`site` Fish script):**
```fish
function build
    uv run python scripts/climbing.py build
    hugo --minify --cleanDestinationDir
    uv run python scripts/secrets.py
end

function serve
    hugo server -D -F --cleanDestinationDir
end

function check
    # New: Link checking and accessibility testing
    lychee --timeout 5 --root-dir public/ 'public/**/*.html'
    npx pa11y http://localhost:13130
end
```

Hugo's simpler hooks story means the build is more explicit - Python scripts run before/after Hugo rather than being triggered by Ruby hooks.

### Development Server

| Aspect | Jekyll | Hugo |
|--------|--------|------|
| Command | `jekyll serve` | `hugo server` |
| Default port | 4000 | 1313 |
| Live reload | Via `--livereload` flag | Built-in |
| Drafts | `--drafts` flag | `-D` flag |
| Future posts | `--future` flag | `-F` flag |
| Incremental | `--incremental` flag | Always (fast enough) |
| Config override | `--config a.yml,b.yml` | Separate config directories |

---

## 6. Plugin/Script Migration

### Script Status

| Script | Jekyll Location | Hugo Location | Status |
|--------|-----------------|---------------|--------|
| `climbing_journal.py` | `_plugins/` → `_includes/diary.md` | `scripts/` → `data/climbing/journal.yaml` | Ported (data-driven) |
| `climbing_videos.py` | `_plugins/` | `scripts/` | Ported |
| `climbing_types.py` | `_plugins/` | `scripts/` | Ported |
| `secrets.py` | N/A (was `secret_generator.rb`) | `scripts/` | Rewritten in Python |
| `photos.py` | `_plugins/` → `_includes/photos.md` | N/A | Data file + shortcode |
| `aoc.py` | `_plugins/` | N/A | Data file + shortcode |
| `tboi.py` | `_plugins/` | N/A | Data file + shortcode |
| `compress_images.py` | `_plugins/` | N/A | Hugo image processing |
| `resize.py` | `_plugins/` | N/A | Hugo image processing |
| `pdf.py` | `_plugins/` | Not ported | Missing |
| `videos.py` | `_plugins/` | Not ported | Missing |
| `spider.py` | `_plugins/` | N/A | Replaced by lychee |
| CV generation | `_plugins/cv/` submodule | Not ported | Missing |
| MA2 LaTeX | `_plugins/ma2/` submodule | Not ported | Missing |

### Pattern Change: Generated Markdown → Data Files

Jekyll used Python scripts that generated Markdown files to be included:

```
Python script → _includes/diary.md → {% include diary.md %}
```

Hugo uses data files consumed directly by templates:

```
Python script → data/climbing/journal.yaml → {{ range .Site.Data.climbing.journal }}
```

This is cleaner because:
1. Data and presentation are separated
2. YAML is easier to validate than generated Markdown
3. Templates can filter/transform data at render time

### Data File Examples

**AOC Progress (`data/aoc.yaml`):**
```yaml
years:
  - year: 2024
  - year: 2023
    silver: [20, 21, 25]
    gray: [23, 24]
  - year: 2022
```

**Climbing Journal (`data/climbing/journal.yaml`):**
```yaml
2021-08-13:
  blue:
    new: 3
  note: Today's gravity felt pretty good!
  yellow:
    new: 1
```

---

## 7. Asset Handling

### SCSS/CSS

| Aspect | Jekyll | Hugo |
|--------|--------|------|
| Compilation | Jekyll's built-in Sass processor | Hugo Pipes (`toCSS`) |
| Per-page CSS | Supported (`css: "page-name"` in frontmatter) | Single compiled `main.css` |
| Import syntax | `@import` | `@use` (Dart Sass) |
| Output | Multiple CSS files | Single minified CSS |
| Source maps | Generated | None (production-focused) |

**Jekyll approach:**
```liquid
<!-- In default.html -->
{% if page.css %}
    {% for name in page.css | split: " " %}
    <link rel="stylesheet" href="/assets/css/{{ name }}.css">
    {% endfor %}
{% endif %}
```

**Hugo approach:**
```go-html-template
<!-- Hugo Pipes compilation -->
{{ $mainStyle := resources.Get "scss/main.scss" | toCSS | minify }}
<link rel="stylesheet" href="{{ $mainStyle.Permalink }}">
```

### SCSS File Organization

Both use similar organization, but Hugo adds a few files:

| Jekyll `_sass/` | Hugo `assets/scss/` |
|-----------------|---------------------|
| `_main-styles.scss` | `main.scss` (entry point) |
| `_variables.scss` | `_variables.scss` |
| `_light_styles.scss` | `_light_styles.scss` |
| `_dark_styles.scss` | `_dark_styles.scss` |
| Feature files... | Feature files... |
| - | `_chroma.scss` (syntax highlighting) |
| - | `_post-list-styles.scss` |

### Image Processing

| Aspect | Jekyll | Hugo |
|--------|--------|------|
| Processing | Manual Python scripts | Built-in (`resources.GetMatch`) |
| WebP conversion | `compress_images.py` | `.Process "webp"` |
| Resizing | `resize.py` | `.Resize "800x"` |
| Cache busting | None | Content hashes on processed images |
| Lazy loading | Manual | Automatic in render hooks |

**Hugo render hook for images (`layouts/_default/_markup/render-image.html`):**
```go-html-template
{{- $img := partial "get-image" (dict "src" $src "page" .Page "process" "webp") -}}
{{- if $img -}}
  <img src="{{ $img.RelPermalink }}" alt="{{ $alt }}"
    {{- if and (not $isSVG) (not $isGIF) -}}
      width="{{ $img.Width }}" height="{{ $img.Height }}"
    {{- end -}}
    loading="lazy">
{{- end -}}
```

This render hook intercepts all Markdown images and:
- Converts to WebP automatically
- Adds width/height attributes (prevents layout shift)
- Adds lazy loading
- Handles page bundle resources

### Image Helper Partial

Hugo uses a reusable partial for image resolution (`layouts/partials/get-image.html`) that:
1. First checks page bundle resources (`.Page.Resources.GetMatch`)
2. Falls back to global resources (`resources.Get`)
3. Falls back to static files
4. Applies processing if requested

---

## 8. Internationalization

### Jekyll Approach

Translations were hardcoded in Ruby tag classes:

```ruby
# _plugins/tags/math.rb
TAG_MAPPINGS = {
  "definition" => ["Definition", "Definice"],
  "theorem" => ["Theorem", "Věta", true],
  # ...
}

language = lookup(context, 'page.language')
tag_type = TAG_MAPPINGS[tag][language ? 1 : 0]
```

### Hugo Approach

Translations live in data files:

**`data/i18n/en.yaml`:**
```yaml
definition: "Definition"
theorem: "Theorem"
lemma: "Lemma"
proof: "Proof"
preface_text: "This website contains my lecture notes from {{ .author }}..."
```

**`data/i18n/cs.yaml`:**
```yaml
definition: "Definice"
theorem: "Věta"
lemma: "Lemma"
proof: "Důkaz"
```

**Usage via partial (`layouts/partials/t.html`):**
```go-html-template
{{- $translations := index site.Data.i18n $lang | default site.Data.i18n.en -}}
{{- $text := index $translations $key | default $key -}}
{{- if $data -}}
  {{- $text = replace $text "{{ .author }}" $data.author -}}
{{- end -}}
{{- $text -}}
```

**In shortcodes:**
```go-html-template
{{- $tagText := partial "t.html" (dict "key" "theorem" "lang" $lang) -}}
```

---

## 9. Navigation/Menus

### Jekyll

Navigation was built by collecting and sorting all documents:

```liquid
{% assign sections = site.documents | concat: site.pages | sort: 'order' %}
{% for p in sections %}
    {% if p.title and p.order %}
        <a href="{{ p.url }}">{{ p.title }}</a>
    {% endif %}
{% endfor %}
```

Menu items needed `order:` in frontmatter.

### Hugo

Menus are defined in config:

```toml
[[menus.main]]
  name = "Home"
  url = "/"
  weight = 100
  [menus.main.params]
    icon = "fa-house"

[[menus.main]]
  name = "Climbing"
  pageRef = "/climbing"
  weight = 400
  [menus.main.params]
    icon = "fa-bolt"
```

Template usage:
```go-html-template
{{- range site.Menus.main -}}
    <a href="{{ .URL }}">
        {{ with .Params.icon }}<i class="fa-solid {{ . }}"></i>{{ end }}
        {{ .Name }}
    </a>
{{- end -}}
```

Benefits:
- Menu definition is centralized
- Can reference pages by path (`pageRef`) or external URLs (`url`)
- Custom params (icons) without polluting page frontmatter
- Automatic current page detection (`$.IsMenuCurrent`)

---

## 10. Configuration

### Jekyll `_config.yml`

```yaml
title: "slama.dev"
description: "Tomáš Sláma's personal website."
url: "https://slama.dev"

permalink: /:slugified_categories/:title/

plugins:
  - jektex

kramdown:
  syntax_highlighter: rouge
  syntax_highlighter_opts:
    block:
      line_numbers: true

halloween:
  enabled: true

exclude:
  - "climbing/*.py"
  - "ignored/"
  - "README.md"
```

### Hugo `config/_default/hugo.toml`

```toml
baseURL = "https://slama.dev"
title = "slama.dev"
defaultContentLanguage = "en"

disableKinds = ["taxonomy", "term"]

[params]
  description = "Tomáš Sláma's personal website."
  halloween = true

[permalinks]
  posts = "/:slug/"

[markup.highlight]
  lineNos = true
  lineNumbersInTable = true
  style = "monokai"

[markup.goldmark.extensions.passthrough]
  enable = true
  [markup.goldmark.extensions.passthrough.delimiters]
    block = [['\[', '\]'], ['$$', '$$']]
    inline = [['\(', '\)']]

[outputFormats.RSS]
  baseName = "feed"
```

### Key Differences

| Aspect | Jekyll | Hugo |
|--------|--------|------|
| Format | YAML | TOML (or YAML) |
| Params | Top-level | Under `[params]` |
| Plugins | Listed in config | Implicit (in layouts/) |
| Permalinks | Single pattern | Per-section patterns |
| Markdown | Kramdown with options | Goldmark with extensions |
| Math | Jektex plugin | Goldmark passthrough |
| Menus | In documents | In config |
| Environments | Multiple config files merged | Config directories |

---

## 11. Math Rendering

Both render math server-side with KaTeX.

### Jekyll (Jektex)

Jektex is a Jekyll plugin that processes math during build:

```yaml
# _config.yml
plugins:
  - jektex

jektex:
  silent: true
```

### Hugo (Goldmark Passthrough)

Hugo uses Goldmark's passthrough extension to preserve math delimiters, then renders with KaTeX:

```toml
[markup.goldmark.extensions.passthrough]
  enable = true
  [markup.goldmark.extensions.passthrough.delimiters]
    block = [['\[', '\]'], ['$$', '$$']]
    inline = [['\(', '\)']]
```

The KaTeX CSS is still needed:
```html
<link rel="stylesheet" href="/assets/css/katex.min.css">
```

---

## 12. Accessibility Improvements

The Hugo version includes several accessibility enhancements:

1. **Skip link**: `<a href="#main-content" class="skip-link">Skip to main content</a>`
2. **Semantic HTML**: `<header>`, `<nav>`, `<main>`, `<footer>` instead of `<div>`
3. **ARIA labels**: `aria-label="Main navigation"`, `aria-label="YouTube"`
4. **Hidden decorative elements**: `aria-hidden="true"` on icons
5. **Button for toggles**: `<button type="button">` instead of `<a href="#">`
6. **External link attributes**: `rel="noopener noreferrer"`

### Accessibility Testing

Hugo's build script includes automated checks:

```fish
function check
    # Link checking
    lychee --timeout 5 --root-dir public/ 'public/**/*.html'

    # Accessibility testing
    npx pa11y http://localhost:13130
end
```

---

## 13. Features Not Yet Ported

1. **PDF generation** - Posts with `pdf: true` that generate downloadable PDFs
2. **CV generation** - Git submodule with LaTeX/Python that generates CV
3. **MA2 notes** - LaTeX submodule for Mathematical Analysis II
4. **Videos processing** - `videos.py` for YouTube embed metadata
5. **Per-page CSS** - Feature dropped (single compiled CSS is simpler)

---

## 14. New in Hugo

1. **Honeypot files** - `secrets.py` generates fake `.env`, `wp-config.php`, etc. to catch bots
2. **Built-in image processing** - WebP conversion, resizing without Python scripts
3. **Page bundles** - Resources co-located with content
4. **Render hooks** - Intercept Markdown rendering (images, links, code blocks)
5. **Hugo Pipes** - Asset pipeline for SCSS, JS, images
6. **Unified video shortcode** - Single shortcode for manim/motion-canvas
7. **Accessibility checks** - pa11y integration in build
8. **Link checking** - lychee integration replaces custom spider.py
9. **Content hashed assets** - Cache busting on processed images
10. **Open Graph meta tags** - Automatic social sharing metadata

---

## 15. Content Migration Tips

### Converting Posts

For each post in `_posts/YYYY-MM-DD-slug.md`:

1. Create `content/slug/index.md`
2. Add explicit `date` and `title` to frontmatter
3. Rename `excerpt` to `description`
4. Move co-located images into the same directory
5. Convert custom tags to shortcodes

### Shortcode Syntax Changes

```diff
- {% math theorem "Pythagoras" %}
+ {{</* math "theorem" "Pythagoras" */>}}
  a² + b² = c²
- {% endmath %}
+ {{</* /math */>}}

- {% photos landscapes/img1.jpg|portraits/img2.jpg %}
+ {{</* image_row "landscapes/img1.jpg|portraits/img2.jpg" */>}}

- {% manim_video pythagorean %}
+ {{</* video "manim" "pythagorean" */>}}
```

### Testing Migration

1. Run `./site serve` and compare pages visually
2. Run `./site check` to validate links and accessibility
3. Compare RSS feed output
4. Check syntax highlighting
5. Verify math rendering

---

## 16. Performance Comparison

| Metric | Jekyll | Hugo |
|--------|--------|------|
| Full build | ~30-60s | ~2-5s |
| Incremental | ~5-10s | ~100-500ms |
| Dev server start | ~10s | ~1s |
| Dependencies | Ruby + Bundler + Python | Hugo binary + Python |
| Memory usage | Higher (Ruby) | Lower (Go) |

Hugo's speed comes from being compiled Go rather than interpreted Ruby, and from parallel processing of content.

---

## Conclusion

The migration from Jekyll to Hugo involved:

- **Simpler architecture**: No Ruby, fewer hooks, explicit Python scripts
- **Better asset handling**: Built-in image processing, SCSS compilation
- **Cleaner data flow**: YAML data files instead of generated Markdown
- **Modern features**: Page bundles, render hooks, Hugo Pipes
- **Improved accessibility**: Semantic HTML, ARIA, automated testing
- **Faster builds**: 10-20x faster full builds

The main tradeoffs:
- Learning curve for Go templates
- Porting complex Ruby tags to Go shortcodes
- Some features not yet migrated (PDF generation, CV)

Overall, Hugo provides a more maintainable and performant foundation for the site's future development.
