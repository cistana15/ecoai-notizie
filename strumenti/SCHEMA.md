# Schema notizie EcoAI (JSON, UTF-8, italiano)

Ogni notizia:
{
  "id": "ai-01",                       // ai-01..ai-10 / eco-01..eco-10
  "sezione": "ai" | "economia",
  "tag": "Modelli" ,                   // breve categoria (es. Modelli, Chip, Regole, Big Tech, Startup, Ricerca | Mercati, Banche centrali, Inflazione, Lavoro, Energia, Aziende, Italia, Europa, Cripto)
  "titolo": "...",                      // titolo chiaro in italiano, max ~90 caratteri, niente clickbait
  "sottotitolo": "...",                 // 1 frase
  "fonte": "Reuters",                   // testata della fonte principale
  "url": "https://...",                 // link all'articolo originale (verificato che esiste)
  "data": "2026-10-23",                 // data di pubblicazione della fonte
  "importanza": 1-5,                    // 5 = notizia del giorno
  "livelli": {
    "1":  "...",  // come a un ragazzo di 12 anni: 2-4 frasi, parole semplici, un esempio concreto/paragone di vita quotidiana
    "4":  "...",  // lettore curioso: 1 paragrafo (~80-120 parole), chi/cosa/quando/perché, termini tecnici spiegati tra parentesi
    "7":  "...",  // lettore informato: 2-3 paragrafi (~200 parole), contesto, numeri, conseguenze per mercati/aziende/persone
    "10": "..."   // esperto: 4-6 paragrafi (~400 parole), dettagli tecnici/finanziari, contesto storico, rischi e scenari, punti ancora incerti. Paragrafi separati da \n\n
  },
  "perche_conta": "...",                // 1 frase: perché dovrebbe interessarmi
  "numeri": [ {"label": "Investimento", "valore": "40 mld $"} ],   // 0-3 numeri chiave, SOLO se presenti nelle fonti
  "chi": [ {"nome": "Nvidia", "tipo": "azienda"|"persona"|"istituzione", "url": "https://..."} ], // 1-4 attori con link (sito ufficiale, Wikipedia o profilo LinkedIn pubblico)
  "approfondimenti": [ {"titolo": "...", "url": "https://..."} ]  // 1-3 link extra (altre fonti, comunicato ufficiale, paper)
}

REGOLE FERREE
- Solo fatti presenti nelle fonti che hai letto. Nessun numero, data, nome o citazione inventati. Se un dato non è certo, non metterlo.
- I livelli 1/4/7/10 raccontano la STESSA notizia con profondità diversa; il 10 può aggiungere contesto generale noto e stabile, ma ogni fatto specifico deve venire dalle fonti.
- Italiano semplice e corretto. Livello 1 senza gergo.
- Notizie delle ultime 24-48 ore (oggi è sabato 24 ottobre 2026; vanno bene notizie del 22-23 ottobre 2026, eccezionalmente fino al 20 se molto importanti).
- url deve essere la pagina dell'articolo, non la home della testata.

# Altri file della ricerca (stessa cartella)
numeri.json  -> {"aggiornato":"chiusura di <giorno>", "voci":[{"nome","valore","variazione","nota","fonte","url"}]}
   Voci: FTSE MIB, Euro Stoxx 50, S&P 500, Nasdaq Composite, euro/dollaro, Brent, oro, Bitcoin, spread BTP-Bund, BTP 10 anni. Solo valori verificati con link; meglio ometterli che sbagliare.
aziende.json -> {"titolo":"...","voci":[{"nome","settore":"AI"|"Economia","cosa_succede","numero","url_notizia","sito","linkedin"}]}  6-8 aziende, linkedin solo se la pagina è stata aperta e verificata, altrimenti "".
voci.json    -> {"voci":[{"autore","ruolo","tipo","titolo","sintesi","perche_leggerlo","url","data","profilo"}]}  4-6 opinioni/riflessioni pubbliche (post LinkedIn pubblici, blog, newsletter, editoriali) degli ultimi 10 giorni; nessuna citazione non copiata dalla pagina.
