from pathlib import Path

p = Path('index.html')
s = p.read_text(encoding='utf-8')

if '"14.08"' in s:
    raise SystemExit(0)

s = s.replace('<span class="stat-val">52</span><span class="stat-lbl">Тренировок</span>', '<span class="stat-val">53</span><span class="stat-lbl">Тренировок</span>', 1)
s = s.replace('"03.08","05.08","07.08","10.08","12.08"]', '"03.08","05.08","07.08","10.08","12.08","14.08"]', 1)
s = s.replace('new Set([29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51])', 'new Set([29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52])', 1)

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

s = append_cells(s, 'Жим гантелей\\n(30°)', ['null'])
s = append_cells(s, 'Жим гантелей\\nсидя (Плечи)', ['{w:"20кг",r:[12,11,8]}'])
s = append_cells(s, 'Тяга верхнего\\nблока', ['null'])
s = append_cells(s, 'Тяга нижнего\\nблока (к поясу)', ['{w:"68.2кг",r:[12,12,12]}'])
s = append_cells(s, 'Тяга гантели\\nк поясу', ['{w:"22.5кг",r:[10,10,10]}'])
s = append_cells(s, 'Отжимания\\nна брусьях', ['null'])
s = append_cells(s, 'Махи гантелями\\nв стороны', ['null'])
s = append_cells(s, 'Подъём гантелей\\nна бицепс', ['null'])
s = append_cells(s, 'Подъём ног\\nв висе', ['null'])
s = append_cells(s, 'Молитва', ['null'])
s = append_cells(s, 'Жим гантелей\\nгоризонтальный', ['null'])
s = append_cells(s, 'Обратная\\nбабочка', ['{w:"49.5кг",r:[12,12,12]}'])
s = append_cells(s, 'Выпады вперёд\\nс гантелями', ['{w:"14кг",r:[12,8]}'])
s = append_cells(s, 'Подъём на носок\\n1 ногой', ['null'])
s = append_cells(s, 'Разгибание рук\\nс канатом', ['{w:"54.5кг",r:[12,12,10]}'])

p.write_text(s, encoding='utf-8')
