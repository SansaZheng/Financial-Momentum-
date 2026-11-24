from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
PROVENANCE = json.loads((ROOT / "data/provenance.json").read_text())

required = {
    "cpd": (ROOT / "vendor/author-cpd", PROVENANCE["author_repositories"]["cpd"]),
    "dmn": (ROOT / "vendor/author-dmn", PROVENANCE["author_repositories"]["dmn"]),
}

for name, (path, record) in required.items():
    if not path.is_dir():
        raise SystemExit(f"missing vendor source: {name}: {path}")
    observed = (path / ".source-commit").read_text().strip()
    if observed != record["commit"]:
        raise SystemExit(f"{name} commit mismatch: {observed} != {record['commit']}")

print(json.dumps({"status": "ok", "sources": {k: v[1]["commit"] for k, v in required.items()}}, indent=2))
