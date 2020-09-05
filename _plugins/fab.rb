module Jekyll
  module Tags
    class FabTag < Liquid::Tag
      def initialize(tag, name, tokens)
        super
        $code = name.strip
      end
      def render(context)
        return "<i class='fab' aria-hidden='true'>&#x#{$code};</i>"
      end
    end
  end
end

Liquid::Template.register_tag('fab', Jekyll::Tags::FabTag)
