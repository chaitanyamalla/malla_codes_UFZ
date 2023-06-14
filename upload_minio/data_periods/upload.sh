#!/bin/bash
set -e
set -x

BUCKET=$1
FILE=$2
HOST=$3
PROTOCOL=$4
S3_ACCESS_KEY="chaitanya"
S3_SECRET_KEY="J95K3Feh2SrZqTxh"

RESOURCE="/${BUCKET}/${FILE}"
CONTENT_TYPE="application/octet-stream"
DATE=`date -R`
REQUEST="PUT\n\n${CONTENT_TYPE}\n${DATE}\n${RESOURCE}"
SIGNATURE=`echo -en ${REQUEST} | openssl sha1 -hmac ${S3_SECRET_KEY} -binary | base64`

echo ${SIGNATURE}

curl -v -X PUT -T "${FILE}" \
          -H "HOST: $HOST" \
          -H "DATE: ${DATE}" \
          -H "Content-Type: ${CONTENT_TYPE}" \
          -H "Authorization: AWS ${S3_ACCESS_KEY}:${SIGNATURE}" \
          ${PROTOCOL}://$HOST${RESOURCE}
