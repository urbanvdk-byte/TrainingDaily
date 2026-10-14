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


# Strength B — 14.10.2026. Idempotent.
if '"14.10"' not in s:
    old_stat = '<span class="stat-val">72</span><span class="stat-lbl">Тренировок</span>'
    old_dates = '"07.10","09.10","12.10"]'
    if old_stat not in s or old_dates not in s:
        raise RuntimeError("Unexpected diary version; refusing to alter index.html")

    s = s.replace(old_stat, '<span class="stat-val">73</span><span class="stat-lbl">Тренировок</span>', 1)
    s = s.replace(old_dates, '"07.10","09.10","12.10","14.10"]', 1)

    idx = re.search(r'const NEW_IDX = new Set\(\[([0-9, ]+)\]\);', s)
    if not idx or not idx.group(1).rstrip().endswith('71'):
        raise RuntimeError("Unexpected NEW_IDX")
    s = s[:idx.start(1)] + idx.group(1) + ', 72' + s[idx.end(1):]

    updates = [
        (r'Жим гантелей\n(30°)', 'null'),
        (r'Жим гантелей\nсидя (Плечи)', '{w:"22.5→22.5→20кг",r:[11,7,12]}'),
        (r'Тяга верхнего\nблока', 'null'),
        (r'Тяга нижнего\nблока (к поясу)', '{w:"72.7кг",r:[11,11,9]}'),
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
        (r'Скручивания\nна наклонной', 'null'),
        (r'Тяга прямыми\nруками', 'null'),
        (r'Разведение рук\nв стороны (тренажёр)', 'null')
    ]
    for name, entry in updates:
        s = append_cell(s, name, entry)

    # New exercise: calf raise machine replaces heavy dumbbell hold because that grip pulls the left elbow.
    new_name = 'name: "Подъём на носки\\nв тренажёре"'
    if new_name not in s:
        ex_end = s.find('];const COMMENTS = {')
        if ex_end < 0:
            raise RuntimeError("EXERCISES end not found")
        cells = ','.join(['null'] * 72 + ['{w:"30кг",r:[14,13,13]}'])
        new_ex = ',{name: "Подъём на носки\\nв тренажёре",cells: [' + cells + ']}'
        s = s[:ex_end] + new_ex + s[ex_end:]

note = ("⚠️ 14.10.2026 — Силовая Б. Общая усталость к концу тренировки высокая, поэтому скручивания сознательно пропущены. "
        "Жим сидя: 22.5 кг 11/7, затем 20 кг ×12 — повторная тяжёлая работа на 22.5 кг сегодня просела относительно 09.10, что согласуется с усталостью; вес не повышать. "
        "Нижний блок 72.7 кг 11/11/9 — снова 31 повтор суммарно, но распределение ровнее; рабочий уровень удержан. "
        "Тяга гантели к поясу 20 кг 12/12/12 — четвёртая подряд тренировка 3×12; вес пока не повышать из-за истории с левым локтем. "
        "Обратная бабочка 54 кг 12/12/12 — третья подряд тренировка 3×12; формально готова к следующей ступени, но прогрессию отложить до тренировки без высокой общей усталости. "
        "Выпады 20 кг 12/12 на каждую ногу — после пропуска 09.10 рабочий вес подтверждён, дальше пока не повышать из-за беговой нагрузки. "
        "Подъём на носок с гантелью заменён на тренажёр: 30 кг 14/13/13, потому что удержание большого веса тянет руку в области локтя. Замена удачная — сохраняет работу икр без лишней нагрузки на хват и локоть. "
        "Канат 59.1 кг 12/12/11 — лучший недавний результат, один повтор до 3×12. "
        "Общий вывод: мышечная работоспособность спины, ног и трицепса сохраняется хорошо, но повторные тяжёлые подходы в жиме плеч и субъективная усталость показывают, что сейчас не время одновременно повышать несколько нагрузок.")
start = s.find('const COMMENTS = {')
end = s.find('};function findPRs', start)
if start < 0 or end < 0:
    raise RuntimeError("COMMENTS not found")
body_start = start + len('const COMMENTS = {')
body = s[body_start:end]
note_escaped = note.replace("\\", "\\\\").replace('"', '\\"')
new_entry = f'72: "{note_escaped}"'
if re.search(r'72:\s*"(?:\\.|[^"\\])*"', body):
    body = re.sub(r'72:\s*"(?:\\.|[^"\\])*"', new_entry, body, count=1)
else:
    body = body.rstrip() + (',' if body.strip() else '') + new_entry
s = s[:body_start] + body + s[end:]

if ('src="run.html"' not in s or '"14.10"' not in s or '72: ' not in s
        or 'Подъём на носки\\nв тренажёре' not in s):
    raise RuntimeError("Post-update validation failed")

p.write_text(s, encoding="utf-8")
