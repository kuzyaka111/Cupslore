from pathlib import Path
import json

root=Path(__file__).resolve().parents[1]
data=json.loads((root/'data/content.json').read_text())
(root/'data/content.js').write_text('window.CUPS = '+json.dumps(data,ensure_ascii=False).replace('</','<\\/')+';\n')
