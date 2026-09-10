# Parser documenti - knowledge base

Applicazione Python da riga di comando per indicizzare documenti presenti in una
cartella e costruire una piccola knowledge base locale. Per ogni documento il
progetto raccoglie contenuto e metadati e rende
possibile una ricerca testuale sull'indice.

## Funzionalita

- scansione di una cartella e delle sue sottocartelle;
- estrazione del contenuto tramite parser specializzati;
- raccolta di titolo, percorso, dimensione, data di modifica e numero di parole;
- ricerca testuale con risultati ordinati in base alla corrispondenza;
- persistenza dell'indice in file JSON;
- aggiornamento, rimozione e svuotamento dell'indice tramite menu interattivo;
- caricamento dinamico dei parser presenti nella cartella `parser/`.

## Requisiti

- Python 3.9 o superiore;
- nessuna dipendenza esterna: il progetto utilizza solo la libreria standard;
- file leggibili in codifica UTF-8.

## Avvio

Dalla directory principale del progetto eseguire:

```bash
python main.py
```

All'avvio viene mostrato un menu interattivo. Le operazioni disponibili sono:

| Comando | Operazione |
| --- | --- |
| `h` | Mostra nuovamente il menu |
| `1` | Indicizza una nuova cartella |
| `2` | Cerca una parola o una frase nell'indice |
| `3` | Visualizza tutti i file indicizzati |
| `4` | Rimuove un file dall'indice |
| `5` | Aggiorna l'indice |
| `6` | Salva l'indice su disco |
| `7` | Svuota l'indice |
| `8` | Esce dall'applicazione |

Esempio di utilizzo:

1. avviare `python main.py`;
2. scegliere `1`;
3. inserire il percorso della cartella da indicizzare;
4. scegliere `2` e inserire i termini da cercare.

## Configurazione

La configurazione si trova in `config.ini`:

```ini
[parsers]
folder = parser

[index]
index = index.json
inverted_index = inverted_index.json

[logging]
level = DEBUG
file = log/indexer.log
```

Le chiavi principali sono:

- `parsers.folder`: directory da cui caricare dinamicamente i parser;
- `index.index`: file JSON che contiene i documenti indicizzati;
- `index.inverted_index`: file JSON usato per la ricerca per parole;
- `logging.file`: file di log dell'applicazione;
- `logging.level`: livello di logging, ad esempio `DEBUG`, `INFO` o `WARNING`.

I file `index.json`, `inverted_index.json` e `log/indexer.log` vengono creati o
aggiornati durante l'esecuzione e non devono essere modificati manualmente.

## Parser

La directory `parser/` contiene le implementazioni basate su
`model.parser.DocumentParser`. Attualmente sono presenti parser per:

- file di testo `.txt`;
- file Markdown `.md`;
- file CSV/TSV tramite `CSVParser`.

Per aggiungere un nuovo formato, creare un modulo Python in `parser/`, definire
una classe che erediti da `DocumentParser`, impostare l'estensione supportata e
implementare il metodo `parse`.
