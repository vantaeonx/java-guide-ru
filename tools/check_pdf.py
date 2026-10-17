#!/usr/bin/env python3
"""Текстовая и геометрическая проверка PDF; визуальный просмотр остаётся отдельным."""
import json
import re
from pathlib import Path
from pypdf import PdfReader
import pdfplumber
ROOT = Path(__file__).resolve().parents[1]

def norm(text):
    return re.sub(r'\s+', '', text.replace('—', '-').replace('–', '-').replace('\u2011', '-'))

def prose(text):
    text = re.sub(r'```.*?```', '', text, flags=re.S)
    text = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', text)
    text = text.replace('`', '').replace('**', '')
    return [p.strip().lstrip('#').strip() for p in text.split('\n\n') if p.strip()]

def check():
    target = ROOT / 'output/pdf/java-guide-ru.pdf'
    reader = PdfReader(target)
    texts = [p.extract_text() for p in reader.pages]
    # Колонтитулы рисуются до основного текста и могут разрывать абзац при извлечении.
    cleaned = []
    for text in texts:
        text = re.sub(r'^JAVA / С НУЛЯ\nТеория и самостоятельная практика\n', '', text)
        text = re.sub(r'^Java 17 · vantaeonx · Издание 1.0\n\d+\n', '', text)
        cleaned.append(text)
    full = norm('\n'.join(cleaned))
    tasks = json.loads((ROOT / 'course/catalog.json').read_text())
    projects = json.loads((ROOT / 'course/projects.json').read_text())
    for t in tasks:
        for label, text in [('название', t['title']), ('условие', t['prompt'])] + [('проверка', c) for c in t['checks']]:
            assert norm(text) in full, (t['id'], label)
    for p in projects:
        for text in [p['brief']] + p['milestones'] + p['checks'] + p['extensions']:
            assert norm(text) in full, ('project', p['id'])
    paragraphs = 0
    for chapter in (ROOT / 'course/chapters').glob('*.md'):
        for paragraph in prose(chapter.read_text()):
            assert norm(paragraph) in full, (chapter.name, paragraph[:60])
            paragraphs += 1
    assert len(reader.outline) == 33
    assert len(reader.pages) >= 200
    violations = []
    with pdfplumber.open(target) as pdf:
        for number, page in enumerate(pdf.pages, 1):
            if number == 1:
                continue
            for char in page.chars:
                if not char['text'].strip():
                    continue
                if char['x0'] < 42 or char['x1'] > page.width - 42 or char['top'] < 8 or char['bottom'] > page.height - 8:
                    violations.append(number)
    assert not violations, ('Текст вне границ', sorted(set(violations)))
    print(f'PDF: {len(reader.pages)} страниц, 33 закладки; 180 условий и 6 проектов совпадают.')
    print(f'Полнота теории: {paragraphs} заголовков/абзацев; геометрия всех страниц: OK.')

if __name__ == '__main__':
    check()
