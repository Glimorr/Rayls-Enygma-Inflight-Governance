#!/usr/bin/env python3
"""Adversarial tests: must reject forged receipts, events, governance and chronology."""
from pathlib import Path
import tempfile,shutil,subprocess,json
P=Path(__file__).resolve().parent
casefiles={
    'source-burn-mutated':'RAW_TRIAL_CANONICAL_RECEIPTS.json',
    'destination-message-mutated':'RAW_TRIAL_CANONICAL_RECEIPTS.json',
    'governance-receipt-removed':'RAW_GOVERNANCE_CANONICAL_RECEIPTS.json',
    'observation-shortened':'SHADOW_BATCH_T3_FROZEN_OBSERVATIONS.jsonl',
    'frozen-cts-false-credit':'SHADOW_BATCH_T6_CTS_FROZEN_REJECTION.json',
    'hub-native-reference-falsified':'SHADOW_BATCH_T5_HUB_CANONICAL.json',
    'chain-genesis-swapped':'RAW_TRIAL_CANONICAL_RECEIPTS.json',
    'final-accounting-forged':'FRESH_SHADOW_ERC20_BALANCE_AUDIT.json',
}
def run(where):
    return subprocess.run(['python3',str(where/'verify_research.py')],capture_output=True,text=True,timeout=8)
check=run(P)
assert check.returncode==0,check.stderr
for case,filename in casefiles.items():
    with tempfile.TemporaryDirectory(prefix='w5-negative-') as tmp:
        out=Path(tmp)
        shutil.copytree(P/'evidence',out/'evidence')
        shutil.copy2(P/'verify_research.py',out/'verify_research.py')
        p=out/'evidence'/filename
        if filename.endswith('jsonl'):
            rows=p.read_text().splitlines()
            p.write_text('\n'.join(rows[:2])+'\n')
        else:
            data=json.loads(p.read_text())
            if case=='source-burn-mutated':data['trials'][0]['receipts']['source']['receipt']['logs'][0]['data']='0x'+'0'*64
            elif case=='destination-message-mutated':data['trials'][0]['receipts']['destination']['receipt']['logs'][1]['topics'][2]='0x'+'0'*64
            elif case=='governance-receipt-removed':data['governance_receipts'].pop()
            elif case=='frozen-cts-false-credit':data['cts']['tx_hash']='0x'+'f'*64
            elif case=='hub-native-reference-falsified':data['message_id']='0x'+'c'*64
            elif case=='chain-genesis-swapped':data['genesis']['B']['chain_id']=12345
            elif case=='final-accounting-forged':data['chain_balances']['b']['user_balance_wei']='4110000000000000000'
            p.write_text(json.dumps(data)+'\n')
        result=run(out)
        assert result.returncode!=0,'FORGED DATA NOT REJECTED: '+case
        print('PASS REJECTED',case)
print('PASS CLEAN BASELINE +',len(casefiles),'ADVERSARIAL EVIDENCE MUTATIONS')
