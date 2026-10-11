from pathlib import Path

p = Path("run.html")
s = p.read_text(encoding="utf-8")

marker = 'data-run-entry="2026-10-11"'
if marker not in s:
    row_0810 = '<tr class="type-aerobic" data-run-entry="2026-10-08"><td>08.10.2026</td><td>Аэробная работа (рельеф)</td><td>6.92</td><td>41:42</td><td>6:01</td><td>154/171</td><td>158</td><td>97</td><td>—</td><td>3.1/2.2</td></tr>'
    row_1110 = '<tr class="type-aerobic" data-run-entry="2026-10-11"><td>11.10.2026</td><td>Аэробно-пороговая прогрессия (5 км легко + 2,7 км быстро)</td><td>7.70</td><td>44:51</td><td>5:50</td><td>149/165</td><td>163</td><td>0</td><td>—</td><td>2.9/2.4</td></tr>'
    if row_0810 not in s:
        raise RuntimeError("08.10 run row not found")
    s = s.replace(row_0810, row_0810 + row_1110, 1)

    note = ('<div class="note-card"><div class="note-header" style="background:#cce5ff">'
            '<strong>11.10.2026 — Аэробно-пороговая прогрессия</strong>'
            '<span class="meta">Маршрут: плоско &nbsp;|&nbsp; COROS: Threshold &nbsp;|&nbsp; Performance: Below Average</span></div>'
            '<div class="note-body"><div class="text">'
            '7,70 км за 44:51, средний темп 5:50/км при ЧСС 149, максимум 165. Тренировка получилась двухчастной: первые 5 км — спокойная аэробная работа примерно по 6:14/км при ЧСС 143, затем последние 2,70 км — выраженный пороговый финиш примерно по 5:04/км при ЧСС 161. '
            'На быстром блоке мощность выросла примерно с 226 до 277 Вт, каденс с 161 до 170, длина шага с 0,99 до 1,16 м, а контакт с землёй сократился примерно с 278 до 243 мс — ускорение выполнено за счёт одновременно более частого и более длинного шага без признаков технического развала. '
            'По сравнению с 04.10 средний темп быстрее на 12 сек/км, дистанция больше на 1,47 км, а средний пульс выше всего на 3 уд/мин; однако значительная часть разницы создана быстрым финишем. '
            'По сравнению с 08.10 темп быстрее на 11 сек/км при ЧСС на 5 уд/мин ниже и большей дистанции, но сегодняшняя трасса плоская против 97 м набора, поэтому прямое сравнение ограничено. '
            'С 27.08 совпал средний темп 5:50/км, при этом сегодня средний пульс 149 против 155, но дистанция короче — хороший признак возврата экономичности, не доказательство полной готовности к прежнему объёму. '
            'Training Load 124, ТЭ 2,9/2,4: это уже качественная работа, а не лёгкий бег. За 04–11.10 выполнено 20,85 км бега, причём 08.10 и 11.10 обе тренировки получили заметную качественную составляющую. Следующая пробежка должна быть действительно лёгкой, без порогового финиша.'
            '</div><div class="stats">'
            'Дист: <span>7.70 км</span> &nbsp;|&nbsp; Время: <span>44:51</span> &nbsp;|&nbsp; Темп: <span>5:50</span><br>'
            'Пульс: <span>149/165</span> &nbsp;|&nbsp; Каденс: <span>163 ср. / 179 макс.</span> &nbsp;|&nbsp; Набор: <span>0 м</span><br>'
            'ТЭ: <span>2.9 / 2.4</span> &nbsp;|&nbsp; Лучший км: <span>4:58</span> &nbsp;|&nbsp; Калории: <span>619</span><br>'
            'ТН: <span>124</span> &nbsp;|&nbsp; Мощность: <span>241 Вт</span> &nbsp;|&nbsp; Длина шага: <span>1,05 м</span> &nbsp;|&nbsp; Контакт на быстром блоке: <span>~243 мс</span><br>'
            'Первые 5 км: <span>~6:14/км, ЧСС 143</span> &nbsp;|&nbsp; Последние 2,70 км: <span>~5:04/км, ЧСС 161</span>'
            '</div></div></div>')
    progress_marker = '</div><div class="section-title">Прогресс ключевых показателей</div>'
    if progress_marker not in s:
        raise RuntimeError("Progress section marker not found")
    s = s.replace(progress_marker, note + progress_marker, 1)

    header_old = '<th>08.10</th><th>Динамика</th>'
    if header_old not in s:
        raise RuntimeError("Progress header marker not found")
    s = s.replace(header_old, '<th>08.10</th><th>11.10</th><th>Динамика</th>', 1)

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

    s = add_progress(s, 'Каденс (ш/мин)', '163', 'Средний каденс 163; на последних 2,7 км вырос примерно до 170 вместе с ускорением — хороший технический ответ на скорость')
    s = add_progress(s, 'Пульс средний', '149', 'Средний пульс ниже 08.10 при более быстром среднем темпе, но плоский маршрут и двухчастная структура ограничивают прямое сравнение')
    s = add_progress(s, 'Дистанция (км)', '7.70', 'Объём вырос до 7,70 км; за 04–11.10 уже 20,85 км, поэтому следующую пробежку не увеличивать')
    s = add_progress(s, 'Аэробный ТЭ', '2.9', 'ТЭ 2.9 / 2.4 и пороговый финиш делают тренировку качественной; следующая работа должна быть лёгкой')
    s = add_progress(s, 'Темп средний (мин/км)', '5:50', 'Средний темп быстрее 04.10 и 08.10, но ключевой прогресс — способность после 5 спокойных км держать около 5:04/км ещё 2,7 км')
    s = add_progress(s, 'Лучший темп (мин/км)', '4:58', 'Лучший километр впервые снова быстрее 5:00/км после возврата; не превращать это в обязательный финиш каждой лёгкой пробежки')
    s = add_progress(s, 'Время на земле (мс)', '~243*', 'На быстром финальном блоке контакт около 243 мс против ~278 мс на первых 5 км — техника ускорилась, а не рассыпалась')
    s = add_progress(s, 'Набор высоты (м)', '0', 'Плоская трасса делает оценку быстрого блока чистой; сравнение с рельефной 08.10 проводить с поправкой на 97 м набора')

if marker not in s:
    raise RuntimeError("11.10 run entry validation failed")

p.write_text(s, encoding="utf-8")
