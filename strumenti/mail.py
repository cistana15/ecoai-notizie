"""Mail del mattino EcoAI (HTML compatibile con Gmail: tabelle e stili inline, tema scuro come l'app, dal 30/10/2026).
Uso: python3 mail.py dati/AAAA-MM-GG.json  -> scrive mail_oggetto.txt, mail.html, mail.txt nella cartella corrente."""
import json, sys, html, pathlib, re as _re

SITO = "https://ecoai.matteo-rizza.workers.dev"
e = html.escape
F = "font-family:'Segoe UI',Helvetica,Arial,sans-serif;"
S = "font-family:Georgia,'Times New Roman',serif;"
# colori dell'app: fondo nero, superfici verde scurissimo, lime = AI, verde = Economia
C = dict(bg="#030504", card="#0B110D", s2="#131C16", ink="#F2F5F1", fog="#A9B3AC", line="#1E2A22",
         ai="#C6FF34", aisoft="#1F2A0A", eco="#2BFF88", ecosoft="#0E2A1B", up="#2BFF88", down="#FF8A7A")
MESI = ["gennaio","febbraio","marzo","aprile","maggio","giugno","luglio","agosto","settembre","ottobre","novembre","dicembre"]
GIORNI = ["lunedì","martedì","mercoledì","giovedì","venerdì","sabato","domenica"]


def gmail_safe(h):
    """Gmail (invio dalle attività di Claude) toglie la proprietà abbreviata `background:` dagli stili:
    lo sfondo sparisce e il testo chiaro resta su bianco. Qui si usa `background-color:` e in più l'attributo
    `bgcolor` su tabelle e celle, che Gmail conserva (verificato il 30/10/2026 con una mail di prova)."""
    h = _re.sub(r'(?<![-\w])background\s*:', 'background-color:', h)
    def add(m):
        tag, attrs = m.group(1), m.group(2)
        if 'bgcolor=' in attrs: return m.group(0)
        c = _re.search(r'background-color:\s*(#[0-9A-Fa-f]{3,8})', attrs)
        return f'<{tag} bgcolor="{c.group(1)}"{attrs}>' if c else m.group(0)
    return _re.sub(r'<(table|td|body)(\s[^>]*)>', add, h)

def colori(n):
    return (C["ai"], C["aisoft"]) if n["sezione"] == "ai" else (C["eco"], C["ecosoft"])

def punto(n):
    p = n.get("il_punto")
    if not p: return ""
    col, _ = colori(n)
    return (f'<table width="100%" cellpadding="0" cellspacing="0" style="background:{C["s2"]};border-radius:12px;margin:0 0 14px"><tr>'
            f'<td width="4" style="background:{col};border-radius:12px 0 0 12px;font-size:0">&nbsp;</td>'
            f'<td style="padding:11px 14px;{F}font-size:15px;line-height:1.5;color:{C["ink"]}"><b style="color:{col}">Il punto</b><br>{e(p)}</td></tr></table>')

def en_block(n):
    t = ((n.get("en") or {}).get("livelli") or {}).get("1")
    if not t: return ""
    return (f'<div style="border-top:1px solid {C["line"]};margin-top:12px;padding-top:10px">'
            f'<div style="{F}font-size:12.5px;font-weight:700;color:{C["fog"]}">In inglese</div>'
            f'<div style="{S}font-size:14.5px;line-height:1.5;color:{C["fog"]};font-style:italic;margin-top:3px">{e(t)}</div></div>')

PARTI = ("Cosa è successo", "Perché", "Cosa cambia")

def parti_testo(n):
    """Le parti della notizia (livello 4) senza "Un esempio": l'esempio resta solo nell'app.
    Se il livello 4 non ha le etichette, usa il livello 1."""
    out = []
    for par in (n.get("livelli", {}).get("4") or "").split("\n\n"):
        et, sep, testo = par.partition(": ")
        if sep and et.strip() in PARTI and testo.strip():
            out.append((et.strip(), testo.strip()))
    return out

def parti(n):
    ps = parti_testo(n)
    if not ps:
        return f'<div style="{S}font-size:15.5px;line-height:1.6;color:{C["ink"]}">{e(n["livelli"]["1"])}</div>'
    col, _ = colori(n)
    return "".join(f'<div style="margin:0 0 12px"><div style="{F}font-size:13px;font-weight:700;color:{col}">{e(et)}</div>'
                   f'<div style="{S}font-size:15.5px;line-height:1.6;color:{C["ink"]};margin-top:2px">{e(t)}</div></div>' for et, t in ps)

def item(n):
    col, soft = colori(n)
    tag = (f'<span style="{F}display:inline-block;background:{soft};color:{col};font-size:12px;font-weight:700;border-radius:99px;padding:3px 10px">{e(n["tag"])}</span>&nbsp; '
           if n.get("tag") else "")
    return f'''<tr><td style="padding:0 0 12px"><table width="100%" cellpadding="0" cellspacing="0" style="background:{C["card"]};border:1px solid {C["line"]};border-radius:18px">
<tr><td style="padding:18px 18px 16px">
<div>{tag}<span style="{F}font-size:12.5px;color:{C["fog"]}">{e(n["fonte"])}</span></div>
<div style="{F}font-size:19px;line-height:1.28;font-weight:800;color:{C["ink"]};margin:10px 0 12px">{e(n["titolo"])}</div>
{punto(n)}{parti(n)}
{en_block(n)}
<table cellpadding="0" cellspacing="0" style="margin-top:12px"><tr>
<td style="border:1px solid {col};border-radius:99px"><a href="{SITO}/#{n["sezione"]}" style="display:inline-block;padding:8px 14px;{F}font-size:13.5px;font-weight:700;color:{col};text-decoration:none">Approfondisci su EcoAI</a></td>
<td style="padding-left:14px"><a href="{e(n["url"])}" style="{F}font-size:13.5px;color:{C["fog"]};text-decoration:underline">Articolo originale</a></td>
</tr></table>
</td></tr></table></td></tr>'''

def titolo(t, col, nota=""):
    n = f'<span style="{F}font-size:14px;font-weight:400;color:{C["fog"]}">&nbsp; {e(nota)}</span>' if nota else ""
    return (f'<tr><td style="padding:22px 0 12px"><table cellpadding="0" cellspacing="0"><tr>'
            f'<td width="5" style="background:{col};border-radius:3px;font-size:0">&nbsp;</td>'
            f'<td style="padding-left:10px;{F}font-size:21px;font-weight:800;color:{C["ink"]}">{t}{n}</td></tr></table></td></tr>')

def section(title, items, col):
    if not items: return ""
    return titolo(title, col, f"{len(items)} " + ("notizia" if len(items) == 1 else "notizie")) + "".join(item(n) for n in items)

def numbers(d):
    tutte = (d.get("numeri") or {}).get("voci", [])
    voci = tutte[:6]
    # il Bitcoin c'è sempre nella mail, anche se nell'elenco viene dopo i primi 6
    btc = [v for v in tutte if "bitcoin" in str(v.get("nome", "")).lower()]
    if btc and btc[0] not in voci:
        voci = tutte[:5] + [btc[0]]
    if not voci: return ""
    cells, row = "", []
    for i, v in enumerate(voci):
        var = str(v.get("variazione") or "").strip()
        su, giu = var.startswith("+"), var[:1] in "-−–"
        vc = C["up"] if su else C["down"] if giu else C["fog"]
        freccia = "▲ " if su else "▼ " if giu else ""
        row.append(f'<td width="33%" valign="top" style="background:{C["s2"]};border-radius:12px;padding:10px 11px;{F}">'
                   f'<div style="font-size:12px;color:{C["fog"]};font-weight:600">{e(v["nome"])}</div>'
                   f'<div style="font-size:15.5px;line-height:1.25;font-weight:800;color:{C["ink"]};margin-top:3px">{e(v["valore"])}</div>'
                   + (f'<div style="font-size:13px;font-weight:700;color:{vc};margin-top:3px">{freccia}{e(var.lstrip("+-−–"))}</div>' if var else "")
                   + '</td>')
        if len(row) == 3 or i == len(voci) - 1:
            while len(row) < 3: row.append('<td width="33%">&nbsp;</td>')
            cells += '<tr>' + '<td width="8" style="font-size:0">&nbsp;</td>'.join(row) + '</tr><tr><td colspan="5" height="8" style="font-size:0;line-height:0">&nbsp;</td></tr>'
            row = []
    return (titolo("I numeri", C["ink"], (d["numeri"].get("aggiornato") or ""))
            + f'<tr><td><table width="100%" cellpadding="0" cellspacing="0">{cells}</table></td></tr>')

def podcast(d):
    p = d.get("podcast") or {}
    caps = p.get("capitoli") or []
    if not caps: return ""
    w = sum(len((c.get("testo") or "").split()) for c in caps)
    return (f'<tr><td style="padding:16px 0 0"><a href="{SITO}/#podcast" style="text-decoration:none">'
            f'<table width="100%" cellpadding="0" cellspacing="0" style="background:{C["card"]};border:1px solid {C["line"]};border-radius:18px"><tr>'
            f'<td width="64" valign="middle" style="padding:16px 0 16px 16px"><table cellpadding="0" cellspacing="0"><tr><td width="48" height="48" align="center" valign="middle" '
            f'style="background:{C["ai"]};border-radius:24px;{F}font-size:18px;color:{C["bg"]}">▶</td></tr></table></td>'
            f'<td valign="middle" style="padding:14px 16px 14px 4px;{F}">'
            f'<div style="font-size:12.5px;font-weight:700;color:{C["ai"]}">Il podcast di oggi · {max(1, round(w/150))} min</div>'
            f'<div style="font-size:17px;line-height:1.3;font-weight:800;color:{C["ink"]};margin-top:3px">{e(p.get("titolo",""))}</div>'
            f'<div style="font-size:13px;line-height:1.45;color:{C["fog"]};margin-top:4px">{e(" · ".join(c["titolo"] for c in caps[:5]))}</div>'
            f'</td></tr></table></a></td></tr>')

def attualita(d):
    v = (d.get("attualita") or {}).get("voci") or []
    if not v: return ""
    rows = "".join(f'<tr><td style="padding:12px 0;{"border-top:1px solid "+C["line"]+";" if i else ""}{F}font-size:14px;line-height:1.45;color:{C["ink"]}">'
                   + (f'<span style="display:inline-block;background:{C["s2"]};color:{C["fog"]};font-size:12px;font-weight:700;border-radius:99px;padding:2px 9px">{e(x["categoria"])}</span><br>' if x.get("categoria") else "")
                   + f'<a href="{e(x.get("url",""))}" style="color:{C["ink"]};text-decoration:none"><b style="font-size:15px">{e(x["titolo"])}</b></a><br>'
                   f'<span style="color:{C["fog"]}">{e(x.get("in_breve",""))}</span></td></tr>' for i, x in enumerate(v))
    return (titolo("Di cosa si parla oggi", C["fog"])
            + f'<tr><td><table width="100%" cellpadding="0" cellspacing="0" style="background:{C["card"]};border:1px solid {C["line"]};border-radius:18px"><tr><td style="padding:4px 16px">'
            f'<table width="100%" cellpadding="0" cellspacing="0">{rows}</table></td></tr></table></td></tr>')

def verifica(d):
    v = d.get("verifica") or {}
    if not v.get("controllati"): return ""
    return f' Verifica dei fatti: {v["controllati"]} controllati, {v.get("corretti", 0)} corretti, {v.get("rimossi", 0)} rimossi.'

def build(d):
    y, m, g = map(int, d["data"].split("-"))
    import datetime
    dt = datetime.date(y, m, g)
    data = f"{GIORNI[dt.weekday()].capitalize()} {g} {MESI[m-1]}"
    imp = lambda x: -(x.get("importanza") or 0)
    ai = sorted([n for n in d["notizie"] if n["sezione"] == "ai"], key=imp)[:5]
    eco = sorted([n for n in d["notizie"] if n["sezione"] == "economia"], key=imp)[:5]
    top = sorted(d["notizie"], key=imp)[0]
    body = f'''<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="color-scheme" content="dark"><meta name="supported-color-schemes" content="dark"></head>
<body style="margin:0;background:{C["bg"]}"><table width="100%" cellpadding="0" cellspacing="0" style="background:{C["bg"]}"><tr><td align="center" style="padding:0 0 28px">
<table width="100%" cellpadding="0" cellspacing="0" style="max-width:600px">
<tr><td style="padding:26px 18px 6px">
<table cellpadding="0" cellspacing="0"><tr>
<td valign="middle"><img src="{SITO}/icon-96.png" width="36" height="36" alt="" style="display:block;border-radius:10px"></td>
<td valign="middle" style="padding-left:10px;{F}font-size:24px;font-weight:800;line-height:1"><span style="color:{C["ink"]}">Eco</span><span style="color:{C["ai"]}">AI</span></td>
</tr></table>
<div style="{F}font-size:14px;font-weight:600;color:{C["fog"]};margin-top:18px">{data}</div>
<div style="{F}font-size:27px;line-height:1.18;font-weight:800;color:{C["ink"]};margin-top:4px">{e(top["titolo"])}</div>
<div style="{F}font-size:14.5px;line-height:1.5;color:{C["fog"]};margin-top:8px">{len(d["notizie"])} {"notizia" if len(d["notizie"]) == 1 else "notizie"} di AI ed economia: qui le più importanti, spiegate semplici. Nell'app scegli tu quanto approfondire.</div>
</td></tr>
<tr><td style="padding:0 12px"><table width="100%" cellpadding="0" cellspacing="0">
{podcast(d)}
{section("Intelligenza artificiale", ai, C["ai"])}
{section("Economia", eco, C["eco"])}
{numbers(d)}
{attualita(d)}
<tr><td align="center" style="padding:24px 0 0"><table cellpadding="0" cellspacing="0"><tr><td style="background:{C["ai"]};border-radius:99px">
<a href="{SITO}" style="display:inline-block;padding:14px 26px;{F}font-size:15px;font-weight:800;color:{C["bg"]};text-decoration:none">Apri EcoAI: tutte le notizie, livelli 1-10</a></td></tr></table>
<div style="{F}font-size:12px;line-height:1.5;color:{C["fog"]};margin-top:12px;padding:0 12px">Ogni notizia ha il link alla fonte originale.{verifica(d)}</div></td></tr>
</table></td></tr></table></td></tr></table></body></html>'''
    subject = f"EcoAI · {data} · {top['titolo']}"
    text = f"EcoAI, {data}\n\n" + "\n\n".join(f"{n['titolo']}\n" + ("\n".join(f"{et}: {t}" for et, t in parti_testo(n)) or n['livelli']['1']) + f"\n{n['url']}" for n in ai + eco) + f"\n\nTutte le notizie: {SITO}"
    return subject, gmail_safe(body), text

if __name__ == "__main__":
    d = json.loads(pathlib.Path(sys.argv[1]).read_text(encoding="utf-8"))
    s, h, t = build(d)
    pathlib.Path("mail_oggetto.txt").write_text(s, encoding="utf-8")
    pathlib.Path("mail.html").write_text(h, encoding="utf-8")
    pathlib.Path("mail.txt").write_text(t, encoding="utf-8")
    print(s, len(h))
