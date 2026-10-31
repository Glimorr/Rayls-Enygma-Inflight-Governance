# Can a Bank Stop a Cross-Chain Payment Already in Flight?

Independent Rayls Enygma SHADOW study by Glimor. Six 1-token trials in a new isolated local three-chain environment.

## Method and results

Chain A 12345, Private Hub 1337, destination B 12346.
The predeclared trial order was UNFROZEN, FROZEN, FROZEN, UNFROZEN, UNFROZEN, FROZEN.

| Trial | Condition | Measured result |
|---|---|---|
| 1 | Unfrozen | Authenticated B receipt and 1-token mint |
| 2 | Frozen | CTS pre-broadcast frozen rejection, no B credit |
| 3 | Frozen | CTS pre-broadcast frozen rejection, no B credit |
| 4 | Unfrozen | Authenticated B receipt and 1-token mint |
| 5 | Unfrozen | Authenticated B receipt and 1-token mint |
| 6 | Frozen | CTS pre-broadcast frozen rejection, no B credit |

Final live RPC verified balances and total supplies: A 13.89, B 3.11; combined 17 versus initial 20.
The 3 tokens burned at source in frozen cases remained unreconciled in the observed workflow.
This is NOT proof of permanent loss or that no approved recovery path exists.

## Evidence quality

All six saved evidence files matched their originally indexed SHA-256 digests.
An additional read-only SHADOW RPC audit directly checked 15 canonical receipts and the final ERC-20 balances.
Frozen outcomes were CTS pre-broadcast rejection, NOT destination mined reversions.
The positive freeze-sensitivity control used a local mint simulation, not a seventh real payment.

## Mandatory scope disclosures

The original W5 environment is distinct: its freeze trial stopped after 4/11 operations, and an old 10-unit reference remains unresolved.
After observing Trial 2, the continuation protocol was amended prospectively to track unresolved source burns; this was NOT the original preregistered gate.
After Trial 4, an independent audit corrected a destination endpoint-address scanner typo. Its original false-negative finding is preserved in private provenance.
Only three observations per condition were obtained. We cannot generalize to network-wide or production reliability.
Observed local Bank B freeze enforcement does not isolate the individual causal contribution of the Hub and Bank A flags.
No full-history fresh destination event scan was conducted in this preparation stage.

## Independent verification upgrade

- **[Full methods, experimental lineage and boundaries](METHODS_AND_EVIDENCE.md)**
- **[Claims and precise evidence limits](CLAIMS_AND_LIMITS.md)** — independent assertion-by-assertion audit and the legitimate team recovery question. — specific claim-to-receipt evidence, amendments, source and governance context.
- **[15 raw payment receipts](evidence/RAW_TRIAL_CANONICAL_RECEIPTS.json)** with source/H/B blocks and logs.
- **[18 canonical governance receipts](evidence/RAW_GOVERNANCE_CANONICAL_RECEIPTS.json)** for freeze/unfreeze at all three ledgers for Trials 2, 3 and 6.
- **[Strong offline forensic verifier](verify_research.py)** checks receipt/block joins, source burns, destination mints, exact message IDs, governance actions, frozen timing and accounting.
- **[Eight adversarial negative tests](test_verifier.py)** verify that forged or mismatched records fail closed.
- **[Read-only live RPC checker](verify_live_chain.py)** can independently validate preserved data when the original isolated chain nodes are available.
- **[Image and runtime provenance](evidence/SHADOW_RUNTIME_PROVENANCE_QA_SNAPSHOT.json)** includes Docker and Compose versions, image IDs, and honest source-to-binary limitations.

## Reproduction

Run python3 verify_evidence.py from this directory to verify the indexed hashes and condition/accounting structure offline.
This offline check alone does not authenticate live blockchain transactions; consult the fresh read-only audit and full raw evidence provenance.

Do not publish the entire original working directory; it contains local credentials, restricted files and secrets.
