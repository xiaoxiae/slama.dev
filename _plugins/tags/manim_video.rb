module Jekyll
  module Tags
    class ManimVideoTag < Liquid::Tag
      def initialize(tag, name, tokens)
        super
        @name = name
      end

      def render(context)
        return "<figure>
  <video poster='/assets/manim/#{@name.strip}.webp' controls preload='none'>
    <source src='/assets/manim/#{@name.strip}.mp4' type='video/mp4'>
  </video>
</figure>"
      end
    end
  end
end

Liquid::Template.register_tag('manim_video', Jekyll::Tags::ManimVideoTag)
