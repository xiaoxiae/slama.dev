module Jekyll
  module Tags
    class StatniceTopics < Liquid::Block
      def initialize(tag, name, tokens)
        super
      end

      def render(context)
        return "<ol class='sttopics'>#{super.strip}</ol>"
      end
    end
  end
end

Liquid::Template.register_tag('sttopics', Jekyll::Tags::StatniceTopics)
