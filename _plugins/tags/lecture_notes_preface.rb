module Jekyll
  module Tags
    class LectureNotesPreface < Liquid::Tag
      def initialize(tag, name, tokens)
        super
        @parts = name.split("|")
      end

      def render(context)
        return "<h3>Úvodní informace</h3><p>Tato stránka obsahuje moje poznámky z přednášky #{@parts[0]} z akademického roku #{@parts[1]}. Pokud by byla někde chyba/nejasnost, nebo byste rádi někam přidali obrázek/text, tak stránku můžete upravit <a href='https://github.com/xiaoxiae/slama.dev/blob/master/_posts/'>pull requestem</a> (případně mi dejte vědět, např. na mail).</p>"
      end
    end
  end
end

Liquid::Template.register_tag('lecture_notes_preface', Jekyll::Tags::LectureNotesPreface)
