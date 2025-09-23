#!/bin/sh
RESULT=$(curl localhost:8000/u 2>/dev/null)
EXPECTED=$(echo '{"temperature":22.5,"humidity":55,"status":"OK"}') 
[ "$RESULT" == "$EXPECTED" ] && echo ok || echo fail

