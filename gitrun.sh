#!/bin/bash

git add .

echo "enter commit msg"

read msg

git commit -m "$msg"

git push -u origin master
