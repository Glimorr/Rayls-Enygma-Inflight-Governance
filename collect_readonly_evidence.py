#!/usr/bin/env python3
"""Capture already mined SHADOW receipts, block headers and genesis through read-only RPC.
This script cannot sign or submit transactions. Run only against isolated W5 SHADOW Docker.
"""
from pathlib import Path
import subprocess,json,datetime
ROOT=Path(__file__).resolve().parent
S=ROOT.parent.parent/'w5-shadow-freeze-20261031'
E=ROOT/'evidence'
E.mkdir(exist_ok=True)
RUNNER='rayls-w5-shadow-20261031-private-hub-1'
TARGETS={'A':('http://rayls-w5-shadow-20261031-pn-a-1:8545',12345),
         'H':('http://127.0.0.1:3445',1337),
         'B':('http://rayls-w5-shadow-20261031-pn-b-1:8546',12346)}
def rpc(chain, method, params):
    if method not in ('eth_chainId','eth_getBlockByNumber','eth_getTransactionReceipt','eth_getTransactionByHash'):
        raise RuntimeError('read-only method allowlist')
    request=json.dumps({'jsonrpc':'2.0','id':1,'method':method,'params':params})
    process=subprocess.run(['docker','exec',RUNNER,'curl','-sS','--max-time','6',
        '-H','Content-Type: application/json','-d',request,TARGETS[chain][0]],
        text=True,capture_output=True,timeout=9,check=True)
    response=json.loads(process.stdout)
    if response.get('error'):raise RuntimeError('RPC error for '+chain+' '+method)
    return response.get('result')
genesis={}
for chain,(url,expected) in TARGETS.items():
    actual=int(rpc(chain,'eth_chainId',[]),16)
    if actual!=expected:raise RuntimeError('wrong chain ID: '+chain)
    block=rpc(chain,'eth_getBlockByNumber',['0x0',False])
    genesis[chain]={'chain_id':actual,'genesis_hash':block['hash']}
audit=['SHADOW_TRIAL1_THREE_CHAIN_CANONICAL_AUDIT.json',
'SHADOW_TRIAL2_FREEZE_PREFLIGHT_FORENSIC_AUDIT.json',
'SHADOW_BATCH_T3_FROZEN_TERMINAL_REJECTION.json',
'SHADOW_BATCH_T4_FULLY_SETTLED.json',
'SHADOW_BATCH_T5_FULLY_SETTLED.json',
'SHADOW_BATCH_T6_FROZEN_TERMINAL_REJECTION.json']
def hget(ob):
    return (ob.get('hash') or ob.get('tx_hash')) if isinstance(ob,dict) else None
def fetch(chain,hash_):
    rc=rpc(chain,'eth_getTransactionReceipt',[hash_])
    if not rc or rc['transactionHash'].lower()!=hash_.lower():
        raise RuntimeError('missing receipt '+hash_)
    height=rc['blockNumber']
    block=rpc(chain,'eth_getBlockByNumber',[height,False])
    tx=rpc(chain,'eth_getTransactionByHash',[hash_])
    if not block or not tx or rc['blockHash']!=block['hash'] or tx['hash'].lower()!=hash_.lower():
        raise RuntimeError('receipt missing canonical block or original transaction '+hash_)
    if int(rc['status'],16)!=1:raise RuntimeError('expected successful receipt '+hash_)
    return {'chain':chain,'hash':hash_,'receipt':rc,
        'block':{'number':block['number'],'hash':block['hash'],'parentHash':block['parentHash'],'timestamp':block['timestamp']},
        'tx':{'hash':tx['hash'],'blockHash':tx['blockHash'],'from':tx['from'],'to':tx['to'],'nonce':tx['nonce'],'input':tx['input'][:10]}}
trials=[]
for i,n in enumerate(audit,1):
    data=json.loads((S/n).read_text())
    row={'trial':i,'condition':'UNFROZEN' if i in (1,4,5) else 'FROZEN','receipts':{}}
    for key,chain in [('source','A'),('hub','H'),('destination','B')]:
        txhash=hget(data.get(key))
        if txhash:row['receipts'][key]=fetch(chain,txhash)
        elif key!='destination':raise RuntimeError('missing expected receipt '+n+' '+key)
    if (i in (1,4,5)) != ('destination' in row['receipts']):
        raise RuntimeError('wrong trial receipt pattern')
    trials.append(row)
governance=[]
for i in (2,3,6):
    prefix='SHADOW_TRIAL2_GOV_' if i==2 else 'SHADOW_BATCH_T'+str(i)+'_GOV_'
    for ch in ('H','A','B'):
        for action in ('freeze','unfreeze'):
            p=S/(prefix+ch+'_'+action+'.verified')
            x=json.loads(p.read_text())
            rec=fetch(ch,x['hash'])
            if rec['block']['hash'].lower()!=x['block_hash'].lower():raise RuntimeError('governance original mismatch '+p.name)
            governance.append({'trial':i,'action':action,'participant':ch,'saved':x,'on_chain':rec})
created=datetime.datetime.now(datetime.timezone.utc).isoformat()
receipts={'capture_utc':created,'method':'read-only eth_chainId eth_getBlockByNumber eth_getTransactionReceipt eth_getTransactionByHash; already-mined only',
 'genesis':genesis,'trials':trials,
 'limitation':'Historical receipts freshly authenticated against chain block lookups; does not cryptographically timestamp independent governance scheduling across chains.'}
gov={'capture_utc':created,'genesis':genesis,'governance_receipts':governance,
'limitation':'Governance inclusion does not itself prove exact timing relative to off-chain relayer release; precommitted gate and sampled observations are separate evidence.'}
for name,data in [('RAW_TRIAL_CANONICAL_RECEIPTS.json',receipts),('RAW_GOVERNANCE_CANONICAL_RECEIPTS.json',gov)]:
    file=E/name
    if file.exists():raise RuntimeError('output already exists; preserve previous capture: '+name)
    file.write_text(json.dumps(data,indent=2)+'\n')
print('EXPORTED_TRIAL_RECEIPTS',sum(len(t['receipts']) for t in trials))
print('EXPORTED_GOVERNANCE_RECEIPTS',len(governance))
print('GENESIS',genesis)
print('WRITTEN_RAW_DATASETS 2')
