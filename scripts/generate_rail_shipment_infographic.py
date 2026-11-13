#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Генерирует деловую блок-схему «Как организовать отправку груза по железной дороге»
в виде SVG (RU и EN). Строгий стиль без эмодзи и иллюстраций, цвета сайта.
"""
import sys

ACCENT = "#0a5c8a"
ACCENT_DARK = "#084a6e"
WHITE = "#ffffff"
TEXT = "#1a2332"
MUTED = "#5c6672"
BORDER = "#d8e0e8"
GRAY_FILL = "#eef2f6"
GRAY_BORDER = "#cbd5e0"

W = 1040
H = 1060

# --- Данные ---
DATA = {
    "ru": {
        "header_title": "КАК ОРГАНИЗОВАТЬ ОТПРАВКУ ГРУЗА ПО ЖЕЛЕЗНОЙ ДОРОГЕ",
        "header_sub": "в пределах РФ · универсальный вагон (полувагон, платформа, крытый вагон)",
        "decision": ["Вы владелец", "подъездного пути?"],
        "no": "НЕТ",
        "yes": "ДА",
        "variant1_title": "ВАРИАНТ 1 · УСЛУГА «ПОД КЛЮЧ»",
        "variant1_lines": ["Договор с организацией, имеющей:", "подъездной путь · грузоподъёмные механизмы ·", "аттестованный персонал · ЕЛС"],
        "variant2_title": "ВАРИАНТ 2 · ПОШАГОВЫЙ ПОРЯДОК",
        "variant2_sub": "11 шагов для владельца подъездного пути",
        "steps": [
            ("Договор на подачу-уборку вагонов", "заключить с РЖД на обслуживание пути"),
            ("Инспекция инфраструктуры", "ПЧ · ШЧ · соответствие ПТЭ"),
            ("Единый лицевой счёт (ЕЛС)", "взаиморасчёты с РЖД за услуги"),
            ("Погрузка и крепление по ТУ", "Технические условия · ЦМ-943"),
            ("Аттестация работников", "проверка знаний ТУ · товарная контора"),
            ("Запись на обороте накладной", "графа 1 · средства крепления · печать"),
            ("Заявка на перевозку (ГУ-12)", "приказ Минтранса № 228 · за 10/15 дней"),
            ("Подача вагонов под погрузку", "планирование со станцией"),
            ("Проверка погрузки", "приёмосдатчик · ТУ / МТУ / НТУ"),
            ("Оформление накладной", "доверенность · товарная контора"),
        ],
        "final_title": "Договор перевозки заключён",
        "final_sub": "ЭТРАН · оплата · ведомость ГУ-46",
        "footer": "Ключевые точки контроля: аттестация персонала · запись о креплении · заявка ГУ-12 · накладная в ЭТРАН",
    },
    "en": {
        "header_title": "HOW TO ORGANISE A RAIL SHIPMENT",
        "header_sub": "within Russia · universal wagon (gondola, flat wagon, covered wagon)",
        "decision": ["Are you the owner", "of the siding?"],
        "no": "NO",
        "yes": "YES",
        "variant1_title": "OPTION 1 · TURNKEY SERVICE",
        "variant1_lines": ["Contract with an organisation that has:", "siding · lifting equipment ·", "certified personnel · ELS"],
        "variant2_title": "OPTION 2 · STEP-BY-STEP PROCEDURE",
        "variant2_sub": "11 steps for the siding owner",
        "steps": [
            ("Wagon supply/removal agreement", "conclude with RZD to service the siding"),
            ("Infrastructure inspection", "PCh · ShCh · compliance with PTE"),
            ("Single settlement account (ELS)", "settlements with RZD for services"),
            ("Loading and securing under the TU", "Technical Conditions · TsM-943"),
            ("Personnel certification", "TU knowledge test · goods office"),
            ("Endorsement on the note reverse", "column 1 · securing devices · seal"),
            ("Carriage application (GU-12)", "Order No. 228 · 10/15 days ahead"),
            ("Wagon supply for loading", "planning with the station"),
            ("Loading check", "cargo acceptance clerk · TU / MTU / NTU"),
            ("Consignment note issue", "power of attorney · goods office"),
        ],
        "final_title": "Contract of carriage concluded",
        "final_sub": "ETRAN · payment · GU-46 record",
        "footer": "Key control points: personnel certification · securing endorsement · GU-12 request · ETRAN consignment note",
    },
}

# --- Геометрия ---
HEADER_H = 92
DIAMOND_CX, DIAMOND_CY, DIAMOND_HW, DIAMOND_HH = 520, 150, 150, 38
PILL_W, PILL_H = 72, 30
OUTCOME_Y, OUTCOME_H = 208, 100
STEPS_Y = 348
BOX_W, BOX_H, ROW_PITCH = 420, 92, 116
COL0, COL1 = 60, 560
CONCL_Y, CONCL_H = 928, 92
FOOTER_Y = 1040

# Серпантин: 10 шагов на 5 рядах (2 колонки), 11-й — финальная широкая полоса
def serpentine_pos(i):
    # i: 0..9
    row = i // 2
    col = i % 2
    # нечётные ряды идут справа налево
    if row % 2 == 1:
        col = 1 - col
    x = COL1 if col == 1 else COL0
    y = STEPS_Y + row * ROW_PITCH
    return x, y

def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

def build(lang):
    d = DATA[lang]
    p = []
    p.append('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" font-family="-apple-system, \'Segoe UI\', Roboto, \'Helvetica Neue\', Arial, sans-serif">' % (W, H))
    p.append('<defs>')
    p.append('<marker id="arr" markerWidth="11" markerHeight="11" refX="8" refY="5" orient="auto" markerUnits="userSpaceOnUse"><path d="M0,0 L11,5 L0,10 z" fill="%s"/></marker>' % ACCENT)
    p.append('</defs>')
    p.append('<rect width="%d" height="%d" fill="%s"/>' % (W, H, WHITE))

    # Шапка
    p.append('<rect x="0" y="0" width="%d" height="%d" fill="%s"/>' % (W, HEADER_H, ACCENT))
    p.append('<text x="%d" y="42" text-anchor="middle" font-size="26" font-weight="bold" fill="%s">%s</text>' % (W // 2, WHITE, esc(d["header_title"])))
    p.append('<text x="%d" y="72" text-anchor="middle" font-size="15" fill="%s" opacity="0.88">%s</text>' % (W // 2, WHITE, esc(d["header_sub"])))

    # Ромб решения
    pt = "%d,%d %d,%d %d,%d %d,%d" % (
        DIAMOND_CX, DIAMOND_CY - DIAMOND_HH,
        DIAMOND_CX + DIAMOND_HW, DIAMOND_CY,
        DIAMOND_CX, DIAMOND_CY + DIAMOND_HH,
        DIAMOND_CX - DIAMOND_HW, DIAMOND_CY,
    )
    p.append('<polygon points="%s" fill="%s" stroke="%s" stroke-width="2"/>' % (pt, WHITE, ACCENT))
    p.append('<text x="%d" y="%d" text-anchor="middle" font-size="15" font-weight="bold" fill="%s">%s</text>' % (DIAMOND_CX, DIAMOND_CY - 3, TEXT, esc(d["decision"][0])))
    p.append('<text x="%d" y="%d" text-anchor="middle" font-size="15" font-weight="bold" fill="%s">%s</text>' % (DIAMOND_CX, DIAMOND_CY + 17, TEXT, esc(d["decision"][1])))

    # Пилюли НЕТ / ДА
    no_cx, yes_cx = 255, 785
    p.append('<rect x="%d" y="%d" width="%d" height="%d" rx="15" fill="%s" stroke="%s" stroke-width="1.5"/>' % (no_cx - PILL_W // 2, DIAMOND_CY - PILL_H // 2, PILL_W, PILL_H, GRAY_FILL, GRAY_BORDER))
    p.append('<text x="%d" y="%d" text-anchor="middle" font-size="14" font-weight="bold" fill="%s">%s</text>' % (no_cx, DIAMOND_CY + 5, TEXT, esc(d["no"])))
    p.append('<rect x="%d" y="%d" width="%d" height="%d" rx="15" fill="%s" stroke="%s" stroke-width="1.5"/>' % (yes_cx - PILL_W // 2, DIAMOND_CY - PILL_H // 2, PILL_W, PILL_H, ACCENT, ACCENT))
    p.append('<text x="%d" y="%d" text-anchor="middle" font-size="14" font-weight="bold" fill="%s">%s</text>' % (yes_cx, DIAMOND_CY + 5, WHITE, esc(d["yes"])))

    # Стрелки: ромб -> пилюли, пилюли -> блоки
    p.append('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="%s" stroke-width="2" marker-end="url(#arr)"/>' % (DIAMOND_CX - DIAMOND_HW, DIAMOND_CY, no_cx + PILL_W // 2 + 6, DIAMOND_CY, ACCENT))
    p.append('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="%s" stroke-width="2" marker-end="url(#arr)"/>' % (DIAMOND_CX + DIAMOND_HW, DIAMOND_CY, yes_cx - PILL_W // 2 - 6, DIAMOND_CY, ACCENT))
    p.append('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="%s" stroke-width="2" marker-end="url(#arr)"/>' % (no_cx, DIAMOND_CY + PILL_H // 2, no_cx, OUTCOME_Y - 6, ACCENT))
    p.append('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="%s" stroke-width="2" marker-end="url(#arr)"/>' % (yes_cx, DIAMOND_CY + PILL_H // 2, yes_cx, OUTCOME_Y - 6, ACCENT))

    # Блок Вариант 1 (серый)
    v1_x, v1_w = 40, 430
    p.append('<rect x="%d" y="%d" width="%d" height="%d" rx="10" fill="%s" stroke="%s" stroke-width="1.5"/>' % (v1_x, OUTCOME_Y, v1_w, OUTCOME_H, GRAY_FILL, GRAY_BORDER))
    p.append('<text x="%d" y="%d" text-anchor="middle" font-size="15" font-weight="bold" fill="%s">%s</text>' % (v1_x + v1_w // 2, OUTCOME_Y + 28, ACCENT, esc(d["variant1_title"])))
    for i, line in enumerate(d["variant1_lines"]):
        p.append('<text x="%d" y="%d" text-anchor="middle" font-size="12.5" fill="%s">%s</text>' % (v1_x + v1_w // 2, OUTCOME_Y + 52 + i * 18, MUTED, esc(line)))

    # Баннер Вариант 2 (акцентный)
    v2_x, v2_w = 560, 440
    p.append('<rect x="%d" y="%d" width="%d" height="%d" rx="10" fill="%s"/>' % (v2_x, OUTCOME_Y, v2_w, OUTCOME_H, ACCENT))
    p.append('<text x="%d" y="%d" text-anchor="middle" font-size="17" font-weight="bold" fill="%s">%s</text>' % (v2_x + v2_w // 2, OUTCOME_Y + 38, WHITE, esc(d["variant2_title"])))
    p.append('<text x="%d" y="%d" text-anchor="middle" font-size="13" fill="%s" opacity="0.9">%s</text>' % (v2_x + v2_w // 2, OUTCOME_Y + 64, WHITE, esc(d["variant2_sub"])))
    p.append('<path d="M %d %d L %d %d L %d %d" fill="none" stroke="%s" stroke-width="2"/>' % (v2_x + v2_w // 2 - 8, OUTCOME_Y + 82, v2_x + v2_w // 2, OUTCOME_Y + 92, v2_x + v2_w // 2 + 8, OUTCOME_Y + 82, WHITE))

    # Шаги 1-10 (серпантин)
    steps = d["steps"]
    for i, (title, sub) in enumerate(steps):
        x, y = serpentine_pos(i)
        num = i + 1
        p.append('<rect x="%d" y="%d" width="%d" height="%d" rx="10" fill="%s" stroke="%s" stroke-width="1.5"/>' % (x, y, BOX_W, BOX_H, WHITE, BORDER))
        p.append('<rect x="%d" y="%d" width="5" height="%d" rx="2" fill="%s"/>' % (x, y + 14, BOX_H - 28, ACCENT))
        p.append('<circle cx="%d" cy="%d" r="16" fill="%s"/>' % (x + 40, y + BOX_H // 2, ACCENT))
        p.append('<text x="%d" y="%d" text-anchor="middle" font-size="14" font-weight="bold" fill="%s">%d</text>' % (x + 40, y + BOX_H // 2 + 5, WHITE, num))
        p.append('<text x="%d" y="%d" font-size="15" font-weight="bold" fill="%s">%s</text>' % (x + 68, y + 40, TEXT, esc(title)))
        p.append('<text x="%d" y="%d" font-size="12" fill="%s">%s</text>' % (x + 68, y + 64, MUTED, esc(sub)))

    # Стрелки между шагами
    def h_arrow(x1, x2, y):
        p.append('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="%s" stroke-width="2" marker-end="url(#arr)"/>' % (x1, y, x2, y, ACCENT))
    def v_arrow(x, y1, y2):
        p.append('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="%s" stroke-width="2" marker-end="url(#arr)"/>' % (x, y1, x, y2, ACCENT))
    COL0_R, COL1_L = COL0 + BOX_W, COL1
    for i in range(9):
        x, y = serpentine_pos(i)
        nx, ny = serpentine_pos(i + 1)
        cy = y + BOX_H // 2
        if y == ny:  # горизонтальная стрелка в том же ряду
            if nx > x:
                h_arrow(x + BOX_W + 2, nx - 6, cy)
            else:
                h_arrow(x - 6, nx + BOX_W + 2, cy)
        else:  # вертикальная стрелка в следующем ряду (та же колонка)
            v_arrow(x + BOX_W // 2, y + BOX_H + 2, ny - 6)

    # Финальный блок 11 (широкая акцентная полоса)
    fx, fw = 60, 920
    p.append('<rect x="%d" y="%d" width="%d" height="%d" rx="10" fill="%s"/>' % (fx, CONCL_Y, fw, CONCL_H, ACCENT))
    p.append('<circle cx="%d" cy="%d" r="16" fill="%s"/>' % (fx + 40, CONCL_Y + CONCL_H // 2, WHITE))
    p.append('<text x="%d" y="%d" text-anchor="middle" font-size="14" font-weight="bold" fill="%s">11</text>' % (fx + 40, CONCL_Y + CONCL_H // 2 + 5, ACCENT))
    p.append('<text x="%d" y="%d" font-size="16" font-weight="bold" fill="%s">%s</text>' % (fx + 68, CONCL_Y + 40, WHITE, esc(d["final_title"])))
    p.append('<text x="%d" y="%d" font-size="12.5" fill="%s" opacity="0.9">%s</text>' % (fx + 68, CONCL_Y + 64, WHITE, esc(d["final_sub"])))
    # стрелка от шага 10 (нижний правый) вниз
    lx, ly = serpentine_pos(9)
    v_arrow(lx + BOX_W // 2, ly + BOX_H + 2, CONCL_Y - 6)

    # Подпись-футер
    p.append('<text x="%d" y="%d" text-anchor="middle" font-size="12" fill="%s">%s</text>' % (W // 2, FOOTER_Y, MUTED, esc(d["footer"])))

    p.append('</svg>')
    return "\n".join(p)

def main():
    out = {
        "ru": "rail-shipment-flow.svg",
        "en": "en/rail-shipment-flow.svg",
    }
    for lang, path in out.items():
        svg = build(lang)
        with open(path, "w", encoding="utf-8") as f:
            f.write(svg)
        print("записано %s (%d байт)" % (path, len(svg.encode("utf-8"))))

if __name__ == "__main__":
    main()
