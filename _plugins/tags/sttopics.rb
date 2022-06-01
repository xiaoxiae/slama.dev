module Jekyll
  module Tags
    class StatniceTopics < Liquid::Block
      def initialize(tag, name, tokens)
        super
        @parts = name.split("|")
      end

      def render(context)
        if @parts.length != 0
          return "<ol class='sttopics' start='#{@parts[0].strip}'>#{super.strip}</ol>"
        else
          return "<ol class='sttopics'>#{super.strip}</ol>"
        end
      end
    end
  end
end

Liquid::Template.register_tag('sttopics', Jekyll::Tags::StatniceTopics)
