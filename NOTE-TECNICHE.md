🇮🇹 Italiano | [🇬🇧 English](TECHNICAL-NOTES.en.md)

# Note tecniche: telecamere, firmware e comportamento dell'MG4

Raccolta di ciò che abbiamo **verificato in auto** o **letto nel firmware** mentre sviluppavamo Rivela 360. Serve a chi vuole capire come funziona la 360° dell'MG4 o sperimentare con la propria unità.

> [!WARNING]
> **Documento non ufficiale.** Non è affiliato né approvato da MG Motor, SAIC o dai loro fornitori. Quasi tutto è stato provato su **una sola auto** (MG4 Electric Luxury MY23). Ogni dato porta un'indicazione di quanto è sicuro:
> - ✅ **Verificato in auto**
> - 🔍 **Letto nel firmware** (non provato direttamente)
> - ❓ **Non verificato**
>
> Non pubblichiamo né distribuiamo codice, applicazioni o file di SAIC o dei suoi fornitori. Modificare un'app di sistema può causare malfunzionamenti e far decadere la garanzia: **a tuo rischio**.

## Indice
1. [Auto e unità provate](#1-auto-e-unità-provate)
2. [Hardware e sistema](#2-hardware-e-sistema)
3. [Installare app di sistema](#3-installare-app-di-sistema)
4. [Le quattro telecamere](#4-le-quattro-telecamere)
5. [La 360° di serie](#5-la-360-di-serie)
6. [Retrocamera rapida (fast RVC)](#6-retrocamera-rapida-fast-rvc)
7. [Dati del veicolo](#7-dati-del-veicolo)
8. [Avvio dell'unità e stranezze osservate](#8-avvio-dellunità-e-stranezze-osservate)
9. [Misure e linee di guida](#9-misure-e-linee-di-guida)
10. [Cose provate e non riuscite](#10-cose-provate-e-non-riuscite)
11. [Risultati per firmware](#11-risultati-per-firmware)
12. [Come contribuire](#12-come-contribuire)

---

## 1. Auto e unità provate

| Dato | Valore |
|---|---|
| Auto | MG4 Electric Luxury MY23, unità FICM |
| Firmware in auto | SWI68 **R67** (build PPR1.181005.003, incremental 22113) ✅ |
| Altri firmware analizzati | SWI68 **R63** e SWI133 **R36** (solo file estratti, non provati in auto) 🔍 |
| Versione della 360° di serie (R67) | versionCode 23062 |

## 2. Hardware e sistema

- **Processore:** MediaTek **MT2712** ✅
- **Sistema:** Android **9** (API 28). Non è l'Android Automotive completo: la libreria `android.car` è quella dell'API 28 (P) ✅
- **Schermo:** 1920×720. La 360° di serie usa un'area di 1780×640: a sinistra c'è la barra di sistema e in alto la barra di stato ✅
- **Firma del firmware:** le app di sistema sono firmate con la chiave *platform* pubblica di AOSP (la stessa che si trova nei sorgenti di Android). Impronta SHA-256 del certificato: `c8a2e9bccf597c2fb6dc66bee293fc13f2fc47ec77bc6b2b0d52c11f51192ab8` ✅
  - Conseguenza: un'app con `android:sharedUserId="android.uid.system"` firmata con quella chiave viene accettata dall'auto come app di sistema.
  - Per aggiornare un'app già installata serve **la stessa firma**.
- **Una sola app per volta** può aprire le telecamere ✅

## 3. Installare app di sistema

- **`adb install`** di un'app con uid di sistema è rifiutato su R67 ("not allowed to install system tools") ✅
- **Funziona:** copiare l'APK in `/sdcard/Download` (con `adb push`) oppure su una **chiavetta USB**, poi installarlo dal **gestore file dell'auto** ✅
- **Sessioni `PackageInstaller`** avviate da un'app: rifiutate dal firmware ("Not allowed to install non-system apps on internal storage") ✅
- **Funziona per aggiornare da un'app:** aprire l'APK con `ACTION_VIEW` da un percorso `file://` in `Download`, che mostra la finestra di conferma di Android ✅. Un `content://` dà "Errore durante l'analisi del pacchetto".
- **Dopo un'installazione o una disinstallazione** serve un riavvio dell'unità: i servizi partono solo all'avvio ✅
- **Non si può aggiornare la 360° di serie:** è un'app `persistent` e Android 9 risponde "Persistent apps are not updateable" ✅. Per questo una 360° alternativa è un pacchetto **separato**, che si affianca a quella di serie.
- **Ripristinare la 360° di serie** (da PC): `adb shell pm enable com.saicmotor.hmi.aroundview/.car.CarBroadcastReceiver`. Lo stato disattivato di un componente **sopravvive alla disinstallazione** dell'app che l'ha disattivato e agli aggiornamenti del firmware ✅

## 4. Le quattro telecamere

- **Dispositivi V4L2:** `/dev/video14` destra, `/dev/video15` anteriore, `/dev/video16` sinistra, `/dev/video17` posteriore ✅. Il nome del driver è `mtk-mipicsi0…3` (camsv a `15004000…15007000`) e i nodi sono leggibili e scrivibili per l'uid di sistema ✅. Lo stesso ordine si trova nella libreria nativa della 360° di serie (`v4l2_OpenCameraByID(14..17)`, indice interno = id − 14) 🔍.
- **Formato:** 720×480 a 30 fps, **UYVY** ✅.
- **Composizione del fotogramma:** il driver dichiara `field=1`, ma il fotogramma contiene **due semiquadri impilati** (righe pari in alto, righe dispari in basso). Per avere l'immagine giusta vanno **ricomposti** (righe pari e dispari rimesse in ordine): nelle nostre prove è risultata l'opzione migliore ✅.
- **Retrocamera:** l'immagine grezza **non è specchiata** (la sinistra dell'auto compare a destra); la 360° di serie la mostra "come uno specchio" ✅.
- **Ottica:** la telecamera anteriore è una fisheye di circa 190° (stima da prove di proiezione) ❓. Le quattro hanno una calibrazione di fabbrica memorizzata dall'auto in `/configure/` 🔍; qui non ne pubblichiamo il formato.
- **Camera2:** da Android si vede **una sola** camera (id 0), non le quattro ✅.
- **Su `/sys/class/video4linux`** un'app senza privilegi vede solo fino a `video14`; non è chiaro se `15–17` compaiano solo a telecamere attive ❓.
- **Condivisione:** se la 360° di serie o un'altra app tiene aperte le telecamere, le altre non possono aprirle. Una dashcam o un'app di terze parti deve quindi **mettersi in pausa** quando parte la 360° di serie (vedi `ACTION_START` / `ACTION_STOP` nella sezione 5) ✅.

## 5. La 360° di serie

Pacchetto `com.saicmotor.hmi.aroundview` 🔍

| Componente | Cosa fa |
|---|---|
| `AVMActivity` | L'interfaccia che si vede in retromarcia e con il tasto 360 |
| `car.CarBroadcastReceiver` | Riceve l'ordine di aprire la vista; all'avvio (`BOOT_COMPLETED`) fa partire `CarManagerServer` |
| `car.CarManagerServer` | Servizio dati (marcia, volante, sensori), avviato all'accensione, in un processo a parte (`:secondCarManager`) |
| `CaliActivity` | Calibrazione di fabbrica. **Non avviarla mai.** |
| `RecordActivity` | Funzione di debug |

**Catena osservata in retromarcia** ✅: `MonitorVehicleService` (`handleGearSTS 2`) → servizio 360° → `CarBroadcastReceiver` → `AVMActivity`, in circa **80 ms**.

**Broadcast di apertura** 🔍:
- Azione `com.saicmotor.hmi.aroundview.startAVMActivity`, inviata con `setPackage` all'app stessa, quindi **non intercettabile** da altre app.
- Extra `startAVMActivityMsg`: `1` = retromarcia, `2` = freccia sinistra, `3` = freccia destra.
- Se la retrocamera rapida (fast RVC) è attiva, la vista non si apre.

**Aperture e chiusure automatiche** 🔍: con la freccia sotto i **15 km/h** la vista si apre da sola (impostazione `LowSpeedTurnAutoStartAVM`); sopra i 15 km/h si chiude se non si è in retromarcia.

**Ordini alle altre app** ✅: la 360° di serie manda `com.saicmotor.hmi.aroundview.ACTION_START` quando prende le telecamere e `ACTION_STOP` quando le lascia. Un `ACTION_START` **implicito** non arriva alle app in background: va inviato **in modo esplicito** al pacchetto.

**Proprietà di sistema** ✅:
- `persist.sys.screen_360` è `true` mentre la 360° è visibile.
- La 360° pubblica lo stato in proprietà `arcsoft.avm.*`, leggibili da altre app: `mCurCarGear` (marcia), `mCurCarWheelAngle` (angolo volante), `ServiceBegin`, i settori dei sensori, ecc.

**Marcia (`arcsoft.avm.mCurCarGear`)** ✅: `1` = P, `2` = R, `3` = N, `4` = D.
Attenzione: da fermi il valore **non è sempre affidabile**. Abbiamo osservato l'auto in P con valore `3` (N), tornato a `1` solo dopo D → P. Conviene accettare sia P sia N quando si controlla "auto ferma".

**Angolo del volante** ✅: `arcsoft.avm.mCurCarWheelAngle` **positivo = volante girato a sinistra**.

## 6. Retrocamera rapida (fast RVC)

È un servizio **nativo** (`/initfastrvc`, MediaTek) che mostra la retrocamera **senza aspettare Android** 🔍:
- Si chiama `fastrvc` nell'init del sistema e parte **all'accensione** e a ogni **risveglio** (`sys.power_state=resume`); si ferma in sospensione.
- La configurazione (`/fastlogo_file/fastrvc_config.xml`) descrive: telecamera indice 0 (720×480 UYVY), visualizzazione a tutto schermo 1920×720 su un piano DRM, attivazione dal segnale della retromarcia, attesa di `surfaceflinger`.
- Funziona **solo prima che Android finisca di avviarsi** ✅. Appena Android è pronto, la mano passa alla 360° (di serie o alternativa).
- Le proprietà `vendor.fastrvc.running` e `vendor.rvc.*` possono essere cambiate solo da processi di sistema (init, kernel, HAL del veicolo): **un'app non può toccarle**. Lasciarla com'è è anche una scelta di sicurezza.
- Finché `persist.sys.screen_360` è `true`, SystemUI mostra una finestra trasparente sopra la fast RVC.

**Conseguenza pratica:** durante l'avvio dell'infotainment la retromarcia funziona comunque grazie alla fast RVC; le app come Rivela 360 sono disponibili solo ad avvio completato.

## 7. Dati del veicolo

L'auto espone proprietà tramite `android.car` (API 28: si usa `createCar(Context, ServiceConnection[, Handler])` seguito da `connect()`). Nel nostro test erano visibili **1364 proprietà** ✅.

Identificativi letti nel firmware 🔍 (i valori delle proprietà `arcsoft.avm.*` sono invece verificati in auto ✅):

| Proprietà | ID | Note |
|---|---|---|
| Velocità | 291504647 (`0x11600207`) | |
| Angolo volante | 559945059 (`0x21601563`) | ±516,95° |
| ACC (accensione) | 289412477 | |
| Frecce | 557880102 (`0x21409326`) | 1 = sinistra, 2 = destra |
| Stato sensori di parcheggio | 557889904 | 0 ok, 2 errore, 3 spento |
| Settori posteriori | 557889910 … 557889913 | da sinistra a destra |
| Distanza minima posteriore | 557889915 | in cm |
| Traffico trasversale sx / dx | 557889916 / 557889917 | |

- **Livelli dei sensori:** 1 = rosso, 2–6 = giallo, 7–9 = verde 🔍. La tabella livello → centimetri **non è stata verificata** con ostacoli a distanza nota ❓.
- **Avviso di traffico trasversale (RCTA)** ✅: in retromarcia, quando passa un veicolo da sinistra, l'auto imposta `mLeftRearCarWarning = 1` per **1–2 secondi** (anche all'istante in cui si inserisce la R). Il segnale è breve: conviene tenerlo visibile almeno 1 s.
- **Suono dell'avviso RCTA** ✅: durante un avviso, per 3 s, non c'era **nessun riproduttore audio Android attivo** (controllo a 0, 350, 900 e 1800 ms) né righe di log sui suoni. Il suono nasce quindi **fuori da Android** e un'app non può sostituirlo.
- **Luci di stop:** nessun segnale affidabile trovato (vedi la sezione 10).
- **Servizi SAIC visibili:** `com.saicmotor.service.vehicle` (`VehicleService`) e i gestori `lamp`, `parkingassistance`, `sensor`, `info` 🔍.

## 8. Avvio dell'unità e stranezze osservate

- **Ordine di avvio:** su R67 il file system non è cifrato per file, quindi `LOCKED_BOOT_COMPLETED` e `BOOT_COMPLETED` arrivano quasi insieme e avviare un'app "prima" non cambia nulla ✅.
- **Avvio guasto osservato** (una volta) ✅: il servizio `com.saicmotor.service.vehicle` andava in crash continuo (`AirConditionBinder.getDrvSeatWindLevel`, tipo di proprietà del clima errato). Effetti: la 360° non riceveva la marcia ("servizio auto non disponibile") e **mancavano i nodi `mipicsi`** delle telecamere. Si risolve **riavviando l'infotainment**. Non dipendeva dalle nostre app.
- **Spegnimento:** se un'app che ha disattivato il ricevitore della 360° di serie lo riattiva troppo presto allo spegnimento, all'accensione successiva può comparire per prima la 360° di serie. Conviene non riattivarla durante `ACTION_SHUTDOWN` e aspettare qualche secondo con ACC spento ✅.
- **Rete:** con la SIM dati (4G) l'unità raggiunge `api.github.com`, `github.com`, `raw.githubusercontent.com` e `gitlab.com` ✅. Un primo tentativo può andare in timeout: conviene riprovare.

## 9. Misure e linee di guida

Dati ufficiali dell'MG4 Luxury (64 kWh) usati per disegnare le linee 🔍:

| Misura | Valore |
|---|---|
| Lunghezza | 4287 mm |
| Larghezza | 1836 mm (senza specchietti) |
| Altezza | 1516 mm |
| Passo | 2705 mm |
| Carreggiata | 1552 mm (anteriore), 1551 mm (posteriore) |
| Sbalzo posteriore | 745 mm |
| Sbalzo anteriore | 837 mm |

**Linee statiche della retrocamera** ✅: provate con del nastro a terra a **1 m** e **2 m** dalla fine del paraurti. Nello screenshot (vista dall'alto e retrocamera) il nastro coincideva con l'estremità rossa (1 m) e gialla (2 m), con uno scarto stimato di **1–2 cm**. Non verificati: 3 m (verde), la larghezza laterale e le linee dinamiche.

## 10. Cose provate e non riuscite

Segnate qui per risparmiare tempo a chi prova dopo di noi.

- **Una sola vista frontale ampia unendo anteriore e laterali:** risultato deforme e senza guadagno di angolo laterale. La anteriore è già una fisheye di circa 190° e vede già tutto quello che si può mostrare davanti; le laterali stanno sotto gli specchietti e guardano in basso e di lato, quindi non aggiungono campo in avanti e sopra il terreno le immagini mescolate danno immagini doppie ✅.
- **Luci di stop col freno:** candidato trovato (`0x2140159D`, 0 = rilasciato, ~2250–2700 = premuto) ma **in auto le luci non si sono accese**: il segnale non è quello giusto o non è leggibile. Non provare senza verificare prima il valore premendo il freno ✅.
- **`Car.createCar(ctx, null, null)`:** l'app si chiude subito all'apertura, perché la libreria auto chiama l'ascoltatore di connessione sul thread principale e con `null` va in crash. Usare un ascoltatore vero ✅.
- **Sfumature con `saveLayer` e maschere:** su questa unità (Android 9, HWUI) le parti mascherate restano piene o spariscono e la grafica scende a **23 fps**. Meglio evitarle ✅. Anche gli sfocati (blur) pesano troppo ✅.
- **Installare con `PackageInstaller`** o con `content://`: rifiutato dal firmware (vedi la sezione 3) ✅.
- **Sapere dove monta la chiavetta USB:** il percorso non è noto con certezza; si cerca nelle cartelle `/storage`, `/mnt/media_rw`, `/mnt/usb_storage`, `/mnt/usb`, `/mnt/udisk`, `/mnt/usbotg` ❓.

## 11. Risultati per firmware

| Firmware | Auto | Stato |
|---|---|---|
| SWI68 **R67** | MG4 Electric Luxury MY23, FICM | ✅ Testato in auto |
| SWI68 **R63** | | 🔍 Analizzato (file estratti). L'app 360° di serie è praticamente identica a R67 |
| SWI133 **R36** | | 🔍 Analizzato. Nessuna differenza rilevante trovata, ma **non provato in auto** ⚠️ |

**Segnalazione di un altro sviluppatore.** Jan ([jamakr4](https://github.com/jamakr4), autore di [MG4-360-Camera-App](https://github.com/jamakr4/MG4-360-Camera-App)) riferisce che la sua app, che usa le stesse telecamere, funziona su **tutte le MG4 con la 360°** e che non ha mai ricevuto segnalazioni legate alla versione del firmware: il sistema 360° sembra uguale su tutte le SWI. Unica eccezione nota: con **SWI165** la registrazione su chiavetta USB funziona solo dalla **porta USB-A**. Non l'abbiamo verificato noi ❓.

> Se hai un'auto o un firmware diverso, i tuoi risultati sono preziosi: vedi la sezione successiva.

## 12. Come contribuire

Apri una [segnalazione (Issue)](https://github.com/andneg7/rivela360-mg4/issues/new) indicando:
- modello e anno dell'auto, unità (FICM/altra) e **versione del firmware**;
- cosa hai provato e cosa è successo, indicando la sezione di questo documento a cui si riferisce;
- se possibile, il file di diagnosi salvato dall'app (Impostazioni › *Prove e avanzate* › Diagnosi).

Le Issue sono pubbliche: **niente dati personali** (niente VIN, targa, posizione, nomi).

---

Questo documento descrive osservazioni fatte da privati su una propria auto, a scopo di interoperabilità e studio. **Non è documentazione ufficiale** e può contenere errori. Controlla sempre sul tuo veicolo prima di fidarti di un dato.
