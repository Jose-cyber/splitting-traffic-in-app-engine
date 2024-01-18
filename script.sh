#!/bin/bash

while true; do
  response=$(curl -s -w " - code: %{http_code}\n" $1)
  echo "response: $response"
done
