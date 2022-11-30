module Jekyll
  module Tags
    class LectureNotesPrefaceHeidelberg < Liquid::Tag
      def initialize(tag, name, tokens)
        super
        @parts = name.split("|")
      end

      def render(context)
        return "<h3>Preface</h3><p>This website contains my lecture notes from a lecture by #{@parts[0]} from the academic year #{@parts[1]} (University of Heidelberg). If you find something incorrect/unclear, or would like to contribute, feel free to submit a <a href='https://github.com/xiaoxiae/slama.dev/blob/master/_posts/'>pull request</a> (or let me know via email).</p>"
      end
    end
  end
end

Liquid::Template.register_tag('lecture_notes_preface_heidelberg', Jekyll::Tags::LectureNotesPrefaceHeidelberg)
