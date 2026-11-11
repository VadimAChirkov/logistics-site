#!/usr/bin/env python3
"""Генератор полнотекстового поискового индекса для сайта «Международная логистика».

Проходит все HTML-страницы в корне сайта, извлекает <title> и текст из
<main>/<article> (без тегов, скриптов и стилей), и пишет search-index.js
со структурой: window.SEARCH_INDEX = [{t, u, text}].

Запуск: python3 scripts/build_search_index.py
"""
import re
import os
import glob

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

TAG_RE = re.compile(r'<[^>]+>')
SCRIPT_STYLE_RE = re.compile(r'<(script|style)[^>]*>.*?</\1>', re.S | re.I)


def strip_tags(html: str) -> str:
    html = SCRIPT_STYLE_RE.sub(' ', html)
    html = TAG_RE.sub(' ', html)
    return html


def extract_main(html: str) -> str:
    """Берём содержимое <main>…</main>, иначе <article>, иначе всё тело."""
    m = re.search(r'<main[^>]*>(.*?)</main>', html, re.S | re.I)
    if m:
        return m.group(1)
    m = re.search(r'<article[^>]*>(.*?)</article>', html, re.S | re.I)
    if m:
        return m.group(1)
    return html


def normalize(text: str) -> str:
    # HTML-сущности
    text = text.replace('&nbsp;', ' ').replace('&amp;', '&').replace('&mdash;', '—')
    text = text.replace('&laquo;', '«').replace('&raquo;', '»').replace('&ndash;', '–')
    text = re.sub(r'\s+', ' ', text)
    return text.strip()


def main():
    files = sorted(glob.glob(os.path.join(BASE, '*.html')))
    entries = []
    for path in files:
        name = os.path.basename(path)
        with open(path, encoding='utf-8') as f:
            html = f.read()
        t = re.search(r'<title[^>]*>(.*?)</title>', html, re.S | re.I)
        title = t.group(1).strip() if t else name
        body = extract_main(html)
        text = normalize(strip_tags(body))
        if not text:
            continue
        entries.append((title, name, text))

    lines = ['// Полнотекстовый поисковый индекс — генерируется скриптом scripts/build_search_index.py',
             'window.SEARCH_INDEX = [']
    for title, name, text in entries:
        # экранируем для JS-строки
        t = title.replace('\\', '\\\\').replace("'", "\\'")
        u = name.replace('\\', '\\\\').replace("'", "\\'")
        x = text.replace('\\', '\\\\').replace("'", "\\'")
        lines.append("  {t:'%s', u:'%s', text:'%s'}," % (t, u, x))
    lines.append('];')

    out = os.path.join(BASE, 'search-index.js')
    with open(out, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))
    print('Сгенерировано %d страниц → %s (%d байт)' % (
        len(entries), out, os.path.getsize(out)))


if __name__ == '__main__':
    main()
