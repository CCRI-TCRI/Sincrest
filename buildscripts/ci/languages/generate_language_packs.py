#!/usr/bin/env python3
"""
Compiles share/locale/*.ts into .qm files, packages them per language code
into resources/backend/languages/locale_<code>.zip, and writes a
resources/backend/languages/details.json manifest with a SHA-1 hash of each
.qm file. This is Sincrest's own replacement for MuseScore's
extensions.musescore.org language-pack server: the app fetches details.json
to see which languages have updates, then downloads the matching zip.

Usage: generate_language_packs.py --lrelease /path/to/lrelease
"""
import argparse
import hashlib
import json
import re
import subprocess
import zipfile
from pathlib import Path

RESOURCE_NAMES = ["musescore", "instruments"]
REPO_ROOT = Path(__file__).resolve().parents[3]
LOCALE_SRC_DIR = REPO_ROOT / "share" / "locale"
OUTPUT_DIR = REPO_ROOT / "resources" / "backend" / "languages"

TS_NAME_RE = re.compile(r"^(musescore|instruments)_(.+)\.ts$")


def find_language_codes():
    codes = set()
    for ts_file in LOCALE_SRC_DIR.glob("*.ts"):
        m = TS_NAME_RE.match(ts_file.name)
        if m:
            codes.add(m.group(2))
    return sorted(codes)


def compile_qm(lrelease, resource, code, build_dir):
    ts_path = LOCALE_SRC_DIR / f"{resource}_{code}.ts"
    if not ts_path.exists():
        return None

    qm_path = build_dir / f"{resource}_{code}.qm"
    subprocess.run([lrelease, "-silent", str(ts_path), "-qm", str(qm_path)], check=True)
    return qm_path if qm_path.exists() else None


def sha1_of(path):
    h = hashlib.sha1()
    h.update(path.read_bytes())
    return h.hexdigest()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--lrelease", default="lrelease", help="Path to the lrelease binary")
    args = parser.parse_args()

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    build_dir = REPO_ROOT / "build.language_packs"
    build_dir.mkdir(exist_ok=True)

    details = {}

    for code in find_language_codes():
        qm_paths = {}
        for resource in RESOURCE_NAMES:
            qm_path = compile_qm(args.lrelease, resource, code, build_dir)
            if qm_path:
                qm_paths[resource] = qm_path

        if not qm_paths:
            continue

        zip_path = OUTPUT_DIR / f"locale_{code}.zip"
        with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
            for resource, qm_path in qm_paths.items():
                zf.write(qm_path, arcname=qm_path.name)

        details[code] = {
            resource: {"hash": sha1_of(qm_path)}
            for resource, qm_path in qm_paths.items()
        }

        print(f"Packed {code}: {', '.join(details[code].keys())}")

    details_path = OUTPUT_DIR / "details.json"
    details_path.write_text(json.dumps(details, indent=4, sort_keys=True) + "\n")
    print(f"Wrote {details_path} with {len(details)} language(s)")


if __name__ == "__main__":
    main()
