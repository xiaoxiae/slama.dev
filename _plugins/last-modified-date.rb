# stolen from https://stackoverflow.com/questions/36758072/how-to-insert-the-last-updated-time-stamp-in-jekyll-page-at-build-time
Jekyll::Hooks.register :posts, :pre_render do |post|
  # get the current post last modified time from Git
  modification_time_string = `git log -1 --pretty='format:%ci' #{post.path}`

  creation_time = post.data['date']

  if modification_time_string == ""
    modification_time = creation_time
  else
    modification_time = Time.parse(modification_time_string)
  end

  # a hack to only show 'updated' when released != update
  if modification_time.year == creation_time.year and modification_time.month == creation_time.month and modification_time.day == creation_time.day
    modification_time = creation_time
  end

  # inject modification_time in post's datas.
  post.data['last-modified-date'] = modification_time
end
