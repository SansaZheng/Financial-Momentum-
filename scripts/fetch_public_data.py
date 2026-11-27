"""Fetch the public constructed futures panel into a project-local data directory.

This is a data acquisition helper, not a claim that the panel reproduces Pinnacle CLC.
It records the upstream commit after cloning so a CQ job can verify provenance.
"""
from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path


URL = "https://github.com/ArturSepp/TrendFollowingSystems.git"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dest", type=Path, required=True)
    # The upstream repository moved its default branch from ``master`` to
    # ``main``.  Keep the ref explicit in provenance while making the helper
    # work out of the box for a fresh remote workspace.
    ap.add_argument("--ref", default="main")
    args = ap.parse_args()
    args.dest.parent.mkdir(parents=True, exist_ok=True)
    if (args.dest / ".git").exists():
        subprocess.run(["git", "-C", str(args.dest), "fetch", "--depth", "1", "origin", args.ref], check=True)
        subprocess.run(["git", "-C", str(args.dest), "reset", "--hard", f"origin/{args.ref}"], check=True)
    else:
        subprocess.run(["git", "clone", "--depth", "1", "--branch", args.ref, URL, str(args.dest)], check=True)
    sha = subprocess.check_output(["git", "-C", str(args.dest), "rev-parse", "HEAD"], text=True).strip()
    (args.dest / "FETCH_PROVENANCE.json").write_text(json.dumps({"url": URL, "ref": args.ref, "commit": sha}, indent=2) + "\n")
    print(json.dumps({"status": "ok", "commit": sha, "path": str(args.dest)}, indent=2))


if __name__ == "__main__":
    main()
