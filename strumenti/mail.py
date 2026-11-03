"""Mail del mattino EcoAI — versione "appunti" (dal 03/11/2026, richiesta di Matteo: molto più corta,
solo le notizie principali, colori giusti, il resto nell'app).
Compatibile con Gmail: tabelle, stili inline e in più gli attributi bgcolor e <font color>, che restano anche
se gli stili vengono tolti durante l'invio (successo il 02/11/2026: testo nero su sfondo nero).
Uso: python3 mail.py dati/AAAA-MM-GG.json  -> scrive mail_oggetto.txt, mail.html, mail.txt nella cartella corrente."""
import json, sys, html, pathlib, re as _re, datetime

SITO = "https://ecoai.matteo-rizza.workers.dev"
e = html.escape
C = dict(bg="#030504", card="#0B110D", ink="#F2F5F1", fog="#A9B3AC", line="#1E2A22",
         ai="#C6FF34", eco="#2BFF88", up="#2BFF88", down="#FF8A7A")
MESI = ["gennaio","febbraio","marzo","aprile","maggio","giugno","luglio","agosto","settembre","ottobre","novembre","dicembre"]
GIORNI = ["lunedì","martedì","mercoledì","giovedì","venerdì","sabato","domenica"]
FONT = "font-family:'Segoe UI',Helvetica,Arial,sans-serif;"
PER_SEZIONE = 4


def t(testo, col, extra=""):
    """Testo colorato due volte: con lo stile e con <font color> (riserva se lo stile sparisce)."""
    return f'<font color="{col}"><span style="color:{col};{extra}">{testo}</span></font>'


def notizia(n, col, giorno):
    """Titolo, il punto e il tasto che apre proprio quella notizia nell'app (/?giorno=…&n=…, come le notifiche)."""
    punto = n.get("il_punto") or n.get("livelli", {}).get("1", "")
    link = f'{SITO}/?giorno={giorno}&amp;n={e(n["id"])}' if n.get("id") else f'{SITO}/#{n["sezione"]}'
    return (f'<tr><td style="padding:10px 0;border-top:1px solid {C["line"]}">'
            f'<a href="{link}" style="text-decoration:none">{t("<b>" + e(n["titolo"]) + "</b>", C["ink"], "font-size:16px;line-height:1.35")}</a><br>'
            f'{t(e(punto), C["fog"], "font-size:14px;line-height:1.45")}'
            f'<table cellpadding="0" cellspacing="0" style="margin-top:8px"><tr><td style="border:1px solid {col};border-radius:99px">'
            f'<a href="{link}" style="display:inline-block;padding:5px 12px;text-decoration:none">{t("<b>Leggi la notizia</b>", col, "font-size:13px")}</a>'
            f'</td></tr></table></td></tr>')


def sezione(nome, items, col, giorno):
    if not items: return ""
    righe = "".join(notizia(n, col, giorno) for n in items)
    return (f'<tr><td style="padding:18px 0 4px">{t("<b>" + nome + "</b>", col, "font-size:13px;letter-spacing:.04em;text-transform:uppercase")}</td></tr>'
            + righe)


def numeri(d):
    tutte = (d.get("numeri") or {}).get("voci", [])
    voci = tutte[:5]
    btc = [v for v in tutte if "bitcoin" in str(v.get("nome", "")).lower()]
    if btc and btc[0] not in voci:  # il Bitcoin c'è sempre (scelta di Matteo del 28/10)
        voci = tutte[:4] + [btc[0]]
    if not voci: return "", ""
    pezzi, testo = [], []
    for v in voci:
        var = str(v.get("variazione") or "").strip()
        su, giu = var.startswith("+"), var[:1] in "-−–"
        vc = C["up"] if su else C["down"] if giu else C["fog"]
        fr = ("▲ " if su else "▼ " if giu else "") + var.lstrip("+-−–")
        pezzi.append(t(e(v["nome"]), C["fog"]) + " " + t("<b>" + e(v["valore"]) + "</b>", C["ink"])
                     + (" " + t(e(fr), vc) if var else ""))
        testo.append(f'{v["nome"]} {v["valore"]} {var}'.strip())
    riga = (f'<tr><td style="padding:18px 0 4px">{t("<b>I NUMERI</b>", C["fog"], "font-size:13px;letter-spacing:.04em")}</td></tr>'
            f'<tr><td style="padding:6px 0;font-size:13.5px;line-height:1.7">{" &nbsp;·&nbsp; ".join(pezzi)}</td></tr>')
    return riga, " · ".join(testo)


def build(d):
    y, m, g = map(int, d["data"].split("-"))
    dt = datetime.date(y, m, g)
    data = f"{GIORNI[dt.weekday()].capitalize()} {g} {MESI[m-1]}"
    imp = lambda x: -(x.get("importanza") or 0)
    ai = sorted([n for n in d["notizie"] if n["sezione"] == "ai"], key=imp)[:PER_SEZIONE]
    eco = sorted([n for n in d["notizie"] if n["sezione"] == "economia"], key=imp)[:PER_SEZIONE]
    top = sorted(d["notizie"], key=imp)[0]
    p = d.get("podcast") or {}
    caps = p.get("capitoli") or []
    minuti = max(1, round(sum(len((c.get("testo") or "").split()) for c in caps) / 150)) if caps else 0
    podcast = (f'<tr><td style="padding:14px 0 0"><a href="{SITO}/#podcast" style="text-decoration:none">'
               f'{t("<b>▶ Podcast di oggi · " + str(minuti) + " min</b>", C["ai"], "font-size:14px")} '
               f'{t(e(p.get("titolo", "")), C["ink"], "font-size:14px")}</a></td></tr>') if caps else ""
    num_html, num_txt = numeri(d)
    tot = len(d["notizie"])
    body = f'''<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="color-scheme" content="dark"><meta name="supported-color-schemes" content="dark"></head>
<body bgcolor="{C["bg"]}" text="{C["ink"]}" link="{C["ink"]}" style="margin:0;background-color:{C["bg"]};color:{C["ink"]}">
<table bgcolor="{C["bg"]}" width="100%" cellpadding="0" cellspacing="0" style="background-color:{C["bg"]}"><tr><td align="center" style="padding:0 0 24px;{FONT}">
<table width="100%" cellpadding="0" cellspacing="0" style="max-width:600px"><tr><td style="padding:22px 18px 0;{FONT}">
<table width="100%" cellpadding="0" cellspacing="0">
<tr><td>{t("<b>Eco</b>", C["ink"], "font-size:22px")}{t("<b>AI</b>", C["ai"], "font-size:22px")} &nbsp;{t(data, C["fog"], "font-size:14px")}</td></tr>
<tr><td style="padding-top:6px">{t(f"{tot} notizie oggi: qui gli appunti, il resto nell'app.", C["fog"], "font-size:14px")}</td></tr>
{podcast}
{sezione("Intelligenza artificiale", ai, C["ai"], d["data"])}
{sezione("Economia", eco, C["eco"], d["data"])}
{num_html}
<tr><td align="center" style="padding:22px 0 0"><table cellpadding="0" cellspacing="0"><tr><td bgcolor="{C["ai"]}" style="background-color:{C["ai"]};border-radius:99px">
<a href="{SITO}" style="display:inline-block;padding:12px 24px;text-decoration:none">{t("<b>Apri EcoAI</b>", C["bg"], "font-size:15px")}</a></td></tr></table></td></tr>
</table></td></tr></table></td></tr></table></body></html>'''
    subject = f"EcoAI · {data} · {top['titolo']}"
    righe = lambda xs: "\n".join(f"- {n['titolo']}: {n.get('il_punto') or ''}".rstrip(": ") for n in xs)
    text = (f"EcoAI, {data}\n\nIntelligenza artificiale\n{righe(ai)}\n\nEconomia\n{righe(eco)}\n\n"
            + (f"I numeri: {num_txt}\n\n" if num_txt else "") + f"Tutto nell'app: {SITO}")
    return subject, body, text


if __name__ == "__main__":
    d = json.loads(pathlib.Path(sys.argv[1]).read_text(encoding="utf-8"))
    s, h, txt = build(d)
    pathlib.Path("mail_oggetto.txt").write_text(s, encoding="utf-8")
    pathlib.Path("mail.html").write_text(h, encoding="utf-8")
    pathlib.Path("mail.txt").write_text(txt, encoding="utf-8")
    print(s, len(h), "caratteri")
