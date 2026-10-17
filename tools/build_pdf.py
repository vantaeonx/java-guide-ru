#!/usr/bin/env python3
"""Воспроизводимая вёрстка учебника из Markdown и единого каталога заданий."""
import html
import json
import re
import textwrap
from pathlib import Path
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (BaseDocTemplate, PageTemplate, Frame, Paragraph,
                               Spacer, PageBreak, Flowable, Table, TableStyle,
                               KeepTogether)
from reportlab.platypus.tableofcontents import TableOfContents
ROOT = Path(__file__).resolve().parents[1]
TASKS = json.loads((ROOT / 'course/catalog.json').read_text())
PROJECTS = json.loads((ROOT / 'course/projects.json').read_text())
W, H = A4
LEFT, RIGHT, TOP, BOTTOM = 49, 49, 57, 48
WIDTH = W - LEFT - RIGHT
NAVY = colors.HexColor('#153148')
TEAL = colors.HexColor('#007F79')
ORANGE = colors.HexColor('#D16B35')
INK = colors.HexColor('#243747')
MUTED = colors.HexColor('#607582')
PAPER = colors.HexColor('#FFFEFA')
PALE = colors.HexColor('#EEF5F4')
LINE = colors.HexColor('#CBD9DB')
FONT_DIR = Path('/usr/share/fonts/truetype/dejavu')
for name, file in [('Body', 'DejaVuSans.ttf'), ('Bold', 'DejaVuSans-Bold.ttf'),
                   ('Mono', 'DejaVuSansMono.ttf')]:
    pdfmetrics.registerFont(TTFont(name, str(FONT_DIR / file)))
pdfmetrics.registerFontFamily('Body', normal='Body', bold='Bold', italic='Body', boldItalic='Bold')
ST = {
    'body': ParagraphStyle('body', fontName='Body', fontSize=10.2, leading=14.3,
                           textColor=INK, spaceAfter=8, allowWidows=0, allowOrphans=0),
    'h1': ParagraphStyle('h1', fontName='Bold', fontSize=25, leading=31,
                         textColor=NAVY, spaceAfter=20, keepWithNext=True),
    'h2': ParagraphStyle('h2', fontName='Bold', fontSize=13.6, leading=18,
                         textColor=TEAL, spaceBefore=10, spaceAfter=7, keepWithNext=True),
    'h3': ParagraphStyle('h3', fontName='Bold', fontSize=10.4, leading=14,
                         textColor=NAVY, spaceBefore=10, spaceAfter=7, keepWithNext=True),
    'meta': ParagraphStyle('meta', fontName='Bold', fontSize=9, leading=13,
                           textColor=TEAL, spaceAfter=12),
    'small': ParagraphStyle('small', fontName='Body', fontSize=8.4, leading=12,
                            textColor=MUTED, spaceAfter=7),
    'bullet': ParagraphStyle('bullet', fontName='Body', fontSize=10, leading=14.5,
                             textColor=INK, leftIndent=12, firstLineIndent=-10, spaceAfter=6),
    'cell': ParagraphStyle('cell', fontName='Body', fontSize=8.5, leading=12,
                           textColor=INK),
    'toc': ParagraphStyle('toc', fontName='Body', fontSize=10, leading=15,
                          textColor=NAVY, spaceBefore=5, spaceAfter=5,
                          rightIndent=25),
}

def clean(s):
    return s.replace('—', '-').replace('–', '-').replace('\u2011', '-').replace('\u00a0', ' ')

def inline(s):
    s = html.escape(clean(s))
    s = re.sub(r'`([^`]+)`', r'<font name="Mono">\1</font>', s)
    s = re.sub(r'\*\*([^*]+)\*\*', r'<b>\1</b>', s)
    def link(m):
        label, url = m.groups()
        if url.startswith('http'):
            return f'<link href="{url}" color="#007F79">{label}</link>'
        return label
    return re.sub(r'\[([^\]]+)\]\(([^)]+)\)', link, s)

def para(s, style='body'):
    return Paragraph(inline(s), ST[style])

def heading(s, level=1, key=None):
    p = para(s, 'h' + str(level))
    if key:
        p.bookmark = key
        p.section_title = clean(s)
    return p

class CodeBlock(Flowable):
    def __init__(self, text, language='java'):
        Flowable.__init__(self)
        self.text, self.language = clean(text), language
        self.spaceAfter = 11
    def wrap(self, availWidth, availHeight):
        self.width = availWidth
        char_width = pdfmetrics.stringWidth('M', 'Mono', 8.4)
        max_chars = int((availWidth - 22) / char_width)
        self.lines = []
        for line in self.text.splitlines() or ['']:
            # Перенос помечается: это вёрстка, а не новая инструкция исходника.
            if len(line) <= max_chars:
                self.lines.append(line)
            else:
                self.lines.extend(textwrap.wrap(line, max_chars,
                    subsequent_indent='    > ', replace_whitespace=False,
                    drop_whitespace=False, break_long_words=True, break_on_hyphens=False))
        self.height = 29 + len(self.lines) * 11.3
        return self.width, self.height
    def split(self, availWidth, availHeight):
        # Блоки примеров короткие; при необходимости делим по отображаемым строкам.
        self.wrap(availWidth, availHeight)
        if self.height <= H - TOP - BOTTOM:
            return []
        max_lines = int((availHeight - 29) // 11.3)
        if max_lines < 3:
            return []
        if len(self.lines) > max_lines:
            return [CodeBlock('\n'.join(self.lines[:max_lines]), self.language),
                    CodeBlock('\n'.join(self.lines[max_lines:]), self.language + ' / продолжение')]
        return [self]
    def draw(self):
        c = self.canv
        c.setFillColor(colors.HexColor('#EFF3F6'))
        c.roundRect(0, 0, self.width, self.height, 5, fill=1, stroke=0)
        c.setFillColor(MUTED)
        c.setFont('Bold', 7)
        label = {'output': 'ВЫВОД ПРИМЕРА', 'input': 'СТАНДАРТНЫЙ ВВОД',
                 'bash': 'ТЕРМИНАЛ'}.get(self.language, self.language.upper())
        c.drawString(11, self.height - 13, label)
        c.setFillColor(NAVY)
        c.setFont('Mono', 8.4)
        y = self.height - 28
        for line in self.lines:
            c.drawString(11, y, line)
            y -= 11.3

class NoteLines(Flowable):
    def __init__(self, count=3):
        Flowable.__init__(self)
        self.count = count
        self.height = 19 * count
    def wrap(self, aw, ah):
        self.width = aw
        return aw, self.height
    def draw(self):
        self.canv.setStrokeColor(LINE)
        for i in range(self.count):
            y = self.height - 17 - i * 19
            self.canv.line(0, y, self.width, y)

class Cover(Flowable):
    def wrap(self, aw, ah):
        self.width, self.height = aw, min(ah, 730)
        return aw, self.height
    def draw(self):
        c = self.canv
        c.setFillColor(NAVY)
        c.rect(-LEFT, -BOTTOM, W, H, fill=1, stroke=0)
        c.setFillColor(TEAL)
        c.circle(W - 135, self.height - 55, 110, fill=1, stroke=0)
        c.setFillColor(colors.HexColor('#36B5A0'))
        c.setFont('Bold', 10)
        c.drawString(0, self.height - 35, 'ПОНЯТЬ МОДЕЛЬ. НАПИСАТЬ КОД. ПРОВЕРИТЬ СЕБЯ.')
        c.setFillColor(colors.white)
        c.setFont('Bold', 79)
        c.drawString(-4, self.height - 177, 'JAVA')
        c.setFont('Bold', 37)
        c.drawString(0, self.height - 229, 'с нуля')
        c.setFont('Body', 16)
        for i, text in enumerate(['До уверенного понимания языка,',
                                  'объектов и небольших приложений.']):
            c.drawString(0, self.height - 278 - i * 24, text)
        c.setFillColor(colors.HexColor('#F7CDAF'))
        c.roundRect(0, self.height - 425, WIDTH, 68, 8, fill=1, stroke=0)
        c.setFillColor(NAVY)
        c.setFont('Bold', 17)
        c.drawString(18, self.height - 386, '20 глав / 180 упражнений / 6 проектов')
        c.setFont('Body', 10)
        c.drawString(18, self.height - 407, 'Теория, примеры, ошибки, самостоятельная практика')
        c.setFillColor(colors.white)
        c.setFont('Mono', 12)
        for i, text in enumerate(['исходник -> компилятор -> JVM',
                                  'значения -> ссылки -> объекты',
                                  'контракт -> реализация -> проверка']):
            c.drawString(0, self.height - 495 - i * 26, text)
        c.setFillColor(colors.HexColor('#BFD6DF'))
        c.setFont('Body', 10)
        c.drawString(0, 56, 'На русском / Java 17 / JDK 25 / Ubuntu / IntelliJ IDEA')
        c.drawString(0, 35, 'Самостоятельная работа без готовых решений упражнений')
        c.setFont('Bold', 10)
        c.drawString(0, 10, 'vantaeonx · Издание 1.0 · 2026')

class ReferenceDiagram(Flowable):
    def wrap(self, aw, ah):
        self.width, self.height = aw, 153
        return aw, self.height
    def draw(self):
        c = self.canv
        c.setFont('Bold', 10)
        c.setFillColor(TEAL)
        c.drawString(0, 135, 'ССЫЛКА И ОБЪЕКТ - РАЗНЫЕ ВЕЩИ')
        boxes = [(0, 78, 105, 30, 'refA'), (0, 33, 105, 30, 'refB'),
                 (235, 60, 215, 58, 'Один общий объект'),
                 (235, 0, 215, 35, 'Копия ссылки не копирует объект')]
        for x,y,w,h,label in boxes:
            c.setFillColor(PALE)
            c.roundRect(x,y,w,h,5,fill=1,stroke=0)
            c.setFillColor(NAVY)
            c.setFont('Body', 8 if h==35 else 10)
            c.drawCentredString(x+w/2,y+h/2-3,label)
        c.setStrokeColor(TEAL)
        for yy in (93,48):
            c.line(105,yy,232,87)
            c.line(232,87,224,88)
            c.line(232,87,227,81)

def table(rows, widths=None, repeat=1):
    data = [[para(cell, 'cell') for cell in row] for row in rows]
    tb = Table(data, colWidths=widths or [WIDTH / len(rows[0])] * len(rows[0]), repeatRows=repeat)
    tb.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#DDEDE9')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F5F7F7')]),
        ('BOX', (0, 0), (-1, -1), 0.4, LINE),
        ('LINEBELOW', (0, 0), (-1, 0), 0.7, TEAL),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('LEFTPADDING', (0, 0), (-1, -1), 7),
        ('RIGHTPADDING', (0, 0), (-1, -1), 7),
        ('TOPPADDING', (0, 0), (-1, -1), 7),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 7),
    ]))
    tb.spaceAfter = 12
    return tb

def markdown(text, key=None, first_level=1):
    lines = text.splitlines()
    out, i, first = [], 0, True
    while i < len(lines):
        line = lines[i]
        if not line.strip():
            i += 1; continue
        if line.startswith('```'):
            language = line[3:]
            i += 1; code = []
            while i < len(lines) and not lines[i].startswith('```'):
                code.append(lines[i]); i += 1
            out.append(CodeBlock('\n'.join(code), language)); i += 1; continue
        if line.startswith('#'):
            n = len(line) - len(line.lstrip('#'))
            out.append(heading(line[n:].strip(), min(n, 3), key if first else None))
            first = False; i += 1; continue
        if line.startswith('|'):
            rows=[]
            while i < len(lines) and lines[i].startswith('|'):
                if not re.match(r'^\|[\s:|\-]+\|$', lines[i]):
                    rows.append([x.strip() for x in lines[i].strip('|').split('|')])
                i += 1
            out.append(table(rows)); continue
        if re.match(r'^(- |\d+\. )', line):
            text = line
            i += 1
            while i < len(lines) and lines[i].strip() and not re.match(r'^(#|```|\||- |\d+\. )', lines[i]):
                text += ' ' + lines[i].strip(); i += 1
            out.append(para(text, 'bullet')); continue
        text = line
        i += 1
        while i < len(lines) and lines[i].strip() and not re.match(r'^(#|```|\||- |\d+\. )', lines[i]):
            text += ' ' + lines[i].strip(); i += 1
        out.append(para(text))
    if key and key.startswith('ch'):
        sections = [i for i,x in enumerate(out) if isinstance(x, Paragraph) and x.style.name == 'h2']
        if sections:
            last = sections[-1]
            out[last:] = [KeepTogether(out[last:])]
    return out

class BookDoc(BaseDocTemplate):
    def afterFlowable(self, item):
        if hasattr(item, 'bookmark'):
            self.canv.bookmarkPage(item.bookmark)
            self.canv.addOutlineEntry(item.section_title, item.bookmark, 0, False)
            self.notify('TOCEntry', (0, html.escape(item.section_title), self.page, item.bookmark))
        if isinstance(item, Paragraph) and hasattr(item, 'exercise_key'):
            self.canv.bookmarkPage(item.exercise_key)

def page(c, doc):
    if doc.page == 1:
        return
    c.saveState()
    c.setFillColor(PAPER)
    c.rect(0, 0, W, H, fill=1, stroke=0)
    c.setStrokeColor(LINE)
    c.line(LEFT, H - 34, W - RIGHT, H - 34)
    c.line(LEFT, 33, W - RIGHT, 33)
    c.setFillColor(TEAL)
    c.rect(LEFT, H - 36, 30, 3, fill=1, stroke=0)
    c.setFillColor(NAVY)
    c.setFont('Bold', 8)
    c.drawString(LEFT, H - 24, 'JAVA / С НУЛЯ')
    c.setFillColor(MUTED)
    c.setFont('Body', 7.5)
    c.drawRightString(W - RIGHT, H - 24, 'Теория и самостоятельная практика')
    c.drawString(LEFT, 20, 'Java 17 · vantaeonx · Издание 1.0')
    c.drawRightString(W - RIGHT, 20, str(doc.page))
    c.restoreState()

def exercise(t):
    out = [PageBreak(), para(f"ГЛАВА {t['chapter']:02} / EX{t['id']:03}", 'meta')]
    title = heading(t['title'], 1)
    title.exercise_key = f"ex{t['id']:03}"
    out += [title, para(f"Уровень {t['level']} · {t['kind']} · Ex{t['id']:03}.java", 'meta')]
    out += [para('Перед началом', 'h3'), para(t['focus']),
            para('Твоя задача', 'h3'), para(t['prompt'])]
    if t['data']:
        out += [CodeBlock(t['data'])]
    if t['faulty']:
        out += [para('НАМЕРЕННАЯ ОШИБКА / ФРАГМЕНТ ДЛЯ АНАЛИЗА', 'meta'),
                para('В стартовом файле фрагмент закомментирован. Переноси его в рабочую '
                     'область только по условию: методы и классы вне main, инструкции внутри.', 'small'),
                CodeBlock(t['faulty'])]
    if t['stdin']:
        out += [CodeBlock(t['stdin'].rstrip('\n'), 'input')]
    if t['members']:
        out += [CodeBlock(t['members']), para('Объявления уже есть в Java-файле. Реализуй TODO перед вызовом; '
                     'для анализа исходные методы оставлены рабочими.', 'small')]
    out += [para('Проверь себя', 'h3')]
    out += [para('- ' + c, 'bullet') for c in t['checks']]
    out += [para('План / прогноз / причина ошибки', 'h3'), NoteLines(3)]
    return out

def build():
    target = ROOT / 'output/pdf/java-guide-ru.pdf'
    target.parent.mkdir(parents=True, exist_ok=True)
    doc = BookDoc(str(target), pagesize=A4, leftMargin=LEFT, rightMargin=RIGHT,
                  topMargin=TOP, bottomMargin=BOTTOM,
                  title='Java с нуля: 20 глав, 180 упражнений и 6 проектов', author='vantaeonx')
    doc.addPageTemplates(PageTemplate(id='book', frames=[Frame(LEFT, BOTTOM, WIDTH,
        H - TOP - BOTTOM, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)], onPage=page))
    story=[Cover(), PageBreak(), heading('Оглавление', 1)]
    toc=TableOfContents()
    toc.levelStyles=[ST['toc']]
    toc.dotsMinLevel=0
    story += [para('Нажми название, чтобы перейти к разделу. Упражнения находятся сразу '
                   'после теории своей главы; номера файлов сквозные.', 'small'), toc, PageBreak()]
    story += markdown((ROOT/'course/INTRO.md').read_text(), 'intro')
    story += [PageBreak()] + markdown((ROOT/'course/SETUP.md').read_text(), 'setup')
    story += [PageBreak(), heading('Карта курса и условия перехода', 1, 'map')]
    rows=[['Главы', 'Что осваиваешь', 'Практика']]
    rows += [['01-05', 'Компиляция, типы, ввод и ветвления', 'Ex001-045 / проект 01'],
             ['06-09', 'Алгоритмы, последовательности и методы', 'Ex046-081 / проект 02'],
             ['10-14', 'Объекты, договоры и отказы', 'Ex082-126 / проект 03'],
             ['15-18', 'Структуры данных, generics и файлы', 'Ex127-162 / проекты 04-05'],
             ['19-20', 'Проверки и законченное приложение', 'Ex163-180 / проект 06']]
    story += [table(rows, [65,240,WIDTH-305]), para('Перед новой темой проверь, можешь ли '
        'объяснить модель и пройти начальные проверки без подсказки. Не используй готовые '
        'ответы как меру освоения. Для сложной задачи сначала выдели минимальный рабочий шаг.'),
        para('Как читать код в PDF', 'h2'), para('Точные исходники находятся в Java-файлах. '
        'Длинные строки в книге могут переноситься; продолжение отмечено >. Этот знак '
        'в начале перенесённой строки не является частью Java-кода. Для копирования '
        'используй исходный файл. Не перепечатывай весь каркас, чтобы начать упражнение.')]
    story += [Spacer(1, 15), ReferenceDiagram()]
    for chapter in sorted((ROOT/'course/chapters').glob('*.md')):
        ch=int(chapter.name[:2])
        story += [PageBreak(), para(f'ГЛАВА {ch:02} / ТЕОРИЯ', 'meta')]
        story += markdown(chapter.read_text(), f'ch{ch:02}')
        for t in TASKS:
            if t['chapter']==ch:
                story += exercise(t)
    for p in PROJECTS:
        story += [PageBreak(), para(f"ПОСЛЕ ГЛАВЫ {p['after']:02} / МИНИ-ПРОЕКТ {p['id']:02}", 'meta'),
                  heading(f"{p['title']}", 1, f"project{p['id']:02}"),
                  para(p['summary']), heading('Договор приложения', 2), para(p['brief']),
                  heading('Исходные данные', 2), CodeBlock(p['data']),
                  para(f"Стартовый файл: Project{p['id']:02}.java. Сначала реализуй модель на этих данных. "
                       'Этапы, проверки и расширения - на следующей странице.', 'small')]
        story += [PageBreak(), heading(f"Проект {p['id']:02}: план и проверка", 1), heading('Этапы', 2)]
        story += [para(f'{i}. {x}', 'bullet') for i,x in enumerate(p['milestones'],1)]
        if p['stdin']:
            story += [heading('Демонстрационный ввод', 2), CodeBlock(p['stdin'].rstrip('\n'), 'input')]
        story += [heading('Критерии готовности', 2)]
        story += [para('- ' + x, 'bullet') for x in p['checks']]
        story += [heading('Следующее расширение', 2)]
        story += [para('- ' + x, 'bullet') for x in p['extensions']]
        story += [heading('Твой следующий проверяемый шаг', 3), NoteLines(2)]
    for path,key in [('docs/REFERENCE.md','reference'), ('docs/GLOSSARY.md','glossary')]:
        story += [PageBreak()] + markdown((ROOT/path).read_text(), key)
    story += [PageBreak(), heading('Таблица прогресса', 1, 'progress'),
        para('Запиши даты решения и повторения. На повторении сначала объясни модель без '
             'просмотра своего кода. Если не получилось, отметь причину и назначь новый срок.')]
    for ch in range(1,21):
        if ch>1 and (ch-1)%2==0:
            story += [PageBreak()]
        story += [heading(f'Глава {ch:02}',2)]
        rows=[['Файл','Ур.','Решено','+1 день','+7 дней','+21 день']]
        rows += [[f"Ex{t['id']:03}",str(t['level']),'','','',''] for t in TASKS if t['chapter']==ch]
        story += [table(rows, [68,30,94,94,94,WIDTH-380])]
    rows=[['Проект','Готово','Что улучшить']]
    rows += [[f"Project{p['id']:02}",'',''] for p in PROJECTS]
    story += [PageBreak(), heading('Прогресс мини-проектов', 1),
              para('Отмечай готовность после проверки всех критериев. Запиши один дефект, '
                   'который обнаружил сам, и объясни, какая проверка его поймала. Готовность '
                   'модели, консольного интерфейса и файла проверяется отдельно.'),
              table(rows,[85,90,WIDTH-175]), heading('Что уже можешь объяснить', 2),
              para('- Как модель сохраняет инварианты после успеха и отказа.', 'bullet'),
              para('- Почему выбран именно этот контейнер и договор равенства.', 'bullet'),
              para('- Как вычисление проверить без реальной консоли и диска.', 'bullet'),
              para('- Что произойдёт при пустом или повреждённом файле.', 'bullet'),
              heading('План следующего этапа', 2), NoteLines(5)]
    story += [PageBreak()] + markdown((ROOT/'docs/SOURCES.md').read_text(),'sources')
    story += [heading('Педагогическая отправная точка',2),
        para('В python-guide-ru сохранён удачный принцип: уровни, независимые файлы, '
             'чтение и исправление кода. В оригинале указана благодарность Nicolas Hinckxt '
             'за структуру PHP-сборника. Java-тексты, примеры и задания написаны отдельно; '
             'механического переноса Python-задач нет. Анализ и проектирование находятся '
             'в docs/ORIGINAL_REVIEW.md. Лицензия нового пособия и кода - MIT.'),
        para('Чего книга не обещает', 'h2'),
        para('Это фундамент языка и консольной разработки. Конкретный Minecraft API, '
             'многопоточность, сеть, базы данных, GUI и фреймворки требуют следующего '
             'этапа. Проверяй требования выбранной платформы по её официальным источникам.')]
    doc.multiBuild(story)
    print(target)

if __name__ == '__main__':
    build()
