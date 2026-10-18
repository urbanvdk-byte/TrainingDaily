from pathlib import Path
import re

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


# Strength A — 18.10.2026. Idempotent.
if '"18.10"' not in s:
    old_stat = '<span class="stat-val">73</span><span class="stat-lbl">Тренировок</span>'
    old_dates = '"09.10","12.10","14.10"]'
    if old_stat not in s or old_dates not in s:
        raise RuntimeError("Unexpected diary version; refusing to alter index.html")

    s = s.replace(old_stat, '<span class="stat-val">74</span><span class="stat-lbl">Тренировок</span>', 1)
    s = s.replace(old_dates, '"09.10","12.10","14.10","18.10"]', 1)

    idx = re.search(r'const NEW_IDX = new Set\\(\\[([0-9, ]+)\\]\\);', s)
    if not idx or not idx.group(1).rstrip().endswith('72'):
        raise RuntimeError("Unexpected NEW_IDX")
    s = s[:idx.start(1)] + idx.group(1) + ', 73' + s[idx.end(1):]

    updates = [
        (r'Жим гантелей\\n(30°)', '{w:"30кг",r:[12,12,11]}'),
        (r'Жим гантелей\\nсидя (Плечи)', 'null'),
        (r'Тяга верхнего\\nблока', '{w:"65кг",r:[12,9,8]}'),
        (r'Тяга нижнего\\nблока (к поясу)', 'null'),
        (r'Тяга гантели\\nк поясу', 'null'),
        (r'Отжимания\\nна брусьях', '{bw:true,r:[28,20]}'),
        (r'Махи гантелями\\nв стороны', 'null'),
        (r'Подъём гантелей\\nна бицепс', 'null'),
        (r'Подъём ног\\nв висе', 'null'),
        ('Молитва', 'null'),
        (r'Жим гантелей\\nгоризонтальный', '{w:"30кг",r:[12,12,10]}'),
        (r'Обратная\\nбабочка', 'null'),
        (r'Выпады вперёд\\nс гантелями', 'null'),
        (r'Подъём на носок\\n1 ногой', 'null'),
        (r'Разгибание рук\\nс канатом', 'null'),
        (r'Молотковые\\nсгибания', 'null'),
        (r'Скручивания\\nна наклонной', 'null'),
        (r'Тяга прямыми\\nруками', '{w:"59.1кг",r:[12,12,12]}'),
        (r'Разведение рук\\nв стороны (тренажёр)', '{w:"9.1кг",r:[12,12,12]}'),
        (r'Подъём на носки\\nв тренажёре', 'null')
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

start = s.find('const COMMENTS = {')
end = s.find('};function findPRs', start)
if start < 0 or end < 0:
    raise RuntimeError("COMMENTS not found")
body_start = start + len('const COMMENTS = {')
body = s[body_start:end]
note_escaped = note.replace("\\", "\\\\").replace('"', '\\"')
new_entry = f'73: "{note_escaped}"'
if re.search(r'73:\\s*"(?:\\\\.|[^"\\\\])*"', body):
    body = re.sub(r'73:\\s*"(?:\\\\.|[^"\\\\])*"', new_entry, body, count=1)
else:
    body = body.rstrip() + (',' if body.strip() else '') + new_entry
s = s[:body_start] + body + s[end:]

if ('src="run.html"' not in s or '"18.10"' not in s or '73: ' not in s):
    raise RuntimeError("Post-update validation failed")

p.write_text(s, encoding="utf-8")
