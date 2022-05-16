module Jekyll
  module Tags
    class StatniceLinkTag < Liquid::Tag
      def initialize(tag, name, tokens)
        super
        @parts = name.split("|")
      end

      def render(context)
        total = ""

        for a in @parts.slice(1, @parts.length) do
          total += " [🔗](#{a.strip})"
        end

        return "<li><ul class='hfill'> <li>#{@parts[0].strip}</li> <li markdown='1'>#{total}</li> </ul></li>"
      end
    end
  end
end

Liquid::Template.register_tag('stlink', Jekyll::Tags::StatniceLinkTag)
