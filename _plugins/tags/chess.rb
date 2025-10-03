module Jekyll
  class ChessParserBlock < Liquid::Block
    def initialize(tag_name, input, tokens)
      super
      @mode = input.strip
    end

    def render(context)
      content = super

      # Character to CSS class mapping
      char_map = {
        '→' => 'yellow',
        '*' => 'yellow',
        '↓' => 'yellow',
        '>' => 'yellow',
        '=' => 'yellow',
        '⏎' => 'gray',
        '.' => 'gray',
        '(' => 'gray',
        ')' => 'gray',
        '┌' => 'gray',
        '┐' => 'gray',
        '│' => 'gray',
        '─' => 'gray',
        '┼' => 'gray',
        '?' => 'gray',
        '!' => 'red',
      }

      # Process each line
      lines = content.split("\n").map do |line|
        # Find all sequences of exactly 8 binary digits
        # Mark their positions for special treatment
        binary_positions = Set.new
        number_positions = Set.new

        # Look for sequences of 8 binary digits
        line.scan(/[01]{8}/) do |match|
          match_start = Regexp.last_match.begin(0)
          # Only count if it's exactly 8 (not part of a longer sequence)
          before_char = match_start > 0 ? line[match_start - 1] : nil
          after_char = match_start + 8 < line.length ? line[match_start + 8] : nil

          if (before_char.nil? || before_char !~ /[01]/) &&
             (after_char.nil? || after_char !~ /[01]/)
            # Mark these 8 positions as binary positions
            (match_start...match_start + 8).each { |i| binary_positions.add(i) }
          end
        end

        # Look for numbers in the form +d.d or -d.d, and also +∞ or -∞
        line.scan(/[+-](?:\d+\.\d+|∞)/) do |match|
          match_start = Regexp.last_match.begin(0)
          match_end = Regexp.last_match.end(0)

          # Mark these positions as number positions
          # Store both the range and the sign for color determination
          (match_start...match_end).each do |i|
            number_positions.add([i, match[0]]) # Store position and sign
          end
        end

        # Map each character to a span with appropriate class
        chars = line.chars.each_with_index.map do |char, idx|
          css_class = nil

          # Check if this position is part of a number (+d.d or -d.d)
          number_info = number_positions.find { |pos_sign| pos_sign[0] == idx }
          if number_info
            sign = number_info[1]
            css_class = sign == '-' ? 'red' : 'green' # Green for +, red for -
          # Check if this position is part of an 8-digit binary sequence
          elsif binary_positions.include?(idx)
            css_class = char == '0' ? 'red' : 'green' if char =~ /[01]/
          else
            css_class = char_map[char]
          end

          if css_class
            "<span class=\"char #{css_class}\">#{char}</span>"
          else
            "<span class=\"char\">#{char}</span>"
          end
        end.join('')

        chars
      end.join("\n")

      # Choose wrapper based on mode
      if @mode == 'inline'
        "<code class=\"language-plaintext highlighter-rouge\">#{lines}</code>"
      else
        "<div class=\"language-plaintext highlighter-rouge\"><div class=\"highlight\"><pre class=\"highlight\"><code>#{lines}</code></pre></div></div>"
      end
    end
  end
end

Liquid::Template.register_tag('chess', Jekyll::ChessParserBlock)
