#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Курсы валют ЦБ РФ (USD, EUR, CNY, AED) -> currency-data.js.
Портативная версия: пишет currency-data.js в директорию скрипта (корень репозитория).
Запускается из GitHub Actions (ежедневно) или вручную."""
import datetime as dt
import json
import re
import urllib.request
from pathlib import Path

SITE = Path(__file__).resolve().parent
CODES = ["USD", "EUR", "CNY", "AED"]
EN_NAMES = {"USD": "US Dollar", "EUR": "Euro", "CNY": "Chinese Yuan", "AED": "UAE Dirham"}
URL_DAILY = "https://www.cbr.ru/scripts/XML_daily.asp"


def fetch(date_str=None):
    url = URL_DAILY + (("?date_req=" + date_str) if date_str else "")
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (currency-fetch)"})
    with urllib.request.urlopen(req, timeout=25) as resp:
        return resp.read().decode("windows-1251")


def parse(xml_text):
    out = {}
    for m in re.finditer(r"<Valute[^>]*>.*?</Valute>", xml_text, re.S):
        block = m.group(0)
        code = re.search(r"<CharCode>([^<]+)</CharCode>", block)
        name = re.search(r"<Name>([^<]+)</Name>", block)
        val = re.search(r"<Value>([^<]+)</Value>", block)
        if code and val and code.group(1) in CODES:
            out[code.group(1)] = {
                "name": name.group(1) if name else code.group(1),
                "value": float(val.group(1).replace(",", ".")),
            }
    return out


def main():
    today = dt.date.today()
    yesterday = today - dt.timedelta(days=1)
    cur = parse(fetch())
    prev = parse(fetch(yesterday.strftime("%d/%m/%Y")))
    rates = []
    for c in CODES:
        if c not in cur:
            continue
        v = cur[c]["value"]
        p = prev.get(c, {}).get("value")
        chg = round(v - p, 2) if p is not None else 0.0
        rates.append({
            "code": c,
            "nameRu": cur[c]["name"],
            "nameEn": EN_NAMES[c],
            "value": f"{v:.2f}".replace(".", ","),
            "change": ("+" if chg >= 0 else "") + f"{chg:.2f}".replace(".", ","),
            "up": chg >= 0,
        })
    js = "// Курсы валют ЦБ РФ (автообновление ежедневно).\n"
    js += "window.CURRENCY = " + json.dumps({
        "updated": today.strftime("%d.%m.%Y"),
        "rates": rates,
    }, ensure_ascii=False) + ";\n"
    out = SITE / "currency-data.js"
    out.write_text(js, encoding="utf-8")
    print("OK updated=" + today.strftime("%d.%m.%Y"))
    for r in rates:
        print(f"  {r['code']}: {r['value']} ({r['change']})")


if __name__ == "__main__":
    main()
