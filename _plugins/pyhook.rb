# a Ruby hook for various Python scripts that I use to properly render the website

Jekyll::Hooks.register :site, :after_init do |site|
  print "              Rick: " + `_plugins/rick_roll.py`

  `_plugins/compress_images.py`.split( /\r?\n/ ).each {
    |x|
    print "            Images: " + x + "\n"
  }

  `_plugins/climbing.py`.split( /\r?\n/ ).each {
    |x|
    print "          Climbing: " + x + "\n"
  }

  print "          Projects: " + `_plugins/projects.py`
  print "                CV: " + `_plugins/cv/cv.py -c --pdf -o cv`
  print "                CV: " + `_plugins/cv/cv.py --html -o _includes/cv`
end
