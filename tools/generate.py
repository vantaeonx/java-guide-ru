#!/usr/bin/env python3
"""Редакторская генерация. Не запускать --write поверх своих решений."""
import argparse
import json
import re
import textwrap
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
TASKS = json.loads((ROOT / 'course/catalog.json').read_text())
PROJECTS = json.loads((ROOT / 'course/projects.json').read_text())
BASE = Path('src/main/java/ru/vantaeonx/javaguide')

def comment(text, indent='    '):
    return '\n'.join(indent + '// ' + line for paragraph in text.splitlines()
                     for line in (textwrap.wrap(paragraph, 84) or ['']))

def imports(code):
    items = []
    mapping = {
        'Scanner': 'java.util.Scanner', 'Locale': 'java.util.Locale',
        'Arrays': 'java.util.Arrays', 'ArrayList': 'java.util.ArrayList',
        'List': 'java.util.List', 'Map': 'java.util.Map',
        'LinkedHashMap': 'java.util.LinkedHashMap', 'Path': 'java.nio.file.Path',
    }
    for name, package in mapping.items():
        if re.search(r'\b' + name + r'\b', code):
            items.append('import ' + package + ';')
    return '\n'.join(sorted(items))

def starter(t):
    name = f"Ex{t['id']:03}"
    package = f"ru.vantaeonx.javaguide.ch{t['chapter']:02}"
    all_code = t['data'] + '\n' + t['members'] + '\n' + t['faulty']
    imp = imports(all_code)
    head = f"package {package};\n\n" + (imp + '\n\n' if imp else '')
    lines = [head + '// Автор: ____________________',
             f"// {name}. {t['title']}",
             f"// Глава {t['chapter']:02}. Уровень {t['level']}. Формат: {t['kind']}",
             '// Условие и проверки синхронизируются с course/catalog.json.',
             f'public class {name} {{', comment('Опора: ' + t['focus']), '',
             comment('Условие: ' + t['prompt'])]
    if t['faulty']:
        lines += ['', comment('НАМЕРЕННАЯ ОШИБКА / ФРАГМЕНТ ДЛЯ АНАЛИЗА. '
                   'Код закомментирован, чтобы стартовый проект компилировался. '
                   'Если условие требует исправления, перенеси нужные части в рабочую '
                   'область и исправь. Не добавляй второй public-класс.'),
                  '    /*\n' + textwrap.indent(t['faulty'].replace('*/', '* /'), '    ') + '\n    */']
    if t['members']:
        lines += ['', textwrap.indent(t['members'], '    ')]
    lines += ['', '    public static void main(String[] args) {']
    if t['stdin']:
        lines += [comment('Пример стандартного ввода (по строкам):', '        ')]
        lines += [comment(line or '(пустая строка)', '        ') for line in t['stdin'].splitlines()]
    lines += ['        // Исходные данные / исходный код для прогноза:']
    if t['data']:
        lines += [textwrap.indent(t['data'], '        ')]
    lines += ['', '        // TODO: твой код. Для методов дополни тело и вызови их здесь.',
              '        // Ответ / прогноз / объяснение: ____________________',
              '        // Проверки своего решения:']
    lines += [comment(c, '        ') for c in t['checks']]
    lines += ['    }', '', '    // TODO: твои вложенные static-классы, методы и интерфейсы (если нужны).', '}', '']
    return '\n'.join(lines)

def practice(t):
    name = f"Ex{t['id']:03}"
    path = f"../../{BASE}/ch{t['chapter']:02}/{name}.java"
    out = [f"## {name}. {t['title']}", '',
           f"Уровень {t['level']} · {t['kind']} · [{name}.java]({path})", '',
           '**Перед началом.** ' + t['focus'], '', t['prompt'], '']
    if t['data']:
        out += ['### Исходные данные / код для анализа', '', '```java', t['data'], '```', '']
    if t['members']:
        out += ['### Объявления в заготовке', '', '```java', t['members'], '```', '']
    if t['faulty']:
        out += ['### Намеренная ошибка / фрагмент для анализа', '',
                'Фрагмент оставлен в комментарии стартового Java-файла. При исправлении '
                'перенеси необходимые части в рабочую область. Если условие просит только '
                'объяснить, запускать опасный вариант не нужно.', '', '```java', t['faulty'], '```', '']
    if t['stdin']:
        out += ['### Пример ввода', '', '```input', t['stdin'].rstrip('\n'), '```', '']
    out += ['### Проверь себя', ''] + ['- ' + c for c in t['checks']]
    out += ['', '**Твой план / прогноз:** ____________________', '',
            '**Результат проверки / причина ошибки:** ____________________', '']
    return '\n'.join(out)

def project_text(p):
    out = [f"# Мини-проект {p['id']:02}. {p['title']}", '',
           f"После главы {p['after']:02}. {p['summary']}", '',
           '## Договор приложения', '', p['brief'], '',
           '## Исходные данные', '', '```java', p['data'], '```', '']
    if p['stdin']:
        out += ['## Демонстрационный ввод', '', '```input', p['stdin'].rstrip('\n'), '```', '']
    out += ['## Этапы', ''] + [f'{i}. {x}' for i, x in enumerate(p['milestones'], 1)]
    out += ['', '## Критерии готовности', ''] + ['- ' + x for x in p['checks']]
    out += ['', '## Следующее расширение', ''] + ['- ' + x for x in p['extensions']]
    out += ['', 'Готового решения нет. Сначала добейся работающей модели на фиксированных данных, '
            'затем подключай остальные части. Запиши в комментарии свой план, трудность и проверенный результат.', '']
    return '\n'.join(out)

def project_starter(p):
    name = f"Project{p['id']:02}"
    imp = imports(p['data'])
    out = [f'package ru.vantaeonx.javaguide.projects;\n', imp + '\n' if imp else '',
           '// Автор: ____________________', f"// {name}. {p['title']}",
           f'public class {name} {{', comment(p['brief']), '',
           '    public static void main(String[] args) {',
           '        // Данные для первой реализации; ввод добавляй по договору проекта.',
           textwrap.indent(p['data'], '        '), '',
           '        // TODO: твой сценарий и проверки. Готового решения здесь нет.',
           '        // План: ____________________']
    out += [comment('Критерий: ' + x, '        ') for x in p['checks']]
    out += ['    }', '', '    // TODO: твои модели, интерфейсы и методы.', '}', '']
    return '\n'.join(out)

def generated():
    out = {}
    for t in TASKS:
        out[BASE / f"ch{t['chapter']:02}/Ex{t['id']:03}.java"] = starter(t)
    for ch in range(1, 21):
        out[Path(f'course/practice/ch{ch:02}.md')] = '\n'.join(
            practice(t) for t in TASKS if t['chapter'] == ch)
    for p in PROJECTS:
        out[BASE / f"projects/Project{p['id']:02}.java"] = project_starter(p)
        out[Path(f"course/projects/project{p['id']:02}.md")] = project_text(p)
    rows = ['# Прогресс: 180 упражнений и 6 проектов', '',
            'Ставь дату, когда решил и можешь объяснить. Повторение: через 1, 7 и 21 день. '
            'Если на повторении не получилось, вернись к модели из главы и назначь новую дату.', '',
            '| ID | Тема / уровень | Сделано | +1 день | +7 дней | +21 день | Что исправить |',
            '|---|---|---|---|---|---|---|']
    rows += [f"| Ex{t['id']:03} | {t['chapter']:02} / {t['level']} | | | | | |" for t in TASKS]
    rows += [f"| Project{p['id']:02} | после {p['after']:02} | | | | | |" for p in PROJECTS]
    out[Path('docs/PROGRESS.md')] = '\n'.join(rows) + '\n'
    for chapter in sorted((ROOT / 'course/chapters').glob('*.md')):
        code = re.findall(r'```java\n(.*?)\n```', chapter.read_text(), re.S)
        assert len(code) == 1, chapter
        number = int(chapter.name[:2])
        out[Path(f'examples/Example{number:02}.java')] = code[0] + '\n'
    return out

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--write', action='store_true', help='Перезаписывает заготовки; только для редактора.')
    args = parser.parse_args()
    mismatches = []
    for path, content in generated().items():
        target = ROOT / path
        if args.write:
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(content)
        elif not target.exists() or target.read_text() != content:
            mismatches.append(str(path))
    if mismatches:
        raise SystemExit('Рассинхронизация редакторской версии:\n' + '\n'.join(mismatches))
    print('Генерация: записано' if args.write else 'Генерация: совпадает', len(generated()), 'файлов')
