#!/usr/bin/env python3
"""Allinea le release di GitHub a releases/update.json (usa il comando `gh`):
- per ogni canale crea la release se manca (etichetta ricavata dal nome dell'APK: Rivela360-v2.11-beta11.apk -> v2.11-beta11),
  con l'APK e le note;
- la versione del canale «stabile» è la Latest, tutte le altre sono pre-release (anche quelle vecchie)."""
import json, os, re, subprocess, sys

DRY = os.environ.get("DRY_RUN") == "1"
SHA = os.environ.get("GITHUB_SHA", "main")

def gh(*a, check=True):
    print("gh", *a)
    if DRY and a[0] in ("release",) and a[1] in ("create", "edit"):
        return ""
    r = subprocess.run(["gh", *a], capture_output=True, text=True)
    if check and r.returncode:
        print(r.stderr); sys.exit(1)
    return r.stdout

def tag_of(path):
    m = re.fullmatch(r"releases/Rivela360-(v[\w.\-]+)\.apk", path)
    return m.group(1) if m else None

ch = json.load(open("releases/update.json", encoding="utf-8"))["channels"]
stable_tag = tag_of(ch["stabile"]["file"]) if "stabile" in ch else None
existing = {x["tagName"]: x for x in json.loads(gh("release", "list", "--limit", "100", "--json", "tagName,isPrerelease") or "[]")}

done = set()
for name, c in ch.items():
    tag = tag_of(c["file"])
    if not tag or tag in done:
        continue
    done.add(tag)
    if not os.path.isfile(c["file"]):
        print(f"ATTENZIONE: manca {c['file']}, salto {tag}"); continue
    is_stable = tag == stable_tag
    flags = ["--latest"] if is_stable else ["--prerelease", "--latest=false"]
    if tag in existing:
        gh("release", "edit", tag, *(["--prerelease=false", "--latest"] if is_stable else ["--prerelease", "--latest=false"]))
    else:
        notes = c["notes"] + "\n\nLeggi le avvertenze prima di installare: DISCLAIMER.md\n"
        open("notes.md", "w", encoding="utf-8").write(notes)
        gh("release", "create", tag, c["file"], "--target", SHA, "--title", "Rivela 360 " + tag[1:], "--notes-file", "notes.md", *flags)

# release vecchie: tutte pre-release tranne la stabile
for tag, x in existing.items():
    if tag in done or tag == stable_tag:
        continue
    if re.search(r"beta", tag) and not x["isPrerelease"]:
        gh("release", "edit", tag, "--prerelease", "--latest=false")
