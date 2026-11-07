🇮🇹 Italiano | [🇬🇧 English](BETATEST.en.md)

# Beta testing di Rivela 360

Grazie per la prova! Le versioni **beta** sono di test: il tuo aiuto serve a scoprire cosa non va sulla tua auto prima che la usi altra gente. Leggi prima le [Avvertenze](DISCLAIMER.md) e la [Guida](GUIDA.md) (installazione e ritorno alla 360 di serie).

> Provata finora solo su **MG4 Electric Luxury MY23, unità FICM, firmware SWI68 R67**. Se hai un'altra versione (per esempio SWI133), il tuo risultato è particolarmente prezioso: scrivi sempre il firmware.

## Prima di cominciare
- Scegli il canale in *Impostazioni › Aggiornamenti*: **Beta** per ricevere le versioni di prova, **Stabile** per le sole versioni approvate.
- Prima di installare **salva una copia** di `/configure/camera_calibdata.bin` e tieni a portata di mano il [ritorno alla 360 di serie](GUIDA.md#tornare-alla-360-di-serie).

## Regole di sicurezza
- Le prove 1-4 si fanno **da fermo, in P, con il piede sul freno**, in un posto sicuro.
- Le prove in manovra (5-6) solo dopo aver visto che le prime funzionano, in uno spazio libero, guardando comunque gli specchietti e direttamente fuori. L'app è solo un aiuto.
- Se qualcosa si blocca o l'immagine sparisce: torna alla 360 di serie e segnalalo.

## Cosa provare
Per ogni prova segna: **OK / non va / non so**.

1. **Prima apertura**
   - Compare la schermata delle avvertenze? Riesci ad accettare?
   - L'app si apre senza chiudersi da sola?
2. **Viste (da fermo)**
   - *360°*: le 4 immagini sono unite bene? Strisce nere, tagli o parti storte?
   - *Telecamere singole*: si vedono tutte?
   - *Vista 3D*: si vede l'auto (la prima volta scarica il modello, circa 8 MB)? Gira fluida col dito? Quanto ci mette ad aprirsi? Il pianale sotto l'auto è a posto?
   - *Impostazioni › Telecamera › Vista* (Originale / Corretta / Originale piena): ogni scelta mostra l'avviso e cambia l'immagine come descritto?
   - *Stile linee guida 1 | 2*: cambia l'aspetto delle linee?
   - Si aprono tutte le schede delle impostazioni? Funzionano i pulsanti?
3. **Retromarcia (da fermo, piede sul freno)**
   - Inserisci la R: l'app si apre da sola? Quanto ci mette, circa?
   - Le linee guida si vedono e cambiano girando lo sterzo?
   - Esci dalla R: torna alla schermata di prima?
   - Se l'immagine non compare entro 2,5 secondi si apre la 360 di serie: se succede, annotalo.
4. **Frecce**
   - Freccia destra e sinistra: si apre la vista del lato giusto? Si chiude dopo?
5. **Sensori e avvisi** (in manovra lenta, spazio libero)
   - Le barre dei sensori mostrano la distanza giusta (avvicina piano un muro)?
   - Avviso di traffico trasversale in retromarcia: compare quando passa qualcuno? Falsi allarmi?
6. **Uso normale** (qualche giorno)
   - L'immagine scatta o va a scatti? Quando?
   - Dopo lo spegnimento e la riaccensione dell'auto l'app parte e funziona come prima?
   - L'infotainment resta veloce, o noti rallentamenti, riavvii, blocchi?
   - Modalità autolavaggio e registrazione, se vuoi provarle.
7. **Aggiornamento**
   - *Impostazioni › Aggiornamenti › Cerca aggiornamenti*: risponde correttamente (nuova versione o "già aggiornato")?
8. **Ritorno alla 360 di serie**
   - Prova una volta a tornare alla 360 di serie (*Impostazioni › Retromarcia e frecce aprono › La 360 di serie*) e poi a rimettere Rivela 360. Funziona?

## Come mandare il risultato
Apri una [**segnalazione (Issue) su GitHub**](https://github.com/andneg7/rivela360-mg4/issues/new) (serve un account GitHub gratuito) e copia e compila questo modulo. Le Issue sono pubbliche: non scrivere dati personali (targa, telaio, indirizzi).

```
Auto: MG4 ... anno ...
Unità / firmware: (es. SWI68 R67)
Versione app: (in fondo alle Impostazioni)
Prove 1-8: OK / non va (cosa)
Problemi visti: cosa, quando, quanto spesso
Suggerimenti: cosa cambieresti
```

## Se c'è un problema
*Impostazioni › Prove e avanzate › Diagnosi › Salva e invia i log di diagnosi*. Il file è in `Download/MG4-360-log`: allegalo alla Issue con una foto dello schermo, se puoi. Più è fresco (subito dopo il problema), meglio è. I log sono ripuliti da token, e-mail, coordinate e numero di telaio.

## Non serve
- Provare tutto in un giorno: anche solo le prove 1-4 sono utili.
- Mandare i file se non hai problemi: basta un «tutto ok» con auto, firmware e versione.
