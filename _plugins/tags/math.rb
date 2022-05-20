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

        contents = super.strip

        # hack for the \( \ \) hack
        if contents.start_with?("-") or contents.start_with?("1.")
          contents = "\n" + contents
        end

        # burn this with fire, god almighty
        if tag.start_with?("EN")
          case tag
          when "ENdefinition"
            return '<strong>Definition' + (name.nil? ? '' : (' (' + name + ')')) + ':</strong> ' + contents
          when "ENdefinition:"
            return '<strong>Definition' + (name.nil? ? '' : (' (' + name + ')')) + '</strong> ' + contents
          when "ENreminder"
            return '<strong>Reminder' + (name.nil? ? '' : (' (' + name + ')')) + ':</strong> ' + contents
          when "ENremark"
            return '<strong>Remark' + (name.nil? ? '' : (' (' + name + ')')) + ':</strong> ' + contents
          when "ENnotation"
            return '<strong>Notation' + (name.nil? ? '' : (' (' + name + ')')) + ':</strong> ' + contents
          when "ENlemma"
            return '<strong>Lemma' + (name.nil? ? '' : (' (' + name + ')')) + ':</strong> <em>' + contents
          when "ENclaim"
            return '<strong>Claim' + (name.nil? ? '' : (' (' + name + ')')) + ':</strong> <em>' + contents
          when "ENtheorem"
            return '<strong>Theorem' + (name.nil? ? '' : (' (' + name + ')')) + ':</strong> <em>' + contents
          when "ENproof"
            return '<strong>Proof' + (name.nil? ? '' : (' (' + name + ')')) + ':</strong> ' + contents
          when "ENalgorithm"
            return '<strong>Algorithm' + (name.nil? ? '' : (' (' + name + ')')) + ':</strong> ' + contents
          when "ENfact"
            return '<strong>Fact' + (name.nil? ? '' : (' (' + name + ')')) + ':</strong> ' + contents
          when "ENproblem"
            return '<strong>Problem' + (name.nil? ? '' : (' (' + name + ')')) + ':</strong> ' + contents
          when "ENexample"
            return '<strong>Example' + (name.nil? ? '' : (' (' + name + ')')) + ':</strong> ' + contents
          when "ENconsequence"
            return '<strong>Consequence' + (name.nil? ? '' : (' (' + name + ')')) + ':</strong> ' + contents
          when "ENobservation"
            return '<strong>(👀)' + (name.nil? ? '' : (' (' + name + ')')) + ':</strong> ' + contents
          when "ENquestion"
            return '<strong>Question' + (name.nil? ? '' : (' (' + name + ')')) + ':</strong> ' + contents
          else
            return "ERROR: tag " + tag + " unrecognized"
          end
        end

        case tag
        when "definition"
          return '<strong>Definice' + (name.nil? ? '' : (' (' + name + ')')) + ':</strong> ' + contents
        when "definition:"
          return '<strong>Definice' + (name.nil? ? '' : (' (' + name + ')')) + '</strong> ' + contents
        when "reminder"
          return '<strong>Připomenutí' + (name.nil? ? '' : (' (' + name + ')')) + ':</strong> ' + contents
        when "remark"
          return '<strong>Poznámka' + (name.nil? ? '' : (' (' + name + ')')) + ':</strong> ' + contents
        when "notation"
          return '<strong>Značení' + (name.nil? ? '' : (' (' + name + ')')) + ':</strong> ' + contents
        when "lemma"
          return '<strong>Lemma' + (name.nil? ? '' : (' (' + name + ')')) + ':</strong> <em>' + contents
        when "claim"
          return '<strong>Tvrzení' + (name.nil? ? '' : (' (' + name + ')')) + ':</strong> <em>' + contents
        when "theorem"
          return '<strong>Věta' + (name.nil? ? '' : (' (' + name + ')')) + ':</strong> <em>' + contents
        when "proof"
          return '<strong>Důkaz' + (name.nil? ? '' : (' (' + name + ')')) + ':</strong> ' + contents
        when "algorithm"
          return '<strong>Algoritmus' + (name.nil? ? '' : (' (' + name + ')')) + ':</strong> ' + contents
        when "fact"
          return '<strong>Fakt' + (name.nil? ? '' : (' (' + name + ')')) + ':</strong> ' + contents
        when "problem"
          return '<strong>Problém' + (name.nil? ? '' : (' (' + name + ')')) + ':</strong> ' + contents
        when "example"
          return '<strong>Příklad' + (name.nil? ? '' : (' (' + name + ')')) + ':</strong> ' + contents
        when "consequence"
          return '<strong>Důsledek' + (name.nil? ? '' : (' (' + name + ')')) + ':</strong> ' + contents
        when "observation"
          return '<strong>(👀)' + (name.nil? ? '' : (' (' + name + ')')) + ':</strong> ' + contents
        when "question"
          return '<strong>Otázka' + (name.nil? ? '' : (' (' + name + ')')) + ':</strong> ' + contents
        else
          return "ERROR: tag " + tag + " unrecognized"
        end
      end
    end
  end
end

Liquid::Template.register_tag('math', Jekyll::Tags::Math)
