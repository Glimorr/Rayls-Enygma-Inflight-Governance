#!/usr/bin/env python3
"""Offline forensic verifier for genuine saved SHADOW receipts and other bounded evidence.

No RPC calls, private keys, live chain operations or automatic publication.
Authentication: receipt/transaction/block consistency within *saved captured data*.
Fresh canonical validation against a currently running chain requires independent RPC.
"""
from pathlib import Path
from collections import Counter
from datetime import datetime
import json
import sys
import re
import hashlib

ROOT=Path(__file__).resolve().parent
E=ROOT/'evidence'
READ=lambda name:json.loads((E/name).read_text())
H=lambda x:str(x).lower()
ZERO='0x'+'0'*64
A='0xad523115cd35a8d4e60b3c0953e0e0ac10418309'
B='0x4878638df091a638e0df0e5d59e73f639f76499c'
USER_A='0xe3e8bb644ecccfc368333d299c588dff1251c1ac'
USER_B='0xb8e3e1ecacfd2466f6bd4b67b0c5b17f3b6eee22'
ENDPOINT_A='0x4a679253410272dd5232b3ff7cf5dbb88f295319'
EXECUTOR_B='0x84ea74d481ee0a5332c457a4d796187f6ba67feb'
TRANSFER='0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef'
DISPATCH='0xa45ed7e52c0a5c8eaddf0cda36a0b3d1e4f928a09a993ea8c9195bf865351060'
EXECUTED='0x00769f3f82cb2a521c5b72f211aff687dae3cebd0b4631790417d1b17e15689a'
ONE=10**18
trialfiles=['SHADOW_TRIAL1_THREE_CHAIN_CANONICAL_AUDIT.json','SHADOW_TRIAL2_FREEZE_PREFLIGHT_FORENSIC_AUDIT.json','SHADOW_BATCH_T3_FROZEN_TERMINAL_REJECTION.json','SHADOW_BATCH_T4_FULLY_SETTLED.json','SHADOW_BATCH_T5_FULLY_SETTLED.json','SHADOW_BATCH_T6_FROZEN_TERMINAL_REJECTION.json']

def check(value,msg):
    if not value:raise AssertionError(msg)
def addr_topic(address):return '0x'+'0'*24+address.lower()[2:]
def find(logs,token,topic):
    return [l for l in logs if H(l['address'])==H(token) and l['topics'] and H(l['topics'][0])==topic]
def checked_receipt(obj,expected_chain,genesis,expected_tx=None):
    check(obj['chain']==expected_chain,'wrong chain label')
    r=obj['receipt']; b=obj['block'];tx=obj['tx']
    check(H(obj['hash'])==H(r['transactionHash'])==H(tx['hash']),'hash disagreement')
    check(H(r['blockHash'])==H(b['hash'])==H(tx['blockHash']),'block hash disagreement')
    check(int(r['blockNumber'],16)==int(b['number'],16),'block number disagreement')
    check(int(r['status'],16)==1,'receipt not successful')
    check(r['logsBloom'].startswith('0x'),'receipt logsBloom missing')
    check(H(r['from'])==H(tx['from']) and H(r['to'])==H(tx['to']),'transaction sender/recipient mismatch')
    check(int(r['transactionIndex'],16)>=0,'bad transaction index')
    check(obj['hash'].lower()==expected_tx.lower() if expected_tx else True,'receipt not saved tx')
    check(H(genesis[expected_chain]['genesis_hash']).startswith('0x'),'genesis hash missing')
    for l in r['logs']:
        check(H(l['transactionHash'])==H(r['transactionHash']),'event transaction mismatch')
        check(H(l['blockHash'])==H(b['hash']),'event block hash mismatch')
        check(int(l['blockNumber'],16)==int(b['number'],16),'event block number mismatch')
    return r

def message_id(trial,record):
    if trial==3 or trial==6:return record['exact_message_id']
    return record['message_id']

def event_source(rc,mid):
    burns=find(rc['logs'],A,TRANSFER)
    burns=[l for l in burns if len(l['topics'])==3 and H(l['topics'][1])==addr_topic(USER_A) and H(l['topics'][2])==ZERO and int(l['data'],16)==ONE]
    check(len(burns)==1,'source must burn exactly 1 token with original sender')
    dispatches=find(rc['logs'],ENDPOINT_A,DISPATCH)
    dispatches=[l for l in dispatches if len(l['topics'])>=4 and H(l['topics'][1])==H(mid) and int(l['topics'][3],16)==12346 and H(l['topics'][2])==addr_topic(A)]
    check(len(dispatches)==1,'missing exact source MessageDispatched event')

def event_dest(rc,mid):
    mints=find(rc['logs'],B,TRANSFER)
    mints=[l for l in mints if len(l['topics'])==3 and H(l['topics'][1])==ZERO and H(l['topics'][2])==addr_topic(USER_B) and int(l['data'],16)==ONE]
    check(len(mints)==1,'recipient did not receive exactly one ERC20 mint')
    events=find(rc['logs'],EXECUTOR_B,EXECUTED)
    events=[l for l in events if len(l['topics'])>=3 and int(l['topics'][1],16)==12345 and H(l['topics'][2])==H(mid)]
    check(len(events)==1,'missing exact destination MessageIdExecuted event')

raw=READ('RAW_TRIAL_CANONICAL_RECEIPTS.json')
gov=READ('RAW_GOVERNANCE_CANONICAL_RECEIPTS.json')
check({k:v['chain_id'] for k,v in raw['genesis'].items()}=={'A':12345,'H':1337,'B':12346},'wrong 3-chain context')
check(raw['genesis']==gov['genesis'],'governance and transfer genesis mismatch')
check(len(raw['trials'])==6 and len(gov['governance_receipts'])==18,'incomplete dataset')
original=READ('SHADOW_AMENDED_SIX_TRIALS_FINAL_EVIDENCE_SUMMARY.json')
check(original['original_condition_order']==['UNFROZEN','FROZEN','FROZEN','UNFROZEN','UNFROZEN','FROZEN'],'condition order drift')

# Every trial must have authentic source + hub receipts; successful controls also
# require a recipient mint and matching MessageIdExecuted event in the captured block.
seen=set()
for i,record in enumerate(raw['trials'],1):
    check(record['trial']==i and record['condition']==original['original_condition_order'][i-1], 'wrong trial condition')
    saved=READ(trialfiles[i-1])
    mid=message_id(i,saved)
    check(re.fullmatch('0x[0-9a-fA-F]{64}',mid) and mid not in seen,'duplicate or invalid message ID')
    seen.add(mid)
    recs=record['receipts']
    check('source' in recs and 'hub' in recs,'missing source or hub')
    src=saved['source']; hub=saved['hub']
    sourcehash=src.get('hash') or src.get('tx_hash')
    hubhash=hub.get('hash') or hub.get('tx_hash')
    sr=checked_receipt(recs['source'],'A',raw['genesis'],sourcehash)
    hr=checked_receipt(recs['hub'],'H',raw['genesis'],hubhash)
    event_source(sr,mid)
    check(len(hr['logs'])>=1,'Hub expected an actual logged operation')
    native_name=('SHADOW_TRIAL2_NATIVE_HUB_REFERENCE.json' if i==2 else
        ('SHADOW_BATCH_T'+str(i)+'_HUB_CANONICAL.json' if i in (3,4,5,6) else None))
    if native_name:
        native=READ(native_name)
        check(H(native.get('source_tx') or native.get('source_tx_hash'))==H(sourcehash),'native source reference mismatch')
        check(H(native.get('message_id') or native.get('msg_id'))==H(mid),'native message reference mismatch')
        n_hash=native.get('batch_tx_hash_on_private_hub') if i==2 else native['hub']['hash']
        check(H(n_hash)==H(hubhash),'native hub receipt association mismatch')
    if record['condition']=='UNFROZEN':
        check('destination' in recs,'unfrozen trial missing B execution')
        dr=checked_receipt(recs['destination'],'B',raw['genesis'],(saved['destination'].get('hash') or saved['destination'].get('tx_hash')))
        event_dest(dr,mid)
    else:
        check('destination' not in recs,'frozen trial unexpectedly has B execution')
        cts=saved['cts']
        check(cts.get('tx_hash') is None and cts.get('send_attempts')==1 and cts.get('receipt_attempts')==0,'frozen CTS is not pre-broadcast')
        check(cts.get('receipt_status')==0 or cts.get('error')=='RaylsApp__PrivacyNodeFrozen(address)','unexpected frozen failure')
        if i in (3,6):
            cts2=READ('SHADOW_BATCH_T'+str(i)+'_CTS_FROZEN_REJECTION.json')
            check(H(cts2['message_id'])==H(mid),'CTS does not match original message')
            check(cts2['cts']['tx_hash'] is None,'frozen CTS accidentally mined a destination tx')
            check(cts2['decoded_inner_error']=='RaylsApp__PrivacyNodeFrozen(address)','wrong CTS inner failure')
            check(cts2['decoded_outer_error']=='MessageFailure(bytes32,bytes)','wrong CTS outer wrapper')
        else:
            g=READ('SHADOW_TRIAL2_THREE_CHAIN_FREEZE_GATE.json')
            check(H(g['message_id'])==H(mid) and g['states']['hub_frozen_A'] and g['states']['hub_frozen_B'],'T2 freeze gate missing')
        check('NO CANONICAL REVERT' not in str(saved),'bad evidence label')

# Independent canonical freeze/unfreeze operation receipts from both participants and Hub.
bytrial={}
for entry in gov['governance_receipts']:
    i=entry['trial']; chain=entry['participant']; action=entry['action']
    check(i in (2,3,6) and chain in ('H','A','B') and action in ('freeze','unfreeze'),'governance unexpected entry')
    key=(i,chain,action)
    check(key not in bytrial,'duplicate governance action')
    bytrial[key]=entry
    rc=checked_receipt(entry['on_chain'],chain,raw['genesis'],entry['saved']['hash'])
    check(int(rc['blockNumber'],16)==int(entry['saved']['block']),'saved governance block mismatch')
    check(H(rc['blockHash'])==H(entry['saved']['block_hash']),'saved governance block hash mismatch')
check(len(bytrial)==18,'missing governance actions')
for i in (2,3,6):
    payment=raw['trials'][i-1]['receipts']
    same_chain_src=int(payment['source']['receipt']['blockNumber'],16)
    same_chain_hub=int(payment['hub']['receipt']['blockNumber'],16)
    same_chain_a_freeze=int(bytrial[(i,'A','freeze')]['on_chain']['receipt']['blockNumber'],16)
    same_chain_h_freeze=int(bytrial[(i,'H','freeze')]['on_chain']['receipt']['blockNumber'],16)
    check(same_chain_a_freeze>same_chain_src,'A freeze occurred before source acceptance on A')
    check(same_chain_h_freeze>same_chain_hub,'Hub freeze occurred before accepted Hub proof on Hub')
    # This establishes intra-chain ordering only, NOT a shared A/H/B clock.
    for chain in ('H','A','B'):
        freeze=bytrial[(i,chain,'freeze')]['on_chain']['block']
        unfreeze=bytrial[(i,chain,'unfreeze')]['on_chain']['block']
        check(int(unfreeze['number'],16)>int(freeze['number'],16),'unfreeze not after freeze on same chain')
    if i in (3,6):
        gate=READ('SHADOW_BATCH_T'+str(i)+'_FROZEN_GATE.json')
        saved=READ(trialfiles[i-1])
        check(H(gate['message_id'])==H(message_id(i,saved)),'frozen gate wrong reference')
        check(gate['states']['hubA'] and gate['states']['hubB'] and gate['states']['pnA']==4 and gate['states']['pnB']==4,'three freeze flags were not active')
        samples=[json.loads(t) for t in (E/('SHADOW_BATCH_T'+str(i)+'_FROZEN_OBSERVATIONS.jsonl')).read_text().splitlines()]
        check(len(samples)==10,'ten observation samples required')
        times=[datetime.fromisoformat(x['time_utc'].replace('Z','+00:00')) for x in samples]
        check(all(a<b for a,b in zip(times,times[1:])) and (times[-1]-times[0]).total_seconds()>=20,'frozen observation duration not met')
        check(all(x['trial']==i and x['recipient_unchanged'] and x['states']['hubA'] and x['states']['hubB'] and x['states']['pnA']==4 and x['states']['pnB']==4 for x in samples),'frozen observations inconsistent')

bal=READ('FRESH_SHADOW_ERC20_BALANCE_AUDIT.json')
a=int(bal['chain_balances']['a']['user_balance_wei']); b=int(bal['chain_balances']['b']['user_balance_wei'])
check(a==13890000000000000000 and b==3110000000000000000 and a+b==17*ONE,'wrong final financial state')
check(all(int(bal['chain_balances'][chain]['supply_wei'])==int(bal['chain_balances'][chain]['user_balance_wei']) for chain in ['a','b']),'supply/user balance mismatch')
check(int(bal['initial_combined_wei'])-a-b==3*ONE,'not exactly three unreconciled units')
check(int(original['final_expected_cumulative_unreconciled_wei'])==3*ONE,'summary accounting mismatch')
print('PASS: 15 original receipt/block/tx consistency checks and ERC-20 source burn/destination mint/message-event joins')
print('PASS: 18 governance receipts; every H freeze follows its Hub acceptance and every A freeze follows its source acceptance on the SAME chain')
print('PASS: 10 time-ordered samples for each T3/T6 frozen observation, joint freeze flags and timing')
print('PASS: 3 unfrozen exact recipient mints; 3 frozen CTS pre-broadcast rejections; 3-unit supply gap')
print('SCOPE: Offline validation of independently captured RPC snapshots; cannot alone prove historical off-chain timing or later absence of recovery')
