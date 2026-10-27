"""Write one compact HTML file per week (same content as the Word docs) for Google Docs upload."""
import json, sys, html, datetime as dt
weeks = json.load(open(sys.argv[1], encoding="utf-8"))
M = "Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec".split()
f = lambda iso: (lambda d: f"{d.day} {M[d.month-1]}")(dt.date.fromisoformat(iso))
e = html.escape
for ws, items in sorted(weeks.items()):
    we = (dt.date.fromisoformat(ws) + dt.timedelta(days=6)).isoformat()
    o = [f"<h1>Reel scripts: {f(ws)} – {f(we)} 2026</h1><p><i>@ron_tamil · 7 reels · English drafts. Say them your way in Tamil/Thanglish. Plain text is spoken; [grey italics] are edit directions; CHECK lines must be confirmed before filming.</i></p>",
         "<table border=1 cellpadding=4><tr><th>Day</th><th>ID</th><th>Format</th><th>Topic</th><th>Length</th><th>Link test</th></tr>"]
    for it in items:
        o.append(f"<tr><td>{it['day']} {f(it['date'])}</td><td>{it['id']}</td><td>{it['format']}</td><td>{e(it['topic'])}</td><td>~{it['secs']} s</td><td>{it['link'][0] if it['link'] else '–'}</td></tr>")
    o.append("</table>")
    for it in items:
        o.append(f"<h2>{it['id']} · {it['day']} {f(it['date'])} · {it['format']}: {e(it['topic'])}</h2>")
        o.append(f"<p><b>Type:</b> {e(it['type'])} · <b>Goal:</b> {it['goal']} · <b>Length:</b> ~{it['secs']} s ({it['words']} words)<br><b>Source:</b> {e(it['source'])} <a href=\"{it['url']}\">{it['url']}</a>" + (f" · also <a href=\"{it['url2']}\">{it['url2']}</a>" if it['url2'] else "") + "</p>")
        if it["link"]:
            o.append(f"<p><b>Link test:</b> Comment \"{it['link'][0]}\" → DM the doc: {e(it['link'][1])}</p>")
        for s in it["sections"]:
            o.append(f"<h3>{s['time']} · {s['label']}{' · FAST: cut every 1–2 s' if s['fast'] else ''}</h3>")
            for typ, t in s["lines"]:
                o.append(f"<p>{e(t)}</p>" if typ == "S" else f"<p><i><font color=\"#6b6b6b\">[{e(t)}]</font></i></p>")
    open(f"{sys.argv[2]}/week_{ws}.html", "w", encoding="utf-8").write("".join(o))
    print(ws, len("".join(o)))
