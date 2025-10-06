module Jekyll
  module Tags
    class MotionCanvasVideoTag < Liquid::Tag
      def initialize(tag, name, tokens)
        super
        @name = name
      end

      def render(context)
        return "<figure>
  <video poster='/assets/motion-canvas/#{@name.strip}.webp' controls preload='none'>
    <source src='/assets/motion-canvas/#{@name.strip}.mp4' type='video/mp4'>
  </video>
</figure>"
      end
    end
  end
end

module Jekyll
  module Tags
    class MotionCanvasSolutionBlock < Liquid::Block
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
```typescript
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
    class MotionCanvasDocTag < Liquid::Tag
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

Liquid::Template.register_tag('motion_canvas_doc', Jekyll::Tags::MotionCanvasDocTag)
Liquid::Template.register_tag('motion_canvas_solution', Jekyll::Tags::MotionCanvasSolutionBlock)
Liquid::Template.register_tag('motion_canvas_video', Jekyll::Tags::MotionCanvasVideoTag)
