require 'execjs'

module Jekyll
  module Tags
    class KatexBlock < Liquid::Block

      def initialize(tag, markup, tokens)
        super

        @display = markup.include? 'display'
      end

      def render(context)
        File.open("scripts/katex_server/in", 'w') { |file| file.write(super(context) ) }
        return File.read("scripts/katex_server/out")
      end
    end
  end
end

Liquid::Template.register_tag('latex', Jekyll::Tags::KatexBlock)
