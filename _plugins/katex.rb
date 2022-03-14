require 'execjs'
require 'digest'
require 'htmlentities'

# shamelessly stolen from https://github.com/yagarea/jektex

module Jekyll
  class ConvertLatex < Jekyll::Generator
    PATH_TO_JS = "./_plugins/katex.min.js"
    DEFAULT_CACHE_DIR = ".jekyll-cache"
    CACHE_FILE = "jektex-cache.marshal"
    KATEX = ExecJS.compile(open(PATH_TO_JS).read)
    PARSE_ERROR_PLACEHOLDER = "<b style='color: red;'>PARSE ERROR</b>"
    FRONT_MATTER_TAG = "jektex"
    INDENT = " " * 13


    def initialize(config)
      @count_newly_generated_expressions = 0

      @path_to_cache = File.join(DEFAULT_CACHE_DIR, CACHE_FILE)
      @cache = nil

      # check if there is defined custom cache location in config
      @path_to_cache = File.join(config["cache_dir"].to_s, CACHE_FILE) if config.has_key?("cache_dir")

      # load content of cache file if it exists
      if File.exist?(@path_to_cache)
        @cache = File.open(@path_to_cache, "r"){ |from_file| Marshal.load(from_file)}
      else
        @cache = Hash.new
      end
    end

    def print_stats
      print "#{INDENT}LaTeX: " \
      "#{@count_newly_generated_expressions} expressions rendered " \
      "(#{@cache.size} already cached)".ljust(72) + "\r"
      $stdout.flush
    end

    def generate(site)
      @site = site
      site.pages.each { |post| convert post }
      site.posts.docs.each { |post| convert post }

      # print new line to prevent overwriting previous output
      print "\n"

      # create cache path
      Pathname.new(@path_to_cache).dirname.mkpath
      # save cache to disk
      File.open(@path_to_cache, "w"){|to_file| Marshal.dump(@cache, to_file)}

      @count_newly_generated_expressions = 0
    end

    def escape_method( type, expression )
      # detect if expression is in display mode
      is_in_display_mode = type.downcase =~ /\[/

      # generate a hash from the math expression
      expression_hash = Digest::SHA2.hexdigest(expression) + is_in_display_mode.to_s

      # use it if it exists
      if(@cache.has_key?(expression_hash))
        @count_newly_generated_expressions += 1
        print_stats
        return @cache[expression_hash]

      # else generate one and store it
      else
        # create the cache directory, if it doesn't exist
        begin
          # render using ExecJS
          result =  KATEX.call("katex.renderToString", expression,
                              { displayMode: is_in_display_mode})
        rescue SystemExit, Interrupt
          # save cache to disk
          File.open(@path_to_cache, "w"){|to_file| Marshal.dump(@cache, to_file)}
          # this stops jekyll being immune to interrupts and kill command
          raise
        rescue ExecJS::ProgramError => pe
          # catch parse error
          return PARSE_ERROR_PLACEHOLDER
        end
        # save to cache
        @cache[expression_hash] = result
        # update count of newly generated expressions
        @count_newly_generated_expressions += 1
        print_stats
        return result
      end
    end

    def convert(post)
      post.content.gsub!(/(\\\()((.|\n)*?)(?<!\\)\\\)/) { |m| escape_method($1, $2) }
      post.content.gsub!(/(\\\[)((.|\n)*?)(?<!\\)\\\]/) { |m| escape_method($1, $2) }
    end
  end
end
