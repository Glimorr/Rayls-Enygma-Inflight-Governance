#!/usr/bin/env python3
"""Fresh read-only chain cross-check for the original already-mined W5 SHADOW references.

Requires accessible, trusted RPC endpoints for the same *isolated* genesis.
Never sends raw transactions or signs. Use the optional Docker runner if RPCs
are reachable only from within the original SHADOW container network.
"""
import argparse,json,subprocess,urllib.request
from pathlib import Path

P=Path(__file__).resolve().parent/'evidence'
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--a',required=True,help='Bank A RPC URL')
parser.add_argument('--hub',required=True,help='Private Hub RPC URL')
parser.add_argument('--b',required=True,help='Bank B RPC URL')
parser.add_argument('--docker-runner',help='Optional running Docker container with curl and access to RPCs')
args=parser.parse_args()
urls={'A':args.a,'H':args.hub,'B':args.b}
targets={'A':12345,'H':1337,'B':12346}
raw=json.loads((P/'RAW_TRIAL_CANONICAL_RECEIPTS.json').read_text())
gov=json.loads((P/'RAW_GOVERNANCE_CANONICAL_RECEIPTS.json').read_text())
allow={'eth_chainId','eth_getBlockByNumber','eth_getTransactionReceipt','eth_getTransactionByHash','eth_call'}
def rpc(chain,method,params):
    if method not in allow:raise RuntimeError('non read-only method')
    url=urls[chain]
    request=json.dumps({'jsonrpc':'2.0','id':1,'method':method,'params':params}).encode()
    if args.docker_runner:
        p=subprocess.run(['docker','exec',args.docker_runner,'curl','--fail','--silent','--show-error','--max-time','6','-H','Content-Type: application/json','--data',request.decode(),url],
            capture_output=True,text=True,timeout=9,check=True)
        response=json.loads(p.stdout)
    else:
        req=urllib.request.Request(url,data=request,headers={'Content-Type':'application/json'})
        with urllib.request.urlopen(req,timeout=7) as result:response=json.load(result)
    if 'error' in response:raise RuntimeError('RPC error '+chain+' '+method)
    return response.get('result')

gen={}
for chain in ('A','H','B'):
    got=int(rpc(chain,'eth_chainId',[]),16)
    if got!=targets[chain]:raise RuntimeError('chain ID mismatch '+chain)
    genesis=rpc(chain,'eth_getBlockByNumber',['0x0',False])
    if genesis['hash'].lower()!=raw['genesis'][chain]['genesis_hash'].lower():
        raise RuntimeError('genesis mismatch '+chain)
    gen[chain]=genesis['hash']
def confirm(row):
    chain=row['chain'];hash_=row['hash']
    rc=rpc(chain,'eth_getTransactionReceipt',[hash_])
    tx=rpc(chain,'eth_getTransactionByHash',[hash_])
    if not rc or not tx:raise RuntimeError('missing canonical transaction '+hash_)
    blk=rpc(chain,'eth_getBlockByNumber',[rc['blockNumber'],False])
    if not blk or rc['blockHash'].lower()!=blk['hash'].lower() or tx['blockHash'].lower()!=blk['hash'].lower():
        raise RuntimeError('canonical block mismatch '+hash_)
    if rc['transactionHash'].lower()!=hash_.lower() or tx['hash'].lower()!=hash_.lower():
        raise RuntimeError('transaction hash mismatch '+hash_)
    if int(rc['status'],16)!=1:raise RuntimeError('transaction failed '+hash_)
    if rc['logs']!=row['receipt']['logs']:raise RuntimeError('event logs differ from saved receipt '+hash_)
    if rc['blockHash'].lower()!=row['block']['hash'].lower():raise RuntimeError('historical snapshot differs '+hash_)
for item in raw['trials']:
    for rec in item['receipts'].values():confirm(rec)
for item in gov['governance_receipts']:confirm(item['on_chain'])
tokens={
'A':('0xad523115cd35a8d4e60b3c0953e0e0ac10418309','0xe3e8bb644ecccfc368333d299c588dff1251c1ac','13890000000000000000'),
'B':('0x4878638df091a638e0df0e5d59e73f639f76499c','0xb8e3e1ecacfd2466f6bd4b67b0c5b17f3b6eee22','3110000000000000000'),
}
for chain,(token,holder,expected) in tokens.items():
    balance=rpc(chain,'eth_call',[{'to':token,'data':'0x70a08231'+holder[2:].rjust(64,'0')},'latest'])
    supply=rpc(chain,'eth_call',[{'to':token,'data':'0x18160ddd'},'latest'])
    if int(balance,16)!=int(expected) or int(supply,16)!=int(expected):
        raise RuntimeError('final ERC20 balance/supply mismatch '+chain)
print('PASS: 3 chain/genesis identities, 15 transaction receipts/logs, 18 governance receipts/logs and 4 latest ERC20 balance/supply checks')
print('Read-only RPC verification completed; no transactions submitted.')
