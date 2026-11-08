🇮🇹 Italiano | [🇬🇧 English](GUIDE.en.md)

# Guida: installare, provare, tornare indietro

Questa guida vale per la prova di **Rivela 360** su MG4 Electric. Leggi prima le [Avvertenze](DISCLAIMER.md).

## Prima di cominciare
- ✅ **Testata solo su MG4 Electric Luxury MY23, unità FICM, firmware SWI68 R67 (Android 9).** Su **SWI133** non è testata (l'analisi del firmware non mostra differenze rilevanti, ma non è una prova). Se la tua auto è diversa, scrivi allo sviluppatore prima di installarla.
- Controlla la tua versione: `adb shell getprop ro.build.fingerprint` e, per le telecamere, `adb shell ls -l /dev/video*`.
- Prima di installare, **salva una copia** di `/configure/camera_calibdata.bin` e tieni pronto il comando per tornare alla 360 di serie (sezione sotto).
- Fai la prima prova **da fermo, in P, con il piede sul freno**, in un posto sicuro. Non usarla in manovra finché non hai visto che funziona sulla tua auto.
- Tieni a portata di mano questa guida, in particolare la sezione «Tornare alla 360 di serie».

## Installare
1. Scarica l'APK `Rivela360-….apk` dalla cartella [`releases/`](releases/) (pulsante *Download raw file*).
2. Copialo in una chiavetta USB.
3. Sull'auto apri il gestore file, scegli la chiavetta, tocca l'APK e poi *Installa*.
4. Se il sistema rifiuta l'installazione, non insistere e scrivi allo sviluppatore: non c'è nessun danno.
5. Apri l'app da ferma in P. Alla prima apertura compare la schermata delle avvertenze: leggila e tocca *Ho letto e accetto*.

## Dopo l'accensione dell'auto
Aspetta che l'infotainment abbia finito di avviarsi: Rivela 360 è disponibile solo a avvio completato. Nel frattempo, in retromarcia, c'è la retrocamera rapida di serie (fast RVC), che è indipendente da Android, funziona anche durante l'avvio e non va mai disattivata.

## Prova da fermo
- Con l'app aperta passa alle varie viste (360°, telecamera singola, 3D) e controlla che le immagini siano corrette.
- La prima volta che attivi la vista 3D l'app scarica il modello dell'auto (circa 8 MB): serve la rete dell'auto o il Wi-Fi, una volta sola.
- In retromarcia e con le frecce l'app si apre da sola. Se in retromarcia l'immagine non compare entro 2,5 secondi, si apre la 360 di serie (rete di sicurezza).

## Tornare alla 360 di serie
Fallo **prima di disinstallare l'app e prima di ogni aggiornamento firmware MG**.

- **Dall'app:** *Impostazioni › Retromarcia e frecce aprono › La 360 di serie*. Da quel momento retromarcia e frecce aprono di nuovo la 360 di serie.
- **Dal PC con adb**, se l'app non si apre: `adb shell pm enable com.saicmotor.hmi.aroundview/.car.CarBroadcastReceiver`.

Dopo aver riattivato la 360 di serie puoi disinstallare l'app dal gestore applicazioni dell'auto.

> La retrocamera rapida dell'avvio dell'auto non va mai disattivata né toccata.

## Vista della telecamera
In *Impostazioni › Telecamera › Vista* ci sono tre scelte:
- **Originale** (di serie): l'immagine intera della telecamera, con le linee curve dell'obiettivo e gli angoli neri.
- **Corretta**: le linee tornano dritte, ma l'angolo di visione è più stretto: circa 125° in orizzontale invece di circa 185°; in verticale la perdita è piccola.
- **Originale piena**: l'immagine originale ingrandita per riempire lo schermo: spariscono gli angoli neri. L'angolo scende a circa 140° in orizzontale (da circa 185°) e a circa 95° in verticale (da circa 125°).

Quando scegli *Corretta* o *Originale piena* l'app mostra un avviso con un disegno e chiede conferma. I valori sono calcolati dalla calibrazione della telecamera, non misurati in auto.

## Canali: Stabile e Beta
In *Impostazioni › Aggiornamenti* puoi scegliere da quale canale ricevere gli aggiornamenti:
- **Stabile** (di serie): solo versioni provate e approvate dall'autore.
- **Beta**: versioni di prova, con le novità prima degli altri e più possibilità di difetti.

Finora non è uscita nessuna versione stabile: per ora i due canali indicano la stessa versione di prova. Quando uscirà la prima stabile, il canale Stabile non riceverà più le beta.

## Aggiornare
- *Impostazioni › Aggiornamenti › Cerca aggiornamenti*: l'app controlla questa repository e propone la nuova versione.
- Oppure scarica l'APK nuovo da [`releases/`](releases/) e installalo come sopra: si installa sopra quello vecchio, senza perdere le impostazioni.

## Segnalare un problema
1. *Impostazioni › Prove e avanzate › Diagnosi › Salva e invia i log di diagnosi*.
2. Il file si trova in `Download/MG4-360-log` (memoria dell'auto).
3. Mandalo allo sviluppatore con: modello e anno dell'auto, versione dell'app (in fondo alle impostazioni), cosa stavi facendo e, se puoi, una foto dello schermo.
4. I log vengono ripuliti da token, indirizzi e-mail, coordinate e numero di telaio, ma possono contenere dati tecnici dell'auto (versioni software, segnali). Se ti interessa, controlla il file prima di inviarlo.
