from pathlib import Path

p = Path("index.html")
s = p.read_text(encoding="utf-8")


def append_cell(text, name, entry):
    marker = f'name: "{name}",cells: ['
    pos = text.find(marker)
    if pos < 0:
        raise RuntimeError(f"Exercise not found: {name}")
    arr_start = pos + len(marker) - 1
    depth = 0
    quoted = False
    escaped = False
    for i in range(arr_start, len(text)):
        ch = text[i]
        if quoted:
            if escaped:
                escaped = False
            elif ch == "\\":
                escaped = True
            elif ch == '"':
                quoted = False
            continue
        if ch == '"':
            quoted = True
        elif ch == '[':
            depth += 1
        elif ch == ']':
            depth -= 1
            if depth == 0:
                return text[:i] + ',' + entry + text[i:]
    raise RuntimeError(f"Exercise array end not found: {name}")


# Strength A — 23.10.2026. Idempotent.
if '"23.10"' not in s:
    old_stat = '<span class="stat-val">75</span><span class="stat-lbl">Тренировок</span>'
    old_dates = '"14.10","18.10","21.10"]'
    if old_stat not in s or old_dates not in s:
        raise RuntimeError("Unexpected diary version")

    s = s.replace(old_stat, '<span class="stat-val">76</span><span class="stat-lbl">Тренировок</span>', 1)
    s = s.replace(old_dates, '"14.10","18.10","21.10","23.10"]', 1)

    ni_start = s.find('const NEW_IDX = new Set([')
    ni_end = s.find(']);const EXERCISES', ni_start)
    if ni_start < 0 or ni_end < 0:
        raise RuntimeError("NEW_IDX not found")
    list_start = ni_start + len('const NEW_IDX = new Set([')
    current = s[list_start:ni_end]
    if not current.rstrip().endswith('74'):
        raise RuntimeError("Unexpected NEW_IDX tail")
    s = s[:list_start] + current + ', 75' + s[ni_end:]

    updates = [
        ("Жим гантелей\\n(30°)", '{w:"30кг",r:[12,12,17]}'),
        ("Жим гантелей\\nсидя (Плечи)", 'null'),
        ("Тяга верхнего\\nблока", '{w:"68.2кг",r:[12,9,9]}'),
        ("Тяга нижнего\\nблока (к поясу)", 'null'),
        ("Тяга гантели\\nк поясу", 'null'),
        ("Отжимания\\nна брусьях", '{bw:true,r:[28,20]}'),
        ("Махи гантелями\\nв стороны", 'null'),
        ("Подъём гантелей\\nна бицепс", 'null'),
        ("Подъём ног\\nв висе", 'null'),
        ("Молитва", '{w:"86.5кг",r:[15,12,11]}'),
        ("Жим гантелей\\nгоризонтальный", '{w:"32.5кг",r:[12,11,9]}'),
        ("Обратная\\nбабочка", 'null'),
        ("Выпады вперёд\\nс гантелями", 'null'),
        ("Подъём на носок\\n1 ногой", 'null'),
        ("Разгибание рук\\nс канатом", 'null'),
        ("Молотковые\\nсгибания", 'null'),
        ("Скручивания\\nна наклонной", 'null'),
        ("Тяга прямыми\\nруками", '{w:"59.1кг",r:[12,12,12]}'),
        ("Разведение рук\\nв стороны (тренажёр)", '{w:"11.4кг",r:[12,12,11]}'),
        ("Подъём на носки\\nв тренажёре", 'null')
    ]
    for name, entry in updates:
        s = append_cell(s, name, entry)

    note = ("🔥 23.10.2026 — Силовая А. Очень сильная тренировка. "
            "Наклонный жим 30 кг 12/12/17: первые два подхода были лёгкими, третий сознательно выполнен до отказа; 30 кг явно перерос и на следующей А можно переходить на 32.5 кг, но отказ не использовать регулярно. "
            "Горизонтальный жим возвращён на 32.5 кг и сразу выполнен 12/11/9 — значительно сильнее последних попыток на этом весе; вес закреплять, не повышать. "
            "Верхний блок 68.2 кг 12/9/9 — рабочий уровень сохранён, суммарно 30 повторов; следующий ориентир 12/10/9+. "
            "Разведение в тренажёре повышено с 9.1 до 11.4 кг и выполнено 12/12/11 — успешная прогрессия, до 3×12 оставить тот же вес. "
            "Брусья 28/20 — повторён лучший первый подход, пока без дополнительного веса. "
            "Тяга прямыми руками 59.1 кг 12/12/12 — верхняя граница закрыта второй раз подряд; из-за нескольких других прогрессий повышение отложить. "
            "Молитва 86.5 кг 15/12/11 — третий подход вырос с 10 до 11 относительно 12.10, вес закрепляется. "
            "Общий вывод: сила верха заметно выросла, особенно в жимах; следующую А строить вокруг перехода наклонного жима на 32.5 кг, остальные упражнения в основном закреплять.")

    c_start = s.find('const COMMENTS = {')
    c_end = s.find('};function findPRs', c_start)
    if c_start < 0 or c_end < 0:
        raise RuntimeError("COMMENTS not found")
    body_start = c_start + len('const COMMENTS = {')
    body = s[body_start:c_end]
    if '75: "' not in body:
        note_escaped = note.replace("\\", "\\\\").replace('"', '\\"')
        body = body.rstrip() + (',' if body.strip() else '') + f'75: "{note_escaped}"'
        s = s[:body_start] + body + s[c_end:]

if ('src="run.html"' not in s or '"23.10"' not in s or '75: "' not in s):
    raise RuntimeError("Post-update validation failed")

p.write_text(s, encoding="utf-8")
