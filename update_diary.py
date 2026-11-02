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


# Strength A — 29.10.2026. Idempotent.
if '"29.10"' not in s:
    old_stat = '<span class="stat-val">77</span><span class="stat-lbl">Тренировок</span>'
    old_dates = '"21.10","23.10","26.10"]'
    if old_stat not in s or old_dates not in s:
        raise RuntimeError("Unexpected diary version")

    s = s.replace(old_stat, '<span class="stat-val">78</span><span class="stat-lbl">Тренировок</span>', 1)
    s = s.replace(old_dates, '"21.10","23.10","26.10","29.10"]', 1)

    ni_start = s.find('const NEW_IDX = new Set([')
    ni_end = s.find(']);const EXERCISES', ni_start)
    if ni_start < 0 or ni_end < 0:
        raise RuntimeError("NEW_IDX not found")
    list_start = ni_start + len('const NEW_IDX = new Set([')
    current = s[list_start:ni_end]
    if not current.rstrip().endswith('76'):
        raise RuntimeError("Unexpected NEW_IDX tail")
    s = s[:list_start] + current + ', 77' + s[ni_end:]

    updates = [
        ("Жим гантелей\\n(30°)", '{w:"30кг",r:[12,10,10]}'),
        ("Жим гантелей\\nсидя (Плечи)", '{w:"20→22.5→22.5кг",r:[12,12,10]}'),
        ("Тяга верхнего\\nблока", '{w:"68.2кг",r:[12,11,9]}'),
        ("Тяга нижнего\\nблока (к поясу)", 'null'),
        ("Тяга гантели\\nк поясу", 'null'),
        ("Отжимания\\nна брусьях", '{bw:true,r:[25,15]}'),
        ("Махи гантелями\\nв стороны", 'null'),
        ("Подъём гантелей\\nна бицепс", 'null'),
        ("Подъём ног\\nв висе", 'null'),
        ("Молитва", '{w:"86.5кг",r:[15,12,12]}'),
        ("Жим гантелей\\nгоризонтальный", '{w:"32.5→30→30кг",r:[9,10,8]}'),
        ("Обратная\\nбабочка", 'null'),
        ("Выпады вперёд\\nс гантелями", 'null'),
        ("Подъём на носок\\n1 ногой", 'null'),
        ("Разгибание рук\\nс канатом", 'null'),
        ("Молотковые\\nсгибания", 'null'),
        ("Скручивания\\nна наклонной", 'null'),
        ("Тяга прямыми\\nруками", '{w:"59.1кг",r:[12,12,12]}'),
        ("Разведение рук\\nв стороны (тренажёр)", 'null'),
        ("Подъём на носки\\nв тренажёре", 'null')
    ]
    for name, entry in updates:
        s = append_cell(s, name, entry)

    note = ("⚠️ 29.10.2026 — Силовая А с нарушенным порядком упражнений. "
            "По ошибке первым выполнен жим гантелей сидя: 20 кг ×12, затем 22.5 кг ×12/10. Это фактически предварительно утомило переднюю дельту и трицепс перед обоими жимами груди, поэтому результаты жимов и брусьев нельзя напрямую сравнивать с обычной А. "
            "Наклонный жим 30 кг 12/10/10 после плеч — закономерно ниже 23.10 (12/12/17); это не основание отменять плановый переход к 32.5 кг на следующей нормально собранной А. "
            "Горизонтальный жим: 32.5 кг ×9, затем 30 кг ×10/8 — просадка ожидаема после жима плеч и наклонного жима; оценивать силу груди по этой тренировке нельзя. "
            "Верхний блок 68.2 кг 12/11/9 — улучшение относительно 23.10 (12/9/9), суммарно 32 повтора; хороший объективный прогресс, так как упражнение не зависит от ошибки в порядке жимов. "
            "Разведение в стороны пропущено осознанно после лишнего жима плеч; нулевые подходы не считать выполненными. "
            "Брусья 25/15 ниже 28/20, что логично после большого предварительного жимового объёма; веса не добавлять. "
            "Тяга прямыми руками 59.1 кг 12/12/12 — третье подряд полное закрытие; упражнение готово к одной ступени вверх, но повышение лучше отложить до тренировки без лишних изменений. "
            "Молитва 86.5 кг 15/12/12 — третий подход вырос с 11 до 12, верхняя граница практически закрыта; можно готовить следующую ступень. "
            "Общий вывод: тренировка дала полезный объём, но из-за ошибочного порядка жимов не является контрольной для груди. Следующую А вернуть к стандартной последовательности и не компенсировать сегодняшнюю просадку дополнительным объёмом.")

    c_start = s.find('const COMMENTS = {')
    c_end = s.find('};function findPRs', c_start)
    if c_start < 0 or c_end < 0:
        raise RuntimeError("COMMENTS not found")
    body_start = c_start + len('const COMMENTS = {')
    body = s[body_start:c_end]
    if '77: "' not in body:
        note_escaped = note.replace("\\", "\\\\").replace('"', '\\"')
        body = body.rstrip() + (',' if body.strip() else '') + f'77: "{note_escaped}"'
        s = s[:body_start] + body + s[c_end:]

if ('src="run.html"' not in s or '"29.10"' not in s or '77: "' not in s):
    raise RuntimeError("Post-update validation failed")

p.write_text(s, encoding="utf-8")
