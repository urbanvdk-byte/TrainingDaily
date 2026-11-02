from pathlib import Path
import re

p = Path("index.html")
s = p.read_text(encoding="utf-8")


def replace_last_in_exercise(text, name, old, new):
    marker = f'name: "{name}",cells: ['
    start = text.find(marker)
    if start < 0:
        raise RuntimeError(f"Exercise not found: {name}")
    next_ex = text.find('},{name: "', start + len(marker))
    end = next_ex if next_ex >= 0 else text.find('}];const COMMENTS', start)
    if end < 0:
        raise RuntimeError(f"Exercise end not found: {name}")
    segment = text[start:end]
    pos = segment.rfind(old)
    if pos < 0:
        raise RuntimeError(f"Old value not found for {name}: {old}")
    segment = segment[:pos] + new + segment[pos + len(old):]
    return text[:start] + segment + text[end:]


# Correct the already existing Strength B entry for 26.10.2026.
if '"26.10"' not in s or '"29.10"' not in s:
    raise RuntimeError("Expected dates are missing")

replacements = [
    ("Жим гантелей\\nсидя (Плечи)", '{w:"22.5→22.5→20кг",r:[12,10,11]}', '{w:"22.5кг",r:[12,12,11]}'),
    ("Тяга нижнего\\nблока (к поясу)", '{w:"72.7кг",r:[12,12,12]}', '{w:"72.7кг",r:[12,12,10]}'),
    ("Тяга гантели\\nк поясу", '{w:"22.5кг",r:[12,12,12]}', '{w:"22.5кг",r:[12,12,12]}'),
    ("Обратная\\nбабочка", '{w:"58.5кг",r:[12,12,10]}', '{w:"58.5кг",r:[12,11,8]}'),
    ("Выпады вперёд\\nс гантелями", '{w:"25кг",r:[12,12]}', '{w:"25кг",r:[12,12]}'),
    ("Подъём на носки\\nв тренажёре", '{w:"40кг",r:[16,16,15]}', '{w:"40кг",r:[16,18,16]}'),
    ("Разгибание рук\\nс канатом", '{w:"59.1кг",r:[12,12,11]}', '{w:"59.1кг",r:[12,12,9]}'),
    ("Скручивания\\nна наклонной", '{w:"10кг",r:[16,14]}', 'null')
]

for name, old, new in replacements:
    if old != new:
        s = replace_last_in_exercise(s, name, old, new)

note = (
    "26.10.2026 — Силовая Б, уточнённые данные. "
    "Жим сидя 22.5 кг 12/12/11 — сильный прогресс относительно 21.10 (12/10/6): вес почти закрыт, но до 3×12 не повышать. "
    "Нижний блок 72.7 кг 12/12/10 — улучшение относительно 21.10 (12/11/10), но верхняя граница ещё не закрыта; следующий ориентир 12/12/11+, вес удержать. "
    "Тяга гантели 22.5 кг 12/12/12 — полностью закрыта; из-за того, что упражнение не нравится, не повышать, а заменить со следующей Б. "
    "Обратная бабочка 58.5 кг 12/11/8 после 54 кг 3×12 — нормальный переход на новую ступень, но третий подход просел до нижней границы; вес удержать. "
    "Выпады 25 кг 12/12 на каждую ногу — стабильное закрепление; дальше пока не повышать из-за беговой нагрузки. "
    "Икры 40 кг 16/18/16 — высокий объём на новом рабочем весе; повышение не нужно, приоритет амплитуда и медленное опускание. "
    "Канат 59.1 кг 12/12/9 — небольшая просадка третьего подхода; вес оставить. "
    "Скручивания пропущены из-за нехватки времени; нулевые подходы не считать выполненными. "
    "Общий вывод: лучший прогресс дня — жим плеч; нижний блок улучшился, но к повышению ещё не готов. Следующую Б сделать закрепляющей."
)

escaped = note.replace("\\", "\\\\").replace('"', '\\"')
pattern = r'76: "(?:\\.|[^"])*",77: "'
replacement = f'76: "{escaped}",77: "'
s, n = re.subn(pattern, replacement, s, count=1)
if n != 1:
    raise RuntimeError("Comment 76 replacement failed")

checks = [
    '{w:"22.5кг",r:[12,12,11]}',
    '{w:"72.7кг",r:[12,12,10]}',
    '{w:"58.5кг",r:[12,11,8]}',
    '{w:"40кг",r:[16,18,16]}',
    '26.10.2026 — Силовая Б, уточнённые данные.'
]
for check in checks:
    if check not in s:
        raise RuntimeError(f"Validation failed: {check}")

p.write_text(s, encoding="utf-8")
