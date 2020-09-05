module Jekyll
  module Tags
    class FaTag < Liquid::Tag
      def initialize(tag, name, tokens)
        super
        $code = name.strip
      end
      def render(context)
        return "<i class='fa' aria-hidden='true'>&#x#{$code};</i>"
      end
    end
  end
end

Liquid::Template.register_tag('fa', Jekyll::Tags::FaTag)
