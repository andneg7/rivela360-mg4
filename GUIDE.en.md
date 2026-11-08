🇬🇧 English | [🇮🇹 Italiano](GUIDA.md)

# Guide: installing, testing, going back

This guide covers the trial of **Rivela 360** on the MG4 Electric. Read the [Warnings](DISCLAIMER.en.md) first.

## Before you start
- ✅ **Tested only on MG4 Electric Luxury MY23, FICM head unit, firmware SWI68 R67 (Android 9).** On **SWI133** it is not tested (a firmware analysis shows no relevant differences, but that is not proof). If your car is different, write to the developer before installing.
- Check your version: `adb shell getprop ro.build.fingerprint` and, for the cameras, `adb shell ls -l /dev/video*`.
- Before installing, **save a copy** of `/configure/camera_calibdata.bin` and keep the command to go back to the stock 360 at hand (section below).
- Do the first test **stationary, in P, with your foot on the brake**, in a safe place. Don't use it while manoeuvring until you have seen that it works on your car.
- Keep this guide handy, especially the section "Going back to the stock 360".

## Installing
1. Download the `Rivela360-….apk` file from the [`releases/`](releases/) folder (*Download raw file* button).
2. Copy it to a USB stick.
3. In the car, open the file manager, choose the stick, tap the APK and then *Install*.
4. If the system refuses the installation, don't insist and write to the developer: there is no damage.
5. Open the app stationary in P. On first launch the warnings screen appears: read it and tap *I have read and accept*.

## After switching the car on
Wait for the infotainment to finish booting: Rivela 360 is only available once the boot is complete. In the meantime, when reversing, the stock fast rear camera (fast RVC) is there: it is independent of Android, works even while it boots, and must never be disabled.

## Stationary test
- With the app open, switch between the views (360°, single camera, 3D) and check that the images are correct.
- The first time you enable the 3D view the app downloads the car model (about 8 MB): you need the car's network or Wi-Fi, once only.
- The app opens by itself when reversing and with the turn signals. If the image doesn't appear within 2.5 seconds when reversing, the stock 360 opens (safety net).

## Going back to the stock 360
Do this **before uninstalling the app and before any MG firmware update**.

- **From the app:** *Settings › Reversing and turn signals open › The stock 360*. From then on, reversing and turn signals open the stock 360 again.
- **From a PC with adb**, if the app won't open: `adb shell pm enable com.saicmotor.hmi.aroundview/.car.CarBroadcastReceiver`.

After re-enabling the stock 360 you can uninstall the app from the car's application manager.

> The fast rear camera shown when the car starts up must never be disabled or touched.

## Camera view
In *Settings › Camera › View* there are three choices:
- **Original** (default): the whole camera image, with the curved lines of the lens and the black corners.
- **Corrected**: lines become straight again, but the field of view is narrower: about 125° horizontally instead of about 185°; vertically the loss is small.
- **Original, filled**: the original image enlarged to fill the screen: the black corners disappear. The angle drops to about 140° horizontally (from about 185°) and about 95° vertically (from about 125°).

When you choose *Corrected* or *Original, filled* the app shows a warning with a drawing and asks for confirmation. The values are calculated from the camera calibration, not measured in the car.

## Channels: Stable and Beta
In *Settings › Updates* you can choose which channel to receive updates from:
- **Stable** (default): only versions tested and approved by the author.
- **Beta**: test versions, with new features first and a higher chance of defects.

No stable version has been released yet: for now both channels point to the same test version. When the first stable one is released, the Stable channel will no longer receive betas.

## Updating
- *Settings › Updates › Check for updates*: the app checks this repository and offers the new version.
- Or download the new APK from [`releases/`](releases/) and install it as above: it installs over the old one, without losing your settings.

## Reporting a problem
1. *Settings › Tests and advanced › Diagnostics › Save and send diagnostic logs*.
2. The file is in `Download/MG4-360-log` (car storage).
3. Send it to the developer with: car model and year, app version (at the bottom of the settings), what you were doing and, if you can, a photo of the screen.
4. Logs are cleaned of tokens, e-mail addresses, coordinates and the VIN, but may contain technical data of the car (software versions, signals). If you care, check the file before sending it.
