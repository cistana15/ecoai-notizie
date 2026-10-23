"""Mail del mattino EcoAI (HTML compatibile con Gmail: tabelle e stili inline).
Uso: python3 mail.py dati/AAAA-MM-GG.json  -> scrive mail_oggetto.txt, mail.html, mail.txt nella cartella corrente."""
import json, sys, html, pathlib

SITO = "https://ecoai.matteo-rizza.workers.dev"
e = html.escape
F = "font-family:'Segoe UI',Helvetica,Arial,sans-serif;"
S = "font-family:Georgia,'Times New Roman',serif;"
C = dict(bg="#EDF1F6", card="#FFFFFF", ink="#14213D", fog="#4A5672", line="#CDD6E3", ai="#5B4FD6", aisoft="#E6E3FB",
         eco="#0B7F62", ecosoft="#D9F0E8", amber="#F2B33D", up="#0B7F62", down="#C2413A")
MESI = ["gennaio","febbraio","marzo","aprile","maggio","giugno","luglio","agosto","settembre","ottobre","novembre","dicembre"]
GIORNI = ["lunedì","martedì","mercoledì","giovedì","venerdì","sabato","domenica"]

def en_block(n):
    t = ((n.get("en") or {}).get("livelli") or {}).get("1")
    if not t: return ""
    return (f'<div style="{F}font-size:11.5px;font-weight:800;color:{C["fog"]};margin-top:10px">IN ENGLISH</div>'
            f'<div style="{S}font-size:14.5px;line-height:1.5;color:{C["fog"]};font-style:italic">{e(t)}</div>')

def item(n):
    ai = n["sezione"] == "ai"
    col, soft = (C["ai"], C["aisoft"]) if ai else (C["eco"], C["ecosoft"])
    return f'''<tr><td style="padding:0 0 12px"><table width="100%" cellpadding="0" cellspacing="0" style="background:{C["card"]};border:1px solid {C["line"]};border-radius:16px">
<tr><td style="padding:16px 18px">
<span style="{F}display:inline-block;background:{soft};color:{col};font-size:12px;font-weight:700;border-radius:99px;padding:2px 9px">{e(n.get("tag",""))}</span>
<span style="{F}font-size:12.5px;color:{C["fog"]}">&nbsp;{e(n["fonte"])}</span>
<div style="{F}font-size:18px;line-height:1.25;font-weight:800;color:{C["ink"]};margin:8px 0 6px">{e(n["titolo"])}</div>
<div style="{S}font-size:15.5px;line-height:1.55;color:{C["ink"]}">{e(n["livelli"]["1"])}</div>
{en_block(n)}
<div style="{F}font-size:13.5px;margin-top:10px"><a href="{SITO}/#{n["sezione"]}" style="color:{col};font-weight:700;text-decoration:none">Approfondisci su EcoAI</a>
&nbsp;&nbsp;<a href="{e(n["url"])}" style="color:{C["fog"]};text-decoration:underline">Articolo originale</a></div>
</td></tr></table></td></tr>'''

def section(title, items):
    if not items: return ""
    return f'<tr><td style="padding:18px 0 10px;{F}font-size:21px;font-weight:800;color:{C["ink"]}">{title}</td></tr>' + "".join(item(n) for n in items)

def numbers(d):
    voci = (d.get("numeri") or {}).get("voci", [])[:6]
    if not voci: return ""
    cells = ""
    for i, v in enumerate(voci):
        var = str(v.get("variazione") or "")
        vc = C["up"] if var.strip().startswith("+") else C["down"] if var.strip()[:1] in "-−–" else C["fog"]
        cells += (f'<td width="33%" valign="top" style="padding:8px;{F}"><div style="font-size:12px;color:{C["fog"]};font-weight:600">{e(v["nome"])}</div>'
                  f'<div style="font-size:16px;font-weight:800;color:{C["ink"]}">{e(v["valore"])}</div><div style="font-size:13px;font-weight:700;color:{vc}">{e(var)}</div></td>')
        if i % 3 == 2 and i < len(voci) - 1: cells += "</tr><tr>"
    return (f'<tr><td style="padding:18px 0 10px;{F}font-size:21px;font-weight:800;color:{C["ink"]}">I numeri</td></tr>'
            f'<tr><td><table width="100%" cellpadding="0" cellspacing="0" style="background:{C["card"]};border:1px solid {C["line"]};border-radius:16px"><tr>{cells}</tr></table>'
            f'<div style="{F}font-size:12px;color:{C["fog"]};margin-top:6px">{e(d["numeri"].get("aggiornato",""))}</div></td></tr>')

def build(d):
    y, m, g = map(int, d["data"].split("-"))
    import datetime
    dt = datetime.date(y, m, g)
    data = f"{GIORNI[dt.weekday()].capitalize()} {g} {MESI[m-1]}"
    imp = lambda x: -(x.get("importanza") or 0)
    ai = sorted([n for n in d["notizie"] if n["sezione"] == "ai"], key=imp)[:5]
    eco = sorted([n for n in d["notizie"] if n["sezione"] == "economia"], key=imp)[:5]
    top = sorted(d["notizie"], key=imp)[0]
    body = f'''<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"></head>
<body style="margin:0;background:{C["bg"]}"><table width="100%" cellpadding="0" cellspacing="0" style="background:{C["bg"]}"><tr><td align="center" style="padding:0 0 28px">
<table width="100%" cellpadding="0" cellspacing="0" style="max-width:600px">
<tr><td style="background:{C["ink"]};padding:26px 22px;border-radius:0 0 22px 22px">
<div style="{F}font-size:30px;font-weight:800;line-height:1"><span style="color:#3FCF9F">Eco</span><span style="color:#9D94FF">AI</span></div>
<div style="{F}font-size:15px;color:#C9D2E6;margin-top:8px">{data}: {len(d["notizie"])} notizie di AI ed economia. Qui le più importanti, spiegate semplici. Nell'app scegli tu quanto approfondire.</div>
</td></tr>
<tr><td style="padding:8px 14px 0"><table width="100%" cellpadding="0" cellspacing="0">
{section("Intelligenza artificiale", ai)}
{section("Economia", eco)}
{numbers(d)}
<tr><td align="center" style="padding:22px 0 0"><table cellpadding="0" cellspacing="0"><tr><td style="background:{C["ink"]};border-radius:99px">
<a href="{SITO}" style="display:inline-block;padding:14px 26px;{F}font-size:15px;font-weight:800;color:#fff;text-decoration:none">Apri EcoAI: tutte le notizie, livelli 1-10</a></td></tr></table>
<div style="{F}font-size:12px;color:{C["fog"]};margin-top:12px">Ogni notizia ha il link alla fonte originale.</div></td></tr>
</table></td></tr></table></td></tr></table></body></html>'''
    subject = f"EcoAI · {data} · {top['titolo']}"
    text = f"EcoAI, {data}\n\n" + "\n\n".join(f"{n['titolo']}\n{n['livelli']['1']}\n{n['url']}" for n in ai + eco) + f"\n\nTutte le notizie: {SITO}"
    return subject, body, text

if __name__ == "__main__":
    d = json.loads(pathlib.Path(sys.argv[1]).read_text(encoding="utf-8"))
    s, h, t = build(d)
    pathlib.Path("mail_oggetto.txt").write_text(s, encoding="utf-8")
    pathlib.Path("mail.html").write_text(h, encoding="utf-8")
    pathlib.Path("mail.txt").write_text(t, encoding="utf-8")
    print(s, len(h))
