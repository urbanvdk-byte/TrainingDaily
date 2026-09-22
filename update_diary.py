from pathlib import Path

p = Path('index.html')
s = p.read_text(encoding='utf-8')

run_start = s.find('<section class="journal-panel" id="tab-run">')
bike_start = s.find('<section class="journal-panel" id="tab-bike">')
if run_start < 0 or bike_start < 0 or bike_start <= run_start:
    raise RuntimeError('Journal panels not found')

desired = '''<section class="journal-panel" id="tab-run">
  <div class="embedded-run-wrap">
    <iframe id="run-journal-frame" class="embedded-run" src="run.html" title="Беговой дневник"></iframe>
  </div>
</section>
'''

current = s[run_start:bike_start]
if current != desired:
    s = s[:run_start] + desired + s[bike_start:]

p.write_text(s, encoding='utf-8')
