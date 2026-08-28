from pathlib import Path

p = Path('index.html')
s = p.read_text(encoding='utf-8')


def append_cells(text, name, entries):
    marker = f'name: "{name}",cells: ['
    start = text.find(marker)
    if start < 0:
        raise RuntimeError(f'Exercise not found: {name}')
    arr_start = start + len(marker) - 1
    depth = 0
    in_str = False
    esc = False
    for i in range(arr_start, len(text)):
        ch = text[i]
        if in_str:
            if esc:
                esc = False
            elif ch == '\\':
                esc = True
            elif ch == '"':
                in_str = False
            continue
        if ch == '"':
            in_str = True
        elif ch == '[':
            depth += 1
        elif ch == ']':
            depth -= 1
            if depth == 0:
                return text[:i] + ',' + ','.join(entries) + text[i:]
    raise RuntimeError('Array end not found')


# 26.08.2026 — preserve cumulative update for clean rebuilds.
if '"26.08"' not in s:
    s = s.replace('<span class="stat-val">56</span><span class="stat-lbl">Тренировок</span>', '<span class="stat-val">57</span><span class="stat-lbl">Тренировок</span>', 1)
    s = s.replace('"03.08","05.08","07.08","10.08","12.08","14.08","17.08","19.08","24.08"]', '"03.08","05.08","07.08","10.08","12.08","14.08","17.08","19.08","24.08","26.08"]', 1)
    s = s.replace('new Set([29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55])', 'new Set([29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56])', 1)
    s = append_cells(s, 'Жим гантелей\\n(30°)', ['null'])
    s = append_cells(s, 'Жим гантелей\\nсидя (Плечи)', ['{w:"20кг",r:[12,12,9]}'])
    s = append_cells(s, 'Тяга верхнего\\nблока', ['null'])
    s = append_cells(s, 'Тяга нижнего\\nблока (к поясу)', ['{w:"68.2кг",r:[12,12,12]}'])
    s = append_cells(s, 'Тяга гантели\\nк поясу', ['{w:"20→22.5кг",r:[14,10,10]}'])
    s = append_cells(s, 'Отжимания\\nна брусьях', ['null'])
    s = append_cells(s, 'Махи гантелями\\nв стороны', ['null'])
    s = append_cells(s, 'Подъём гантелей\\nна бицепс', ['null'])
    s = append_cells(s, 'Подъём ног\\nв висе', ['null'])
    s = append_cells(s, 'Молитва', ['null'])
    s = append_cells(s, 'Жим гантелей\\nгоризонтальный', ['null'])
    s = append_cells(s, 'Обратная\\nбабочка', ['{w:"49.5кг",r:[12,12,12]}'])
    s = append_cells(s, 'Выпады вперёд\\nс гантелями', ['{w:"16кг",r:[12,12]}'])
    s = append_cells(s, 'Подъём на носок\\n1 ногой', ['{w:"30кг",r:[15,14,13]}'])
    s = append_cells(s, 'Разгибание рук\\nс канатом', ['{w:"54.5кг",r:[12,12,10]}'])

# 28.08.2026 — Training A.
if '"28.08"' not in s:
    s = s.replace('<span class="stat-val">57</span><span class="stat-lbl">Тренировок</span>', '<span class="stat-val">58</span><span class="stat-lbl">Тренировок</span>', 1)
    s = s.replace('"17.08","19.08","24.08","26.08"]', '"17.08","19.08","24.08","26.08","28.08"]', 1)
    s = s.replace('new Set([29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56])', 'new Set([29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57])', 1)

    s = append_cells(s, 'Жим гантелей\\n(30°)', ['{w:"30кг",r:[12,12,10]}'])
    s = append_cells(s, 'Жим гантелей\\nсидя (Плечи)', ['null'])
    s = append_cells(s, 'Тяга верхнего\\nблока', ['{w:"68.2кг",r:[12,12,10]}'])
    s = append_cells(s, 'Тяга нижнего\\nблока (к поясу)', ['null'])
    s = append_cells(s, 'Тяга гантели\\nк поясу', ['null'])
    s = append_cells(s, 'Отжимания\\nна брусьях', ['{bw:true,r:[22,20]}'])
    s = append_cells(s, 'Махи гантелями\\nв стороны', ['{w:"12.5кг",r:[12,12,12]}'])
    s = append_cells(s, 'Подъём гантелей\\nна бицепс', ['null'])
    s = append_cells(s, 'Подъём ног\\nв висе', ['null'])
    s = append_cells(s, 'Молитва', ['{w:"82кг",r:[18,16,15]}'])
    s = append_cells(s, 'Жим гантелей\\nгоризонтальный', ['{w:"30кг",r:[12,12,12]}'])
    s = append_cells(s, 'Обратная\\nбабочка', ['null'])
    s = append_cells(s, 'Выпады вперёд\\nс гантелями', ['null'])
    s = append_cells(s, 'Подъём на носок\\n1 ногой', ['null'])
    s = append_cells(s, 'Разгибание рук\\nс канатом', ['null'])

    if 'name: "Молотковые\\nсгибания"' not in s:
        marker = '];const COMMENTS = {'
        pos = s.find(marker)
        if pos < 0:
            raise RuntimeError('EXERCISES end marker not found')
        cells = ','.join(['null'] * 57 + ['{w:"12.5кг",r:[12,12,12]}'])
        obj = ',{name: "Молотковые\\nсгибания",cells: [' + cells + ']}'
        s = s[:pos] + obj + s[pos:]

# Preserve previously restored user comments. Add new workout comments only when the user supplies them.
comments = {
    52: "ℹ️ 14.08.2026 — Подъём на носок не выполнялся: икры болят после вчерашнего забега и вело. Подъём ног в висе не выполнялся: корпус напряжён после вчерашнего забега и вело.",
    53: "ℹ️ 17.08.2026 — Тяга верхнего блока выполнена после махов: упражнения поменяны местами, потому что тренажёр был занят.",
    55: "⚠️ 24.08.2026 — Бицепс снижен до 12.5 кг: с прошлой тренировки есть дискомфорт и тянущее ощущение при сильном сгибании левого локтя; 15 кг ещё на прошлой тренировке шли плохо.",
}

start = s.find('const COMMENTS = {')
end = s.find('};function findPRs', start)
if start < 0 or end < 0:
    raise RuntimeError('COMMENTS object not found')
obj_start = start + len('const COMMENTS = {')
body = s[obj_start:end]
for idx, text in comments.items():
    marker = f'{idx}: '
    if marker in body:
        continue
    escaped = text.replace('\\', '\\\\').replace('"', '\\"')
    body = body.rstrip() + (',' if body.strip() else '') + f'{idx}: "{escaped}"'
s = s[:obj_start] + body + s[end:]

p.write_text(s, encoding='utf-8')
