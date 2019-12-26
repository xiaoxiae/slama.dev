require 'execjs'

module Jekyll
	module Tags
		class KatexBlock < Liquid::Block
		
			def initialize(tag, markup, tokens)
				super
				@tag = tag
				@tokens = tokens
				@markup = markup
				
				@display = markup.include? 'display'
			end
			
			PATH_TO_JS = "./assets/js/katex.min.js"
			
			def render(context)
				@katex = ExecJS.compile(open(PATH_TO_JS).read)
				
				latex_source = super
				
				if @display
						return @katex.call("katex.renderToString", latex_source, {displayMode: true})
				else
						return @katex.call("katex.renderToString", latex_source)
				end
			end
		end
	end
end

Liquid::Template.register_tag('latex', Jekyll::Tags::KatexBlock)
