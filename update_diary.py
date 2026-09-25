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

# Strength A — 25.09.2026. Idempotent on repeated workflow runs.
if '"25.09"' not in s:
    old_stat = '<span class="stat-val">65</span><span class="stat-lbl">Тренировок</span>'
    old_dates = '"11.09","14.09","21.09"]'
    if old_stat not in s or old_dates not in s:
        raise RuntimeError("Unexpected diary version; refusing to alter index.html")

    s = s.replace(old_stat, '<span class="stat-val">66</span><span class="stat-lbl">Тренировок</span>', 1)
    s = s.replace(old_dates, '"11.09","14.09","21.09","25.09"]', 1)

    idx = re.search(r'const NEW_IDX = new Set\(\[([0-9, ]+)\]\);', s)
    if not idx or not idx.group(1).rstrip().endswith('64'):
        raise RuntimeError("Unexpected NEW_IDX")
    s = s[:idx.start(1)] + idx.group(1) + ', 65' + s[idx.end(1):]

    updates = [
        (r'Жим гантелей\n(30°)', '{w:"30кг",r:[12,10,9]}'),
        (r'Жим гантелей\nсидя (Плечи)', 'null'),
        (r'Тяга верхнего\nблока', '{w:"68.2кг",r:[11,8,7]}'),
        (r'Тяга нижнего\nблока (к поясу)', 'null'),
        (r'Тяга гантели\nк поясу', 'null'),
        (r'Отжимания\nна брусьях', '{bw:true,r:[21,19]}'),
        (r'Махи гантелями\nв стороны', '{w:"10кг",r:[12,12,11]}'),
        (r'Подъём гантелей\nна бицепс', 'null'),
        (r'Подъём ног\nв висе', 'null'),
        ('Молитва', '{w:"82кг",r:[20,14,11]}'),
        (r'Жим гантелей\nгоризонтальный', '{w:"32.5→30кг",r:[10,6,9]}'),
        (r'Обратная\nбабочка', 'null'),
        (r'Выпады вперёд\nс гантелями', 'null'),
        (r'Подъём на носок\n1 ногой', 'null'),
        (r'Разгибание рук\nс канатом', 'null'),
        (r'Молотковые\nсгибания', 'null'),
        (r'Скручивания\nна наклонной', 'null'),
        (r'Тяга прямыми\nруками', '{w:"45.5→50→50кг",r:[12,12,12]}')
    ]
    for name, entry in updates:
        s = append_cell(s, name, entry)

note = ("⚠️ 25.09.2026 — Силовая А. Жимы шли тяжело: наклонный жим 30 кг "
        "12/10/9 сильно вымотал; на горизонтальном после 32.5 кг 10/6 "
        "пришлось снизить третий подход до 30 кг ×9. Верхний блок "
        "68.2 кг 11/8/7 — выраженное падение повторений. "
        "Махи: левый локоть всё ещё тянет, хотя слабее, чем ранее; "
        "несмотря на это, выполнены с уменьшенным весом 10 кг 12/12/11. "
        "Брусья: свой вес 21/19. Тяга прямыми руками: "
        "45.5 кг ×12, затем 50 кг ×12/12. Молитва 82 кг 20/14/11.")
start = s.find('const COMMENTS = {')
end = s.find('};function findPRs', start)
if start < 0 or end < 0:
    raise RuntimeError("COMMENTS not found")
body = s[start+len('const COMMENTS = {'):end]
if '65: ' not in body:
    note_escaped = note.replace("\\", "\\\\").replace('"', '\\"')
    body = body.rstrip() + (',' if body.strip() else '') + f'65: "{note_escaped}"'
    s = s[:start+len('const COMMENTS = {')] + body + s[end:]

# Keep all existing tabs and the local running journal intact.
if 'src="run.html"' not in s or '"25.09"' not in s or '65: ' not in s:
    raise RuntimeError("Post-update validation failed")

# Correct the pre-existing trailing placeholder that shifted the 21.09 row
# one column into the 25.09 date. Do not change any other exercise history.
bad = '{w:"22.5кг",r:[10,9,9]},null,{w:"20кг",r:[12,12,11]},null]'
good = '{w:"22.5кг",r:[10,9,9]},{w:"20кг",r:[12,12,11]},null]'
if bad in s:
    if s.count(bad) != 1:
        raise RuntimeError("Ambiguous row alignment; refusing to edit")
    s = s.replace(bad, good, 1)
elif good not in s:
    raise RuntimeError("One-arm row structure changed; inspect manually")

p.write_text(s, encoding="utf-8")
