"""Unisce i file della ricerca nel file del giorno e aggiorna indice.json.
Uso: python3 unisci.py RICERCA_DIR DATI_DIR AAAA-MM-GG "etichetta generato" """
import json, sys, pathlib, re
src, out, day, gen = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2]), sys.argv[3], sys.argv[4]
def load(n, d=None):
    p = src / n
    return json.loads(p.read_text(encoding="utf-8")) if p.exists() else d
notizie = (load("ai.json", []) or []) + (load("economia.json", []) or [])
errs = []
for n in notizie:
    for k in ("id", "sezione", "titolo", "fonte", "url", "livelli"):
        if not n.get(k): errs.append(f"{n.get('id')}: manca {k}")
    for l in ("1", "4", "7", "10"):
        if not (n.get("livelli") or {}).get(l): errs.append(f"{n.get('id')}: manca livello {l}")
    if not re.match(r"^https?://", n.get("url", "")): errs.append(f"{n.get('id')}: url non valido")
    for l in ("1", "4", "7", "10"):
        if not ((n.get("en") or {}).get("livelli") or {}).get(l): errs.append(f"{n.get('id')}: manca inglese livello {l}")
    if not n.get("il_punto"): errs.append(f"{n.get('id')}: manca il_punto")
    if len(n.get("termini") or []) < 3: errs.append(f"{n.get('id')}: pochi termini spiegati")
    l4 = (n.get("livelli") or {}).get("4", "")
    if len(l4.split()) < 220: errs.append(f"{n.get('id')}: livello 4 troppo corto ({len(l4.split())} parole, servono 250-350)")
    for lab in ("Cosa è successo:", "Perché:", "Cosa cambia:", "Un esempio:"):
        if lab not in l4: errs.append(f"{n.get('id')}: livello 4 senza '{lab}'")
ids = [n["id"] for n in notizie]
if len(ids) != len(set(ids)): errs.append("id duplicati")
doc = {"data": day, "generato": gen, "notizie": notizie,
       "numeri": load("numeri.json", {"voci": []}), "aziende": load("aziende.json", {"voci": []}), "voci": load("voci.json", {"voci": []})}
out.mkdir(parents=True, exist_ok=True)
(out / f"{day}.json").write_text(json.dumps(doc, ensure_ascii=False, indent=1), encoding="utf-8")
ip = out / "indice.json"
idx = json.loads(ip.read_text(encoding="utf-8")) if ip.exists() else {"giorni": []}
idx["giorni"] = sorted(set(idx["giorni"]) | {day}, reverse=True)
idx["ultimo"] = idx["giorni"][0]
ip.write_text(json.dumps(idx, ensure_ascii=False, indent=1), encoding="utf-8")
print(f"{len(notizie)} notizie ({sum(n['sezione']=='ai' for n in notizie)} AI)"); print("\n".join(errs) or "nessun errore")
