# frozen_string_literal: true

Gem::Specification.new do |spec|
  spec.name          = "s-theme"
  spec.version       = "0.2.0"
  spec.authors       = ["xiaoxiae"]
  spec.email         = ["tomas.slama.131@gmail.com"]

  spec.summary       = "A simple Jekyll theme developed to be used for my personal website."
  spec.homepage      = "http://slama.dev/"
  spec.license       = "MIT"

  spec.files         = `git ls-files -z`.split("\x0").select { |f| f.match(%r!^(assets|_layouts|_includes|_sass|LICENSE|README)!i) }

  spec.add_runtime_dependency "jekyll", ">= 3.6", "< 5.0"

  spec.add_development_dependency "bundler", "~> 1.16"
  spec.add_development_dependency "rake", "~> 12.0"
end
