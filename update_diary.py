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


if '"18.10"' not in s:
    old_stat = '<span class="stat-val">73</span><span class="stat-lbl">Тренировок</span>'
    old_dates = '"09.10","12.10","14.10"]'
    if old_stat not in s or old_dates not in s:
        raise RuntimeError("Unexpected diary version")

    s = s.replace(old_stat, '<span class="stat-val">74</span><span class="stat-lbl">Тренировок</span>', 1)
    s = s.replace(old_dates, '"09.10","12.10","14.10","18.10"]', 1)

    ni_start = s.find('const NEW_IDX = new Set([')
    ni_end = s.find(']);const EXERCISES', ni_start)
    if ni_start < 0 or ni_end < 0:
        raise RuntimeError("NEW_IDX not found")
    list_start = ni_start + len('const NEW_IDX = new Set([')
    current = s[list_start:ni_end]
    if not current.rstrip().endswith('72'):
        raise RuntimeError("Unexpected NEW_IDX tail")
    s = s[:list_start] + current + ', 73' + s[ni_end:]

    updates = [
        ("Жим гантелей\\n(30°)", '{w:"30кг",r:[12,12,11]}'),
        ("Жим гантелей\\nсидя (Плечи)", 'null'),
        ("Тяга верхнего\\nблока", '{w:"65кг",r:[12,9,8]}'),
        ("Тяга нижнего\\nблока (к поясу)", 'null'),
        ("Тяга гантели\\nк поясу", 'null'),
        ("Отжимания\\nна брусьях", '{bw:true,r:[28,20]}'),
        ("Махи гантелями\\nв стороны", 'null'),
        ("Подъём гантелей\\nна бицепс", 'null'),
        ("Подъём ног\\nв висе", 'null'),
        ("Молитва", 'null'),
        ("Жим гантелей\\nгоризонтальный", '{w:"30кг",r:[12,12,10]}'),
        ("Обратная\\nбабочка", 'null'),
        ("Выпады вперёд\\nс гантелями", 'null'),
        ("Подъём на носок\\n1 ногой", 'null'),
        ("Разгибание рук\\nс канатом", 'null'),
        ("Молотковые\\nсгибания", 'null'),
        ("Скручивания\\nна наклонной", 'null'),
        ("Тяга прямыми\\nруками", '{w:"59.1кг",r:[12,12,12]}'),
        ("Разведение рук\\nв стороны (тренажёр)", '{w:"9.1кг",r:[12,12,12]}'),
        ("Подъём на носки\\nв тренажёре", 'null')
    ]
    for name, entry in updates:
        s = append_cell(s, name, entry)

    note = ("🔥 18.10.2026 — Силовая А в другом зале. "
            "Наклонный жим 30 кг 12/12/11 и горизонтальный 30 кг 12/12/10 — полностью удержан сильный уровень 12.10, несмотря на большую походную нагрузку 15.10. "
            "Тяга верхнего блока выполнена на 65 кг 12/9/8, потому что в этом зале 65 кг был ближайшим доступным весом к обычным 68.2 кг; прямое сравнение между тренажёрами ограничено. "
            "Разведение рук в стороны в тренажёре 9.1 кг 12/12/12 — верхняя граница снова закрыта, но из-за другого зала сопротивление тренажёра не считать строго эквивалентным привычному. "
            "Брусья 28/20 — новый лучший первый подход текущего периода. "
            "Тяга прямыми руками 59.1 кг 12/12/12 — впервые полностью закрыта верхняя граница на этом весе; из-за другого зала сначала подтвердить результат на привычном тренажёре, затем решать о повышении. "
            "Молитва пропущена только из-за нехватки времени, а не из-за усталости; нулевые подходы не считаются выполненными. "
            "Общий вывод: свободные веса и брусья показывают хорошее восстановление и стабильную силовую форму. Следующая А — не повышать сразу несколько нагрузок; приоритет закрыть жимы 30 кг 3×12 и сохранить локоть спокойным.")

    c_start = s.find('const COMMENTS = {')
    c_end = s.find('};function findPRs', c_start)
    if c_start < 0 or c_end < 0:
        raise RuntimeError("COMMENTS not found")
    body_start = c_start + len('const COMMENTS = {')
    body = s[body_start:c_end]
    if '73: "' not in body:
        note_escaped = note.replace("\\", "\\\\").replace('"', '\\"')
        body = body.rstrip() + (',' if body.strip() else '') + f'73: "{note_escaped}"'
        s = s[:body_start] + body + s[c_end:]

if ('src="run.html"' not in s or '"18.10"' not in s or '73: "' not in s):
    raise RuntimeError("Post-update validation failed")

p.write_text(s, encoding="utf-8")
