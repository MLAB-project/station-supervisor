#!/bin/bash

csv=;
csv_header=;

while getopts ch flag
do
    case "$flag" in
        c) csv="1";;
        h) csv_header="1";;
    esac
done

save () {
  if [ -n "$csv" ]; then
    echo -n "0x`busybox devmem 0x$1 32`,"
  elif [ -n "$csv_header" ]; then
    echo -n "$2,"
  else
    echo "busybox devmem 0x$1 32 `busybox devmem 0x$1 32` # $2"
  fi
}

if [ -n "$csv_header" ]; then
  echo -n "# time,"
elif [ -n "$csv" ]; then
  echo -n "`date --utc --rfc-3339=ns`,"
else
  echo "#!/bin/bash"
  echo "# RSMS detector register dump at `date +"%Y-%m-%dT%H:%M:%S%z"`"
fi

save "60001018" "SHAPEON"
save "6000101c" "SHAPEOFF"
save "60001020" "DET0TH"
save "60001024" "DET0DU"
save "60001028" "DET1TH"
save "6000102C" "DET1DU"

if [ -n "$csv" ] || [ -n "$csv_header" ]; then
  echo ""
fi
