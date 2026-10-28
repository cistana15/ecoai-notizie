# Schema notizie EcoAI v2 (JSON, UTF-8)

Lettore: Matteo, 25 anni, Milano, lavora nella compliance finanziaria. Intelligente ma NON esperto di finanza o tecnologia: sigle e gergo lo bloccano. Vuole capire IL PUNTO: cosa è successo, perché, cosa cambia, con esempi.

## Stile di scrittura (deciso da Matteo il 28/10/2026, vale per italiano e inglese)
Modello: gli articoli di Medium (Daily Digest) e in particolare quelli di Alessandro Villani (medium.com/@alessandrovillani0000, es. "Identity is the new money"). Prendere il METODO, mai copiare frasi o contenuti.
- Frasi brevi: una idea per frase, di solito sotto le 20 parole. Paragrafi di 2-4 frasi.
- Apri con qualcosa che il lettore conosce dalla vita di tutti i giorni, poi la svolta ("Ma la realtà è diversa." / "The reality is different.").
- Ogni tanto una frase da sola, secca, che fissa il concetto chiave (massimo 1-2 per notizia).
- Un'immagine semplice che regge tutto il ragionamento (es. "una linea che diventa un triangolo"), al posto di tanti esempi sparsi.
- Domande retoriche solo se aiutano a capire, al massimo una.
- Chiudi con la conseguenza pratica o la domanda che resta aperta, non con un riassunto.
- Parole comuni; ogni sigla o termine tecnico spiegato la prima volta (regola già sopra).
- Inglese ("en"): frasi brevi, parole semplici (A2-B1 per i livelli 1 e 4), forma attiva, niente idiomi difficili: deve servire a Matteo per imparare.
- Lo stile non cambia le REGOLE FERREE: nessun fatto, numero, nome o citazione inventati.

Ogni notizia:
{
  "id": "ai-01",                        // ai-01..ai-10 / eco-01..eco-10
  "sezione": "ai" | "economia",
  "tag": "Modelli",                     // breve categoria in italiano
  "titolo": "...",                      // CHIARO: dice cosa è successo con parole comuni, niente sigle o gergo non spiegati. Max ~90 caratteri.
                                        //   NO: "Meta, impegni per 825 mld e il titolo cade"  SÌ: "Meta spenderà cifre enormi per l'AI e gli investitori vendono le sue azioni"
  "il_punto": "...",                    // 1-2 frasi CROCCANTI: il gancio che cattura l'attenzione e dice la sostanza (cosa significa davvero e perché conta). Es: "Meta guadagna come mai prima, ma spende ancora di più: per la prima volta la Borsa le chiede il conto."
  "sottotitolo": "...",                 // 1 frase di contesto
  "fonte": "Reuters", "url": "https://...articolo", "data": "AAAA-MM-GG", "importanza": 1-5,
  "immagine": "",                       // facoltativo: URL og:image solo se visto davvero
  "livelli": {                          // stessa notizia, profondità crescente. OGNI livello deve far capire: cosa è successo, PERCHÉ (cause), COSA CAMBIA (conseguenze), un ESEMPIO concreto (meglio se con numeri)
    "1":  "...",   // 12 anni: 80-120 parole, frasi brevi, un paragone di vita quotidiana, zero sigle
    "4":  "...",   // lettore curioso: LUNGO COME LA NOTIZIA (250-350 parole). 4 paragrafi che iniziano esattamente con
                   //   "Cosa è successo: ", "Perché: ", "Cosa cambia: ", "Un esempio: ". Ogni termine tecnico o sigla spiegato tra parentesi la prima volta.
    "7":  "...",   // informato: 400-500 parole, stessi 4 paragrafi + "Il contesto: " (prima di "Cosa cambia"). Termini spiegati tra parentesi la prima volta.
    "10": "..."    // esperto: 550-750 parole, paragrafi con etichette "Cosa è successo: ", "Il contesto: ", "Perché: ", "I numeri: ", "Cosa cambia: ", "Rischi e scenari: ", "Cosa resta incerto: "
  },                                    // paragrafi separati da \n\n; ogni paragrafo inizia con l'etichetta seguita da ": "
  "termini": [ {"termine": "Brent", "spiegazione": "Il petrolio estratto nel Mare del Nord, usato come prezzo di riferimento in Europa."} ],
                                        // TUTTE le sigle e i termini tecnici che compaiono nei testi (anche titolo), 4-12 per notizia. "termine" scritto ESATTAMENTE come compare nel testo. Spiegazione in 1-2 frasi semplici.
  "perche_conta": "...",                // 1 frase: perché dovrebbe interessare a Matteo (soldi, lavoro, vita quotidiana, carriera)
  "numeri": [ {"label": "Prezzo del Brent", "valore": "116,7 $"} ],   // 0-3, solo dalle fonti
  "chi": [ {"nome": "...", "tipo": "azienda"|"persona"|"istituzione", "url": "https://..."} ],
  "approfondimenti": [ {"titolo": "...", "url": "https://..."} ],
  "en": {                               // VERSIONE INGLESE (Matteo impara l'inglese): stessi fatti, stessa struttura
    "titolo": "...", "il_punto": "...", "sottotitolo": "...", "perche_conta": "...",
    "livelli": {"1": "...", "4": "...", "7": "...", "10": "..."},   // 1 e 4 inglese semplice A2-B1; 7 e 10 B2. Etichette: "What happened: ", "Why: ", "The context: ", "What changes: ", "An example: ", "The numbers: ", "Risks and scenarios: ", "Still unclear: "
    "termini": [ {"termine": "...", "spiegazione": "..."} ]          // termini come compaiono nel testo inglese, spiegati in inglese semplice
  },
  "glossario": [ {"en": "funding round", "it": "round di finanziamento"} ]   // 5-7 parole inglesi utili dal testo inglese
}

REGOLE FERREE
- Solo fatti presenti nelle fonti lette con WebFetch. Nessun numero, data, nome o citazione inventati. Cause e conseguenze: quelle scritte nelle fonti; se aggiungi un ragionamento tuo, dillo ("Questo significa che...", "Probabilmente..."). Se un dato non è certo, non metterlo.
- Spiegazioni di concetti generali (cos'è uno spread, un'IPO, un modello linguistico) possono venire dalla conoscenza generale stabile.
- Citazioni tra virgolette solo se copiate esattamente dalla fonte (in inglese le parole originali; in italiano traduzione fedele dichiarata o discorso indiretto).
- Notizie delle ultime 24-48 ore. url = pagina dell'articolo, non la home.

# Altri file della ricerca
numeri.json  -> {"aggiornato":"chiusura di <giorno>", "voci":[{"nome","valore","variazione","nota","nota_en","spiegazione","fonte","url"}]}
   "spiegazione": 1 frase semplice su cos'è (es. "FTSE MIB: l'indice delle 40 aziende più grandi della Borsa di Milano"). Voci: FTSE MIB, Euro Stoxx 50, S&P 500, Nasdaq Composite, euro/dollaro, Brent, oro, Bitcoin, spread BTP-Bund, BTP 10 anni. Solo valori verificati con link.
aziende.json -> {"titolo":"Aziende in movimento oggi","voci":[{"nome","settore":"AI"|"Economia","cosa_fa","cosa_fa_en","novita","novita_en","cosa_succede","cosa_succede_en","data","numero","url_notizia","sito","linkedin"}]}
   6-8 aziende con una NOVITÀ DEL GIORNO (ultime 24-48 ore: conti trimestrali, forte movimento in Borsa, accordo, lancio, causa, multa, nomina). NON "aziende da seguire" in generale.
   "novita" = titolo breve della novità (es. "Crolla del 16% in Borsa dopo i conti di Gucci"); "cosa_succede" = 2-3 frasi: cosa è successo, perché, cosa significa; "data" = AAAA-MM-GG della novità; "cosa_fa" = 1 frase su cosa fa l'azienda; linkedin solo se verificato, altrimenti "".
voci.json    -> {"voci":[{"autore","ruolo","tipo","titolo","titolo_en","sintesi","sintesi_en","punti","punti_en","riassunto","riassunto_en","perche_leggerlo","perche_leggerlo_en","url","data","profilo"}]}
   4-6 opinioni pubbliche degli ultimi 10 giorni. Apri DAVVERO il pezzo con WebFetch.
   "sintesi" = 2-3 frasi; "punti" = 3-5 frasi brevi con le tesi principali; "riassunto" = 180-280 parole che rielaborano fedelmente il ragionamento dell'autore (cosa sostiene, con quali argomenti e dati, cosa conclude), in italiano semplice, attribuendo tutto all'autore ("secondo Krugman..."); citazioni tra virgolette solo se copiate esattamente. Versioni _en in inglese semplice.

# Podcast del giorno (podcast.json)
{"titolo": "...", "titolo_en": "...",
 "capitoli": [ {"titolo": "Apertura", "testo": "...", "titolo_en": "Opening", "testo_en": "..."} , ...]}
- Un discorso che FILA, come un buon podcast di un solo conduttore: apertura con il tema del giorno, poi 4-6 capitoli che collegano le notizie tra loro (AI ed economia si intrecciano: es. spese per l'AI → Borsa → petrolio → tassi → famiglie), una riflessione finale con i pensieri delle "voci" (attribuiti per nome: "Secondo l'economista X...") e una chiusura con "cosa tenere d'occhio domani".
- Testo scritto PER ESSERE ASCOLTATO: frasi brevi, niente sigle (o spiegate a voce), numeri arrotondati e detti a parole ("circa 117 dollari al barile"), domande retoriche, passaggi tra capitoli ("E qui arriva il punto interessante..."). Niente elenchi puntati, niente parentesi, niente URL.
- Durata: 1.100-1.500 parole in italiano (circa 8-10 minuti). Versione inglese "testo_en" semplice (B1), stessa struttura, 900-1.200 parole.
- Solo fatti presenti nelle notizie e nelle voci del giorno. Le riflessioni sono ragionamenti dichiarati ("Io la vedo così...", "Una possibile lettura è...").

# Attualità (attualita.json) — il minimo per parlare con i colleghi
{"voci": [ {"categoria": "Italia"|"Mondo"|"Politica"|"Sport"|"Cultura"|"Tecnologia"|"Meteo", "titolo": "...", "in_breve": "1-2 frasi semplici", "titolo_en": "...", "in_breve_en": "...", "fonte": "ANSA", "url": "https://..."} ]}
- 5-7 fatti del giorno (non AI/economia, già coperti), i più discussi in Italia: almeno 2 Italia, 1-2 mondo, 1 sport. Verificati su fonte aperta con WebFetch.

# Verifica (campo "verifica" del file del giorno, scritto dal controllo dei fatti)
{"controllati": 180, "corretti": 3, "rimossi": 1, "note": ["eco-04: rendimento corretto da 5,14% a 5,12% (Reuters)"]}
