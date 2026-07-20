from pathlib import Path

p = Path('index.html')
s = p.read_text(encoding='utf-8')

if '"17.07"' in s:
    raise SystemExit(0)

s = s.replace('<span class="stat-val">39</span><span class="stat-lbl">Тренировок</span>', '<span class="stat-val">42</span><span class="stat-lbl">Тренировок</span>', 1)
s = s.replace('"01.07","09.07"]', '"01.07","09.07","13.07","15.07","17.07"]', 1)
s = s.replace('new Set([29, 30, 31, 32, 33, 34, 35, 36, 37, 38])', 'new Set([29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41])', 1)

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

s = append_cells(s, 'Жим гантелей\\n(30°)', ['{w:"30кг",r:[12,8,6]}','{w:"30кг",r:[12,10,8]}','{w:"30кг",r:[12,12,12]}'])
s = append_cells(s, 'Жим гантелей\\nсидя (Плечи)', ['null','{w:"17.5кг",r:[10,11,10]}','null'])
s = append_cells(s, 'Тяга верхнего\\nблока', ['{w:"68.2кг",r:[12,9,9]}','{w:"68.2кг",r:[11,10,10]}','{w:"68.2кг",r:[12,12,10]}'])
s = append_cells(s, 'Тяга нижнего\\nблока (к поясу)', ['{w:"63.6кг",r:[12,11,10]}','{w:"63.6кг",r:[11,11,10]}','{w:"63.6кг",r:[10,10,10]}'])
s = append_cells(s, 'Тяга гантели\\nк поясу', ['{w:"20кг",r:[12,11,10]}','{w:"20кг",r:[9,9,9]}','{w:"20кг",r:[10,10,9]}'])
s = append_cells(s, 'Отжимания\\nна брусьях', ['null','{bw:true,r:[15,13,15]}','null'])
s = append_cells(s, 'Махи гантелями\\nв стороны', ['{w:"12.5кг",r:[9,9,8]}','null','{w:"12.5кг",r:[10,10,9]}'])
s = append_cells(s, 'Подъём гантелей\\nна бицепс', ['{w:"12.5кг",r:[11,11,10]}','{w:"12.5кг",r:[12,12,12]}','{w:"12.5кг",r:[12,12,12]}'])
s = append_cells(s, 'Подъём ног\\nв висе', ['null','null','null'])

needle = '];const COMMENTS ='
pos = s.find(needle)
if pos < 0:
    raise RuntimeError('EXERCISES end not found')
prayer_cells = ['null'] * 39 + ['{w:"68.2→72.7кг",r:[12,11,11]}','{w:"72.7→77.2кг",r:[12,13,12]}','null']
new_obj = ',{name: "Молитва",cells: [' + ','.join(prayer_cells) + ']}'
s = s[:pos] + new_obj + s[pos:]

p.write_text(s, encoding='utf-8')
