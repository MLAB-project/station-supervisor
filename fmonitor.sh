#!/bin/bash
let n=0
while :
do
    let n=$n+1
    echo -n $n" "
    tail -n 1 ~/bolidozor/station/data/*freq.csv
    sleep 5
done