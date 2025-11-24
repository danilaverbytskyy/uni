#!/bin/bash
set -e

git status
git add .

git commit -m "new"

git push
