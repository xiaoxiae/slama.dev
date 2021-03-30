module Jekyll
  module Tags
    class Math < Liquid::Block
      def initialize(tag, name, tokens)
        super
        @type = name
      end

      def render(context)
        parts = @type.split(/\s(?=(?:[^"]|"[^"]*")*$)/)

        tag = parts[0]
        name = parts[1].nil? ? nil : (parts[1].strip[1..-2])

        case tag
        when "definition"
          return '<strong>Definice' + (name.nil? ? '' : (' (' + name + ')')) + ':</strong> ' + super.strip
        when "reminder"
          return '<strong>Připomenutí' + (name.nil? ? '' : (' (' + name + ')')) + ':</strong> ' + super.strip
        when "lemma"
          return '<strong>Lemma' + (name.nil? ? '' : (' (' + name + ')')) + ':</strong> <em>' + super.strip + "</em>"
        when "theorem"
          return '<strong>Věta' + (name.nil? ? '' : (' (' + name + ')')) + ':</strong> <em>' + super.strip + "</em>"
        when "proof"
          return '<strong>Důkaz' + (name.nil? ? '' : (' (' + name + ')')) + ':</strong>' + super.strip
        when "algorithm"
          return '<strong>Algoritmus' + (name.nil? ? '' : (' (' + name + ')')) + ':</strong> ' + super.strip
        when "fact"
          return '<strong>Fakt' + (name.nil? ? '' : (' (' + name + ')')) + ':</strong> ' + super.strip
        when "consequence"
          return '<strong>Důsledek' + (name.nil? ? '' : (' (' + name + ')')) + ':</strong> ' + super.strip
        else
          return "ERROR: tag " + tag + " unrecognized"
        end
      end
    end
  end
end

Liquid::Template.register_tag('math', Jekyll::Tags::Math)
