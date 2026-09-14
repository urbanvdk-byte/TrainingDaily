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


# 14.09.2026 — Training A.
if '"14.09"' not in s:
    s = s.replace('<span class="stat-val">63</span><span class="stat-lbl">Тренировок</span>', '<span class="stat-val">64</span><span class="stat-lbl">Тренировок</span>', 1)
    s = s.replace('"09.09","11.09"]', '"09.09","11.09","14.09"]', 1)
    s = s.replace('new Set([29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62])', 'new Set([29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63])', 1)

    s = append_cells(s, 'Жим гантелей\\n(30°)', ['{w:"30кг",r:[12,10,6]}'])
    s = append_cells(s, 'Жим гантелей\\nсидя (Плечи)', ['null'])
    s = append_cells(s, 'Тяга верхнего\\nблока', ['{w:"68.2кг",r:[11,10,10]}'])
    s = append_cells(s, 'Тяга нижнего\\nблока (к поясу)', ['null'])
    s = append_cells(s, 'Тяга гантели\\nк поясу', ['null'])
    s = append_cells(s, 'Отжимания\\nна брусьях', ['{bw:true,r:[25,21]}'])
    s = append_cells(s, 'Махи гантелями\\nв стороны', ['{w:"12.5кг",r:[0,0,0]}'])
    s = append_cells(s, 'Подъём гантелей\\nна бицепс', ['null'])
    s = append_cells(s, 'Подъём ног\\nв висе', ['null'])
    s = append_cells(s, 'Молитва', ['{w:"82кг",r:[20,14,13]}'])
    s = append_cells(s, 'Жим гантелей\\nгоризонтальный', ['{w:"32.5кг",r:[12,11,10]}'])
    s = append_cells(s, 'Обратная\\nбабочка', ['null'])
    s = append_cells(s, 'Выпады вперёд\\nс гантелями', ['null'])
    s = append_cells(s, 'Подъём на носок\\n1 ногой', ['null'])
    s = append_cells(s, 'Разгибание рук\\nс канатом', ['null'])
    s = append_cells(s, 'Молотковые\\nсгибания', ['null'])
    s = append_cells(s, 'Скручивания\\nна наклонной', ['null'])

    if 'name: "Тяга прямыми\\nруками"' not in s:
        marker = '];const COMMENTS = {'
        pos = s.find(marker)
        if pos < 0:
            raise RuntimeError('EXERCISES end marker not found')
        cells = ','.join(['null'] * 63 + ['{w:"36.4→40.9→45.5кг",r:[12,12,12]}'])
        obj = ',{name: "Тяга прямыми\\nруками",cells: [' + cells + ']}'
        s = s[:pos] + obj + s[pos:]

comments = {
    52: "ℹ️ 14.08.2026 — Подъём на носок не выполнялся: икры болят после вчерашнего забега и вело. Подъём ног в висе не выполнялся: корпус напряжён после вчерашнего забега и вело.",
    53: "ℹ️ 17.08.2026 — Тяга верхнего блока выполнена после махов: упражнения поменяны местами, потому что тренажёр был занят.",
    55: "⚠️ 24.08.2026 — Бицепс снижен до 12.5 кг: с прошлой тренировки есть дискомфорт и тянущее ощущение при сильном сгибании левого локтя; 15 кг ещё на прошлой тренировке шли плохо.",
    58: "ℹ️ 31.08.2026 — В жиме гантелей сидя был заметный запас даже в последнем подходе. Выпады и икры сознательно убраны: после вчерашних 15 км бега ногам нужен отдых.",
    61: "⚠️ 09.09.2026 — Очень тяжёлая тренировка: веса шли тяжело, показатели просели почти во всех упражнениях, после тренировки самочувствие плохое. Молотковые сгибания: боль слева в области локтя/бицепса при сгибании и в начальной фазе разгибания; вес снижен с 15 до 12.5 кг.",
    62: "⚠️ 11.09.2026 — Тяга гантели к поясу: левой рукой неприятно, при растяжении появляются лёгкие болезненные ощущения в области бицепса/передней части локтя; к третьему подходу ощущение стало слабее. Скручивания: раньше блин 10 кг лежал на груди и было легко; сегодня блин убран за голову — стало заметно тяжелее и корпус получается скручивать лучше.",
    63: "⚠️ 14.09.2026 — Махи гантелями не выполнены: боль в левом локте стреляла достаточно сильно, сильнее, чем при сгибаниях на бицепс. Прямой бицепс исключён, так как боль не уменьшается; вместо него выполнена тяга прямыми руками с верхнего блока 36.4→40.9→45.5 кг по 12 повторений."
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
