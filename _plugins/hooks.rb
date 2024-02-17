Jekyll::Hooks.register :site, :after_init do |site|
  `_plugins/compress_images.py`.split( /\r?\n/ ).each {
    |x|
    print "            Images: " + x + "\n"
  }

  `_plugins/videos.py`.split( /\r?\n/ ).each {
    |x|
    print "            Videos: " + x + "\n"
  }

  `_plugins/climbing.py`.split( /\r?\n/ ).each {
    |x|
    print "          Climbing: " + x + "\n"
  }

  `_plugins/climbing_journal.py`.split( /\r?\n/ ).each {
    |x|
    print "  Climbing journal: " + x + "\n"
  }

  `_plugins/resize.py`.split( /\r?\n/ ).each {
    |x|
    print "            Resize: " + x + "\n"
  }


  print "                CV: " + `git submodule foreach git fetch --all`
  print "                CV: " + `git submodule foreach git reset --hard origin/master`
  print "                CV: " + `_plugins/cv/cv.py --pdf -c`
  print "                CV: " + `_plugins/cv/cv.py --html -o _includes/cv`

  print "              Life: " + `_plugins/cv/cv.py --html -o _includes/life -i ../../_plugins/life.yaml`
end

Jekyll::Hooks.register :posts, :post_render do |post|
  begin
    if post.data['pdf']
      print "               PDF: " + `_plugins/pdf.py #{post.path.to_str} #{post.url.to_str}`
    end
  rescue
  end
end
