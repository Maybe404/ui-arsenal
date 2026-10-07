#!/bin/sh
# Print a Bencho block's source (tsx + css + deps + tokens + stubs). Read-only.
# usage: bencho.sh <block-id> [tsx|css|prompt|meta]
set -e
ID=$1; PART=${2:-prompt}
case "$PART" in tsx|css|prompt|meta) ;; *) PART=prompt;; esac
UA="Mozilla/5.0"
IDX=$(curl -sL -A "$UA" https://bencho.dev/ | grep -o '/assets/index-[A-Za-z0-9_-]*\.js' | head -1)
[ -n "$IDX" ] || { echo "bencho: index bundle not found" >&2; exit 1; }
CHUNK=$(curl -sL -A "$UA" "https://bencho.dev$IDX" | grep -o 'blocks-[A-Za-z0-9_-]*\.js' | head -1)
[ -n "$CHUNK" ] || { echo "bencho: blocks chunk not found" >&2; exit 1; }
T=${TMPDIR:-/tmp}/bencho-blocks-$$.mjs
curl -sL -A "$UA" "https://bencho.dev/assets/$CHUNK" -o "$T"
node -e '
import(process.argv[1]).then(({BLOCKS})=>{const id=process.argv[2],p=process.argv[3],b=BLOCKS[id];
if(!b){console.error("unknown id; available: "+Object.keys(BLOCKS).join(" "));process.exit(1)}
if(p==="tsx")console.log(b.tsx);else if(p==="css")console.log(b.css);
else if(p==="meta")console.log(JSON.stringify({name:b.name,deps:b.deps,tokens:b.tokens,stubs:b.stubs,props:b.props},null,1));
else{console.log("--- "+b.name+".tsx ---\n"+b.tsx.trim()+"\n\n--- css ---\n"+b.css.trim()+"\n\n# deps: npm i "+b.deps.join(" ")+"\n# css tokens to map: "+b.tokens.join(", ")+"\n# stubs (replace with own assets): "+b.stubs.join(", "))}})' "$T" "$ID" "$PART"
rm -f "$T"
