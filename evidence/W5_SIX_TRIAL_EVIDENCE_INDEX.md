# Rayls W5 shadow six-trial forensic evidence index

Generated UTC: 2026-10-31T17:03:34.530436+00:00

**Scope:** isolated local SHADOW setup; 6 measured transfers of 1 W5S1031 Bank A (12345) → private Hub (1337) → Bank B (12346).
**Original sealed condition order:** UNFROZEN, FROZEN, FROZEN, UNFROZEN, UNFROZEN, FROZEN.
**Measured outcomes:** three unfrozen transfers authenticated destination mint; three frozen transfers authenticated exact CTS pre-broadcast `RaylsApp__PrivacyNodeFrozen` rejection and no B mint.
**Token accounting:** Initial combined 20, final Bank A 13.89 and Bank B 3.11, combined 17, three source-burn tokens remain unreconciled.
**Important nuance:** frozen results are NOT mined reverted destination transactions and NOT successful payment settlements.

## Trial-by-trial verified provenance

### Trial 1 — UNFROZEN — Exact destination execution and ERC20 mint
- Source Bank A canonical tx: `0x5fa4974749ffb45f18c4666680e71e539f2a25bbc93f1aeba29a405bf7fd8e7a`
- Hub canonical tx: `0xa30288089ef03b807c8c0eb934f321b04523751f5f38d815263076ff61f78401`
- Bank B outcome tx: `0x74cb297099ea412f6854c4fd417280356020a3cecc80307ae282221b05d22f7b`
- Exact source message ID: `0x7a0f35546764afc7098f24cfdf85a8ad9d2e6440e5ade61ca6796b705c2bafda`
- Evidence file: `SHADOW_TRIAL1_THREE_CHAIN_CANONICAL_AUDIT.json`
- Evidence SHA-256: `584dff177cba43ac75349117fb6292ad41fd2f0b1530bb8393731e2822bb1516`

### Trial 2 — FROZEN — CTS pre-broadcast frozen rejection, source burn unreconciled
- Source Bank A canonical tx: `0x5dcb97b1986f9a4d759ef638c1c05b606ecba905d20353a97bb551754b5c5670`
- Hub canonical tx: `0xf4d4af8885c6ffa9a4682d2006f0b7419f13bfbdeb62109e7fd47aaed78a0d4f`
- Bank B outcome tx: `No destination tx (CTS preflight rejection)`
- Exact source message ID: `0x2ce134b7092c8717710be0076de7a975e3ae5ca33712cf2ae5c84a31b0e05572`
- Evidence file: `SHADOW_TRIAL2_FREEZE_PREFLIGHT_FORENSIC_AUDIT.json`
- Evidence SHA-256: `a2dd08d31ee306fcd320a6b36124e5829597f9d3270502e26cdff15340a263a5`

### Trial 3 — FROZEN — CTS pre-broadcast frozen rejection, source burn unreconciled
- Source Bank A canonical tx: `0xc18be24f8e7e75eeda3d07bd1ed0b3f86fcab8431d7f4de1d381d2871eb64389`
- Hub canonical tx: `0x4069b11207baf4c2d03532533e100a13636d1a55ce78fdb4c6c4593cddaf6544`
- Bank B outcome tx: `No destination tx (CTS preflight rejection)`
- Exact source message ID: `0x578ff14fa9c5c41487b019b5ec84072ee40d6027bb337ec68596aee9434ff600`
- Evidence file: `SHADOW_BATCH_T3_FROZEN_TERMINAL_REJECTION.json`
- Evidence SHA-256: `5237f9c5345bb3067c9758a36dc678528b2eb3f64f44a3523b45d8161a441683`

### Trial 4 — UNFROZEN — Exact destination execution and ERC20 mint
- Source Bank A canonical tx: `0xbb557f707e63971c5115e86472465ca2b927f00661e7dc659cdec233df5ce024`
- Hub canonical tx: `0xe430e200295b3b724d7886eb8786bd8844e8d9c1d3cb84dacaaf73acb9b800d1`
- Bank B outcome tx: `0x775ed63f035788cdb3ff3ea2f253c70645f36bb481b1af4f15f01f8896718978`
- Exact source message ID: `0x9e4ba52aa52d990155d57a15ba4f57969a50b1695d044761d7b142cdb8ae67d1`
- Evidence file: `SHADOW_BATCH_T4_FULLY_SETTLED.json`
- Evidence SHA-256: `ee0696a76ce4d20967b35a87f3bb9669e93d9091f161f5d93e54db8d7534555f`

### Trial 5 — UNFROZEN — Exact destination execution and ERC20 mint
- Source Bank A canonical tx: `0x7bca50293ffbc361bb495b7801b37c8c152669db0cd116e77965c92ebd78c9e8`
- Hub canonical tx: `0x83d68b5edf475dfd644ea97a162f9606e017f0d5f734bcedbc4f279a9b1968e1`
- Bank B outcome tx: `0x03a39e8b33b9e7c68eb7ce664b185ac1c2f32b88061971979414b827cf048419`
- Exact source message ID: `0x0fb068b3cdd4d5b4c9a640714ee3642a77a779e24f8c3c7ed1168d7c559535c3`
- Evidence file: `SHADOW_BATCH_T5_FULLY_SETTLED.json`
- Evidence SHA-256: `80de552cb94dce531654fd223aef56653b7cc2b52cf634979070ee2dfd343088`

### Trial 6 — FROZEN — CTS pre-broadcast frozen rejection, source burn unreconciled
- Source Bank A canonical tx: `0xcb94101191d444671d856c41f73b8875f8dbbdb34174525b7e72a1af501ebbf6`
- Hub canonical tx: `0xb853c41e87706f2ab0992b23aa732fb0a3755d123ff82c1c5988f4e9c364c687`
- Bank B outcome tx: `No destination tx (CTS preflight rejection)`
- Exact source message ID: `0x5366df04e70b0840f61a675101ac77286f440b32311ac90be4185ce9c12b7498`
- Evidence file: `SHADOW_BATCH_T6_FROZEN_TERMINAL_REJECTION.json`
- Evidence SHA-256: `e1739a2704c2a9bdcaac6b0e4808bda2748f983225e6124e8f98ebf3203b720a`

## Additional essential evidence

- `SHADOW_TRIAL2_FREEZE_PREFLIGHT_FORENSIC_AUDIT.json`: exact CTS correlation, `MessageFailure(bytes32,bytes)` wrapping `RaylsApp__PrivacyNodeFrozen(address)`.
- `SHADOW_BATCH_T3_CTS_FROZEN_REJECTION.json` and `SHADOW_BATCH_T6_CTS_FROZEN_REJECTION.json`: exact source-message CTO records with no destination transaction hash.
- `SHADOW_BATCH_T3_FROZEN_OBSERVATIONS.jsonl` and `SHADOW_BATCH_T6_FROZEN_OBSERVATIONS.jsonl`: ten timestamped host observations each while freezes were active.
- `SHADOW_TRIAL2_RECOVERY_ACCOUNTING_CANONICAL_AUDIT.json`: no source refund and unresolved source burn after Trial 2.
- `SHADOW_TRIALS3_TO6_AFTER_T2_PREFLIGHT_REJECTION_AMENDMENT.json`: PROSPECTIVE change to permit tracking unresolved burns and continuing trials; drafted after observing T2.
- `SHADOW_TRIALS5_TO6_POST_T4_SCAN_CORRECTION_AMENDMENT.json`: T4 independent canonical correction; audit scanner initially contained a mistyped destination endpoint literal.
- `SHADOW_BATCH_T4_OUTCOME_UNSETTLED.json`: preserve original false-negative scan as an honest QA failure, do not delete.
- `SHADOW_AMENDED_SIX_TRIALS_FINAL_EVIDENCE_SUMMARY.json`: six verified terminal outcome summary.

## Interpretation constraints

- Distinguish user-source burn, Hub acceptance, CTS preflight, actual mined destination tx and Bank B ERC20 mint.
- Do not claim freeze stopped Hub acceptance; in this design Hub acceptance was proven before freezing.
- Do not infer a mined revert from native relayer `outcome = reverted`; pinned CTS treats a pre-broadcast simulation error as a reverted result.
- Do not claim permanent loss: no refund is observed, but supported recovery beyond this run was not conclusively exhausted.
- Do not claim isolation of all causal roles for Hub freeze versus local Bank A/B freeze: local Bank B guard error is the identified immediate enforcement point.
- Do not claim protocol preregistration stayed intact throughout: both prospective amendments must be disclosed, including the after-T2 settlement continuation and the after-T4 audit correction.
- Sample size = 3 conditions each; descriptive evidence, not a privacy/security guarantee or production prevalence estimate.
