[🇮🇹 Italiano](NOTE-TECNICHE.md) | 🇬🇧 English

# Technical notes: cameras, firmware and MG4 behaviour

A collection of what we **verified in the car** or **read in the firmware** while developing Rivela 360. It is meant for anyone who wants to understand how the MG4's 360° system works or experiment with their own unit.

> [!WARNING]
> **Unofficial document.** It is not affiliated with or endorsed by MG Motor, SAIC or their suppliers. Almost everything was tested on **a single car** (MG4 Electric Luxury MY23). Each item shows how certain it is:
> - ✅ **Verified in the car**
> - 🔍 **Read in the firmware** (not tested directly)
> - ❓ **Not verified**
>
> We do not publish or distribute code, applications or files belonging to SAIC or its suppliers. Modifying a system app can cause malfunctions and void the warranty: **at your own risk**.

## Contents
1. [Cars and units tested](#1-cars-and-units-tested)
2. [Hardware and system](#2-hardware-and-system)
3. [Installing system apps](#3-installing-system-apps)
4. [The four cameras](#4-the-four-cameras)
5. [The stock 360° app](#5-the-stock-360-app)
6. [Fast rear-view camera (fast RVC)](#6-fast-rear-view-camera-fast-rvc)
7. [Vehicle data](#7-vehicle-data)
8. [Unit start-up and odd behaviour](#8-unit-start-up-and-odd-behaviour)
9. [Dimensions and guide lines](#9-dimensions-and-guide-lines)
10. [Things tried that did not work](#10-things-tried-that-did-not-work)
11. [Results by firmware](#11-results-by-firmware)
12. [How to contribute](#12-how-to-contribute)

---

## 1. Cars and units tested

| Item | Value |
|---|---|
| Car | MG4 Electric Luxury MY23, FICM unit |
| Firmware in the car | SWI68 **R67** (build PPR1.181005.003, incremental 22113) ✅ |
| Other firmware analysed | SWI68 **R63** and SWI133 **R36** (extracted files only, not tested in the car) 🔍 |
| Stock 360° app version (R67) | versionCode 23062 |

## 2. Hardware and system

- **Processor:** MediaTek **MT2712** ✅
- **System:** Android **9** (API 28). It is not full Android Automotive: the `android.car` library is the API 28 (P) one ✅
- **Screen:** 1920×720. The stock 360° view uses a 1780×640 area: the system bar is on the left and the status bar at the top ✅
- **Firmware signature:** system apps are signed with AOSP's public *platform* key (the one found in the Android sources). SHA-256 fingerprint of the certificate: `c8a2e9bccf597c2fb6dc66bee293fc13f2fc47ec77bc6b2b0d52c11f51192ab8` ✅
  - Consequence: an app with `android:sharedUserId="android.uid.system"` signed with that key is accepted by the car as a system app.
  - Updating an installed app requires **the same signature**.
- **Only one app at a time** can open the cameras ✅

## 3. Installing system apps

- **`adb install`** of an app with the system uid is refused on R67 ("not allowed to install system tools") ✅
- **What works:** copy the APK to `/sdcard/Download` (with `adb push`) or to a **USB stick**, then install it from the **car's file manager** ✅
- **`PackageInstaller` sessions** started by an app: refused by the firmware ("Not allowed to install non-system apps on internal storage") ✅
- **What works for in-app updates:** open the APK with `ACTION_VIEW` from a `file://` path in `Download`, which shows Android's confirmation window ✅. A `content://` URI gives "There was a problem parsing the package".
- **After installing or uninstalling** the unit needs a restart: the services only start at boot ✅
- **The stock 360° app cannot be updated:** it is a `persistent` app and Android 9 replies "Persistent apps are not updateable" ✅. This is why an alternative 360° view is a **separate** package that sits next to the stock one.
- **Restoring the stock 360° view** (from a PC): `adb shell pm enable com.saicmotor.hmi.aroundview/.car.CarBroadcastReceiver`. A component's disabled state **survives uninstalling** the app that disabled it, and firmware updates ✅

## 4. The four cameras

- **V4L2 devices:** `/dev/video14` right, `/dev/video15` front, `/dev/video16` left, `/dev/video17` rear ✅. The driver name is `mtk-mipicsi0…3` (camsv at `15004000…15007000`) and the nodes are readable and writable by the system uid ✅. The same order appears in the stock 360° app's native library (`v4l2_OpenCameraByID(14..17)`, internal index = id − 14) 🔍.
- **Format:** 720×480 at 30 fps, **UYVY** ✅.
- **Frame layout:** the driver reports `field=1`, but the frame contains **two stacked fields** (even lines at the top, odd lines at the bottom). To get the right picture they must be **recombined** (even and odd lines put back in order): in our tests this was the best option ✅.
- **Rear camera:** the raw image is **not mirrored** (the car's left side appears on the right); the stock 360° view shows it "like a mirror" ✅.
- **Optics:** the front camera is a fisheye of about 190° (estimate from projection tests) ❓. All four have a factory calibration stored by the car in `/configure/` 🔍; we do not publish its format here.
- **Camera2:** Android exposes **only one** camera (id 0), not the four ✅.
- **In `/sys/class/video4linux`** an unprivileged app only sees up to `video14`; it is unclear whether `15–17` only appear while the cameras are active ❓.
- **Sharing:** if the stock 360° view or another app holds the cameras, no other app can open them. A dashcam or third-party app must therefore **pause** when the stock 360° view starts (see `ACTION_START` / `ACTION_STOP` in section 5) ✅.

## 5. The stock 360° app

Package `com.saicmotor.hmi.aroundview` 🔍

| Component | What it does |
|---|---|
| `AVMActivity` | The screen shown in reverse and with the 360 button |
| `car.CarBroadcastReceiver` | Receives the order to open the view; at boot (`BOOT_COMPLETED`) it starts `CarManagerServer` |
| `car.CarManagerServer` | Data service (gear, steering, sensors), started at power-on, in a separate process (`:secondCarManager`) |
| `CaliActivity` | Factory calibration. **Never start it.** |
| `RecordActivity` | Debug function |

**Chain observed in reverse** ✅: `MonitorVehicleService` (`handleGearSTS 2`) → 360° service → `CarBroadcastReceiver` → `AVMActivity`, in about **80 ms**.

**Opening broadcast** 🔍:
- Action `com.saicmotor.hmi.aroundview.startAVMActivity`, sent with `setPackage` to the app itself, so other apps **cannot intercept it**.
- Extra `startAVMActivityMsg`: `1` = reverse, `2` = left indicator, `3` = right indicator.
- If the fast rear-view camera (fast RVC) is active, the view does not open.

**Automatic opening and closing** 🔍: with an indicator on below **15 km/h** the view opens by itself (setting `LowSpeedTurnAutoStartAVM`); above 15 km/h it closes unless in reverse.

**Messages to other apps** ✅: the stock 360° app sends `com.saicmotor.hmi.aroundview.ACTION_START` when it takes the cameras and `ACTION_STOP` when it releases them. An **implicit** `ACTION_START` does not reach apps in the background: it must be sent **explicitly** to the package.

**System properties** ✅:
- `persist.sys.screen_360` is `true` while the 360° view is visible.
- The 360° app publishes its state in `arcsoft.avm.*` properties that other apps can read: `mCurCarGear` (gear), `mCurCarWheelAngle` (steering wheel angle), `ServiceBegin`, the sensor sectors, and so on.

**Gear (`arcsoft.avm.mCurCarGear`)** ✅: `1` = P, `2` = R, `3` = N, `4` = D.
Note: when stationary the value is **not always reliable**. We saw the car in P with value `3` (N), which only went back to `1` after D → P. It is safer to accept both P and N when checking "car stationary".

**Steering wheel angle** ✅: `arcsoft.avm.mCurCarWheelAngle` **positive = wheel turned left**.

## 6. Fast rear-view camera (fast RVC)

It is a **native** service (`/initfastrvc`, MediaTek) that shows the rear camera **without waiting for Android** 🔍:
- It is called `fastrvc` in the system init and starts **at power-on** and at every **wake-up** (`sys.power_state=resume`); it stops in suspend.
- Its configuration (`/fastlogo_file/fastrvc_config.xml`) describes: camera index 0 (720×480 UYVY), full-screen display at 1920×720 on a DRM plane, activation by the reverse signal, waiting for `surfaceflinger`.
- It works **only before Android has finished booting** ✅. As soon as Android is ready, control passes to the 360° view (stock or alternative).
- The `vendor.fastrvc.running` and `vendor.rvc.*` properties can only be changed by system processes (init, kernel, vehicle HAL): **an app cannot touch them**. Leaving it as it is is also a safety choice.
- While `persist.sys.screen_360` is `true`, SystemUI shows a transparent window above the fast RVC.

**In practice:** while the infotainment is booting, reverse still works thanks to the fast RVC; apps such as Rivela 360 are available only once the boot is complete.

## 7. Vehicle data

The car exposes properties through `android.car` (API 28: use `createCar(Context, ServiceConnection[, Handler])` followed by `connect()`). In our test **1364 properties** were visible ✅.

Identifiers read in the firmware 🔍 (the values of the `arcsoft.avm.*` properties, on the other hand, are verified in the car ✅):

| Property | ID | Notes |
|---|---|---|
| Speed | 291504647 (`0x11600207`) | |
| Steering wheel angle | 559945059 (`0x21601563`) | ±516.95° |
| ACC (ignition) | 289412477 | |
| Indicators | 557880102 (`0x21409326`) | 1 = left, 2 = right |
| Parking sensor status | 557889904 | 0 ok, 2 error, 3 off |
| Rear sectors | 557889910 … 557889913 | left to right |
| Minimum rear distance | 557889915 | in cm |
| Cross traffic left / right | 557889916 / 557889917 | |

- **Sensor levels:** 1 = red, 2–6 = yellow, 7–9 = green 🔍. The level → centimetres table has **not been verified** with obstacles at known distances ❓.
- **Rear cross-traffic alert (RCTA)** ✅: in reverse, when a vehicle passes from the left, the car sets `mLeftRearCarWarning = 1` for **1–2 seconds** (also at the moment R is engaged). The signal is short: it is worth keeping it visible for at least 1 s.
- **RCTA sound** ✅: during an alert, for 3 s, there was **no active Android audio player** (checked at 0, 350, 900 and 1800 ms) and no log lines about sounds. The sound is therefore generated **outside Android** and an app cannot replace it.
- **Brake lights:** no reliable signal found (see section 10).
- **Visible SAIC services:** `com.saicmotor.service.vehicle` (`VehicleService`) and the `lamp`, `parkingassistance`, `sensor` and `info` managers 🔍.

## 8. Unit start-up and odd behaviour

- **Boot order:** on R67 the file system is not file-based encrypted, so `LOCKED_BOOT_COMPLETED` and `BOOT_COMPLETED` arrive almost together and starting an app "earlier" changes nothing ✅.
- **Faulty start-up observed** (once) ✅: the `com.saicmotor.service.vehicle` service kept crashing (`AirConditionBinder.getDrvSeatWindLevel`, wrong climate property type). Effects: the 360° view did not receive the gear ("vehicle service not available") and the cameras' **`mipicsi` nodes were missing**. **Restarting the infotainment** fixes it. It was not caused by our apps.
- **Shutdown:** if an app that disabled the stock 360° receiver re-enables it too early during shutdown, the stock 360° view may appear first at the next power-on. Better not to re-enable it during `ACTION_SHUTDOWN` and to wait a few seconds with ACC off ✅.
- **Network:** with the data SIM (4G) the unit reaches `api.github.com`, `github.com`, `raw.githubusercontent.com` and `gitlab.com` ✅. A first attempt may time out: retrying is worthwhile.

## 9. Dimensions and guide lines

Official MG4 Luxury (64 kWh) data used to draw the lines 🔍:

| Dimension | Value |
|---|---|
| Length | 4287 mm |
| Width | 1836 mm (without mirrors) |
| Height | 1516 mm |
| Wheelbase | 2705 mm |
| Track | 1552 mm (front), 1551 mm (rear) |
| Rear overhang | 745 mm |
| Front overhang | 837 mm |

**Rear camera static lines** ✅: tested with tape on the ground at **1 m** and **2 m** from the end of the bumper. In the screenshot (top view and rear camera) the tape matched the red (1 m) and yellow (2 m) ends, with an estimated error of **1–2 cm**. Not verified: 3 m (green), lateral width and the dynamic lines.

## 10. Things tried that did not work

Listed here to save time for whoever tries next.

- **A single wide front view combining the front and side cameras:** distorted result with no gain in side angle. The front camera is already a fisheye of about 190° and already sees everything that can be shown ahead; the side cameras sit under the mirrors and look down and sideways, so they add no forward field, and above the ground the blended images produce double images ✅.
- **Brake lights from the brake pedal:** a candidate was found (`0x2140159D`, 0 = released, ~2250–2700 = pressed) but **the lights did not come on in the car**: either the signal is wrong or it cannot be read. Do not try again without first checking that the value changes when pressing the brake ✅.
- **`Car.createCar(ctx, null, null)`:** the app closes immediately on opening, because the car library calls the connection listener on the main thread and crashes with `null`. Use a real listener ✅.
- **Fades with `saveLayer` and masks:** on this unit (Android 9, HWUI) masked parts stay solid or disappear and graphics drop to **23 fps**. Better avoided ✅. Blur effects are also too heavy ✅.
- **Installing with `PackageInstaller`** or via `content://`: refused by the firmware (see section 3) ✅.
- **Where the USB stick is mounted:** the path is not known for sure; we search `/storage`, `/mnt/media_rw`, `/mnt/usb_storage`, `/mnt/usb`, `/mnt/udisk`, `/mnt/usbotg` ❓.

## 11. Results by firmware

| Firmware | Car | Status |
|---|---|---|
| SWI68 **R67** | MG4 Electric Luxury MY23, FICM | ✅ Tested in the car |
| SWI68 **R63** | | 🔍 Analysed (extracted files). The stock 360° app is practically identical to R67 |
| SWI133 **R36** | | 🔍 Analysed. No relevant differences found, but **not tested in the car** ⚠️ |

> If you have a different car or firmware, your results are valuable: see the next section.

## 12. How to contribute

Open an [issue](https://github.com/andneg7/rivela360-mg4/issues/new) stating:
- car model and year, unit (FICM/other) and **firmware version**;
- what you tried and what happened, naming the section of this document it refers to;
- if possible, the diagnostic file saved by the app (Settings › *Tests and advanced* › Diagnostics).

Issues are public: **no personal data** (no VIN, number plate, location or names).

---

This document describes observations made by private individuals on their own car, for interoperability and study purposes. **It is not official documentation** and may contain errors. Always check on your own vehicle before relying on any item.
