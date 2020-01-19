module Jekyll
  module Tags
    class XoppTag < Liquid::Tag
      def initialize(tag, name, tokens)
        super
        parts = name.split("&")

        # parse the name
        @name = parts[0].strip()

        # parse the optional caption
        @caption = ""
        if parts.length != 1
          @caption = parts[1].strip()
        end
      end

      def render(context)
        title = context.environments.first["page"]["slug"]
        image = `python scripts/xopp_to_svg.py -f=_includes/#{title}/#{@name}.xopp`

        return "<figure>" + image + (@caption == "" ? "" : "<figcaption>#{@caption}</figcaption>") + "</figure>"
      end
    end
  end
end

Liquid::Template.register_tag('xopp', Jekyll::Tags::XoppTag)
