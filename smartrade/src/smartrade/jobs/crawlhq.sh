#!/bin/sh
START_DATE=$(date +%Y%m%d)
END_DATE=$(date +%Y%m%d)
curl -X POST "http://localhost:8000/api/hangqing/" \
     -H "accept: application/json" \
     -H "Content-Type: application/json" \
     -d "{\"start\": \"$START_DATE\", \"end\": \"$END_DATE\"}" \
     >> /var/log/crawlers.log 2>&1
