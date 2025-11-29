import json
from datetime import datetime

IN_JSON = "analysis_output.json"
OUT_HTML = "report.html"

print("Loading analysis_output.json...")
data = json.load(open(IN_JSON, encoding="utf-8"))
words = data.get("word_analysis", [])

html_header = """
<!DOCTYPE html>
<html>
<head>
<title>Speech Analysis Report</title>
<style>
body { font-family: Arial; margin: 20px; }
table { border-collapse: collapse; width: 100%; margin-top: 20px; }
th, td { border: 1px solid #aaa; padding: 8px; text-align: left; }
th { background: #111; color: white; }
tr:nth-child(even) { background: #f2f2f2; }
.score-good { color: green; font-weight: bold; }
.score-bad { color: red; font-weight: bold; }
</style>
</head>
<body>
<h1>Speech Analysis Report</h1>
<p>Generated: """ + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + """</p>
"""

html_table = """
<table>
<tr>
<th>Word</th>
<th>Start</th>
<th>End</th>
<th>Energy</th>
<th>F0 (Hz)</th>
<th>Pronunciation</th>
<th>Fluency</th>
<th>Tension</th>
<th>Breathiness</th>
<th>Emphasis</th>
</tr>
"""

for w in words:
    def cls(val): 
        return "score-good" if val >= 0.7 else "score-bad"

    html_table += f"""
<tr>
<td>{w['word']}</td>
<td>{w['start']}</td>
<td>{w['end']}</td>
<td>{w['energy']:.4f}</td>
<td>{w['f0_median']}</td>
<td class="{cls(w['pronunciation_score'])}">{w['pronunciation_score']}</td>
<td class="{cls(w['fluency_score'])}">{w['fluency_score']}</td>
<td class="{cls(w['tension_score'])}">{w['tension_score']}</td>
<td class="{cls(w['breathiness_score'])}">{w['breathiness_score']}</td>
<td>{w['emphasis_score']}</td>
</tr>
"""

html_footer = """
</table>
</body>
</html>
"""

html = html_header + html_table + html_footer

with open(OUT_HTML, "w", encoding="utf-8") as f:
    f.write(html)

print(f"Report generated: {OUT_HTML}")
