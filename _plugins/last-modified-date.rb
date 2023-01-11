# stolen from https://stackoverflow.com/questions/36758072/how-to-insert-the-last-updated-time-stamp-in-jekyll-page-at-build-time
Jekyll::Hooks.register :posts, :pre_render do |post|
  # get the current post last modified time
  #modification_time = File.mtime( post.path )

  modification_time_string = `git log -1 --pretty='format:%ci' #{post.path}`

  modification_time = Time.parse(modification_time_string)

  creation_time = post.data['date']

  # a hack to only show 'updated' when released != update
  if modification_time.year == creation_time.year and modification_time.month == creation_time.month and modification_time.day == creation_time.day
    modification_time = creation_time
  end

  # inject modification_time in post's datas.
  post.data['last-modified-date'] = modification_time
end
