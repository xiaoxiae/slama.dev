# jekyll_inline_highlight (modified)
#
# https://github.com/bdesham/inline_highlight

module Jekyll
	class InlineHighlightBlock < Tags::HighlightBlock

		def add_code_tag(code)
			code_attributes = [
				"class=\"language-#{@lang.to_s.gsub('+', '-')} highlighter-rouge highlight\"",
				"data-lang=\"#{@lang.to_s}\""
			].join(" ")

			"<code #{code_attributes}>#{code.chomp.strip}</code>"
		end

		def render(context)
			super.strip
		end
	end
end

Liquid::Template.register_tag('ihighlight', Jekyll::InlineHighlightBlock)
