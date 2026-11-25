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

## Continuous verification

Every push and pull request runs `scripts/run_source_smoke.py` through GitHub Actions. This verifies the vendored upstream commit markers and confirms that the repository still distinguishes licensed Pinnacle data from the public constructed-data pilot.
