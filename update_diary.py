from pathlib import Path

p = Path('index.html')
s = p.read_text(encoding='utf-8')

if '"24.07"' in s:
    raise SystemExit(0)

s = s.replace('<span class="stat-val">44</span><span class="stat-lbl">Тренировок</span>', '<span class="stat-val">45</span><span class="stat-lbl">Тренировок</span>', 1)
s = s.replace('"20.07","22.07"]', '"20.07","22.07","24.07"]', 1)
s = s.replace('new Set([29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43])', 'new Set([29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44])', 1)

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

# Existing columns
s = append_cells(s, 'Жим гантелей\\n(30°)', ['null'])
s = append_cells(s, 'Жим гантелей\\nсидя (Плечи)', ['{w:"17.5кг",r:[12,12,12]}'])
s = append_cells(s, 'Тяга верхнего\\nблока', ['null'])
s = append_cells(s, 'Тяга нижнего\\nблока (к поясу)', ['{w:"63.6кг",r:[12,12,12]}'])
s = append_cells(s, 'Тяга гантели\\nк поясу', ['{w:"20кг",r:[12,11,11]}'])
s = append_cells(s, 'Отжимания\\nна брусьях', ['null'])
s = append_cells(s, 'Махи гантелями\\nв стороны', ['null'])
s = append_cells(s, 'Подъём гантелей\\nна бицепс', ['null'])
s = append_cells(s, 'Подъём ног\\nв висе', ['{bw:true,r:[14,14,11]}'])
s = append_cells(s, 'Молитва', ['null'])
s = append_cells(s, 'Жим гантелей\\nгоризонтальный', ['null'])

# New columns
needle = '];const COMMENTS ='
pos = s.find(needle)
if pos < 0:
    raise RuntimeError('EXERCISES end not found')

prefix = ['null'] * 44
new_objects = [
    ',{name: "Обратная\\nбабочка",cells: [' + ','.join(prefix + ['{w:"36кг",r:[12,12,12]}']) + ']}',
    ',{name: "Выпады вперёд\\nс гантелями",cells: [' + ','.join(prefix + ['{w:"10кг общий",r:[12,12]}']) + ']}',
    ',{name: "Подъём на носок\\n1 ногой",cells: [' + ','.join(prefix + ['{w:"27.5кг",r:[14,14,14]}']) + ']}',
    ',{name: "Разгибание рук\\nс канатом",cells: [' + ','.join(prefix + ['{w:"41кг",r:[12,12,12]}']) + ']}'
]
s = s[:pos] + ''.join(new_objects) + s[pos:]

p.write_text(s, encoding='utf-8')
