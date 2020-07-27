---
layout: post

title: Typesetting math with <span class="katex"><span class="katex-mathml"><math xmlns="http://www.w3.org/1998/Math/MathML"><semantics><mrow><mtext>LaTeX</mtext></mrow><annotation encoding="application/x-tex"> \LaTeX </annotation></semantics></math></span><span class="katex-html" aria-hidden="true"><span class="base"><span class="strut" style="height:0.89883em;vertical-align:-0.2155em;"></span><span class="mord text"><span class="mord textrm">L</span><span class="mspace" style="margin-right:-0.36em;"></span><span class="vlist-t"><span class="vlist-r"><span class="vlist" style="height:0.68333em;"><span style="top:-2.904999em;"><span class="pstrut" style="height:2.7em;"></span><span class="mord"><span class="mord textrm mtight sizing reset-size6 size3">A</span></span></span></span></span></span><span class="mspace" style="margin-right:-0.15em;"></span><span class="mord text"><span class="mord textrm">T</span><span class="mspace" style="margin-right:-0.1667em;"></span><span class="vlist-t vlist-t2"><span class="vlist-r"><span class="vlist" style="height:0.46782999999999997em;"><span style="top:-2.7845em;"><span class="pstrut" style="height:3em;"></span><span class="mord"><span class="mord textrm">E</span></span></span></span><span class="vlist-s">​</span></span><span class="vlist-r"><span class="vlist" style="height:0.2155em;"><span></span></span></span></span><span class="mspace" style="margin-right:-0.125em;"></span><span class="mord textrm">X</span></span></span></span></span></span> in Jekyll
html_title: Typesetting math with LaTeX in Jekyll
excerpt: There are many posts on the internet describing how to typeset LaTeX math with Jekyll, but none of them exactly met my requirements. After experimenting with various options for typesetting math with Jekyll, I found a pretty good solution. This post is a tutorial on how it works and how to set it up.
---

**UPDATE (27. 7. 2020):** the post has been updated to include caching the generated HTML, making the solution much faster than previously.

---

[There](https://stackoverflow.com/questions/10987992/using-mathjax-with-jekyll) [are](http://haixing-hu.github.io/programming/2013/09/20/how-to-use-mathjax-in-jekyll-generated-github-pages/) [many](https://stackoverflow.com/questions/25146431/how-to-use-mathjax-in-jekyll) [posts](http://dasonk.com/blog/2012/10/09/Using-Jekyll-and-Mathjax) [on](https://lyk6756.github.io/2016/11/25/write_latex_equations.html) [the](http://sgeos.github.io/github/jekyll/2016/08/21/adding_mathjax_to_a_jekyll_github_pages_blog.html) [internet](https://quuxplusone.github.io/blog/2018/08/05/mathjax-in-jekyll/) describing how to typeset LaTeX math with Jekyll, but none of them exactly met my requirements. After experimenting with various options for typesetting math with Jekyll, I found a pretty good solution that is *easy to implement + use* and *doesn't require client-side JavaScript*.

If you'd like to see the results first, [skip to the end](#results) of the post.

### Overview
The solution involves running [KaTeX](https://katex.org/) from Ruby using `ExecJS` to locally generate HTML for the website. Math blocks themselves are denoted using a custom [Liquid tag](https://jekyllrb.com/docs/plugins/tags/). Then it's just a matter of adding KaTeX CSS sheets to the header of the website for the browser to properly render the math.

### 1) Create a Liquid tag
We're first going to register a new liquid tag. This can be done by creating a new Ruby file in `_plugins/` called `katex.rb` (or pretty much any other name) with the following code:

```ruby
require 'execjs'
require 'digest'

module Jekyll
  module Tags
    class KatexBlock < Liquid::Block

      PATH_TO_JS = "./_plugins/katex.min.js"

      def initialize(tag, markup, tokens)
        super

        @display = markup.include? 'display'
      end

      def render(context)
        # generate a hash from the math expression
        @hash = Digest::SHA2.hexdigest super
        @cache_path = './.katex-cache/' + @hash

        # use it if it exists
        if(File.exist?(@cache_path))
          return File.read(@cache_path)

        # else generate one and store it
        else
          # create the cache directory, if it doesn't exist
          @cache_dir_path = File.dirname(@cache_path)
          Dir.mkdir(@cache_dir_path) unless Dir.exist?(@cache_dir_path)

          # render using ExecJS
          @katex = ExecJS.compile(open(PATH_TO_JS).read)
          @result =  @katex.call("katex.renderToString", super, {displayMode: @display})

          # save to cache
          File.open(@cache_path, 'w') { |file| file.write(@result) }

          return @result
        end
      end
    end
  end
end

Liquid::Template.register_tag('latex', Jekyll::Tags::KatexBlock)
```

This will cause any math inside the tag to be converted to HTML by calling KaTeX from Ruby. It also caches this result to be used in the future, since calling JS from Ruby is very, very slow.

_Note: if you're worried about two different expressions producing the same hash, don't be -- to my knowledge, noone has ever found a SHA-256 collision, so you would be pretty safe._

### 2) Install the execjs Gem
Since we're using the execjs gem, we need to install it.

If you have your Jekyll website set up as a Ruby gem, you need to add a new dependency. This can be done quite easily by adding `gem 'execjs'` to your `Gemfile` and then running `bundle update` in the folder of your Jekyll website.

You can also install the gem globally by running `gem install execjs`.

### 3) Add KaTeX CSS to your header
Now that the HTML is being generated, we need to style it with KaTeX CSS. To do this, add the following line to your HTML header:

{% raw %}
```
<link rel="stylesheet" href="{{ site.url }}/assets/css/katex.min.css">
```
{% endraw %}

### 4) Download the latest KaTeX release
The last step is to download the KaTeX CSS, JS and fonts that we're using from their [GitHub releases page](https://github.com/KaTeX/KaTeX/releases). What you then should do is to put `katex.min.js` file to wherever your `PATH_TO_JS` variable is pointing (`_plugins/`) and `katex.min.css` + the `fonts/` folder to where the HTML link from the previous step is pointing (`assets/css/`).

### 5) Profit?
That's it! You should now be able to use {% latex %} \LaTeX {% endlatex %} math in your blog posts.

---


### Results

{% raw %}
```
The equation {% latex %} x^2 + 2x + 3 = 0 {% endlatex %} has no solution in {% latex %} \mathbb{R} {% endlatex %}.
```
{% endraw %}

The equation {% latex %} x^2 + 2x + 3 = 0 {% endlatex %} has no solution in {% latex %}\mathbb{R}{% endlatex %}.


{% raw %}
```
The liquid tag also supports the "display" parameter (for display math):
{% latex display %}
\sum_{i = 0}^{\infty} \binom{i}{k} \binom{j}{k} = \binom{i + j}{i}
{% endlatex %}
```
{% endraw %}

The liquid tag also supports the "display" parameter (for display math):
{% latex display %}
\sum_{i = 0}^{\infty} \binom{i}{k} \binom{j}{k} = \binom{i + j}{i}
{% endlatex %}


{% raw %}
```
{% latex display %}
\mathcal{T} = \begin{bmatrix} 1 & 2 & 3 \\ 4 & 5 & 6 \\ 7 & 8 & 9 \\ \end{bmatrix}
{% endlatex %}
```
{% endraw %}

{% latex display %}
\mathcal{T} = \begin{bmatrix} 1 & 2 & 3 \\ 4 & 5 & 6 \\ 7 & 8 & 9 \\ \end{bmatrix}
{% endlatex %}
