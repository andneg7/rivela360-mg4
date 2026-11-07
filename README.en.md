🇬🇧 English | [🇮🇹 Italiano](README.md)

<p align="center"><img src="immagini/rivela360-logo-orizzontale.svg" alt="Rivela 360" width="520"></p>

# Rivela 360

**An alternative 360° view for the MG4 Electric.** An independent, free project that replaces the stock 360° camera interface with a clearer view, a 3D model of the car and many extra features.

> [!CAUTION]
> ## ⚠️ A DRIVING AID: IT DOES NOT REPLACE YOUR ATTENTION
> - **Rivela 360 is only an aid.** Images, guide lines, distances, colours, sensor bars and warnings can be **inaccurate, late, missing or wrong**.
> - **The driver is always solely responsible for the manoeuvre.** **Always** also check the mirrors and **look directly outside** the window, and comply with traffic law.
> - **Don't rely on the screen alone** for distances, obstacles, people, animals or children near the car.
> - **It replaces a stock application of the car** and uses system permissions: it can cause malfunctions, including of the original camera, and may void the warranty. **Installation and use are at your sole risk.**
> - **Always try it stationary**, in P, in a safe place, before using it to manoeuvre.
> - Before installing it, read the [**Warnings and liability**](DISCLAIMER.en.md): by installing it you accept them.

> **Personal, unofficial project, not affiliated with MG Motor or SAIC.**
>
> 🔬 **Test version.** It has been tried on a single configuration only: **MG4 Electric Luxury MY23, FICM head unit, firmware SWI68 R67, Android 9**. I don't know how it behaves on other versions.
>
> | Firmware | Status |
> |---|---|
> | **SWI68 R67** | ✅ **Tested** |
> | **SWI133** | ⚠️ **Not tested.** A firmware analysis shows no relevant differences (same Android 9 base, same stock 360 app, same system signature), but only a test on the car can confirm it |
> | Others | ❓ Unknown |

## What it does
- **360° view** built from the 4 cameras, shown next to a single-camera view or the **3D view** with the car model.
- **Dynamic guide lines** that follow the steering, **side clearance lines** with the full arc when stationary, and **sensor bars** also in 3D.
- **Parking sensors** with distance in cm and automatic zoom on the obstacle, plus a **cross-traffic** warning when reversing.
- **Car wash mode**: light-blue bands on the front wheels to line up with the track of car wash tunnels, also in 3D with the car semi-transparent.
- **Automatic opening** when reversing and with the turn signals, with adjustable opening and closing speed.
- **Safety net**: if the app doesn't show the image within 2.5 seconds when reversing, the stock 360 opens.
- **Photos, videos and automatic recording of manoeuvres**, also to a USB stick.
- Languages: English, Italian, German, French and Spanish.

## What it looks like
> The reversing and 3D view images are **mockups** (a simulated screen and a render of the 3D model); the settings ones are real screenshots of the demo version. None is a photo of the car. In the car the look may differ in some details.

**Reversing:** 360° view on the left, rear camera on the right, with guide lines, sensor bars and distance in cm.

![Reversing](immagini/retromarcia.png)

**3D view** with the car model:

![3D view](immagini/vista-3d.png)

**Settings** (real screenshots of the demo version, designed for touch):

![Settings: opening and closing](immagini/impostazioni-apertura.png)
![Settings: reversing](immagini/impostazioni-retromarcia.png)
![Settings: 3D view](immagini/impostazioni-vista-3d.png)

> The app's screens appear in the language of the car; the screenshots above are in Italian.

## Installing
The step-by-step guide, including how to go back to the stock 360, is in [**GUIDE.en.md**](GUIDE.en.md). In short:
1. Download the latest APK from the [`releases/`](releases/) folder.
2. Copy it to a USB stick, open it from the car's file manager and tap *Install*.
3. On first launch, stationary in P, read and accept the warnings. **Always try it while stationary before using it to manoeuvre: it is only an aid, responsibility for the manoeuvre stays with you.**

## Going back to the stock 360
Before uninstalling the app or doing an MG firmware update: *Settings › Reversing and turn signals open › The stock 360*. Full details are in the [guide](GUIDE.en.md#going-back-to-the-stock-360).

## How the 3D view works
The projection of the cameras onto the "bowl", the distortions and the limits of the 4 cameras are explained in [**PROJECTION-3D.en.md**](PROJECTION-3D.en.md).

## Beta testing
Want to help test it? The instructions, with the list of tests and the form for your result, are in [**BETATEST.en.md**](BETATEST.en.md).

## Reporting a problem
Settings › *Tests and advanced* › Diagnostics › *Save and send diagnostic logs*: the file is saved to `Download/MG4-360-log`. Open a [GitHub Issue](https://github.com/andneg7/rivela360-mg4/issues/new) and attach the file, stating the car model and year, firmware, app version and what you were doing. Issues are public: no personal data.

## Updates
The app checks for updates from this repository (Settings › Updates). The list of versions is in [`releases/`](releases/). There are two channels: **Stable** (default) and **Beta**, which gets test builds first.

## License and credits
- **Rivela 360** is free for personal, non-commercial use. The source code is not published. Selling it or distributing it for a fee is not allowed.
- **3D car model**: "[2025 MG MG4 (GLB)(mgmotor.com.mx)](https://sketchfab.com/3d-models/2025-mg-mg4-glbmgmotorcommx-ee2e3b0e1a7b481cb2c08e6fc6d2ed9e)" by **MattDoesBlender** (Sketchfab), licensed [**CC BY-NC-SA 4.0**](https://creativecommons.org/licenses/by-nc-sa/4.0/). The `car3d-pub-v4.bin` file is a **modified** version: simplified (from about 1.1 million to about 550,000 triangles), split into groups and reordered for the graphics chip, with the bodywork recoloured black, interior and brake calipers removed, wheels replaced by a custom design, and manufacturer logos and number plates removed. It is distributed under the same license: non-commercial use only, with this attribution.
- **Fonts**: Exo 2, Chakra Petch and Orbitron, under the SIL Open Font License 1.1.
- The car's original images and data are not included: the app reads them from the car while running.
- MG, MG4 and SAIC are trademarks of their respective owners, mentioned only to indicate compatibility.
