#!/bin/bash
set -e  # останавливаемся при первой ошибке

git status
git add .

git commit -m "new"

git push
