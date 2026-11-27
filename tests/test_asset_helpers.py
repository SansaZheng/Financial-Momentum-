import hashlib
import tempfile
import unittest
from pathlib import Path

from scripts.hf_assets import cache_dir, sha256


class AssetHelpers(unittest.TestCase):
    def test_sha256_and_explicit_cache(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / 'x.bin'; p.write_bytes(b'abc')
            self.assertEqual(sha256(p), hashlib.sha256(b'abc').hexdigest())
            self.assertEqual(cache_dir(d), Path(d))


if __name__ == '__main__': unittest.main()
