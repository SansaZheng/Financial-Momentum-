# Preregistered evidence matrix

The current repository distinguishes mechanism evidence from financial evidence. Synthetic panels are used only to test whether a claimed mechanism reacts to trend flips, variance-only changes, and no-change negatives. They cannot establish trading performance.

The financial matrix must contain, for every dataset and fold:

| family | CPD input | cost objective | locked test | required output |
|---|---:|---:|---:|---|
| plain LSTM/DMN | no | gross | yes | daily gross/net returns |
| fixed CPD | yes | gross | yes | scores, turnover, returns |
| selected CPD | yes | gross | yes | selection trace, returns |
| cost control | no | net | yes | matched-turnover comparison |
| proposed gate | yes | net | yes | gate decisions, returns |

No model may be selected using the locked test period. The primary comparison is paired net-return difference under the same asset universe, delay, turnover budget, and bootstrap procedure. A positive headline Sharpe on a different public dataset is not evidence of beating the paper.
