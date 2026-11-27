# Slow Momentum with Fast Reversion: reproducible research

This repository rebuilds the empirical study of Wood, Roberts, and Zohren, “Slow Momentum with Fast Reversion” (Journal of Financial Data Science, 2022), and provides a place for preregistered extensions.

The project follows a strict evidence policy:

- author code and commit hashes are preserved under `vendor/`;
- public data sources are recorded in `data/provenance.json`;
- every experiment must pin a source commit, dataset hash, split calendar, seed list, cost model, and output manifest;
- Pinnacle CLC data are not redistributed and public constructed futures data are not relabeled as Pinnacle;
- no result is claimed until the code and output manifest have been executed and checked.

## First reproducibility stage

`vendor/author-cpd` and `vendor/author-dmn` are shallow snapshots of the authors’ public repositories. `EXPERIMENT_PROTOCOL.md` defines the matched baseline, causal calendar audit, transaction-cost controls, and locked evaluation plan. `scripts/verify_sources.py` checks vendor commit hashes and required files before a CQ job is submitted.

The original paper reports a mean five-window gross Sharpe of 2.16 for its validation-selected change-point model. This repository does not claim to reproduce or exceed that number yet.

## Running the source audit

```bash
python3 scripts/verify_sources.py
```

The next stage is a bounded CQ smoke job, followed by a matched baseline and preregistered ablations. Large data and model outputs belong in the authorized `/date` or `/data` workspace; only provenance, summaries, and reproducible code should be committed here.

## GitHub, Hugging Face, and remote workspaces

GitHub stores code, configuration, protocols, lightweight summaries, and `storage/asset-manifest.json`. Dataset shards, selected recovery checkpoints, and model artifacts belong in private Hugging Face Dataset/Model repositories. The manifest pins each asset to an HF revision and SHA-256; experiments must use that revision instead of a moving `main`.

```bash
# Install and authenticate without putting a token in a file or command history.
python -m pip install huggingface_hub
hf auth login

# Check identity (the token is never printed).
python scripts/hf_assets.py status

# Download only a required file into a remote-server cache/work directory.
PROJECT_CACHE=/date/zyy/hf-cache python scripts/hf_assets.py download \
  --repo-id ORG_OR_USER/private-dataset --repo-type dataset \
  --filename shards/train-00000.parquet --revision REVISION_SHA \
  --local-dir /date/zyy/slow-momentum-fast-reversion/data

# Upload one approved shard or checkpoint; --create creates a private repo.
python scripts/hf_assets.py upload --create \
  --repo-id ORG_OR_USER/private-dataset --repo-type dataset \
  --local-path /date/zyy/slow-momentum-fast-reversion/data/train.parquet \
  --path-in-repo shards/train.parquet --revision main

# Validate files listed in the committed manifest.
python scripts/check_asset_manifest.py --manifest storage/asset-manifest.json
```

Do not upload an entire work directory, virtual environment, cache, credentials, or every intermediate checkpoint. Update the manifest only after recording the exact HF commit and SHA-256, then commit the manifest and code to GitHub. Local cache cleanup is safe only after a remote download and checksum verification succeeds.

## Continuous verification

Every push and pull request runs `scripts/run_source_smoke.py` through GitHub Actions. This verifies the vendored upstream commit markers and confirms that the repository still distinguishes licensed Pinnacle data from the public constructed-data pilot.
