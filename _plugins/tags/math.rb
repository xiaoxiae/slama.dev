module Jekyll
  module Tags
    class Math < Liquid::Block
      TAG_MAPPINGS = {
        "definition" => ["Definition", "Definice"],
        "reminder" => ["Reminder", "Připomenutí"],
        "remark" => ["Remark", "Poznámka"],
        "notation" => ["Notation", "Značení"],
        "lemma" => ["Lemma", "Lemma", true],
        "claim" => ["Claim", "Tvrzení", true],
        "theorem" => ["Theorem", "Věta", true],
        "proof" => ["Proof", "Důkaz"],
        "algorithm" => ["Algorithm", "Algoritmus"],
        "fact" => ["Fact", "Fakt"],
        "problem" => ["Problem", "Problém"],
        "example" => ["Example", "Příklad"],
        "consequence" => ["Consequence", "Důsledek"],
        "observation" => ["(👀)", "(👀)"],
        "question" => ["Question", "Otázka"]
      }.freeze

      def initialize(tag, name, tokens)
        super
        @type = name
      end

      # Lookup allows access to the page/post variables through the tag context
      # Thanks https://blog.sverrirs.com/2016/04/custom-jekyll-tags.html
      def lookup(context, name)
        lookup = context
        name.split(".").each { |value| lookup = lookup[value] }
        lookup
      end

      def render(context)
        parts = @type.split(/\s(?=(?:[^"]|"[^"]*")*$)/)

        tag, name = parts[0], parts[1].nil? ? nil : parts[1].strip[1..-2]
        contents = super.strip

        # Hack for the \( \ \) (don't remove)
        if contents.start_with?("-") or contents.start_with?("1.")
          contents = "\n" + contents
        end

        format_tag(context, tag, name, contents)
      end

      def format_tag(context, tag, name, contents)
        # If there is a :, we want to suppress it (a bit weird but default is :)
        colon = tag.end_with?(":") ? "" : ":"
        tag = tag.chomp(":")

        tag_type_info = TAG_MAPPINGS[tag]
        return "ERROR: tag #{tag} unrecognized" unless tag_type_info

        language = lookup(context, 'page.language')

        tag_type = tag_type_info[language ? 1 : 0]
        em_tag = tag_type_info.size > 2 && tag_type_info[2] ? "<em>" : ""

        return "<strong>#{tag_type}#{name.nil? ? '' : " (#{name})"}#{colon}</strong> #{em_tag}#{contents}"
      end
    end
  end
end

Liquid::Template.register_tag('math', Jekyll::Tags::Math)
