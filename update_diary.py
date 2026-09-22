from pathlib import Path

p = Path('index.html')
s = p.read_text(encoding='utf-8')

# Since 22.09.2026 all new run entries live in TrainingDaily.
marker = 'data-run-entry="2026-09-22"'
if marker not in s:
    start = s.find('<section class="journal-panel" id="tab-run">')
    if start < 0:
        raise RuntimeError('Run panel start not found')
    end = s.find('</section>', start)
    if end < 0:
        raise RuntimeError('Run panel end not found')
    end += len('</section>')

    run_panel = '''
<section class="journal-panel" id="tab-run">
  <div class="sport-page">
    <div class="sport-title">Бег</div>
    <div class="sport-subtitle">Новые беговые тренировки с 22.09.2026 ведутся прямо в TrainingDaily. Старый Run ниже оставлен только как архив истории до 30.08.2026.</div>
    <div class="sport-summary">
      <div class="sport-pill"><strong>1</strong>новая тренировка</div>
      <div class="sport-pill"><strong>5,00 км</strong>с 22.09</div>
      <div class="sport-pill"><strong>37:52</strong>время</div>
      <div class="sport-pill"><strong>139</strong>ср. пульс</div>
    </div>
    <div class="sport-table-wrap"><table class="sport-table">
      <thead><tr><th>Дата</th><th>Тип</th><th>Дистанция</th><th>Время</th><th>Темп</th><th>Пульс ср./макс.</th><th>Каденс</th><th>ТЭ А/Ан</th><th>ТН</th><th>Комментарий</th></tr></thead>
      <tbody>
        <tr data-run-entry="2026-09-22">
          <td>22.09.2026</td>
          <td>Базовый / восстановительный</td>
          <td>5,00 км</td>
          <td>37:52</td>
          <td>7:34/км</td>
          <td>139 / 147</td>
          <td>158 ср. / 167 макс.</td>
          <td>2,5 / 0,0</td>
          <td>68</td>
          <td class="note">Возврат к бегу после паузы: первые 3 км ровные (7:26–7:36, ЧСС 136–139), на 4-м км был сброс до 7:56, затем 5-й км снова 7:25. COROS: Base. Средняя мощность 186 Вт, длина шага 0,84 м, контакт с землёй ~300 мс. Тренировка выполнена правильно как лёгкая базовая: низкий пульс, нулевой анаэробный стресс, без попытки сразу вернуться к прежнему темпу.</td>
        </tr>
      </tbody>
    </table></div>
    <div class="sport-note">Сплиты по 1 км: 7:26 / ЧСС 136 / 189 Вт; 7:28 / 137 / 188 Вт; 7:36 / 139 / 185 Вт; 7:56 / 141 / 178 Вт; 7:25 / 145 / 188 Вт. Следующий ориентир — лёгкие 6–7 км и оценка темпа при сопоставимой ЧСС, без резкого возврата к пороговой работе.</div>
    <div style="margin-top:24px" class="sport-title">Архив бегового дневника до 30.08.2026</div>
    <div class="sport-subtitle">Архив остаётся доступным для просмотра, но новые записи в старый репозиторий Run больше не добавляются.</div>
    <div class="embedded-run-wrap">
      <iframe id="run-journal-frame" class="embedded-run" src="https://urbanvdk-byte.github.io/Run/" title="Архив бегового дневника"></iframe>
    </div>
  </div>
</section>'''
    s = s[:start] + run_panel + s[end:]

p.write_text(s, encoding='utf-8')
