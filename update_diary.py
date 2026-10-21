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


# Strength B — 21.10.2026. Idempotent.
if '"21.10"' not in s:
    old_stat = '<span class="stat-val">74</span><span class="stat-lbl">Тренировок</span>'
    old_dates = '"12.10","14.10","18.10"]'
    if old_stat not in s or old_dates not in s:
        raise RuntimeError("Unexpected diary version")

    s = s.replace(old_stat, '<span class="stat-val">75</span><span class="stat-lbl">Тренировок</span>', 1)
    s = s.replace(old_dates, '"12.10","14.10","18.10","21.10"]', 1)

    ni_start = s.find('const NEW_IDX = new Set([')
    ni_end = s.find(']);const EXERCISES', ni_start)
    if ni_start < 0 or ni_end < 0:
        raise RuntimeError("NEW_IDX not found")
    list_start = ni_start + len('const NEW_IDX = new Set([')
    current = s[list_start:ni_end]
    if not current.rstrip().endswith('73'):
        raise RuntimeError("Unexpected NEW_IDX tail")
    s = s[:list_start] + current + ', 74' + s[ni_end:]

    updates = [
        ("Жим гантелей\\n(30°)", 'null'),
        ("Жим гантелей\\nсидя (Плечи)", '{w:"22.5кг",r:[12,10,6]}'),
        ("Тяга верхнего\\nблока", 'null'),
        ("Тяга нижнего\\nблока (к поясу)", '{w:"72.7кг",r:[12,11,10]}'),
        ("Тяга гантели\\nк поясу", '{w:"22.5кг",r:[12,12,11]}'),
        ("Отжимания\\nна брусьях", 'null'),
        ("Махи гантелями\\nв стороны", 'null'),
        ("Подъём гантелей\\nна бицепс", 'null'),
        ("Подъём ног\\nв висе", 'null'),
        ("Молитва", 'null'),
        ("Жим гантелей\\nгоризонтальный", 'null'),
        ("Обратная\\nбабочка", '{w:"54кг",r:[12,12,12]}'),
        ("Выпады вперёд\\nс гантелями", '{w:"25кг",r:[12,12]}'),
        ("Подъём на носок\\n1 ногой", 'null'),
        ("Разгибание рук\\nс канатом", '{w:"59.1кг",r:[12,12,10]}'),
        ("Молотковые\\nсгибания", 'null'),
        ("Скручивания\\nна наклонной", '{w:"10кг",r:[15,12]}'),
        ("Тяга прямыми\\nруками", 'null'),
        ("Разведение рук\\nв стороны (тренажёр)", 'null'),
        ("Подъём на носки\\nв тренажёре", '{w:"30→35→35кг",r:[19,16,16]}')
    ]
    for name, entry in updates:
        s = append_cell(s, name, entry)

    note = ("🔥 21.10.2026 — Силовая Б. Сильная прогрессия сразу в нескольких движениях. "
            "Жим сидя 22.5 кг 12/10/6 — первые два подхода заметно лучше 14.10 (11/7), но третий резко просел; вес пока не повышать и не доводить каждый подход до отказа. "
            "Нижний блок 72.7 кг 12/11/10 — 33 повтора, лучший недавний результат на этом весе. "
            "Тяга гантели к поясу повышена с 20 до 22.5 кг и выполнена 12/12/11 — очень сильный переход; из-за истории левого локтя не повышать дальше и контролировать знакомое тянущее/стреляющее ощущение. "
            "Обратная бабочка 54 кг 12/12/12 — четвёртая подряд тренировка 3×12; к следующей ступени готова, но не совмещать её повышение с другими прогрессиями. "
            "Выпады повышены с 20 до 25 кг и выполнены 12/12 на каждую ногу — большой шаг по нагрузке; следующий раз вес удержать, особенно с учётом бега 19.10. "
            "Икры в тренажёре: 30 кг ×19, затем 35 кг ×16/16 — 35 кг уже рабочий вес; сохранять его и улучшать контроль/амплитуду. "
            "Канат 59.1 кг 12/12/10 — на один повтор меньше 14.10, что несущественно на фоне общего роста нагрузки. "
            "Скручивания 10 кг 15/12 — возвращены после пропуска. Общий вывод: силовая форма растёт, но сегодня одновременно выросли тяга гантели, выпады и икры; следующую Б не превращать в ещё одну волну повышений.")

    c_start = s.find('const COMMENTS = {')
    c_end = s.find('};function findPRs', c_start)
    if c_start < 0 or c_end < 0:
        raise RuntimeError("COMMENTS not found")
    body_start = c_start + len('const COMMENTS = {')
    body = s[body_start:c_end]
    if '74: "' not in body:
        note_escaped = note.replace("\\", "\\\\").replace('"', '\\"')
        body = body.rstrip() + (',' if body.strip() else '') + f'74: "{note_escaped}"'
        s = s[:body_start] + body + s[c_end:]

if ('src="run.html"' not in s or '"21.10"' not in s or '74: "' not in s):
    raise RuntimeError("Post-update validation failed")

p.write_text(s, encoding="utf-8")
