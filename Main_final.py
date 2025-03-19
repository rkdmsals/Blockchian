import hashlib
import json
from Crypto.PublicKey import DSA
from Crypto.Signature import DSS
from Crypto.Hash import SHA256

# 블록 생성 함수
def create_block(previous_hash, tx_id, nonce, value, script_pub_key, key):
    block = {
        'TxID': tx_id,
        'Hash': previous_hash,
        'Nonce': nonce,
        'Input': {
            "Previous TX": previous_hash,
            "Index": 0,
            "ScriptSig": key.x
        },
        'Output': {
            "Value": value,
            "ScriptPubKey": f"{script_pub_key} OP_CHECKSIG"
        }
    }
    block_json = json.dumps(block, sort_keys=True, indent=4, separators=(',', ':'))
    return block_json

# 앨리스와 밥의 키 생성
AliceKey = DSA.generate(1024)
BobKey = DSA.generate(1024)
AlicePubKey = [AliceKey.y, AliceKey.g, AliceKey.p, AliceKey.q]
BobPubKey = [BobKey.y, BobKey.g, BobKey.p, BobKey.q]

# 제네시스 블록 생성
genesis_block = create_block("This is the Genesis block.", 0, 0, 1, AlicePubKey, AliceKey)
HashGenesis = hashlib.sha256(genesis_block.encode()).hexdigest()
print(genesis_block)
print(HashGenesis)

fw = open("block0.txt", "w+")
fw.write(genesis_block)
fw.close()

# 초기 변수 설정
limit = "0x0000ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff"
limit_int = int(limit, 16)
Nonce = 0
blocks = []

# 블록 생성 및 체인 완성
while len(blocks) < 10:
    block = create_block(HashGenesis, len(blocks) + 1, Nonce, 1, BobPubKey, AliceKey)
    HashBlock = hashlib.sha256(block.encode()).hexdigest()
    HashBlock_int = int(HashBlock, 16)

    if HashBlock_int < limit_int:
        blocks.append(block)
        with open(f"block{len(blocks)}.txt", "w+") as fw:
            fw.write(block)
        Nonce = 0
        HashGenesis = HashBlock
    else:
        Nonce += 1

print(blocks)