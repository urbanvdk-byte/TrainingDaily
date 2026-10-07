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


# Strength A — 07.10.2026. Idempotent.
if '"07.10"' not in s:
    old_stat = '<span class="stat-val">69</span><span class="stat-lbl">Тренировок</span>'
    old_dates = '"29.09","01.10","05.10"]'
    if old_stat not in s or old_dates not in s:
        raise RuntimeError("Unexpected diary version; refusing to alter index.html")

    s = s.replace(old_stat, '<span class="stat-val">70</span><span class="stat-lbl">Тренировок</span>', 1)
    s = s.replace(old_dates, '"29.09","01.10","05.10","07.10"]', 1)

    idx = re.search(r'const NEW_IDX = new Set\(\[([0-9, ]+)\]\);', s)
    if not idx or not idx.group(1).rstrip().endswith('68'):
        raise RuntimeError("Unexpected NEW_IDX")
    s = s[:idx.start(1)] + idx.group(1) + ', 69' + s[idx.end(1):]

    updates = [
        (r'Жим гантелей\n(30°)', '{w:"30кг",r:[12,11,8]}'),
        (r'Жим гантелей\nсидя (Плечи)', 'null'),
        (r'Тяга верхнего\nблока', '{w:"68.2кг",r:[11,8,7]}'),
        (r'Тяга нижнего\nблока (к поясу)', 'null'),
        (r'Тяга гантели\nк поясу', 'null'),
        (r'Отжимания\nна брусьях', '{bw:true,r:[26,20]}'),
        (r'Махи гантелями\nв стороны', 'null'),
        (r'Подъём гантелей\nна бицепс', 'null'),
        (r'Подъём ног\nв висе', 'null'),
        ('Молитва', '{w:"82→86.5→86.5кг",r:[15,11,11]}'),
        (r'Жим гантелей\nгоризонтальный', '{w:"30кг",r:[9,9,8]}'),
        (r'Обратная\nбабочка', 'null'),
        (r'Выпады вперёд\nс гантелями', 'null'),
        (r'Подъём на носок\n1 ногой', 'null'),
        (r'Разгибание рук\nс канатом', 'null'),
        (r'Молотковые\nсгибания', 'null'),
        (r'Скручивания\nна наклонной', 'null'),
        (r'Тяга прямыми\nруками', '{w:"54.5→59.1→59.1кг",r:[12,12,10]}'),
        (r'Разведение рук\nв стороны (тренажёр)', '{w:"9.1кг",r:[12,12,11]}')
    ]
    for name, entry in updates:
        s = append_cell(s, name, entry)

note = ("ℹ️ 07.10.2026 — Силовая А. Наклонный жим 30 кг 12/11/8; горизонтальный жим 30 кг 9/9/8. "
        "Верхний блок 68.2 кг 11/8/7 — заметный спад к третьему подходу. "
        "Разведение рук в тренажёре 9.1 кг 12/12/11 — почти закрыта верхняя граница диапазона без возврата к провоцирующим локоть махам гантелями. "
        "Брусья 26/20 — лучший первый подход текущего периода. "
        "Тяга прямыми руками: 54.5 кг ×12, затем 59.1 кг ×12/10 — повышение веса. "
        "Молитва: 82 кг ×15, затем 86.5 кг ×11/11 — повышение веса при хорошем сохранении повторений.")
start = s.find('const COMMENTS = {')
end = s.find('};function findPRs', start)
if start < 0 or end < 0:
    raise RuntimeError("COMMENTS not found")
body_start = start + len('const COMMENTS = {')
body = s[body_start:end]
note_escaped = note.replace("\\", "\\\\").replace('"', '\\"')
new_entry = f'69: "{note_escaped}"'
if re.search(r'69:\s*"(?:\\.|[^"\\])*"', body):
    body = re.sub(r'69:\s*"(?:\\.|[^"\\])*"', new_entry, body, count=1)
else:
    body = body.rstrip() + (',' if body.strip() else '') + new_entry
s = s[:body_start] + body + s[end:]

if 'src="run.html"' not in s or '"07.10"' not in s or '69: ' not in s:
    raise RuntimeError("Post-update validation failed")

p.write_text(s, encoding="utf-8")
