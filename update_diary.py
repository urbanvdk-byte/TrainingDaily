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
    depth, quoted, escaped = 0, False, False
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

# Strength B — 29.09.2026. Idempotent.
if '"29.09"' not in s:
    old_stat = '<span class="stat-val">66</span><span class="stat-lbl">Тренировок</span>'
    old_dates = '"14.09","21.09","25.09"]'
    if old_stat not in s or old_dates not in s:
        raise RuntimeError("Unexpected diary version; refusing to alter index.html")

    s = s.replace(old_stat, '<span class="stat-val">67</span><span class="stat-lbl">Тренировок</span>', 1)
    s = s.replace(old_dates, '"14.09","21.09","25.09","29.09"]', 1)

    idx = re.search(r'const NEW_IDX = new Set\(\[([0-9, ]+)\]\);', s)
    if not idx or not idx.group(1).rstrip().endswith('65'):
        raise RuntimeError("Unexpected NEW_IDX")
    s = s[:idx.start(1)] + idx.group(1) + ', 66' + s[idx.end(1):]

    updates = [
        (r'Жим гантелей\n(30°)', 'null'),
        (r'Жим гантелей\nсидя (Плечи)', '{w:"20кг",r:[12,12,12]}'),
        (r'Тяга верхнего\nблока', 'null'),
        (r'Тяга нижнего\nблока (к поясу)', '{w:"72.7кг",r:[12,11,8]}'),
        (r'Тяга гантели\nк поясу', '{w:"20кг",r:[12,12,12]}'),
        (r'Отжимания\nна брусьях', 'null'),
        (r'Махи гантелями\nв стороны', 'null'),
        (r'Подъём гантелей\nна бицепс', 'null'),
        (r'Подъём ног\nв висе', 'null'),
        ('Молитва', 'null'),
        (r'Жим гантелей\nгоризонтальный', 'null'),
        (r'Обратная\nбабочка', '{w:"54кг",r:[12,12,11]}'),
        (r'Выпады вперёд\nс гантелями', '{w:"18кг",r:[12,12]}'),
        (r'Подъём на носок\n1 ногой', '{w:"32.5кг",r:[15,13,11]}'),
        (r'Разгибание рук\nс канатом', '{w:"59.1кг",r:[12,11,9]}'),
        (r'Молотковые\nсгибания', 'null'),
        (r'Скручивания\nна наклонной', '{w:"10кг",r:[16,14]}'),
        (r'Тяга прямыми\nруками', 'null')
    ]
    for name, entry in updates:
        s = append_cell(s, name, entry)

note = ("⚠️ 29.09.2026 — Силовая Б. Тяга гантели к поясу выполнена с уменьшенным "
        "до 20 кг весом из-за левого локтя; 12/12/12. Жим сидя 20 кг 12/12/12. "
        "Нижний блок 72.7 кг 12/11/8. Обратная бабочка 54 кг 12/12/11. "
        "Выпады 18 кг 12/12 на каждую ногу. Подъём на носок 32.5 кг 15/13/11. "
        "Канат 59.1 кг 12/11/9. Скручивания 10 кг 16/14.")
start = s.find('const COMMENTS = {')
end = s.find('};function findPRs', start)
if start < 0 or end < 0:
    raise RuntimeError("COMMENTS not found")
body = s[start+len('const COMMENTS = {'):end]
if '66: ' not in body:
    note_escaped = note.replace("\\", "\\\\").replace('"', '\\"')
    body = body.rstrip() + (',' if body.strip() else '') + f'66: "{note_escaped}"'
    s = s[:start+len('const COMMENTS = {')] + body + s[end:]

if 'src="run.html"' not in s or '"29.09"' not in s or '66: ' not in s:
    raise RuntimeError("Post-update validation failed")

p.write_text(s, encoding="utf-8")
