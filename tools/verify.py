#!/usr/bin/env python3
"""Проверка исходной редакторской версии, не автопроверка решений ученика."""
import argparse
import collections
import concurrent.futures
import json
import re
import subprocess
import tempfile
from pathlib import Path
import generate
ROOT = generate.ROOT

def run(command, *, data='', cwd=ROOT):
    result = subprocess.run(command, input=data, text=True, encoding='utf-8',
                            capture_output=True, cwd=cwd, timeout=30)
    if result.returncode:
        raise AssertionError(' '.join(map(str, command)) + '\n' + result.stderr)
    return result

def validate_catalog():
    tasks = generate.TASKS
    assert [t['id'] for t in tasks] == list(range(1, 181))
    assert len({t['title'] for t in tasks}) == 180
    for ch in range(1, 21):
        items = [t for t in tasks if t['chapter'] == ch]
        assert len(items) == 9
        assert collections.Counter(t['level'] for t in items) == {1: 3, 2: 3, 3: 3}
        assert len({t['kind'] for t in items}) == 5
        for t in items:
            assert t['focus'] and t['prompt'] and len(t['checks']) >= 2
            if t['kind'] in ('Найти ошибку', 'Исправить программу'):
                assert t['faulty'], t['id']
    assert [p['id'] for p in generate.PROJECTS] == list(range(1, 7))
    for path, content in generate.generated().items():
        assert (ROOT / path).read_text() == content, f'Рассинхронизация: {path}'
    # Локальные ссылки Markdown: файл и регистр должны быть верны.
    for path in ROOT.rglob('*.md'):
        if any(part in ('build', '.git', '.venv', 'dist', 'tmp', 'target') for part in path.relative_to(ROOT).parts):
            continue
        for link in re.findall(r'\]\(([^)]+)\)', path.read_text()):
            if '://' in link or link.startswith('#'):
                continue
            target = link.split('#')[0]
            assert (path.parent / target).exists(), f'Ссылка {path}: {link}'

def compile_one(source, folder):
    output = folder / source.stem
    output.mkdir()
    run(['javac', '--release', '17', '-encoding', 'UTF-8', '-Xlint:all',
         '-d', str(output), str(source)])
    return source, output

def verify(skip_isolation):
    validate_catalog()
    sources = sorted((ROOT / 'src/main/java').rglob('*.java'))
    examples = sorted((ROOT / 'examples').glob('*.java'))
    assert len(sources) == 186 and len(examples) == 20
    with tempfile.TemporaryDirectory(prefix='java-guide-verify-') as folder:
        folder = Path(folder)
        together = folder / 'together'
        run(['javac', '--release', '17', '-encoding', 'UTF-8', '-Xlint:all',
             '-d', str(together)] + list(map(str, sources)))
        print('Совместная компиляция: 186 файлов, Java release 17', flush=True)
        if not skip_isolation:
            with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
                isolated = list(pool.map(lambda s: compile_one(s, folder), sources + examples))
            class_dirs = {source: output for source, output in isolated}
            print('Независимая компиляция: 186 каркасов + 20 примеров', flush=True)
        else:
            class_dirs = {s: together for s in sources}
            for source in examples:
                _, output = compile_one(source, folder)
                class_dirs[source] = output
        by_id = {f"Ex{t['id']:03}": t for t in generate.TASKS}
        for source in sources:
            text = source.read_text()
            package = re.search(r'^package (.*);', text).group(1)
            stdin = by_id.get(source.stem, {}).get('stdin', '')
            run(['java', '-Dfile.encoding=UTF-8', '-cp', str(class_dirs[source]),
                 package + '.' + source.stem], data=stdin)
        print('Штатный старт и завершение: 186 каркасов', flush=True)
        for source in examples:
            number = int(source.stem[-2:])
            chapter = next((ROOT / 'course/chapters').glob(f'{number:02}-*.md'))
            text = chapter.read_text()
            stdin = re.findall(r'```input\n(.*?)\n```', text, re.S)
            expected = re.search(r'```output\n(.*?)\n```', text, re.S).group(1) + '\n'
            result = run(['java', '-Dfile.encoding=UTF-8', '-cp', str(class_dirs[source]),
                          source.stem], data=stdin[0] + '\n' if stdin else '')
            assert result.stdout == expected, f'{source.name}: вывод отличается от главы'
        print('Точный вывод примеров: 20/20 совпадений', flush=True)
        for source in sources:
            package = re.search(r'^package (.*);', source.read_text()).group(1)
            bytecode = class_dirs[source] / Path(package.replace('.', '/')) / (source.stem + '.class')
            assert int.from_bytes(bytecode.read_bytes()[6:8], 'big') == 61
        print('Целевой байткод: major 61 (Java 17)', flush=True)
    print('Каталог, уровни, форматы, шаблоны и ссылки: OK', flush=True)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--skip-isolation', action='store_true')
    args = parser.parse_args()
    verify(args.skip_isolation)
