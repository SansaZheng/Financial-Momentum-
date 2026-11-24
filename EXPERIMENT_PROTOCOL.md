# Experimental protocol

## Research question

Can causal online Gaussian-process change-point evidence improve net utility beyond an equally tuned no-change-point policy under identical information timing, turnover budget, and transaction costs?

## Baselines

1. Buy-and-hold and classical slow momentum.
2. Plain LSTM/DMN without CPD features.
3. Fixed 63-day CPD feature.
4. Validation-selected CPD horizons, with selection performed only before each locked test window.
5. Cost-aware training control without CPD input.

## Required controls

- features at time `t` may use observations no later than `t-1`;
- target return is from `t` to `t+1`;
- validation decisions precede all test labels and observations;
- gross and net returns, turnover, drawdown, and exposure are reported;
- entry and rebalancing costs are charged with the same convention for every model;
- seeds, package versions, commit SHA, data hash, and output manifest are saved;
- all model selection is frozen before the final locked evaluation.

## Falsification

The CPD contribution is rejected if matched-turnover cost controls explain the gain, if the gain disappears under a locked independent dataset, or if paired block-bootstrap intervals include zero with no robust directional evidence.

## Current status

This protocol is defined. No new performance result is asserted until a CQ execution produces verified outputs.
