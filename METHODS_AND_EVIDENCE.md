# Experiment design, evidence, and reproducibility

> Independent local Rayls Enygma research by Glimor (October 2026). The study is confined to the SHADOW test deployment, not a live financial system.

## Research question

After source and Private Hub acceptance, can a joint Hub/Bank A/Bank B freeze prevent the destination from crediting a payment in flight, and what happens to the source debit?

## Conditions and exact identifiers

Six 1-token payments, with the original condition order: **U, F, F, U, U, F**.

| Trial | Condition | Source tx (A) | Hub tx (H) | Destination tx (B) | Outcome |
|---|---|---|---|---|---|
| 1 | UNFROZEN | `0x5fa4974749ff…` | `0xa30288089ef0…` | `0x74cb297099ea…` | Mint 1 |
| 2 | FROZEN | `0x5dcb97b1986f…` | `0xf4d4af8885c6…` | No B tx hash | CTS pre-broadcast frozen rejection |
| 3 | FROZEN | `0xc18be24f8e7e…` | `0x4069b11207ba…` | No B tx hash | CTS pre-broadcast frozen rejection |
| 4 | UNFROZEN | `0xbb557f707e63…` | `0xe430e200295b…` | `0x775ed63f0357…` | Mint 1 |
| 5 | UNFROZEN | `0x7bca50293ffb…` | `0x83d68b5edf47…` | `0x03a39e8b33b9…` | Mint 1 |
| 6 | FROZEN | `0xcb94101191d4…` | `0xb853c41e8770…` | No B tx hash | CTS pre-broadcast frozen rejection |

The full 32-byte references, mined logs, receipts, block headers, genesis hashes, and original message IDs are provided in `evidence/RAW_TRIAL_CANONICAL_RECEIPTS.json` and the per-trial audit files. Do not infer cross-chain timing by comparing A/H/B block heights.

## What the stronger verifier actually checks

Run:

```sh
python3 verify_evidence.py
python3 verify_research.py
python3 test_verifier.py
sha256sum -c EVIDENCE_SHA256SUMS.txt
```

- Six records on chain A: ERC-20 burn of exactly 1 token plus exact `MessageDispatched` with matching 32-byte message ID and destination chain 12346.
- Six source-associated Hub receipts: direct receipt, original transaction and block identity, with the Hub message association backed by native-relayer reference records. This relationship is not claimed as a cryptographic proof solely from a Hub event.
- Three successful B receipts: `MessageIdExecuted` joins the exact source message ID and `Transfer` mints exactly 1 token from address zero to the known recipient.
- Eighteen governance receipts: freeze/unfreeze actions at Hub, Bank A and Bank B on the three frozen trials, canonical inclusion and the order of freeze before unfreeze **on the same chain**.
- Three frozen CTS failure records: no broadcast hash, zero destination receipt attempts, and recorded preflight `RaylsApp__PrivacyNodeFrozen(address)` result.
- Frozen hold time: T3 and T6 have ten sequential sampled snapshots each, with true freeze flags and unchanged recipient balance. The snapshots are operator-observed measurements rather than signed on-chain timestamps.
- Full final supply: 20 initial units versus 13.89 at A and 3.11 at B, leaving three units unresolved in this local workflow.

`test_verifier.py` independently tests that eight material manipulations of preserved evidence cause rejection, including a changed burn amount, a changed execution message ID, missing governance receipt, shortened frozen window, forged CTS broadcast, changed Hub correlation, changed chain identity, and altered final balance.

## Experimental controls and protocol chronology

- Initial protocol: `evidence/W5_PREREGISTERED_SCIENTIFIC_PROTOCOL.json` (before original freeze experiment), plus a separate `SHADOW_PRETRIAL_PROTOCOL_AMENDMENT.json` explicitly splitting the experiments.
- Joint freeze was applied after source + Hub acceptance and before releasing the destination relayer, with a minimum 20-second hold observation.
- Unfrozen Trials 1, 4 and 5 are real successful local-chain controls, rather than simulated payments.
- A separate positive sensitivity control used mint-path simulation before, during and after freeze; it did not create another real payment trial.
- Trial 2 resulted in an unresolved debit, triggering the **prospective** `SHADOW_TRIALS3_TO6_AFTER_T2_PREFLIGHT_REJECTION_AMENDMENT.json` continuation rule before later trials.
- A destination endpoint scanner typo led to a false negative in the first Trial 4 analysis. A subsequent independent receipt audit established an actual mint; the correction and later continuation amendment are preserved.
- For T2, the preserved bounded B block scan documents what was examined. A new full-history B execution event scan was not completed as part of the later QA due to tool restrictions; it is not claimed as a passing independent test.

## Governance semantics and limits

Rayls distinguishes a Hub-managed freeze list for a token/participant from a local Privacy Node freeze. The local freeze can block minting with `RaylsApp__PrivacyNodeFrozen`.
All three intervention flags were applied together in our frozen cases. We **did not independently isolate** the contribution of the Hub flag from Bank A and Bank B local flags.
Our matched observations support a causal enforcement mechanism in this controlled deployment, but not universal production reliability.
The 3 source burns were **not automatically compensated in the observed follow-up**. This is not evidence of permanent fund loss and not proof that Rayls has no approved recovery route. No post-freeze same-reference recovery was executed for those SHADOW trials.

## Environment and reproducibility boundary

Chain IDs: A 12345, Hub 1337, B 12346. Exact genesis hashes are in the raw receipt dataset.
The captured Docker, Compose and container image IDs are in `evidence/SHADOW_RUNTIME_PROVENANCE_QA_SNAPSHOT.json`.
These observations document the environment at QA, not an independent signed build attestation linking each image to a commit. Relayer B used a modified research image; do not generalize its behavior to an unmodified release.
This repository enables offline reconstruction and checking of previously captured evidence. It does not start or clone a fresh Rayls network with the same states.
The earlier original Codex W5 environment was a separate deployment, and its unfinished 10-unit reference remains unresolved.

## Primary sources

- [Rayls: Freezing tokens](https://docs.rayls.com/docs/freezing-tokens)
- [Rayls: How Enygma works](https://docs.rayls.com/docs/how-enygma-works)
- [Rayls: Sending Enygma transactions](https://docs.rayls.com/docs/send-enygma-transactions)
- [Rayls relayer source — pinned experimental revision](https://github.com/raylsnetwork/rayls-sovereign-relayer/tree/b01b427de4cfc2ac66e75eba0d5070b73a3b137c)

The documentation explains the intended compensation model for failed transfers. Our specific local CTS pre-broadcast failure path did not display automatic compensation during our observations; the correct supported recovery path remains an open question for the Rayls team.
