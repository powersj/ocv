#!/bin/bash

./site_deploy.sh

if [ -d "/tmp/public" ];
    then rm -rf /tmp/public
fi

cp -R public/ /tmp/public

cd ..
git checkout gh-pages

# nuclear option, trying to avoid this
# rm -rf *
cp -R /tmp/public/* .

git add -A
git commit -m "Updating github pages"
git push origin gh-pages

if [ -d "/tmp/public" ];
    then rm -rf /tmp/public
fi

git checkout origin

exit
