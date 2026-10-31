from pathlib import Path
import hashlib,json,re
p=Path(__file__).resolve().parent/"evidence"
index=(p/"W5_SIX_TRIAL_EVIDENCE_INDEX.md").read_text()
names=["SHADOW_TRIAL1_THREE_CHAIN_CANONICAL_AUDIT.json","SHADOW_TRIAL2_FREEZE_PREFLIGHT_FORENSIC_AUDIT.json","SHADOW_BATCH_T3_FROZEN_TERMINAL_REJECTION.json","SHADOW_BATCH_T4_FULLY_SETTLED.json","SHADOW_BATCH_T5_FULLY_SETTLED.json","SHADOW_BATCH_T6_FROZEN_TERMINAL_REJECTION.json"]
parts=index.split("### Trial ")[1:]
assert len(parts)>=6
for i,name in enumerate(names,1):
    section=next(x for x in parts if x.startswith(str(i)+" —"))
    expected=re.search(r"Evidence SHA-256:\s*\x60?([a-f0-9]{64})",section)
    assert expected and hashlib.sha256((p/name).read_bytes()).hexdigest()==expected.group(1), "FAIL trial "+str(i)
    assert json.loads((p/name).read_text()).get("trial")==i
s=json.loads((p/"SHADOW_AMENDED_SIX_TRIALS_FINAL_EVIDENCE_SUMMARY.json").read_text())
assert s["original_condition_order"]==["UNFROZEN","FROZEN","FROZEN","UNFROZEN","UNFROZEN","FROZEN"]
assert s["final_expected_cumulative_unreconciled_wei"]=="3000000000000000000"
r=json.loads((p/"FRESH_SHADOW_CANONICAL_RPC_AUDIT.json").read_text())
assert r["canonical_receipts_checked"]==15 and r["all_checked_canonical"]
b=json.loads((p/"FRESH_SHADOW_ERC20_BALANCE_AUDIT.json").read_text())
assert b["final_combined_wei"]=="17000000000000000000"
print("PASS: six indexed file hashes, six-trial order, accounting, and saved live-RPC audit structure")
print("Scope: offline integrity check, not independent fresh RPC authentication")
