# Evidence-to-claim matrix

Independent local Rayls Private Network vanilla ERC-20 SHADOW study (October 2026). **This is not a production security assessment.**

| Scientific claim | Highest-strength available evidence | What is *not* established |
|---|---|---|
| Six real 1-token source payments occurred | 6 canonical Bank A receipts + exact ERC-20 burns and `MessageDispatched` logs; `verify_research.py` | None of this proves a production deployment |
| All six payments reached a matching Hub batch | 6 canonical Hub receipts plus exact source/message association from saved native relayer records | The Hub log alone is not a cryptographic independent source-to-hidden-recipient proof |
| 3/3 unfrozen cases settled | 3 Bank B canonical receipts: exact `MessageIdExecuted` matching the A message ID and 1-token zero-address-to-recipient mint | Does not establish broader network reliability |
| 3/3 frozen cases were stopped before B broadcast | 3 exact CTS failed-preflight records; B tx hash null; 18 governance freeze/unfreeze receipts; tested local mint revert | Does not show mined destination reverts; absence of every conceivable future replay was not established |
| Governance had been applied during a controlled hold | On-chain governance receipt pairs, true freeze flags in gate snapshots, 10 ordered T3/T6 hold observations, T2 bounded block scan | Off-chain gate timing is operator-recorded; different chain block heights cannot order events globally |
| Freeze caused the immediate failure in this local test | CTS `MessageFailure` wrapping `RaylsApp__PrivacyNodeFrozen` plus positive local mint simulation; unfrozen controls minted | The independent contribution of Hub, Bank A and Bank B freezes was not isolated |
| Three units remained unreconciled in the observed follow-up | Latest independent read-only `eth_call` of ERC-20 user balances and total supplies: A13.89, B3.11, combined17 vs initial20 | No claim of permanent loss, protocol-wide defect or proof that an approved recovery path cannot work |
| The original scientific hypothesis received local experimental support | Three frozen versus three matched unfrozen trials, predeclared condition order and independent receipts | Protocol changed prospectively after T2; only three samples per condition |
| Audit files were not silently altered | SHA-256 manifest, six original indexed hashes, pass/fail verifier and eight tamper tests | Internal SHA-256 hashes do not independently timestamp preregistration or prove chain state without live RPC |

## Exact scientific boundary

The primary question was whether a joint governance freeze **after successful source/Hub acceptance and before Bank B release** could prevent destination credit. The controlled SHADOW experiment supplies evidence that it can, with a CTS pre-broadcast frozen rejection.

The secondary question of approved compensation or same-reference settlement after unfreezing remains unanswered. The original separate W5 Codex deployment also remains unrestored with its own outstanding 10-unit reference. Neither was counted as a successful recovery.

## Provenance

- `RAW_TRIAL_CANONICAL_RECEIPTS.json`: 15 actual source/Hub/B transaction receipts, logs and block headers, freshly obtained read-only from live SHADOW nodes.
- `RAW_GOVERNANCE_CANONICAL_RECEIPTS.json`: 18 canonical Hub, A and B freeze/unfreeze transaction receipts.
- `verify_research.py`: independent offline EVM event/topic/message/amount reconstruction.
- `verify_live_chain.py`: separate read-only RPC verification when same-genesis SHADOW RPCs are reachable.
- `SHADOW_RUNTIME_PROVENANCE_QA_SNAPSHOT.json`: observed Docker/Compose versions and image IDs; not a signed build attestation.
- `SHADOW_TRIALS3_TO6_AFTER_T2_PREFLIGHT_REJECTION_AMENDMENT.json`: prospective continuation change after observing the first frozen rejection.
- `SHADOW_TRIALS5_TO6_POST_T4_SCAN_CORRECTION_AMENDMENT.json`: documented scanner correction.

## Open technical question for the Rayls maintainers

> For a standard ERC-20 `crosschain.vanilla` transfer whose source burn and Hub transaction already succeeded, if Bank B CTS rejects delivery before broadcasting a destination transaction with `MessageFailure(RaylsApp__PrivacyNodeFrozen)`, which native component is expected to initiate same-reference compensation, and what is the supported recovery procedure after governance is restored? In three controlled local trials, no automatic credit or refund was observed.

This is a question arising from our controlled local deployment, **not** an allegation of a general Rayls vulnerability.

## Primary documentation

- [Rayls freezing tokens](https://docs.rayls.com/docs/freezing-tokens)
- [Rayls standard cross-chain transaction lifecycle](https://docs.rayls.com/docs/how-a-cross-chain-transaction-works)
- [Rayls ERC-20 teleport handlers](https://docs.rayls.com/docs/raylserc20handler)
- [Pinned relayer source revision](https://github.com/raylsnetwork/rayls-sovereign-relayer/tree/b01b427de4cfc2ac66e75eba0d5070b73a3b137c)
