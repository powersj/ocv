#!/bin/bash

build_site.sh

if [ -d "/tmp/public" ];
    then rm -rf /tmp/public
fi

cp -R public /tmp/public
git checkout gh-pages
git add -A
git commit -m "Updating github pages"
git push origin gh-pages
