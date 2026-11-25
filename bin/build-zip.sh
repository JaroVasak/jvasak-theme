#!/usr/bin/env bash
# Build an installable theme ZIP from the last commit.
# Usage: bin/build-zip.sh [output-dir]   (default: dist/)
set -euo pipefail

root=$(git -C "$(dirname "$0")" rev-parse --show-toplevel)
cd "$root"

if [ -n "$(git status --porcelain)" ]; then
  echo "Warning: uncommitted changes are NOT included. The ZIP is built from the last commit." >&2
fi

version=$(sed -n 's/^Version:[[:space:]]*//p' style.css | tr -d '\r')
out_dir=${1:-dist}
mkdir -p "$out_dir"
zip_path="$out_dir/jvasak-$version.zip"

# The jvasak/ prefix makes WordPress install it as the "jvasak" theme folder.
git archive --format=zip --prefix=jvasak/ -o "$zip_path" HEAD

echo "Built $zip_path (version $version, commit $(git rev-parse --short HEAD))"
