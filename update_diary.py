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

# Strength A — 01.10.2026. Idempotent.
if '"01.10"' not in s:
    old_stat = '<span class="stat-val">67</span><span class="stat-lbl">Тренировок</span>'
    old_dates = '"21.09","25.09","29.09"]'
    if old_stat not in s or old_dates not in s:
        raise RuntimeError("Unexpected diary version; refusing to alter index.html")

    s = s.replace(old_stat, '<span class="stat-val">68</span><span class="stat-lbl">Тренировок</span>', 1)
    s = s.replace(old_dates, '"21.09","25.09","29.09","01.10"]', 1)

    idx = re.search(r'const NEW_IDX = new Set\(\[([0-9, ]+)\]\);', s)
    if not idx or not idx.group(1).rstrip().endswith('66'):
        raise RuntimeError("Unexpected NEW_IDX")
    s = s[:idx.start(1)] + idx.group(1) + ', 67' + s[idx.end(1):]

    updates = [
        (r'Жим гантелей\n(30°)', '{w:"30кг",r:[12,11,9]}'),
        (r'Жим гантелей\nсидя (Плечи)', 'null'),
        (r'Тяга верхнего\nблока', '{w:"68.2→63.6→63.6кг",r:[11,10,10]}'),
        (r'Тяга нижнего\nблока (к поясу)', 'null'),
        (r'Тяга гантели\nк поясу', 'null'),
        (r'Отжимания\nна брусьях', '{bw:true,r:[25,20]}'),
        (r'Махи гантелями\nв стороны', 'null'),
        (r'Подъём гантелей\nна бицепс', 'null'),
        (r'Подъём ног\nв висе', 'null'),
        ('Молитва', '{w:"82кг",r:[15,13,11]}'),
        (r'Жим гантелей\nгоризонтальный', '{w:"32.5→30→30кг",r:[9,10,11]}'),
        (r'Обратная\nбабочка', 'null'),
        (r'Выпады вперёд\nс гантелями', 'null'),
        (r'Подъём на носок\n1 ногой', 'null'),
        (r'Разгибание рук\nс канатом', 'null'),
        (r'Молотковые\nсгибания', 'null'),
        (r'Скручивания\nна наклонной', 'null'),
        (r'Тяга прямыми\nруками', '{w:"50→54.5→54.5кг",r:[12,12,12]}')
    ]
    for name, entry in updates:
        s = append_cell(s, name, entry)

    # New permanent exercise row for the lateral-deltoid machine.
    machine_name = r'Разведение рук\nв стороны (тренажёр)'
    if f'name: "{machine_name}"' not in s:
        marker = '];const COMMENTS = {'
        pos = s.find(marker)
        if pos < 0:
            raise RuntimeError("EXERCISES end marker not found")
        cells = ','.join(['null'] * 67 + ['{w:"6.8→6.8→9.1кг",r:[12,12,12]}'])
        obj = ',{name: "' + machine_name + '",cells: [' + cells + ']}'
        s = s[:pos] + obj + s[pos:]

note = ("⚠️ 01.10.2026 — Силовая А. Еле заставил себя пойти на тренировку; "
        "общее состояние усталости сохраняется уже некоторое время. "
        "Жимы снова шли тяжело: наклонный 30 кг 12/11/9; горизонтальный "
        "начат 32.5 кг ×9, затем снижен до 30 кг ×10/11. Верхний блок тоже "
        "шёл тяжело: 68.2 кг ×11, затем снижение до 63.6 кг ×10/10. "
        "Махи гантелями заменены на разведение рук в тренажёре для средней дельты: "
        "локоть при гантелях ещё тянет, в тренажёре заметно легче; "
        "6.8 кг 12/12, 9.1 кг ×12. Брусья 25/20. "
        "Тяга прямыми руками: 50 кг ×12, 54.5 кг ×12/12. "
        "Молитва 82 кг 15/13/11.")
start = s.find('const COMMENTS = {')
end = s.find('};function findPRs', start)
if start < 0 or end < 0:
    raise RuntimeError("COMMENTS not found")
body = s[start+len('const COMMENTS = {'):end]
if '67: ' not in body:
    note_escaped = note.replace("\\", "\\\\").replace('"', '\\"')
    body = body.rstrip() + (',' if body.strip() else '') + f'67: "{note_escaped}"'
    s = s[:start+len('const COMMENTS = {')] + body + s[end:]

if 'src="run.html"' not in s or '"01.10"' not in s or '67: ' not in s or r'Разведение рук\nв стороны (тренажёр)' not in s:
    raise RuntimeError("Post-update validation failed")

p.write_text(s, encoding="utf-8")
