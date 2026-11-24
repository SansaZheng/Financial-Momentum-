# CQ status

The GitHub source package is ready at commit `2d081bd59381b94e39547cc5256a73393d225093`.

The first CPU-only smoke submission was rejected by CQ because its `code.git` repository must be owned by `SuuTTT`, while the canonical repository is owned by `SansaZheng`. No job was created and no unrelated CQ job was touched.

Required resolution: update the CQ GitHub allow-list for `SansaZheng/Financial-Momentum-`, or provide an explicitly authorized `SuuTTT` mirror. Do not silently copy the project into an unrelated repository.
