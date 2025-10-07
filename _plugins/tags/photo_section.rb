module Jekyll
  class PhotoSection < Liquid::Block
    def render(context)
      content = super
      "<div class='photo-section'>\n<figure>\n#{content}</figure>\n</div>"
    end
  end

  class PhotoRow < Liquid::Tag
    def initialize(tag_name, markup, tokens)
      super
      @images = markup.strip.split('|').map(&:strip)
    end

    def render(context)
      html = "\t<div class=\"row\">\n"

      @images.each do |img_spec|
        # Check if it's a relative path (no leading /)
        is_relative = !img_spec.start_with?('/')

        if is_relative
          # Old photos tag behavior - clickable with raw version
          # Extract alt text if provided with ::
          if img_spec.include?('::')
            img_path, alt_text = img_spec.split('::').map(&:strip)
          else
            img_path = img_spec.strip
            alt_text = nil
          end

          # Extract category from path (e.g., "ai" from "ai/fantasy.png")
          parts = img_path.split('/')
          category = parts[0]
          filename = parts[1..-1].join('/')

          # Add /raw/ to the path for the raw version
          raw_path = "/photos/#{category}/raw/#{filename}"

          # Generate compressed version path (no /raw/)
          compressed_path = "/photos/#{img_path.gsub('.jpg', '.webp').gsub('.jpeg', '.webp').gsub('.png', '.webp')}"

          # Use custom alt text if provided, otherwise use default
          alt = alt_text || "Compressed picture of the category #{category}."

          html += "\t\t<div>"
          html += "<a aria-label='Link to the uncompressed picture of the category #{category}.' href='#{raw_path}'>"
          html += "<img alt='#{alt}' src='#{compressed_path}'>"
          html += "</a>"
          html += "</div>\n"
        else
          # New photorow behavior - absolute path, not clickable
          # Extract alt text if provided with ::
          if img_spec.include?('::')
            path, alt = img_spec.split('::').map(&:strip)
          else
            path = img_spec
            alt = File.basename(img_spec, '.*').gsub(/[-_]/, ' ')
          end

          html += "\t\t<div><img src=\"#{path}\" alt=\"#{alt}\"></div>\n"
        end
      end

      html += "\t</div>\n"
      html
    end
  end

  class PhotoCaption < Liquid::Tag
    def initialize(tag_name, markup, tokens)
      super
      @caption = markup.strip
    end

    def render(context)
      "\t<figcaption>#{@caption}</figcaption>\n"
    end
  end
end

Liquid::Template.register_tag('photosection', Jekyll::PhotoSection)
Liquid::Template.register_tag('photorow', Jekyll::PhotoRow)
Liquid::Template.register_tag('photocaption', Jekyll::PhotoCaption)
