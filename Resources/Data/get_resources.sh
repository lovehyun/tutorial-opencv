#!/bin/bash
RESOURCES=(
    "yolov3.cfg":"1mVhquMtEms6F0OrmUxNVgYK3zfZjWQfK"
    "yolov3.weights":"1h3ziD90T_QjCQNrCMMYlZ8GSeh2nlX7T"
)

for res in ${RESOURCES[@]}; do
    FILE="${res%%:*}"
    ID="${res##*:}"
    curl -sc /tmp/cookie "https://drive.google.com/uc?export=download&id=${ID}" > /dev/null
    code="$(awk '/_warning_/ {print $NF}' /tmp/cookie)"  
    curl -Lb /tmp/cookie "https://drive.google.com/uc?export=download&confirm=${code}&id=${ID}" -o ${FILE} 
done
