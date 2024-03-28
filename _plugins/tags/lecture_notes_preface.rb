module Jekyll
  module Tags
    class LectureNotesPreface < Liquid::Tag
      def initialize(tag, name, tokens)
        super
        @parts = name.split("|").map(&:strip)
      end

      def render(context)
        language = lookup(context, 'page.language')
        institution = @parts[2] == 'MFF' ? 'MFF UK' : 'University of Heidelberg'

        if language == 'cz'
          return "<h3>Úvodní informace</h3><p>Tato stránka obsahuje moje poznámky z přednášky #{@parts[0]} z akademického roku #{@parts[1]} (#{institution}). Pokud by byla někde chyba/nejasnost, nebo byste rádi něco přidali, tak stránku můžete upravit <a href='https://github.com/xiaoxiae/slama.dev/blob/master/_posts/'>pull requestem</a> (případně mi dejte vědět na mail).</p>"
        else
          return "<h3>Preface</h3><p>This website contains my lecture notes from a lecture by #{@parts[0]} from the academic year #{@parts[1]} (#{institution}). If you find something incorrect/unclear, or would like to contribute, feel free to submit a <a href='https://github.com/xiaoxiae/slama.dev/blob/master/_posts/'>pull request</a> (or let me know via email).</p>"
        end
      end

      def lookup(context, name)
        lookup = context
        name.split(".").each { |value| lookup = lookup[value] }
        lookup
      end
    end
  end
end

Liquid::Template.register_tag('lecture_notes_preface', Jekyll::Tags::LectureNotesPreface)

