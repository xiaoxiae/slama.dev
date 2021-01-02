require 'execjs'
require 'digest'

module Jekyll
  module Tags
    class KatexBlock < Liquid::Block

      PATH_TO_JS = "./_plugins/katex.min.js"

      def initialize(tag, markup, tokens)
        super

        @display = markup.include? 'display'
      end

      def render(context)
        # generate a hash from the math expression
        @hash = Digest::SHA2.hexdigest super
        @cache_path = './.katex-cache/' + @hash + @display.to_s

        # use it if it exists
        if(File.exist?(@cache_path))
          return File.read(@cache_path)

        # else generate one and store it
        else
          # create the cache directory, if it doesn't exist
          @cache_dir_path = File.dirname(@cache_path)
          Dir.mkdir(@cache_dir_path) unless Dir.exist?(@cache_dir_path)

          # render using ExecJS
          @katex = ExecJS.compile(open(PATH_TO_JS).read)
          @result =  @katex.call("katex.renderToString", super, {displayMode: @display})

          # save to cache
          File.open(@cache_path, 'w') { |file| file.write(@result) }

          return @result
        end
      end
    end
  end
end

Liquid::Template.register_tag('latex', Jekyll::Tags::KatexBlock)
