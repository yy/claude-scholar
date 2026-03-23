#!/bin/bash
# Fetch BibTeX entry from DOI

if [ -z "$1" ]; then
    echo "Usage: doi2bib.sh <DOI>" >&2
    exit 1
fi

DOI="$1"

# Handle both full URLs and bare DOIs
if [[ "$DOI" == http* ]]; then
    URL="$DOI"
else
    URL="https://doi.org/$DOI"
fi

response=$(curl -sL -w "\n%{http_code}" -H "Accept: text/bibliography; style=bibtex" "$URL")
http_code=$(echo "$response" | tail -n1)
body=$(echo "$response" | sed '$d')

if [ "$http_code" -ne 200 ]; then
    echo "Error: DOI lookup failed (HTTP $http_code)" >&2
    exit 1
fi

echo "$body"
