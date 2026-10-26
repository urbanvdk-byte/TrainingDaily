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


# Strength B — 26.10.2026. Idempotent.
if '"26.10"' not in s:
    old_stat = '<span class="stat-val">76</span><span class="stat-lbl">Тренировок</span>'
    old_dates = '"18.10","21.10","23.10"]'
    if old_stat not in s or old_dates not in s:
        raise RuntimeError("Unexpected diary version")

    s = s.replace(old_stat, '<span class="stat-val">77</span><span class="stat-lbl">Тренировок</span>', 1)
    s = s.replace(old_dates, '"18.10","21.10","23.10","26.10"]', 1)

    ni_start = s.find('const NEW_IDX = new Set([')
    ni_end = s.find(']);const EXERCISES', ni_start)
    if ni_start < 0 or ni_end < 0:
        raise RuntimeError("NEW_IDX not found")
    list_start = ni_start + len('const NEW_IDX = new Set([')
    current = s[list_start:ni_end]
    if not current.rstrip().endswith('75'):
        raise RuntimeError("Unexpected NEW_IDX tail")
    s = s[:list_start] + current + ', 76' + s[ni_end:]

    updates = [
        ("Жим гантелей\\n(30°)", 'null'),
        ("Жим гантелей\\nсидя (Плечи)", '{w:"22.5→22.5→20кг",r:[12,10,11]}'),
        ("Тяга верхнего\\nблока", 'null'),
        ("Тяга нижнего\\nблока (к поясу)", '{w:"72.7кг",r:[12,12,12]}'),
        ("Тяга гантели\\nк поясу", '{w:"22.5кг",r:[12,12,12]}'),
        ("Отжимания\\nна брусьях", 'null'),
        ("Махи гантелями\\nв стороны", 'null'),
        ("Подъём гантелей\\nна бицепс", 'null'),
        ("Подъём ног\\nв висе", 'null'),
        ("Молитва", 'null'),
        ("Жим гантелей\\nгоризонтальный", 'null'),
        ("Обратная\\nбабочка", '{w:"58.5кг",r:[12,12,10]}'),
        ("Выпады вперёд\\nс гантелями", '{w:"25кг",r:[12,12]}'),
        ("Подъём на носок\\n1 ногой", 'null'),
        ("Разгибание рук\\nс канатом", '{w:"59.1кг",r:[12,12,11]}'),
        ("Молотковые\\nсгибания", 'null'),
        ("Скручивания\\nна наклонной", '{w:"10кг",r:[16,14]}'),
        ("Тяга прямыми\\nруками", 'null'),
        ("Разведение рук\\nв стороны (тренажёр)", 'null'),
        ("Подъём на носки\\nв тренажёре", '{w:"40кг",r:[16,16,15]}')
    ]
    for name, entry in updates:
        s = append_cell(s, name, entry)

    note = ("🔥 26.10.2026 — Силовая Б. Сильная тренировка с несколькими подтверждёнными прогрессиями. "
            "Жим сидя: 22.5 кг 12/10, затем 20 кг ×11 — первые два тяжёлых подхода полностью повторили 21.10, а своевременный сброс веса в третьем подходе лучше контролирует качество, чем попытка дожимать 22.5 кг до 6 повторов. "
            "Нижний блок 72.7 кг 12/12/12 — впервые полностью закрыта верхняя граница на этом весе; следующую Б можно рассматривать одну ступень вверх, если техника остаётся чистой. "
            "Тяга гантели 22.5 кг 12/12/12 — вес также полностью закрыт, но упражнение спортсмену не нравится; считать это финальным подтверждением текущего уровня и со следующей Б заменить на другое тяговое движение, не дублирующее нижний блок. "
            "Обратная бабочка повышена до 58.5 кг и сразу выполнена 12/12/10 — хорошая прогрессия; вес оставить до 3×12. "
            "Выпады 25 кг 12/12 на каждую ногу — второй раз подряд подтверждены; дальше пока не повышать из-за беговой нагрузки. "
            "Икры 40 кг 16/16/15 — существенный рост относительно 21.10; 40 кг уже более чем достаточный рабочий вес, следующий раз не повышать и контролировать полную амплитуду и медленное опускание. "
            "Канат 59.1 кг 12/12/11 — вернулся к лучшему недавнему уровню, один повтор до 3×12. "
            "Скручивания 10 кг 16/14 — лучший результат последних недель. "
            "Общий вывод: спина, икры и корпус явно прибавили; следующую Б сделать закрепляющей, а не повышать одновременно нижний блок, бабочку и икры.")

    c_start = s.find('const COMMENTS = {')
    c_end = s.find('};function findPRs', c_start)
    if c_start < 0 or c_end < 0:
        raise RuntimeError("COMMENTS not found")
    body_start = c_start + len('const COMMENTS = {')
    body = s[body_start:c_end]
    if '76: "' not in body:
        note_escaped = note.replace("\\", "\\\\").replace('"', '\\"')
        body = body.rstrip() + (',' if body.strip() else '') + f'76: "{note_escaped}"'
        s = s[:body_start] + body + s[c_end:]

if ('src="run.html"' not in s or '"26.10"' not in s or '76: "' not in s):
    raise RuntimeError("Post-update validation failed")

p.write_text(s, encoding="utf-8")
