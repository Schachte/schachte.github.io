#!/usr/bin/env bash
set -e # halt script on error

echo 'Testing travis...'
bundle exec travis-lint

echo 'Jekyll build...'
bundle exec jekyll build

echo 'Testing htmlproof...'
bundle exec htmlproof ./_site --href-ignore "#","/simplest/" --disable-external

cd ${HTML_FOLDER}

# config
git config --global user.email "code@ryan-schachte.com"
git config --global user.name "Ryan Schachte"

# deploy
git init
git add --all
git commit -m "Deploy to GitHub Pages"
git push --force --quiet "https://github.com/Schachte/schachte.github.io.git" master:gh-pages
