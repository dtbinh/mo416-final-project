#!/usr/bin/env bash

mkdir renamed

a=1
for i in *.png; do
  new=$(printf "%04d.png" "$a") #04 pad to length of 4
  cp "$i" renamed/"$new"
  let a=a+1
done