module Jekyll
  module Tags
    class StatniceTopic < Liquid::Block
      def initialize(tag, name, tokens)
        super
        @parts = name.split("|")
      end

      def render(context)
        return "<li><ul class='hfill'> <li><strong>#{@parts[0].strip}</strong></li> <li markdown='1'>#{@parts[1].strip}</li></ul> <ul>#{super.strip}</ul></li>"
      end
    end
  end
end

Liquid::Template.register_tag('sttopic', Jekyll::Tags::StatniceTopic)
