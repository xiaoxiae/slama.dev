module Jekyll
  module Tags
    class XoppTag < Liquid::Tag
      def initialize(tag, name, tokens)
        super
        parts = name.split("&")

        @name = parts[0].strip()

        unless parts[1].nil?
          @caption = parts[1].strip()
        end
      end

      def render(context)
        content =  File.read("_includes/#{context.environments.first["page"]["slug"]}/#{@name}.svg")

        return "<figure>#{content}#{@caption == 0 or @caption == nil ? "" : "<figcaption>#{@caption}</figcaption>"}</figure>"
      end
    end
  end
end

Liquid::Template.register_tag('xopp', Jekyll::Tags::XoppTag)
