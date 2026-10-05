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


# Strength B — 05.10.2026. Idempotent.
if '"05.10"' not in s:
    old_stat = '<span class="stat-val">68</span><span class="stat-lbl">Тренировок</span>'
    old_dates = '"25.09","29.09","01.10"]'
    if old_stat not in s or old_dates not in s:
        raise RuntimeError("Unexpected diary version; refusing to alter index.html")

    s = s.replace(old_stat, '<span class="stat-val">69</span><span class="stat-lbl">Тренировок</span>', 1)
    s = s.replace(old_dates, '"25.09","29.09","01.10","05.10"]', 1)

    idx = re.search(r'const NEW_IDX = new Set\(\[([0-9, ]+)\]\);', s)
    if not idx or not idx.group(1).rstrip().endswith('67'):
        raise RuntimeError("Unexpected NEW_IDX")
    s = s[:idx.start(1)] + idx.group(1) + ', 68' + s[idx.end(1):]

    updates = [
        (r'Жим гантелей\n(30°)', 'null'),
        (r'Жим гантелей\nсидя (Плечи)', '{w:"20→22.5→22.5кг",r:[12,12,12]}'),
        (r'Тяга верхнего\nблока', 'null'),
        (r'Тяга нижнего\nблока (к поясу)', '{w:"72.7кг",r:[11,10,10]}'),
        (r'Тяга гантели\nк поясу', '{w:"20кг",r:[12,12,12]}'),
        (r'Отжимания\nна брусьях', 'null'),
        (r'Махи гантелями\nв стороны', 'null'),
        (r'Подъём гантелей\nна бицепс', 'null'),
        (r'Подъём ног\nв висе', 'null'),
        ('Молитва', 'null'),
        (r'Жим гантелей\nгоризонтальный', 'null'),
        (r'Обратная\nбабочка', '{w:"54кг",r:[12,12,12]}'),
        (r'Выпады вперёд\nс гантелями', '{w:"20кг",r:[12,12]}'),
        (r'Подъём на носок\n1 ногой', 'null'),
        (r'Разгибание рук\nс канатом', '{w:"59.1кг",r:[12,12,11]}'),
        (r'Молотковые\nсгибания', 'null'),
        (r'Скручивания\nна наклонной', '{w:"10кг",r:[16,14]}'),
        (r'Тяга прямыми\nруками', 'null'),
        (r'Разведение рук\nв стороны (тренажёр)', 'null')
    ]
    for name, entry in updates:
        s = append_cell(s, name, entry)

note = ("ℹ️ 05.10.2026 — Силовая Б на следующий день после беговой тренировки 04.10. "
        "По самочувствию выраженной усталости, как на предыдущих тяжёлых тренировках, не было: работа шла хорошо, "
        "но привычной высокой энергичности, которая бывала раньше, пока не было. "
        "Жим сидя: 20 кг ×12, затем 22.5 кг ×12/12 — повышение рабочего веса при сохранении верхней границы повторений. "
        "Нижний блок 72.7 кг 11/10/10. Тяга гантели к поясу 20 кг 12/12/12. "
        "Обратная бабочка 54 кг 12/12/12. Выпады повышены до 20 кг и выполнены 12/12 на каждую ногу. "
        "Подъёмы на носок сознательно пропущены: после вчерашнего бега икры болят; нулевые подходы в таблицу не считаются выполненными. "
        "Канат 59.1 кг 12/12/11. Скручивания 10 кг 16/14.")
start = s.find('const COMMENTS = {')
end = s.find('};function findPRs', start)
if start < 0 or end < 0:
    raise RuntimeError("COMMENTS not found")
body_start = start + len('const COMMENTS = {')
body = s[body_start:end]
note_escaped = note.replace("\\", "\\\\").replace('"', '\\"')
new_entry = f'68: "{note_escaped}"'
if re.search(r'68:\s*"(?:\\.|[^"\\])*"', body):
    body = re.sub(r'68:\s*"(?:\\.|[^"\\])*"', new_entry, body, count=1)
else:
    body = body.rstrip() + (',' if body.strip() else '') + new_entry
s = s[:body_start] + body + s[end:]

if 'src="run.html"' not in s or '"05.10"' not in s or '68: ' not in s:
    raise RuntimeError("Post-update validation failed")

p.write_text(s, encoding="utf-8")
