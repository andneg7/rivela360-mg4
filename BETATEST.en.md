🇬🇧 English | [🇮🇹 Italiano](BETATEST.md)

# Beta testing Rivela 360

Thanks for helping out! **Beta** versions are test builds: your help is needed to find what doesn't work on your car before other people use it. Read the [Warnings](DISCLAIMER.en.md) and the [Guide](GUIDE.en.md) (installation and going back to the stock 360) first.

> So far tried only on **MG4 Electric Luxury MY23, FICM head unit, firmware SWI68 R67**. If you have another version (for example SWI133), your result is especially valuable: always state the firmware.

## Before you start
- Choose the channel in *Settings › Updates*: **Beta** to receive test builds, **Stable** for approved versions only.
- Before installing, **save a copy** of `/configure/camera_calibdata.bin` and keep [going back to the stock 360](GUIDE.en.md#going-back-to-the-stock-360) at hand.

## Safety rules
- Tests 1-4 are done **stationary, in P, with your foot on the brake**, in a safe place.
- Manoeuvring tests (5-6) only after you have seen that the first ones work, in a free space, still looking at the mirrors and directly outside. The app is only an aid.
- If something freezes or the image disappears: go back to the stock 360 and report it.

## What to try
For each test note: **OK / doesn't work / not sure**.

1. **First launch**
   - Does the warnings screen appear? Can you accept it?
   - Does the app open without closing by itself?
2. **Views (stationary)**
   - *360°*: are the 4 images stitched well? Black stripes, cuts or crooked parts?
   - *Single cameras*: are they all visible?
   - *3D view*: is the car visible (the first time it downloads the model, about 8 MB)? Does it rotate smoothly with your finger? How long does it take to open? Is the floor under the car right?
   - *Settings › Camera › View* (Original / Corrected / Original, filled): does each choice show the warning and change the image as described?
   - *Guide line style 1 | 2*: does the look of the lines change?
   - Do all settings tabs open? Do the buttons work?
3. **Reversing (stationary, foot on the brake)**
   - Engage R: does the app open by itself? Roughly how long does it take?
   - Are the guide lines visible and do they change as you turn the wheel?
   - Leave R: does it return to the previous screen?
   - If the image doesn't appear within 2.5 seconds the stock 360 opens: if that happens, note it.
4. **Turn signals**
   - Right and left signal: does the correct side view open? Does it close afterwards?
5. **Sensors and warnings** (slow manoeuvring, free space)
   - Do the sensor bars show the right distance (slowly approach a wall)?
   - Cross-traffic warning when reversing: does it appear when someone passes? False alarms?
6. **Normal use** (a few days)
   - Does the image stutter? When?
   - After switching the car off and on, does the app start and work as before?
   - Does the infotainment stay fast, or do you notice slowdowns, restarts, freezes?
   - Car wash mode and recording, if you want to try them.
7. **Updating**
   - *Settings › Updates › Check for updates*: does it answer correctly (new version or "up to date")?
8. **Going back to the stock 360**
   - Try once to go back to the stock 360 (*Settings › Reversing and turn signals open › The stock 360*) and then to put Rivela 360 back. Does it work?

## How to send the result
Open a [**GitHub Issue**](https://github.com/andneg7/rivela360-mg4/issues/new) (a free GitHub account is needed) and copy and fill in this form. Issues are public: don't write personal data (plate, VIN, addresses).

```
Car: MG4 ... year ...
Head unit / firmware: (e.g. SWI68 R67)
App version: (at the bottom of Settings)
Tests 1-8: OK / doesn't work (what)
Problems seen: what, when, how often
Suggestions: what you would change
```

## If there is a problem
*Settings › Tests and advanced › Diagnostics › Save and send diagnostic logs*. The file is in `Download/MG4-360-log`: attach it to the Issue with a photo of the screen, if you can. The fresher it is (right after the problem), the better. Logs are cleaned of tokens, e-mail addresses, coordinates and the VIN.

## Not needed
- Trying everything in one day: even just tests 1-4 are useful.
- Sending files if you have no problems: just an "all OK" with car, firmware and version.
