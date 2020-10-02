# a Ruby hook for various Python scripts that I use to properly render the website

Jekyll::Hooks.register :site, :after_init do |site|
  print `scripts/generate_cv`
  print `scripts/rick_roll`
  print `scripts/compress_images`
end
