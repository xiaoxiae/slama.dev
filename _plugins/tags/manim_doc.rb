module Jekyll
  module Tags
    class ManimDocTag < Liquid::Tag
      def initialize(tag, name, tokens)
        super
        @parts = name.split(" ")
      end

      def render(context)
        return "[#{@parts[0].strip}](https://docs.manim.community/en/stable/#{@parts[1].strip})"
      end
    end
  end
end

Liquid::Template.register_tag('manim_doc', Jekyll::Tags::ManimDocTag)
