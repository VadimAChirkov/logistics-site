#!/usr/bin/env python3
"""Автообновление новостей логистики из RSS-лент.

Вызывается из GitHub Actions (workflow .github/workflows/update-news.yml).
Тянет RSS-ленты, берёт свежие заголовки, пишет news-data.js.
Только стандартная библиотека — без pip-зависимостей.
"""
import json
import re
import sys
import urllib.request
import xml.etree.ElementTree as ET
from email.utils import parsedate_to_datetime

# Источники: (url RSS, отображаемое имя)
SOURCES = [
    ("https://portnews.ru/news/rss/", "PortNews"),
    ("https://infranews.ru/rss/", "InfraNews"),
    ("https://logirus.ru/news/rss/", "Logirus"),
    ("https://www.freightwaves.com/rss", "FreightWaves"),
    ("https://splash247.com/feed/", "Splash 247"),
    ("https://theloadstar.com/feed/", "The Loadstar"),
    ("https://www.rzd-partner.ru/news/rss/", "РЖД-Партнер"),
    ("https://seanews.ru/rss/", "SeaNews"),
]

MAX_ITEMS = 14
PER_SOURCE = 2   # сколько самых свежих записей брать с каждого источника
OUTPUT = "news-data.js"
UA = "Mozilla/5.0 (compatible; logistics-news-bot/1.0)"


def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=20) as r:
        return r.read()


def strip_tags(text):
    return re.sub(r"<[^>]+>", "", text or "").strip()


def clean(text):
    text = strip_tags(text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def parse_feed(data, src_name):
    items = []
    try:
        root = ET.fromstring(data)
    except ET.ParseError:
        return items

    # RSS 2.0
    for item in root.iter("item"):
        title = clean(item.findtext("title"))
        link = (item.findtext("link") or "").strip()
        pub = item.findtext("pubDate") or item.findtext("dc:date") or ""
        if not title or not link:
            continue
        items.append({"title": title, "url": link, "src": src_name, "date_raw": pub})

    # Atom
    ns = {"a": "http://www.w3.org/2005/Atom"}
    for entry in root.iter("{http://www.w3.org/2005/Atom}entry"):
        title = clean(entry.find("a:title", ns).text if entry.find("a:title", ns) is not None else "")
        link_el = entry.find("a:link", ns)
        link = link_el.get("href", "") if link_el is not None else ""
        pub = entry.find("a:updated", ns).text if entry.find("a:updated", ns) is not None else ""
        if not title or not link:
            continue
        items.append({"title": title, "url": link, "src": src_name, "date_raw": pub})

    return items


def parse_date(raw):
    if not raw:
        return None
    try:
        return parsedate_to_datetime(raw)
    except (TypeError, ValueError):
        return None


def main():
    def sort_key(it):
        d = parse_date(it.get("date_raw"))
        return d.timestamp() if d else 0

    # 1) с каждого источника берём PER_SOURCE самых свежих записей,
    #    чтобы в ленте были представлены ВСЕ источники, а не только самые оперативные
    balanced = []
    for url, name in SOURCES:
        try:
            data = fetch(url)
            items = parse_feed(data, name)
            items.sort(key=sort_key, reverse=True)
            kept = items[:PER_SOURCE]
            balanced.extend(kept)
            print(f"[OK] {name}: {len(items)} записей, взято {len(kept)}")
        except Exception as e:  # noqa: BLE001
            print(f"[SKIP] {name}: {e}", file=sys.stderr)

    if not balanced:
        print("Не удалось получить ни одной записи. Выход без записи.", file=sys.stderr)
        return 0

    # 2) сортируем всё вместе по дате (новые сверху), без даты — в конец
    balanced.sort(key=sort_key, reverse=True)

    # 3) дедупликация по URL + ограничение MAX_ITEMS
    seen = set()
    picked = []
    for it in balanced:
        if it["url"] in seen:
            continue
        seen.add(it["url"])
        picked.append(it)
        if len(picked) >= MAX_ITEMS:
            break

    if not picked:
        print("Нет записей после дедупликации.", file=sys.stderr)
        return 0

    # дата обновления (сегодня, UTC → но для отображения ок)
    from datetime import datetime, timezone
    now = datetime.now(timezone.utc)

    items_out = []
    for it in picked:
        d = parse_date(it.get("date_raw"))
        date_str = d.strftime("%d.%m.%Y") if d else ""
        items_out.append({
            "title": it["title"],
            "src": it["src"],
            "date": date_str,
            "url": it["url"],
        })

    payload = {
        "updated": now.strftime("%d.%m.%Y"),
        "items": items_out,
    }

    js = "// Новости рынка логистики и перевозок (автообновление GitHub Actions из RSS).\n" \
         "// Ручная правка перезапишется при следующем автообновлении.\n" \
         "window.NEWS = " + json.dumps(payload, ensure_ascii=False, indent=2) + ";\n"

    with open(OUTPUT, "w", encoding="utf-8") as f:
        f.write(js)

    print(f"Записано {len(items_out)} новостей в {OUTPUT}")


if __name__ == "__main__":
    main()
