from pathlib import Path

p = Path("run.html")
s = p.read_text(encoding="utf-8")

marker = 'data-run-entry="2026-10-08"'
if marker not in s:
    row_0410 = '<tr class="type-aerobic" data-run-entry="2026-10-04"><td>04.10.2026</td><td>Аэробная работа с прогрессией финиша</td><td>6.23</td><td>37:33</td><td>6:02</td><td>146/161</td><td>162</td><td>4</td><td>—</td><td>2.7/1.8</td></tr>'
    row_0810 = '<tr class="type-aerobic" data-run-entry="2026-10-08"><td>08.10.2026</td><td>Аэробная работа (рельеф)</td><td>6.92</td><td>41:42</td><td>6:01</td><td>154/171</td><td>158</td><td>97</td><td>—</td><td>3.1/2.2</td></tr>'
    if row_0410 not in s:
        raise RuntimeError("04.10 run row not found")
    s = s.replace(row_0410, row_0410 + row_0810, 1)

    note = ('<div class="note-card"><div class="note-header" style="background:#cce5ff">'
            '<strong>08.10.2026 — Аэробная работа (рельеф)</strong>'
            '<span class="meta">Маршрут: рельеф &nbsp;|&nbsp; COROS: Tempo &nbsp;|&nbsp; Борг: —</span></div>'
            '<div class="note-body"><div class="text">'
            '6,92 км за 41:42, средний темп 6:01/км при ЧСС 154, максимум 171. Набор 97 м — нагрузка заметно тяжелее, чем на почти плоской тренировке 04.10. '
            'При этом средний темп практически не изменился (6:02 → 6:01), дистанция выросла на 0,69 км, а приведённый темп составил 5:56/км. '
            'Цена этого прогресса — рост среднего пульса на 8 уд/мин и тренировочной нагрузки с 96 до 138; ТЭ вырос с 2,7/1,8 до 3,1/2,2. '
            'По километрам рельеф сильно влиял на темп: 6:09, 5:42, 6:14, 5:46, 6:53, 5:45 и последние 0,92 км примерно по 5:40. '
            'Самый тяжёлый 5-й км включал около 37 м набора: 6:53 при ЧСС 161, поэтому замедление объясняется подъёмом, а не развалом формы. '
            'На 6-м км после спуска темп вернулся к 5:45 при ЧСС 153, а финиш прошёл около 5:40 при ЧСС 159 — хороший признак сохранения работоспособности после подъёма. '
            'Средняя мощность 238 Вт, каденс 158, длина шага 1,05 м, средний контакт с землёй по километровым отрезкам около 282 мс. '
            'На фоне силовой А 07.10 эта пробежка даёт хороший аэробно-силовой стимул, но уже не является лёгкой. Следующий бег — 5–7 км ровно и разговорно, без рельефной гонки и быстрого финиша.'
            '</div><div class="stats">'
            'Дист: <span>6.92 км</span> &nbsp;|&nbsp; Время: <span>41:42</span> &nbsp;|&nbsp; Темп: <span>6:01</span><br>'
            'Пульс: <span>154/171</span> &nbsp;|&nbsp; Каденс: <span>158 ср. / 177 макс.</span> &nbsp;|&nbsp; Набор: <span>97 м</span><br>'
            'ТЭ: <span>3.1 / 2.2</span> &nbsp;|&nbsp; Лучший км: <span>5:22</span> &nbsp;|&nbsp; Калории: <span>611</span><br>'
            'ТН: <span>138</span> &nbsp;|&nbsp; Мощность: <span>238 Вт</span> &nbsp;|&nbsp; Длина шага: <span>1,05 м</span> &nbsp;|&nbsp; Приведённый темп: <span>5:56</span> &nbsp;|&nbsp; Контакт: <span>~282 мс</span>'
            '</div></div></div>')
    progress_marker = '</div><div class="section-title">Прогресс ключевых показателей</div>'
    if progress_marker not in s:
        raise RuntimeError("Progress section marker not found")
    s = s.replace(progress_marker, note + progress_marker, 1)

    header_old = '<th>04.10</th><th>Динамика</th>'
    if header_old not in s:
        raise RuntimeError("Progress header marker not found")
    s = s.replace(header_old, '<th>04.10</th><th>08.10</th><th>Динамика</th>', 1)

    def add_progress(text, label, value, indicator):
        row_marker = '<td class="left">' + label + '</td>'
        start = text.find(row_marker)
        if start < 0:
            raise RuntimeError(f"Progress row not found: {label}")
        end = text.find('</tr>', start)
        if end < 0:
            raise RuntimeError(f"Progress row end not found: {label}")
        ind = text.rfind('<td class="indicator">', start, end)
        if ind < 0:
            raise RuntimeError(f"Progress indicator not found: {label}")
        text = text[:ind] + '<td>' + value + '</td>' + text[ind:]
        ind = text.find('<td class="indicator">', ind + len(value))
        ind_end = text.find('</td>', ind)
        text = text[:ind] + '<td class="indicator">' + indicator + text[ind_end:]
        return text

    s = add_progress(s, 'Каденс (ш/мин)', '158', 'На рельефе каденс снизился 162 → 158; это объяснимо подъёмами и не требует искусственного повышения')
    s = add_progress(s, 'Пульс средний', '154', 'Темп 6:01/км при ЧСС 154 и наборе 97 м: нагрузка выше 04.10, но рельеф объясняет значительную часть роста пульса')
    s = add_progress(s, 'Дистанция (км)', '6.92', 'Объём вырос с 6,23 до 6,92 км (+11%); дальше не повышать одновременно дистанцию и интенсивность')
    s = add_progress(s, 'Аэробный ТЭ', '3.1', 'ТЭ 3.1 / 2.2 — полноценная развивающая аэробная работа, не восстановительная')
    s = add_progress(s, 'Темп средний (мин/км)', '6:01', 'Практически тот же темп, что 04.10, но на маршруте с 97 м набора; приведённый темп 5:56')
    s = add_progress(s, 'Лучший темп (мин/км)', '5:22', 'Лучший км 5:22; скорость вернулась после подъёмов, но следующий бег должен быть лёгким')
    s = add_progress(s, 'Время на земле (мс)', '~282', 'Контакт около 282 мс закономерен для рельефа и более низкого каденса; явного развала к финишу нет')
    s = add_progress(s, 'Набор высоты (м)', '97', '97 м набора на 6,92 км — существенный рельеф; темп нужно оценивать вместе с пульсом и приведённым темпом')

if marker not in s:
    raise RuntimeError("Run entry validation failed")

p.write_text(s, encoding="utf-8")
