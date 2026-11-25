# CQ status

The GitHub source package is ready at commit `2d081bd59381b94e39547cc5256a73393d225093`.

The first CPU-only smoke submission was rejected by CQ because its `code.git` repository must be owned by `SuuTTT`, while the canonical repository is owned by `SansaZheng`. No job was created and no unrelated CQ job was touched.

The canonical repository is now actively maintained through the `SuuTTT` GitHub permission. Required compute-side resolution: update the CQ GitHub allow-list for `SansaZheng/Financial-Momentum-`, or provide an explicitly authorized `SuuTTT` mirror. Do not silently copy the project into an unrelated repository.

Retry on 2026-11-26 with commit `8cec31377981470c9259e1f892a478d06f80a47c` produced the same pre-submission rejection. No CQ job was created.
