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
	<summary class='code-summary'>Author's Solution</summary>
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

Liquid::Template.register_tag('manim_solution', Jekyll::Tags::ManimSolutionBlock)
