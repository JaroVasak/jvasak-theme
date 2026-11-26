#!/usr/bin/env bash
# Lint the theme: PHP syntax, theme files, shell scripts. Needs docker and python3.
# Usage: bin/check.sh
set -euo pipefail

root=$(git -C "$(dirname "$0")" rev-parse --show-toplevel)
cd "$root"

# Lowest supported PHP (style.css "Requires PHP") and the current release.
php_images=(php:8.1-cli-alpine php:8.5-cli-alpine)
shellcheck_image=koalaman/shellcheck:v0.11.0

mapfile -t php_files < <(git ls-files '*.php')
for image in "${php_images[@]}"; do
  echo "PHP syntax ($image)"
  for file in "${php_files[@]}"; do
    docker run --rm --network none --volume "$PWD:/theme:ro" --workdir /theme \
      "$image" php -d error_reporting=-1 -d display_errors=stderr -l "$file" >/dev/null
  done
done

echo "Theme files"
python3 bin/check-theme.py

echo "Shell scripts"
mapfile -t shell_files < <(git ls-files '*.sh')
docker run --rm --network none --volume "$PWD:/theme:ro" --workdir /theme \
  "$shellcheck_image" "${shell_files[@]}"

echo "All checks passed."
