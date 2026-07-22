from pathlib import Path

p = Path('index.html')
s = p.read_text(encoding='utf-8')

if '"22.07"' in s:
    raise SystemExit(0)

s = s.replace('<span class="stat-val">43</span><span class="stat-lbl">Тренировок</span>', '<span class="stat-val">44</span><span class="stat-lbl">Тренировок</span>', 1)
s = s.replace('"17.07","20.07"]', '"17.07","20.07","22.07"]', 1)
s = s.replace('new Set([29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42])', 'new Set([29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43])', 1)

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

s = append_cells(s, 'Жим гантелей\\n(30°)', ['{w:"30кг",r:[12,12,9]}'])
s = append_cells(s, 'Жим гантелей\\nсидя (Плечи)', ['null'])
s = append_cells(s, 'Тяга верхнего\\nблока', ['{w:"68.2кг",r:[12,12,10]}'])
s = append_cells(s, 'Тяга нижнего\\nблока (к поясу)', ['null'])
s = append_cells(s, 'Тяга гантели\\nк поясу', ['null'])
s = append_cells(s, 'Отжимания\\nна брусьях', ['{bw:true,r:[15,15]}'])
s = append_cells(s, 'Махи гантелями\\nв стороны', ['{w:"12.5кг",r:[11,10,9]}'])
s = append_cells(s, 'Подъём гантелей\\nна бицепс', ['{w:"12.5кг",r:[14,13,12]}'])
s = append_cells(s, 'Подъём ног\\nв висе', ['null'])
s = append_cells(s, 'Молитва', ['{w:"72.7→77кг",r:[15,13,13]}'])

needle = '];const COMMENTS ='
pos = s.find(needle)
if pos < 0:
    raise RuntimeError('EXERCISES end not found')
new_cells = ['null'] * 43 + ['{w:"25кг",r:[12,12,12]}']
new_obj = ',{name: "Жим гантелей\\nгоризонтальный",cells: [' + ','.join(new_cells) + ']}'
s = s[:pos] + new_obj + s[pos:]

p.write_text(s, encoding='utf-8')
