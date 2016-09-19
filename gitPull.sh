#/usr/bin/env bash

git checkout mysite/settings.py
git pull
cp mysite/settings-release.py mysite/settings.py
cp -af statics/*  ~/workspace/static/

