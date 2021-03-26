module Jekyll
  module Tags
    class PhotosTag < Liquid::Tag
      def initialize(tag, name, tokens)
        super
        @parts = name.split("|")
      end

      def render(context)
        result = "<div class='row'>"

        for i in 0..(@parts.length - 1)
          result = result + "<div class='photos#{@parts.length}'>" \
          "<a href='#{@parts[i]}'>" \
          "<img src='#{@parts[i].gsub("raw/", "")}'>" \
          "</a>" \
          "</div>" \
        end

        return result + "</div>"
      end
    end
  end
end

Liquid::Template.register_tag('photos', Jekyll::Tags::PhotosTag)
