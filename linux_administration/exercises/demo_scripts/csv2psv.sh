#!/bin/bash
for csv; do
    psv="${csv%.csv}.psv"
    echo converting "$csv" ...
    sed 's/,/|/g' "$csv" > "$psv"
done
echo all conversions successful
exit 0
