#!/bin/bash

fn="/data/`date --utc +'%Y%m%d'`_rsms_detector_dumpreg.txt"
dumpreg="$(dirname $0)/dumpregs.sh"

if ! [ -f "$fn" ]; then
    "$dumpreg" -h > "$fn"
fi

"$dumpreg" -c >> "$fn"

lastregs_fn="$(dirname $0)/lastregs.sh"

"$dumpreg" > "$lastregs_fn"
chmod +x "$lastregs_fn"
