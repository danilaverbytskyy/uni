#!/bin/bash
set -e

git status
git add .

git commit -m "Полная версия"

git push
