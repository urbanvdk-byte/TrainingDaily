from pathlib import Path

p = Path('index.html')
s = p.read_text(encoding='utf-8')

MARKER = 'id="journal-tabs"'

if MARKER not in s:
    extra_css = r'''
.journal-tabs{position:sticky;top:0;z-index:60;display:flex;gap:8px;padding:10px 2rem;background:rgba(255,255,255,.96);backdrop-filter:blur(8px);border-bottom:1px solid var(--border);box-shadow:var(--shadow);overflow-x:auto}
.journal-tab{appearance:none;border:1px solid var(--border2);background:var(--surface2);color:var(--text);font:600 12px var(--sans);padding:8px 14px;border-radius:999px;cursor:pointer;white-space:nowrap;transition:.15s ease}
.journal-tab:hover{border-color:var(--accent);color:var(--accent)}
.journal-tab.active{background:var(--accent);color:#fff;border-color:var(--accent)}
.journal-panel{display:none}.journal-panel.active{display:block}
#tab-strength .controls{top:53px}
.embedded-run-wrap{padding:14px 0 0;background:var(--bg)}
.embedded-run{display:block;width:100%;min-height:1200px;border:0;background:#f2f4f8}
.sport-page{max-width:1180px;margin:0 auto;padding:26px 2rem 40px}
.sport-title{font-size:20px;font-weight:700;margin-bottom:4px}.sport-subtitle{font-size:12px;color:var(--muted);margin-bottom:18px}
.sport-summary{display:flex;gap:12px;flex-wrap:wrap;margin-bottom:16px}.sport-pill{background:var(--surface);border:1px solid var(--border);box-shadow:var(--shadow);border-radius:8px;padding:8px 11px;font-size:12px}.sport-pill strong{font-size:15px;margin-right:4px}
.sport-table-wrap{overflow-x:auto;background:var(--surface);border-radius:10px;box-shadow:var(--shadow)}
.sport-table{width:100%;min-width:880px;border-collapse:collapse;border-radius:10px;overflow:hidden;box-shadow:none}
.sport-table th{background:var(--surface2);color:var(--muted);font-size:11px;font-weight:700;padding:9px 7px;border-bottom:2px solid var(--border2);white-space:nowrap}
.sport-table td{font-size:12px;padding:9px 7px;border-bottom:1px solid var(--border);text-align:center;vertical-align:top}
.sport-table td.note{text-align:left;min-width:260px;line-height:1.45}.sport-table tr:last-child td{border-bottom:0}
.sport-note{margin-top:12px;padding:10px 12px;background:var(--amber-dim);border:1px solid #fde68a;border-radius:7px;color:#92400e;font-size:11.5px;line-height:1.45}
@media(max-width:600px){.journal-tabs,.sport-page{padding-left:1rem;padding-right:1rem}.embedded-run{min-height:900px}#tab-strength .controls{top:52px}}
'''
    s = s.replace('</style>', extra_css + '</style>', 1)

    tabs = '''<nav class="journal-tabs" id="journal-tabs" aria-label="Разделы дневника">
<button class="journal-tab active" type="button" data-tab="strength">Силовые</button>
<button class="journal-tab" type="button" data-tab="run">Бег</button>
<button class="journal-tab" type="button" data-tab="bike">Велосипед</button>
<button class="journal-tab" type="button" data-tab="kayak">Каяк</button>
</nav>'''
    s = s.replace('</header>', '</header>' + tabs, 1)

    start = s.find(tabs) + len(tabs)
    end = s.rfind('</body>')
    if start < len(tabs) or end < 0:
        raise RuntimeError('Could not locate body for tab migration')
    strength_content = s[start:end]

    bike_panel = '''
<section class="journal-panel" id="tab-bike">
  <div class="sport-page">
    <div class="sport-title">Велосипед</div>
    <div class="sport-subtitle">Отдельный журнал велосипедных тренировок</div>
    <div class="sport-summary">
      <div class="sport-pill"><strong>2</strong>тренировки</div>
      <div class="sport-pill"><strong>12,63 км</strong>суммарно</div>
      <div class="sport-pill"><strong>49:22</strong>в движении</div>
      <div class="sport-pill"><strong>465 ккал</strong>суммарно</div>
    </div>
    <div class="sport-table-wrap"><table class="sport-table">
      <thead><tr><th>Дата</th><th>Дистанция</th><th>Время</th><th>Ср. скорость</th><th>Макс. скорость</th><th>Пульс ср./макс.</th><th>Набор</th><th>Калории</th><th>ТН</th><th>ТЭ А/Ан</th><th>Комментарий</th></tr></thead>
      <tbody>
        <tr><td>25.08.2026</td><td>5,51 км</td><td>25:38</td><td>12,9 км/ч</td><td>33,7 км/ч</td><td>125 / 148</td><td>104 м</td><td>227</td><td>30</td><td>1,9 / 0,0</td><td class="note">Первая часть велосипедной тренировки. Умеренная кросс‑нагрузка.</td></tr>
        <tr><td>25.08.2026</td><td>7,12 км</td><td>23:44</td><td>18,0 км/ч</td><td>46,5 км/ч</td><td>136 / 160</td><td>61 м</td><td>238</td><td>44</td><td>2,1 / 1,0</td><td class="note">Вторая часть. Интенсивность выше первой, но без высокой тренировочной нагрузки.</td></tr>
      </tbody>
    </table></div>
    <div class="sport-note">Итог 25.08: 12,63 км, 49:22, около 165 м набора и 465 ккал. Эти поездки учитываются как кросс‑тренинг и не заменяют ключевую беговую работу.</div>
  </div>
</section>'''

    kayak_panel = '''
<section class="journal-panel" id="tab-kayak">
  <div class="sport-page">
    <div class="sport-title">Каяк</div>
    <div class="sport-subtitle">Водные тренировки. Темп COROS здесь указан на 500 м, не на километр.</div>
    <div class="sport-summary">
      <div class="sport-pill"><strong>2</strong>тренировки</div>
      <div class="sport-pill"><strong>25,35 км</strong>суммарная дистанция</div>
      <div class="sport-pill"><strong>4,3</strong>макс. аэробный ТЭ</div>
    </div>
    <div class="sport-table-wrap"><table class="sport-table">
      <thead><tr><th>Дата</th><th>Дистанция</th><th>Время</th><th>Темп ср.</th><th>Лучший темп</th><th>Пульс ср./макс.</th><th>Гребки/мин</th><th>Калории</th><th>ТН</th><th>ТЭ А/Ан</th><th>Комментарий</th></tr></thead>
      <tbody>
        <tr><td>23.08.2026</td><td>4,93 км</td><td>2:19:38 активное<br>2:34:46 всего</td><td>14:10 / 500 м</td><td>9:47 / 500 м</td><td>87 / 126</td><td>10 ср. / 48 макс.</td><td>652</td><td>—</td><td>1,4 / 0,0</td><td class="note">Очень лёгкая по сердечно‑сосудистой нагрузке, но длительная механическая работа спины, плеч, предплечий и корпуса. Дистанция за гребок ~2,27 м.</td></tr>
        <tr><td>16.09.2026</td><td>20,42 км</td><td>5:56:30</td><td>8:44 / 500 м</td><td>4:34 / 500 м</td><td>115 / 159</td><td>16 ср.</td><td>2792</td><td>261</td><td>4,3 / 0,1</td><td class="note">Очень длинная аэробная работа. Главный стресс — почти 6 часов объёма и локальная выносливость верха, а не высокая скорость. При анализе обязательно учитывать текущую историю с левым локтем.</td></tr>
      </tbody>
    </table></div>
    <div class="sport-note">Важно: в каяке COROS показывает темп в мин/500 м. Например, 8:44/500 м соответствует примерно 17:28/км и ~3,44 км/ч.</div>
  </div>
</section>'''

    run_panel = '''
<section class="journal-panel" id="tab-run">
  <div class="embedded-run-wrap">
    <iframe id="run-journal-frame" class="embedded-run" src="https://urbanvdk-byte.github.io/Run/" title="Беговой дневник"></iframe>
  </div>
</section>'''

    tab_script = r'''
<script>
(function(){
  const buttons=[...document.querySelectorAll('.journal-tab')];
  const panels=[...document.querySelectorAll('.journal-panel')];
  const stats=document.querySelector('header .stats-row');
  const periodTag=document.querySelector('header .tag-green');
  function selectTab(name, pushHash){
    const valid=['strength','run','bike','kayak'];
    if(!valid.includes(name)) name='strength';
    buttons.forEach(b=>b.classList.toggle('active',b.dataset.tab===name));
    panels.forEach(p=>p.classList.toggle('active',p.id==='tab-'+name));
    if(stats) stats.style.display=name==='strength'?'flex':'none';
    if(periodTag) periodTag.style.display=name==='strength'?'inline-block':'none';
    if(pushHash) history.replaceState(null,'','#'+name);
    if(name==='run') resizeRunFrame();
  }
  function resizeRunFrame(){
    const f=document.getElementById('run-journal-frame'); if(!f) return;
    try{const d=f.contentDocument; if(d&&d.documentElement){f.style.height=Math.max(d.documentElement.scrollHeight,d.body?d.body.scrollHeight:0,900)+24+'px';}}catch(e){}
  }
  buttons.forEach(b=>b.addEventListener('click',()=>selectTab(b.dataset.tab,true)));
  const frame=document.getElementById('run-journal-frame');
  if(frame) frame.addEventListener('load',()=>{resizeRunFrame();setTimeout(resizeRunFrame,400);setTimeout(resizeRunFrame,1400)});
  selectTab(location.hash.slice(1)||'strength',false);
  window.addEventListener('resize',()=>{if(document.getElementById('tab-run')?.classList.contains('active'))resizeRunFrame()});
})();
</script>'''

    merged = '<section class="journal-panel active" id="tab-strength">' + strength_content + '</section>' + run_panel + bike_panel + kayak_panel + tab_script
    s = s[:start] + merged + s[end:]

p.write_text(s, encoding='utf-8')
