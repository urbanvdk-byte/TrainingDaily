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


# Strength B — 09.10.2026. Idempotent.
if '"09.10"' not in s:
    old_stat = '<span class="stat-val">70</span><span class="stat-lbl">Тренировок</span>'
    old_dates = '"01.10","05.10","07.10"]'
    if old_stat not in s or old_dates not in s:
        raise RuntimeError("Unexpected diary version; refusing to alter index.html")

    s = s.replace(old_stat, '<span class="stat-val">71</span><span class="stat-lbl">Тренировок</span>', 1)
    s = s.replace(old_dates, '"01.10","05.10","07.10","09.10"]', 1)

    idx = re.search(r'const NEW_IDX = new Set\(\[([0-9, ]+)\]\);', s)
    if not idx or not idx.group(1).rstrip().endswith('69'):
        raise RuntimeError("Unexpected NEW_IDX")
    s = s[:idx.start(1)] + idx.group(1) + ', 70' + s[idx.end(1):]

    updates = [
        (r'Жим гантелей\n(30°)', 'null'),
        (r'Жим гантелей\nсидя (Плечи)', '{w:"22.5→22.5→20кг",r:[12,8,12]}'),
        (r'Тяга верхнего\nблока', 'null'),
        (r'Тяга нижнего\nблока (к поясу)', '{w:"72.7кг",r:[12,10,9]}'),
        (r'Тяга гантели\nк поясу', '{w:"20кг",r:[12,12,12]}'),
        (r'Отжимания\nна брусьях', 'null'),
        (r'Махи гантелями\nв стороны', 'null'),
        (r'Подъём гантелей\nна бицепс', 'null'),
        (r'Подъём ног\nв висе', 'null'),
        ('Молитва', 'null'),
        (r'Жим гантелей\nгоризонтальный', 'null'),
        (r'Обратная\nбабочка', '{w:"54кг",r:[12,12,12]}'),
        (r'Выпады вперёд\nс гантелями', 'null'),
        (r'Подъём на носок\n1 ногой', 'null'),
        (r'Разгибание рук\nс канатом', '{w:"59.1кг",r:[12,11,11]}'),
        (r'Молотковые\nсгибания', 'null'),
        (r'Скручивания\nна наклонной', 'null'),
        (r'Тяга прямыми\nруками', 'null'),
        (r'Разведение рук\nв стороны (тренажёр)', 'null')
    ]
    for name, entry in updates:
        s = append_cell(s, name, entry)

note = ("⚠️ 09.10.2026 — Силовая Б на следующий день после рельефного бега 08.10 (6.92 км, набор 97 м, ТН 138). "
        "Общая усталость к концу тренировки высокая. Жим сидя: 22.5 кг ×12/8, затем снижение до 20 кг ×12 — первый подход сильный, но второй резко просел. "
        "Нижний блок 72.7 кг 12/10/9 — суммарно 31 повтор, уровень последних Б удержан. Тяга гантели к поясу 20 кг 12/12/12 — стабильная работа; вес не повышать из-за истории с локтем. "
        "Обратная бабочка 54 кг 12/12/12 — второй раз подряд закрыта верхняя граница. "
        "Выпады и подъёмы на носок сознательно пропущены после вчерашнего рельефного бега; нулевые подходы не считаются выполненными. "
        "Канат 59.1 кг 12/11/11 — почти закрыта верхняя граница. Скручивания пропущены из-за высокой общей усталости. "
        "Следующую Б не перегружать прогрессиями: сначала подтвердить восстановление и вернуть ровность плечевого жима.")
start = s.find('const COMMENTS = {')
end = s.find('};function findPRs', start)
if start < 0 or end < 0:
    raise RuntimeError("COMMENTS not found")
body_start = start + len('const COMMENTS = {')
body = s[body_start:end]
note_escaped = note.replace("\\", "\\\\").replace('"', '\\"')
new_entry = f'70: "{note_escaped}"'
if re.search(r'70:\s*"(?:\\.|[^"\\])*"', body):
    body = re.sub(r'70:\s*"(?:\\.|[^"\\])*"', new_entry, body, count=1)
else:
    body = body.rstrip() + (',' if body.strip() else '') + new_entry
s = s[:body_start] + body + s[end:]

if 'src="run.html"' not in s or '"09.10"' not in s or '70: ' not in s:
    raise RuntimeError("Post-update validation failed")

p.write_text(s, encoding="utf-8")
