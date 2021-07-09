require 'execjs'
require 'digest'

module Jekyll
  class ConvertLatex < Jekyll::Generator
    PATH_TO_JS = "./_plugins/katex.min.js"

    def initialize(config)
    end

    def generate(site)
      @site = site
      site.pages.each { |post| convert post }
      site.posts.docs.each { |post| convert post }
    end

    private

    def convert(post)
      post.content.gsub!(/(\\\()((.|\n)*?)(?<!\\)\\\)/) { |m| escape_method($1, $2) }
      post.content.gsub!(/(\\\[)((.|\n)*?)(?<!\\)\\\]/) { |m| escape_method($1, $2) }
    end

    def escape_method( type, string )
      @display = false

      case type.downcase
        when /\(/
          @display = false
        else /\[/
          @display = true
      end

      # generate a hash from the math expression
      @hash = Digest::SHA2.hexdigest string
      @cache_path = './.jekyll-cache/katex-cache/' + @hash + @display.to_s

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
        @result =  @katex.call("katex.renderToString", string, {displayMode: @display})

        # save to cache
        File.open(@cache_path, 'w') { |file| file.write(@result) }

        return @result
      end
    end
  end
end
