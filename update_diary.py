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


# Strength A — 12.10.2026. Idempotent.
if '"12.10"' not in s:
    old_stat = '<span class="stat-val">71</span><span class="stat-lbl">Тренировок</span>'
    old_dates = '"05.10","07.10","09.10"]'
    if old_stat not in s or old_dates not in s:
        raise RuntimeError("Unexpected diary version; refusing to alter index.html")

    s = s.replace(old_stat, '<span class="stat-val">72</span><span class="stat-lbl">Тренировок</span>', 1)
    s = s.replace(old_dates, '"05.10","07.10","09.10","12.10"]', 1)

    idx = re.search(r'const NEW_IDX = new Set\(\[([0-9, ]+)\]\);', s)
    if not idx or not idx.group(1).rstrip().endswith('70'):
        raise RuntimeError("Unexpected NEW_IDX")
    s = s[:idx.start(1)] + idx.group(1) + ', 71' + s[idx.end(1):]

    updates = [
        (r'Жим гантелей\n(30°)', '{w:"30кг",r:[12,12,11]}'),
        (r'Жим гантелей\nсидя (Плечи)', 'null'),
        (r'Тяга верхнего\nблока', '{w:"68.2кг",r:[12,10,8]}'),
        (r'Тяга нижнего\nблока (к поясу)', 'null'),
        (r'Тяга гантели\nк поясу', 'null'),
        (r'Отжимания\nна брусьях', '{bw:true,r:[27,20]}'),
        (r'Махи гантелями\nв стороны', 'null'),
        (r'Подъём гантелей\nна бицепс', 'null'),
        (r'Подъём ног\nв висе', 'null'),
        ('Молитва', '{w:"86.5кг",r:[15,12,10]}'),
        (r'Жим гантелей\nгоризонтальный', '{w:"30кг",r:[12,12,10]}'),
        (r'Обратная\nбабочка', 'null'),
        (r'Выпады вперёд\nс гантелями', 'null'),
        (r'Подъём на носок\n1 ногой', 'null'),
        (r'Разгибание рук\nс канатом', 'null'),
        (r'Молотковые\nсгибания', 'null'),
        (r'Скручивания\nна наклонной', 'null'),
        (r'Тяга прямыми\nруками', '{w:"59.1кг",r:[12,12,10]}'),
        (r'Разведение рук\nв стороны (тренажёр)', '{w:"9.1кг",r:[12,12,12]}')
    ]
    for name, entry in updates:
        s = append_cell(s, name, entry)

note = ("🔥 12.10.2026 — Силовая А. Очень сильная тренировка на следующий день после бега 11.10. "
        "Наклонный жим 30 кг 12/12/11 — лучший результат последних недель и почти закрыта верхняя граница. "
        "Горизонтальный жим 30 кг 12/12/10 — заметное восстановление после 07.10 (9/9/8). "
        "Верхний блок 68.2 кг 12/10/8 — лучший суммарный результат последних А на этом весе, но третий подход всё ещё проседает. "
        "Разведение в тренажёре 9.1 кг 12/12/12 — диапазон закрыт, упражнение хорошо переносится локтем. "
        "Брусья 27/20 — новый лучший первый подход текущего периода. "
        "Тяга прямыми руками 59.1 кг 12/12/10 — рабочий вес подтверждён. "
        "Молитва 86.5 кг 15/12/10 — новый вес закреплён уверенно. "
        "Общий вывод: после недавних колебаний усталости верх тела сегодня показал явное восстановление и рост работоспособности; не повышать сразу все веса одновременно, чтобы сохранить беговую готовность и не перегрузить локоть/плечевой пояс.")
start = s.find('const COMMENTS = {')
end = s.find('};function findPRs', start)
if start < 0 or end < 0:
    raise RuntimeError("COMMENTS not found")
body_start = start + len('const COMMENTS = {')
body = s[body_start:end]
note_escaped = note.replace("\\", "\\\\").replace('"', '\\"')
new_entry = f'71: "{note_escaped}"'
if re.search(r'71:\s*"(?:\\.|[^"\\])*"', body):
    body = re.sub(r'71:\s*"(?:\\.|[^"\\])*"', new_entry, body, count=1)
else:
    body = body.rstrip() + (',' if body.strip() else '') + new_entry
s = s[:body_start] + body + s[end:]

if 'src="run.html"' not in s or '"12.10"' not in s or '71: ' not in s:
    raise RuntimeError("Post-update validation failed")

p.write_text(s, encoding="utf-8")
