#!/usr/bin/env python3
"""Controlla releases/update.json: file, sha256, size e versione di ogni canale. Esce con 1 se qualcosa non torna.
Cerca anche token GitHub scritti per sbaglio nei file di testo. Uso: python3 check_update.py [cartella-repo]"""
import hashlib, json, os, re, sys

root = sys.argv[1] if len(sys.argv) > 1 else "."
bad = []

def fail(msg):
    bad.append(msg)
    print("ERRORE:", msg)

d = json.load(open(os.path.join(root, "releases", "update.json"), encoding="utf-8"))
for name, ch in d.get("channels", {}).items():
    f = ch.get("file", "")
    if not f.startswith("releases/"):
        fail(f"[{name}] «file» deve iniziare con releases/ (altrimenti l'app riceve HTTP 404): {f!r}")
    p = os.path.join(root, f)
    if not os.path.isfile(p):
        fail(f"[{name}] il file {f} non esiste")
        continue
    data = open(p, "rb").read()
    if len(data) != ch.get("size"):
        fail(f"[{name}] size {ch.get('size')} ma il file pesa {len(data)}")
    if hashlib.sha256(data).hexdigest() != ch.get("sha256"):
        fail(f"[{name}] sha256 diverso dal file {f}")
    m = re.fullmatch(r"(\d+)\.(\d+)(?: beta (\d+))?", ch.get("versionName", ""))
    if not m:
        fail(f"[{name}] versionName non valido: {ch.get('versionName')!r}")
    else:
        vc = int(m.group(1)) * 10000 + int(m.group(2)) * 100 + (int(m.group(3)) if m.group(3) else 99)
        if vc != ch.get("versionCode"):
            fail(f"[{name}] versionCode {ch.get('versionCode')} non corrisponde a «{ch['versionName']}» (atteso {vc})")
    if not ch.get("notes"):
        fail(f"[{name}] notes vuote")
    print(f"ok [{name}] {ch.get('versionName')} -> {f}")

tok = re.compile(r"gh[pousr]_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{30,}")
for dp, dn, fn in os.walk(root):
    dn[:] = [x for x in dn if x != ".git"]
    for n in fn:
        if n.endswith((".md", ".json", ".yml", ".yaml", ".txt", ".py", ".html", ".js")):
            t = open(os.path.join(dp, n), encoding="utf-8", errors="ignore").read()
            if tok.search(t):
                fail(f"sembra un token GitHub in {os.path.join(dp, n)}")

sys.exit(1 if bad else 0)
