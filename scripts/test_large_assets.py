"""Test archive restoration, tamper detection and overwrite protection."""
import hashlib
from pathlib import Path
import tempfile
import unittest

from large_assets import process, safe_path


class ArchiveTests(unittest.TestCase):
    def test_restore_and_protection(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            archive = root / 'archive'
            archive.mkdir()
            data = b'animation-archive\x00\xff' * 100
            parts = [data[:100], data[100:]]
            entry = {'path': 'output/asset.bin', 'size': len(data),
                     'sha256': hashlib.sha256(data).hexdigest(), 'parts': []}
            for i, part in enumerate(parts):
                name = f'{i}.chunk'
                (archive / name).write_bytes(part)
                entry['parts'].append({'path': name, 'size': len(part),
                                       'sha256': hashlib.sha256(part).hexdigest()})
            process(entry, root, archive, restore=True)
            target = root / entry['path']
            self.assertEqual(target.read_bytes(), data)
            process(entry, root, archive, restore=True)
            target.write_bytes(b'local edits')
            with self.assertRaisesRegex(ValueError, 'Refusing'):
                process(entry, root, archive, restore=True)
            self.assertEqual(target.read_bytes(), b'local edits')
            target.unlink()
            (archive / '1.chunk').write_bytes(b'corrupt')
            with self.assertRaisesRegex(ValueError, 'Corrupt'):
                process(entry, root, archive, restore=True)
            self.assertFalse(target.exists())
            self.assertFalse(target.with_name(target.name + '.restore-tmp').exists())
            with self.assertRaises(ValueError):
                safe_path(root, '../outside')


if __name__ == '__main__':
    unittest.main()
