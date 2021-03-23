module Jekyll
  module Tags
    class Math < Liquid::Block
      def initialize(tag, name, tokens)
        super
        @type = name
      end

      def render(context)
        case @type.strip
        when "definition"
          return '<strong>Definice:</strong> ' + super.strip
        when "lemma"
          return '<strong>Lemma:</strong> <em>' + super.strip + "</em>"
        when "theorem"
          return '<strong>Věta:</strong> <em>' + super.strip + "</em>"
        when "proof"
          return '<strong>Důkaz:</strong> ' + super.strip
        when "algorithm"
          return '<strong>Algoritmus:</strong> ' + super.strip
        when "fact"
          return '<strong>Fakt:</strong> ' + super.strip
        else
          return "ERROR: TAG UNRECOGNIZED"
        end
      end
    end
  end
end

Liquid::Template.register_tag('math', Jekyll::Tags::Math)
