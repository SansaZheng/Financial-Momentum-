"""Versioned Hugging Face asset operations for the project.

The script uses the official huggingface_hub client. Authentication comes from
the CLI login store or HF_TOKEN/HUGGINGFACE_HUB_TOKEN; tokens are never printed.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
from typing import Optional


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def cache_dir(explicit: Optional[str]) -> Path:
    p = explicit or os.environ.get("PROJECT_CACHE") or os.environ.get("HF_HUB_CACHE")
    return Path(p).expanduser() if p else Path.home() / ".cache" / "huggingface" / "hub"


def api():
    try:
        from huggingface_hub import HfApi
    except ImportError as e:
        raise SystemExit("Install official client first: python -m pip install huggingface_hub") from e
    return HfApi()


def repo_type(value: str) -> Optional[str]:
    if value == "dataset": return "dataset"
    if value == "model": return "model"
    raise ValueError(value)


def cmd_status(_args):
    info = api().whoami()
    print(json.dumps({"name": info.get("name"), "orgs": [x.get("name") for x in info.get("orgs", [])]}, indent=2))


def cmd_download(args):
    from huggingface_hub import hf_hub_download
    target = hf_hub_download(
        repo_id=args.repo_id, filename=args.filename, repo_type=repo_type(args.repo_type),
        revision=args.revision, cache_dir=str(cache_dir(args.cache_dir)), local_dir=args.local_dir,
    )
    p = Path(target)
    result = {"path": str(p), "sha256": sha256(p), "bytes": p.stat().st_size, "revision": args.revision}
    print(json.dumps(result, indent=2))
    if args.sha256 and result["sha256"] != args.sha256:
        raise SystemExit("sha256 mismatch")


def cmd_upload(args):
    p = Path(args.local_path)
    if not p.is_file(): raise SystemExit(f"missing file: {p}")
    a = api()
    if args.create:
        a.create_repo(args.repo_id, repo_type=repo_type(args.repo_type), private=True, exist_ok=True)
    result = a.upload_file(
        path_or_fileobj=str(p), path_in_repo=args.path_in_repo, repo_id=args.repo_id,
        repo_type=repo_type(args.repo_type), revision=args.revision,
        commit_message=args.commit_message,
    )
    print(json.dumps({"repo_id": args.repo_id, "repo_type": args.repo_type, "path": args.path_in_repo,
                      "sha256": sha256(p), "commit": getattr(result, "oid", None) or str(result)}, indent=2))


def build_parser():
    p = argparse.ArgumentParser()
    sub = p.add_subparsers(dest="command", required=True)
    s = sub.add_parser("status"); s.set_defaults(func=cmd_status)
    d = sub.add_parser("download"); d.add_argument("--repo-id", required=True); d.add_argument("--repo-type", choices=["dataset", "model"], required=True); d.add_argument("--filename", required=True); d.add_argument("--local-dir"); d.add_argument("--revision", required=True); d.add_argument("--cache-dir"); d.add_argument("--sha256"); d.set_defaults(func=cmd_download)
    u = sub.add_parser("upload"); u.add_argument("--repo-id", required=True); u.add_argument("--repo-type", choices=["dataset", "model"], required=True); u.add_argument("--local-path", required=True); u.add_argument("--path-in-repo", required=True); u.add_argument("--revision", default="main"); u.add_argument("--commit-message", default="Upload versioned project asset"); u.add_argument("--create", action="store_true"); u.set_defaults(func=cmd_upload)
    return p


if __name__ == "__main__":
    args = build_parser().parse_args()
    args.func(args)
