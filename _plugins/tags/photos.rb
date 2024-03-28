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
          pts = @parts[i].split("&")

          # We possibly have description.
          description = ""
          if pts.length == 2
            description = "<figcaption>#{pts[1]}</figcaption>"
          end

          @parts[i] = pts[0]

          type = @parts[i].split("/")
          result = result + "<div class='photos#{@parts.length}-#{i}'>" \
          "<a aria-label='Link to the uncompressed picture of the category #{type[0].strip}.' href='/photos/#{@parts[i].strip}'>" \
          "<img alt='Compressed picture of the category #{type[0].strip}.' src='/photos/#{@parts[i].gsub("raw/", "").gsub(".jpg", ".webp").gsub(".jpeg", ".webp").gsub(".png", ".webp").strip}'>" \
          "</a>" \
          "#{description}" \
          "</div>" \
        end

        return result + "</div>"
      end
    end
  end
end

Liquid::Template.register_tag('photos', Jekyll::Tags::PhotosTag)
