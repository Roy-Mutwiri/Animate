"""Lossless archive for files too large for regular GitHub blobs. No dependencies."""
import argparse
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARCHIVE = ROOT / '.repo-assets'
MANIFEST = ARCHIVE / 'manifest.json'
CHUNK = 45 * 1024 * 1024
ORIGINALS = [
    'Goal/GPU-Link-Setup (1).exe',
    'Goal/GPU-Link-Setup.exe',
    'Goal/TikTokStreamClipper-v1.0.2-win64.zip',
    'Goal/TikTokStreamClipper-v1.0.2-win64/TikTokStreamClipper/TikTokStreamClipper.exe',
    'Projects/HonestInterview/tools/Rhubarb-Lip-Sync-1.14.0-Windows.zip',
]


def safe_path(root, relative):
    base = root.resolve()
    path = (base / relative).resolve()
    if not path.is_relative_to(base) or path == base:
        raise ValueError(f'Path outside archive/workspace: {relative}')
    return path


def digest(path):
    with path.open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def pack():
    entries = []
    for relative in ORIGINALS:
        source = safe_path(ROOT, relative)
        whole = hashlib.sha256()
        entry = {'path': relative, 'size': source.stat().st_size, 'parts': []}
        key = hashlib.sha256(relative.encode()).hexdigest()[:16]
        with source.open('rb') as stream:
            index = 0
            while data := stream.read(CHUNK):
                part = f'parts/{key}/{index:03d}.chunk'
                target = safe_path(ARCHIVE, part)
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(data)
                whole.update(data)
                entry['parts'].append({'path': part, 'size': len(data),
                                       'sha256': hashlib.sha256(data).hexdigest()})
                index += 1
        entry['sha256'] = whole.hexdigest()
        entries.append(entry)
        print(f'Packed {relative}: {index} parts')
    MANIFEST.write_text(json.dumps({'version': 1, 'files': entries}, indent=2) + '\n', encoding='utf-8')


def process(entry, root, archive, restore=False):
    destination = safe_path(root, entry['path'])
    existing = destination.exists()
    if restore and existing:
        if destination.stat().st_size != entry['size'] or digest(destination) != entry['sha256']:
            raise ValueError(f'Refusing to overwrite differing local file: {destination}')
    temporary = destination.with_name(destination.name + '.restore-tmp')
    output = None
    created = False
    whole = hashlib.sha256()
    total = 0
    try:
        if restore and not existing:
            destination.parent.mkdir(parents=True, exist_ok=True)
            output = temporary.open('xb')
            created = True
        for part in entry['parts']:
            data = safe_path(archive, part['path']).read_bytes()
            if len(data) != part['size'] or hashlib.sha256(data).hexdigest() != part['sha256']:
                raise ValueError(f'Corrupt part: {part["path"]}')
            whole.update(data)
            total += len(data)
            if output:
                output.write(data)
        if total != entry['size'] or whole.hexdigest() != entry['sha256']:
            raise ValueError(f'Combined hash/size mismatch: {entry["path"]}')
        if output:
            output.close()
            output = None
            # Fail rather than replace a file created concurrently.
            if destination.exists():
                raise FileExistsError(destination)
            temporary.rename(destination)
    finally:
        if output:
            output.close()
        if created and temporary.exists():
            temporary.unlink()
    print(f'{"Restored/verified" if restore else "Verified"}: {entry["path"]}')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=['pack', 'verify', 'restore'])
    args = parser.parse_args()
    if args.action == 'pack':
        pack()
        return
    manifest = json.loads(MANIFEST.read_text(encoding='utf-8'))
    if manifest['version'] != 1:
        raise ValueError('Unsupported manifest version')
    for entry in manifest['files']:
        process(entry, ROOT, ARCHIVE, restore=args.action == 'restore')


if __name__ == '__main__':
    main()
