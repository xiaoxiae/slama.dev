require 'execjs'

module Jekyll
  module Tags
    class KatexBlock < Liquid::Block

      PATH_TO_JS = "./assets/js/katex.min.js"

      def initialize(tag, markup, tokens)
        super

        @display = markup.include? 'display'
      end

      def render(context)
        @katex = ExecJS.compile(open(PATH_TO_JS).read)

        return @katex.call("katex.renderToString", super, {displayMode: @display})
      end
    end
  end
end

Liquid::Template.register_tag('latex', Jekyll::Tags::KatexBlock)
