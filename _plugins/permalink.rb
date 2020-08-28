module Jekyll
  class PermalinkRewriter < Generator
    safe true
    priority :low
    
    def generate(site)
      # see https://stackoverflow.com/questions/31416559/i18ninvalidlocale-en-is-not-a-valid-locale
      I18n.config.available_locales = :en
      
      # slugify all posts
      site.posts.docs.each do |item|
        title = nil
        category = item.data['category']

        if !item.data['html_title'].nil?
          title = item.data['html_title']
        else
          title = item.data['title']
        end

        item.data['permalink'] = I18n.transliterate("#{category}/#{title}/").downcase.gsub(" ", "-")
      end

      # slugify pages with titles
      site.pages.each do |item|
        if item.data['title'].nil?
          next
        end

        if !item.data['html_title'].nil?
          title = item.data['html_title']
        else
          title = item.data['title']
        end

        item.data['permalink'] = I18n.transliterate("#{title}/").downcase.gsub(" ", "-")
      end
    end
  end
end
