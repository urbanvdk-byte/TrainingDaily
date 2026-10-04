from pathlib import Path

p = Path("run.html")
s = p.read_text(encoding="utf-8")

marker = 'data-run-entry="2026-10-04"'
if marker not in s:
    row_2209 = '<tr class="type-recovery" data-run-entry="2026-09-22"><td>22.09.2026</td><td>Восстановительно-базовый бег (возврат после паузы)</td><td>5.00</td><td>37:52</td><td>7:34</td><td>139/147</td><td>158</td><td>0</td><td>—</td><td>2.5/0.0</td></tr>'
    row_0410 = '<tr class="type-aerobic" data-run-entry="2026-10-04"><td>04.10.2026</td><td>Аэробная работа с прогрессией финиша</td><td>6.23</td><td>37:33</td><td>6:02</td><td>146/161</td><td>162</td><td>4</td><td>—</td><td>2.7/1.8</td></tr>'
    if row_2209 not in s:
        raise RuntimeError("22.09 run row not found")
    s = s.replace(row_2209, row_2209 + row_0410, 1)

    note = ('<div class="note-card"><div class="note-header" style="background:#cce5ff">'
            '<strong>04.10.2026 — Аэробная работа с прогрессией финиша</strong>'
            '<span class="meta">Маршрут: почти плоско &nbsp;|&nbsp; COROS: Tempo &nbsp;|&nbsp; Борг: —</span></div>'
            '<div class="note-body"><div class="text">'
            '6,23 км за 37:33, средний темп 6:02/км при ЧСС 146, максимум 161. '
            'После возвратной пробежки 22.09 (5,00 км по 7:34 при ЧСС 139) скорость заметно вернулась: '
            'темп быстрее на 1:32/км при росте среднего пульса всего на 7 уд/мин. '
            'Первые километры были неровными: 5:33, 6:15, 6:21, 6:13; затем выраженная прогрессия 5-го и 6-го км — 5:55 и 5:44. '
            'Пульс при этом вырос от 139 в начале до 152–155 на последних полных километрах, то есть финиш уже вышел из чисто лёгкой зоны. '
            'Средняя мощность 233 Вт, каденс 162, длина шага 1,02 м, контакт с землёй около 272 мс. '
            'ТЭ 2,7/1,8 и ТН 96 — умеренная развивающая работа, не тяжёлая, но и не восстановительная. '
            'На фоне сохраняющейся общей усталости следующую пробежку не ускорять: 5–7 км разговорно, без быстрого финиша. '
            'По COROS краткосрочная нагрузка 31 против долгосрочной 41 (отношение 0,75), восстановление 82%; перегруза по объёму не видно, поэтому субъективную усталость продолжаем оценивать отдельно от тренировочной нагрузки.'
            '</div><div class="stats">'
            'Дист: <span>6.23 км</span> &nbsp;|&nbsp; Время: <span>37:33</span> &nbsp;|&nbsp; Темп: <span>6:02</span><br>'
            'Пульс: <span>146/161</span> &nbsp;|&nbsp; Каденс: <span>162 ср. / 177 макс.</span> &nbsp;|&nbsp; Набор: <span>4 м</span><br>'
            'ТЭ: <span>2.7 / 1.8</span> &nbsp;|&nbsp; Лучший км: <span>5:30</span> &nbsp;|&nbsp; Калории: <span>519</span><br>'
            'ТН: <span>96</span> &nbsp;|&nbsp; Мощность: <span>233 Вт</span> &nbsp;|&nbsp; Длина шага: <span>1,02 м</span> &nbsp;|&nbsp; Контакт: <span>~272 мс</span>'
            '</div></div></div>')
    progress_marker = '</div><div class="section-title">Прогресс ключевых показателей</div>'
    if progress_marker not in s:
        raise RuntimeError("Progress section marker not found")
    s = s.replace(progress_marker, note + progress_marker, 1)

    header_old = '<th>22.09</th><th>Динамика</th>'
    if header_old not in s:
        raise RuntimeError("Progress header marker not found")
    s = s.replace(header_old, '<th>22.09</th><th>04.10</th><th>Динамика</th>', 1)

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

    s = add_progress(s, 'Каденс (ш/мин)', '162', 'Каденс вернулся к 162 на более быстром темпе; искусственно повышать не нужно')
    s = add_progress(s, 'Пульс средний', '146', '6:02/км при ЧСС 146 — заметно экономичнее возвратной пробежки 22.09')
    s = add_progress(s, 'Дистанция (км)', '6.23', 'Объём вырос с 5,00 до 6,23 км; следующую тренировку не увеличивать одновременно по скорости и дистанции')
    s = add_progress(s, 'Аэробный ТЭ', '2.7', 'ТЭ 2.7 / 1.8 — умеренная развивающая нагрузка, уже не чисто восстановительная')
    s = add_progress(s, 'Темп средний (мин/км)', '6:02', 'На 1:32/км быстрее 22.09 при +7 уд/мин среднего пульса — хороший возврат аэробной экономичности')
    s = add_progress(s, 'Лучший темп (мин/км)', '5:30', 'Лучший км 5:30; быстрый финиш пока не делать обязательной частью лёгких пробежек')
    s = add_progress(s, 'Время на земле (мс)', '~272', 'Контакт сократился примерно с 300 до 272 мс вместе с ростом скорости — ожидаемое улучшение динамики шага')
    s = add_progress(s, 'Набор высоты (м)', '4', 'Практически плоский маршрут — сравнение темпа и пульса достаточно чистое')

if marker not in s:
    raise RuntimeError("Run entry validation failed")

p.write_text(s, encoding="utf-8")
