#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Регенерация хлебных крошек (breadcrumbs) на сайте logistics-site.
Каждый уровень крошки становится кликабельной ссылкой на родительскую страницу.
Обновляет: <p class="breadcrumb"> и JSON-LD BreadcrumbList.
"""
import re, os, sys

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RU_DIR = BASE          # RU страницы в корне
EN_DIR = os.path.join(BASE, 'en')

# ---------- Иерархия (родитель -> дочерние). None = верхний уровень (родитель index) ----------
PARENTS = {
    # верхний уровень
    'incoterms': None, 'sea-freight': None, 'rail-freight': None, 'air-freight': None,
    'road-freight': None, 'dangerous-goods': None, 'customs-clearance': None,
    'ucp600': None, 'vat-export-import': None, 'export-support': None, 'glossary': None, 'news': None,
    'admin-news': None, 'about': None, 'contact': None, 'literature': None,
    'disclaimer': None, 'contributors': None,
    # sea-freight
    'documents-sea': 'sea-freight', 'regulations-sea': 'sea-freight',
    'chartering': 'sea-freight', 'chartering-technique': 'sea-freight',
    'chartering-abbreviations': 'sea-freight',
    # rail-freight
    'documents-rail': 'rail-freight', 'regulations-rail': 'rail-freight',
    'rail-shipment-guide': 'rail-freight', 'railway-technical-conditions': 'rail-freight',
    'railway-experimental-check': 'rail-freight', 'railway-gu12': 'rail-freight',
    'railway-acts': 'rail-freight', 'railway-oversized': 'rail-freight',
    # air-freight
    'documents-air': 'air-freight', 'regulations-air': 'air-freight',
    # road-freight
    'documents-road': 'road-freight', 'regulations-road': 'road-freight',
    # dangerous-goods
    'dangerous-goods-road': 'dangerous-goods', 'dangerous-goods-rail': 'dangerous-goods',
    'dangerous-goods-sea': 'dangerous-goods', 'dangerous-goods-air': 'dangerous-goods',
    # customs
    'tnved-hs-code': 'customs-clearance', 'currency-control': 'customs-clearance',
    'customs-calculation': 'customs-clearance', 'non-tariff-regulation': 'customs-clearance',
    'export-control': 'customs-clearance',
    # regulations-road (уровень 3)
    'cmr-convention': 'regulations-road', 'tir-convention': 'regulations-road',
    'road-transport-rules': 'regulations-road',
}

LABELS_RU = {
    'index': 'Главная',
    'incoterms': 'Инкотермс 2020', 'sea-freight': 'Морские перевозки',
    'rail-freight': 'Железнодорожные перевозки', 'air-freight': 'Авиаперевозки',
    'road-freight': 'Автоперевозки', 'dangerous-goods': 'Опасные грузы',
    'customs-clearance': 'Таможенное оформление', 'ucp600': 'UCP-600',
    'vat-export-import': 'НДС при экспорте и импорте', 'export-support': 'Поддержка экспорта из РФ', 'glossary': 'Глоссарий',
    'news': 'Новости рынка', 'admin-news': 'Информация от администратора',
    'about': 'О себе', 'contact': 'Связаться', 'literature': 'Литература и источники',
    'disclaimer': 'Правовая информация', 'contributors': 'Рецензенты и материалы',
    'documents-sea': 'Коносамент (B/L)', 'regulations-sea': 'Морские конвенции',
    'chartering': 'Фрахтование судов', 'chartering-technique': 'Техника фрахтовых операций',
    'chartering-abbreviations': 'Фрахтовые сокращения',
    'documents-rail': 'Перевозочные документы', 'regulations-rail': 'Соглашения и правила',
    'rail-shipment-guide': 'Как организовать отправку груза',
    'railway-technical-conditions': 'Технические условия (ЦМ-943)',
    'railway-experimental-check': 'Экспериментальная проверка',
    'railway-gu12': 'Заявка на перевозку (ГУ-12)',
    'railway-acts': 'Коммерческий акт',
    'railway-oversized': 'Негабаритные и тяжеловесные грузы',
    'documents-air': 'Авианакладная (AWB)', 'regulations-air': 'Авиационные конвенции',
    'documents-road': 'Документы автоперевозок', 'regulations-road': 'Конвенции и правила',
    'dangerous-goods-road': 'Автомобильные перевозки',
    'dangerous-goods-rail': 'Железнодорожные перевозки',
    'dangerous-goods-sea': 'Морские перевозки',
    'dangerous-goods-air': 'Авиаперевозки',
    'tnved-hs-code': 'ТН ВЭД / код HS', 'currency-control': 'Валютный контроль',
    'customs-calculation': 'Расчёт таможенных платежей',
    'non-tariff-regulation': 'Нетарифное регулирование', 'export-control': 'Экспортный контроль',
    'cmr-convention': 'Конвенция CMR', 'tir-convention': 'Конвенция TIR / МДП',
    'road-transport-rules': 'Правила перевозок грузов',
}

LABELS_EN = {
    'index': 'Home',
    'incoterms': 'Incoterms 2020', 'sea-freight': 'Sea freight',
    'rail-freight': 'Rail freight', 'air-freight': 'Air freight',
    'road-freight': 'Road freight', 'dangerous-goods': 'Dangerous goods',
    'customs-clearance': 'Customs clearance', 'ucp600': 'UCP-600',
    'vat-export-import': 'VAT on export and import', 'export-support': 'Export support', 'glossary': 'Glossary',
    'news': 'Market news', 'admin-news': 'Information from the administrator',
    'about': 'About', 'contact': 'Contact', 'literature': 'References and sources',
    'disclaimer': 'Legal information', 'contributors': 'Reviewers and contributions',
    'documents-sea': 'Bill of Lading (B/L)', 'regulations-sea': 'Maritime conventions',
    'chartering': 'Ship chartering', 'chartering-technique': 'Chartering operations technique',
    'chartering-abbreviations': 'Chartering abbreviations',
    'documents-rail': 'Consignment documents', 'regulations-rail': 'Rail agreements',
    'rail-shipment-guide': 'How to organise a rail shipment',
    'railway-technical-conditions': 'Technical Conditions (TsM-943)',
    'railway-experimental-check': 'Experimental verification',
    'railway-gu12': 'Consignment request (GU-12)',
    'railway-acts': 'Commercial report',
    'railway-oversized': 'Oversized and heavy cargo',
    'documents-air': 'Air Waybill (AWB)', 'regulations-air': 'Air conventions',
    'documents-road': 'Road transport documents', 'regulations-road': 'Road conventions',
    'dangerous-goods-road': 'Road transport', 'dangerous-goods-rail': 'Rail transport',
    'dangerous-goods-sea': 'Sea transport', 'dangerous-goods-air': 'Air transport',
    'tnved-hs-code': 'TN VED / HS code', 'currency-control': 'Currency control',
    'customs-calculation': 'Calculation of customs payments',
    'non-tariff-regulation': 'Non-tariff regulation', 'export-control': 'Export control',
    'cmr-convention': 'CMR Convention', 'tir-convention': 'TIR Convention',
    'road-transport-rules': 'Rules for the carriage of goods',
}


def trail_for(page, labels):
    """Возвращает список [(slug, label), ...] от index до текущей страницы."""
    chain = [page]
    cur = page
    while True:
        p = PARENTS.get(cur)
        if p is None:
            break
        chain.append(p)
        cur = p
    chain.append('index')
    chain.reverse()
    return [(slug, labels[slug]) for slug in chain]


def build_breadcrumb_html(page, labels):
    """Видимая крошка: все уровни, кроме последнего, — ссылки."""
    trail = trail_for(page, labels)
    parts = []
    for i, (slug, label) in enumerate(trail):
        if i == len(trail) - 1:
            parts.append(label)  # текущая страница — текст
        else:
            parts.append('<a href="%s.html">%s</a>' % (slug, label))
    return '<p class="breadcrumb">' + ' → '.join(parts) + '</p>'


def build_jsonld(page, labels, url_base):
    """JSON-LD BreadcrumbList."""
    trail = trail_for(page, labels)
    items = []
    for i, (slug, label) in enumerate(trail, start=1):
        url = url_base + '/' + ('' if slug == 'index' else slug + '.html')
        if slug == 'index':
            url = url_base + '/index.html'
        items.append('{"@type": "ListItem", "position": %d, "name": "%s", "item": "%s"}' % (i, label, url))
    inner = ', '.join(items)
    return '{"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [%s]}' % inner


def process_dir(directory, labels, url_base):
    changed = 0
    for fn in sorted(os.listdir(directory)):
        if not fn.endswith('.html') or fn == 'index.html':
            continue
        path = os.path.join(directory, fn)
        with open(path, 'r', encoding='utf-8') as f:
            html = f.read()

        page = fn[:-5]  # без .html
        if page not in PARENTS:
            print('  !! пропуск (нет в PARENTS):', fn)
            continue

        new_bc = build_breadcrumb_html(page, labels)
        new_ld = build_jsonld(page, labels, url_base)

        # 1) видимая крошка
        html, n1 = re.subn(r'<p class="breadcrumb">.*?</p>', new_bc, html, count=1, flags=re.S)
        # 2) JSON-LD BreadcrumbList (весь объект на одной строке — до конца строки)
        html, n2 = re.subn(
            r'\{"@context": "https://schema.org", "@type": "BreadcrumbList"[^\n]*',
            new_ld, html, count=1)

        if n1 == 0 or n2 == 0:
            print('  !! не найдено на', fn, '(bc=%d, ld=%d)' % (n1, n2))
            continue

        with open(path, 'w', encoding='utf-8') as f:
            f.write(html)
        changed += 1
    return changed


def main():
    ru = process_dir(RU_DIR, LABELS_RU, 'https://chirkov-logistics.ru')
    en = process_dir(EN_DIR, LABELS_EN, 'https://chirkov-logistics.ru/en')
    print('RU обновлено:', ru)
    print('EN обновлено:', en)


if __name__ == '__main__':
    main()
