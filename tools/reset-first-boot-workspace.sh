#!/usr/bin/env bash
set -euo pipefail

if [ "$#" -ne 1 ]; then
  echo "usage: $0 <1.3|1.4|1.4.1|1.4.2|1.7.3>" >&2
  exit 64
fi

version="$1"
repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

case "$version" in
  1.3)
    source_dir="$repo_root/archive/original-pixelpost/extracted/pixelpost-1.3/pixelpost_1.3/www"
    ;;
  1.4)
    source_dir="$repo_root/archive/original-pixelpost/extracted/pixelpost-1.4"
    ;;
  1.4.1)
    source_dir="$repo_root/archive/original-pixelpost/extracted/pixelpost-1.4.1/pixelpost_1.4.1"
    ;;
  1.4.2)
    source_dir="$repo_root/archive/original-pixelpost/extracted/pixelpost-1.4.2/pixelpost_1.4.2"
    ;;
  1.7.3)
    source_dir="$repo_root/archive/original-pixelpost/extracted/pixelpost-1.7.3"
    ;;
  *)
    echo "unsupported Pixelpost version: $version" >&2
    exit 64
    ;;
esac

target_dir="$repo_root/docker/restoration-workspaces/pixelpost-$version-first-boot"

if [ ! -d "$source_dir" ]; then
  echo "source tree not found: $source_dir" >&2
  exit 66
fi

rm -rf "$target_dir"
mkdir -p "$(dirname "$target_dir")"
cp -R "$source_dir" "$target_dir"

mkdir -p "$target_dir/images" "$target_dir/thumbnails"
chmod -R u+rwX "$target_dir"

echo "reset $target_dir from $source_dir"

