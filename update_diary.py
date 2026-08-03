from pathlib import Path

p = Path('index.html')
s = p.read_text(encoding='utf-8')

if '"03.08"' in s:
    raise SystemExit(0)

s = s.replace('<span class="stat-val">47</span><span class="stat-lbl">Тренировок</span>', '<span class="stat-val">48</span><span class="stat-lbl">Тренировок</span>', 1)
s = s.replace('Март — Июль 2026', 'Март — Август 2026', 1)
s = s.replace('<option value="07">Июль</option>', '<option value="07">Июль</option><option value="08">Август</option>', 1)
s = s.replace('<span class="stat-val">36.4→63.6</span><span class="stat-lbl">Нижний блок (кг)</span>', '<span class="stat-val">36.4→68.2</span><span class="stat-lbl">Нижний блок (кг)</span>', 1)
s = s.replace('"27.07","29.07"]', '"27.07","29.07","03.08"]', 1)
s = s.replace('new Set([29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46])', 'new Set([29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47])', 1)

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

s = append_cells(s, 'Жим гантелей\\n(30°)', ['{w:"30кг",r:[12,11,9]}'])
s = append_cells(s, 'Жим гантелей\\nсидя (Плечи)', ['null'])
s = append_cells(s, 'Тяга верхнего\\nблока', ['{w:"68.2кг",r:[12,11,10]}'])
s = append_cells(s, 'Тяга нижнего\\nблока (к поясу)', ['null'])
s = append_cells(s, 'Тяга гантели\\nк поясу', ['null'])
s = append_cells(s, 'Отжимания\\nна брусьях', ['{bw:true,r:[21,15]}'])
s = append_cells(s, 'Махи гантелями\\nв стороны', ['{w:"12.5кг",r:[12,10,9]}'])
s = append_cells(s, 'Подъём гантелей\\nна бицепс', ['{w:"12.5кг",r:[14,13,14]}'])
s = append_cells(s, 'Подъём ног\\nв висе', ['null'])
s = append_cells(s, 'Молитва', ['{w:"77кг",r:[16,15,16]}'])
s = append_cells(s, 'Жим гантелей\\nгоризонтальный', ['{w:"27.5кг",r:[12,12,12]}'])
s = append_cells(s, 'Обратная\\nбабочка', ['null'])
s = append_cells(s, 'Выпады вперёд\\nс гантелями', ['null'])
s = append_cells(s, 'Подъём на носок\\n1 ногой', ['null'])
s = append_cells(s, 'Разгибание рук\\nс канатом', ['null'])

p.write_text(s, encoding='utf-8')
