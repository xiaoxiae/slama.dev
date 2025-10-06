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

module Jekyll
  module Tags
    class ManimSolutionBlock < Liquid::Block
      def initialize(tag, name, tokens)
        super
        @tokens = tokens
      end

      def render(context)
        contents = super.strip

        return "
<details>
	<summary>Author's Solution</summary>
<div markdown='1'>
```py
#{contents}
```
</div>
</details>
"
      end
    end
  end
end

module Jekyll
  module Tags
    class ManimDocTag < Liquid::Tag
      def initialize(tag, name, tokens)
        super
        @parts = name.split(" ")
      end

      def render(context)
        return "[#{@parts[0].strip}](https://docs.manim.community/en/stable/#{@parts[1].strip})"
      end
    end
  end
end

Liquid::Template.register_tag('manim_doc', Jekyll::Tags::ManimDocTag)
Liquid::Template.register_tag('manim_solution', Jekyll::Tags::ManimSolutionBlock)
Liquid::Template.register_tag('manim_video', Jekyll::Tags::ManimVideoTag)
