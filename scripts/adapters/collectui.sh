#!/bin/sh
# List the latest published Collect UI posts in one category (read-only GET on the public anon API).
# usage: collectui.sh <category-slug> [limit]
set -e
SLUG=$1; LIMIT=${2:-20}
UA="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130 Safari/537.36"
S=https://collectui.com
B=https://tuzpqmdnxvlzwqthgseg.supabase.co/rest/v1
APP=$(curl -s -A "$UA" $S/ | grep -o '_app/immutable/entry/app\.[A-Za-z0-9_-]*\.js' | head -1)
K=$(for n in $(curl -s -A "$UA" "$S/$APP" | grep -o 'nodes/[0-9]*\.[A-Za-z0-9_-]*\.js' | sort -u); do
  curl -s -A "$UA" "$S/_app/immutable/$n" | grep -o 'chunks/[A-Za-z0-9_-]*\.js'; done | sort -u | while read c; do
  k=$(curl -s -A "$UA" "$S/_app/immutable/$c" | grep -o 'eyJ[A-Za-z0-9_-]*\.eyJ[A-Za-z0-9_-]*\.[A-Za-z0-9_-]*' | head -1)
  [ -n "$k" ] && { echo "$k"; break; }; done)
[ -n "$K" ] || { echo "collectui: anon key not found (site changed? open $S/designs/$SLUG-ui-design-inspiration in a browser)" >&2; exit 1; }
curl -s "$B/collectui_posts?select=title,media_type,media_url,thumbnail,source_url,categories,created_at&status=eq.Published&categories=cs.%7B$SLUG%7D&order=created_at.desc,id.desc&limit=$LIMIT" -H "apikey: $K" |
python3 -c '
import json,sys
d=json.load(sys.stdin)
if not isinstance(d,list) or not d: sys.exit("collectui: no posts for this category")
for p in d: print("%s\t%s\t%s\t%s" % (p.get("media_type"), p.get("title") or "", p.get("media_url"), p.get("source_url") or ""))
print("# %d posts. 图片 avif→png: sips -s format png x.avif --out x.png ; 视频抽帧: ffmpeg -i x.mp4 -vf fps=1/3,scale=960:-1,tile=2x2 -frames:v 1 grid.png" % len(d))'
