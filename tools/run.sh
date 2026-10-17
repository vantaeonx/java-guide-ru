#!/usr/bin/env bash
set -euo pipefail
cd -- "$(dirname -- "$0")/.."
target="${1:-Ex001}"
if (($#)); then shift; fi
case "$target" in
    Ex[0-9][0-9][0-9])
        number=$((10#${target:2}))
        if ((number < 1 || number > 180)); then echo 'Номер Ex: 001..180' >&2; exit 2; fi
        printf -v chapter '%02d' "$(((number - 1) / 9 + 1))"
        source="src/main/java/ru/vantaeonx/javaguide/ch${chapter}/${target}.java"
        main="ru.vantaeonx.javaguide.ch${chapter}.${target}" ;;
    Project0[1-6])
        source="src/main/java/ru/vantaeonx/javaguide/projects/${target}.java"
        main="ru.vantaeonx.javaguide.projects.${target}" ;;
    Example[0-9][0-9])
        source="examples/${target}.java"
        main="$target" ;;
    *) echo 'Использование: bash tools/run.sh Ex001 | Project01 | Example01 [аргументы]' >&2; exit 2 ;;
esac
if [[ ! -f "$source" ]]; then echo "Файл не найден: $source" >&2; exit 2; fi
# Отдельный каталог изолирует байткод от других упражнений.
class_dir="build/run/${target}"
mkdir -p -- "$class_dir"
javac --release 17 -encoding UTF-8 -d "$class_dir" "$source"
java -Dfile.encoding=UTF-8 -cp "$class_dir" "$main" "$@"
