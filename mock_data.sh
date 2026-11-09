#!/bin/bash


sites=( "google.com" "facebook.com" "twitter.com" "linkedin.com" "github.com" "expired.badssl.com" "self-signed.badssl.com"  )

for i in "${sites[@]}"

do 

echo "testing $i"
curl -X POST -d domain=$i http://localhost:80/submit


done 