module Jekyll
  module Tags
    class StatniceTag < Liquid::Tag
      def initialize(tag, name, tokens)
        super
        @tag_type = tag
        @parts = name.split("|")
      end

      def render(context)
        case @tag_type
        when 'stlink'
          render_link
        when 'sttopic'
          render_topic(context)
        when 'sttopics'
          render_topics(context)
        else
          ""
        end
      end

      private

      def render_link
        total = ""

        @parts.slice(1, @parts.length).each do |a|
          total += "<a href='#{a.strip}'> 🔗</a>"
        end

        "<li><ul class='hfill'> <li>#{@parts[0].strip}</li> <li> #{total} </li> </ul></li>"
      end

      def render_topic(context)
        # This needs to be a block tag, see StatniceBlockTag below
        ""
      end

      def render_topics(context)
        # This needs to be a block tag, see StatniceBlockTag below
        ""
      end
    end

    class StatniceBlockTag < Liquid::Block
      def initialize(tag, name, tokens)
        super
        @tag_type = tag
        @parts = name.split("|")
      end

      def render(context)
        case @tag_type
        when 'sttopic'
          "<li><ul class='hfill'> <li><strong>#{@parts[0].strip}</strong></li> <li>#{@parts[1].strip}</li></ul><ul>#{super.strip}</ul></li>"
        when 'sttopics'
          if @parts.length != 0
            "<ol class='sttopics' start='#{@parts[0].strip}'>#{super.strip}</ol>"
          else
            "<ol class='sttopics'>#{super.strip}</ol>"
          end
        else
          ""
        end
      end
    end
  end
end

Liquid::Template.register_tag('stlink', Jekyll::Tags::StatniceTag)
Liquid::Template.register_tag('sttopic', Jekyll::Tags::StatniceBlockTag)
Liquid::Template.register_tag('sttopics', Jekyll::Tags::StatniceBlockTag)
