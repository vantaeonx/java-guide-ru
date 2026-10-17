#!/usr/bin/env bash
set -euo pipefail
cd -- "$(dirname -- "$0")/.."
mkdir -p build/classes
mapfile -d '' sources < <(find src/main/java -name '*.java' -print0 | sort -z)
javac --release 17 -encoding UTF-8 -Xlint:all -d build/classes "${sources[@]}"
printf 'Скомпилировано %s исходников с --release 17.\n' "${#sources[@]}"
