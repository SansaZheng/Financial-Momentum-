"""Small deterministic smoke checks for the vendored source and protocol files."""
from pathlib import Path
import json
import subprocess

ROOT = Path(__file__).resolve().parents[1]
subprocess.run(["python3", str(ROOT / "scripts/verify_sources.py")], check=True)
protocol = json.loads((ROOT / "data/provenance.json").read_text())
assert protocol["licensed_pinnacle_data"]["available"] is False
assert (ROOT / "EXPERIMENT_PROTOCOL.md").is_file()
print(json.dumps({"status": "ok", "pinnacle_available": False}, indent=2))
