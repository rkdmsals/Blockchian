from Crypto.PublicKey import DSA
from Crypto.Signature import DSS
from Crypto.Hash import SHA256
import binascii
from Main import blocks, AlicePubKey, AliceKey


# 각 블록 검증
for i, block in enumerate(blocks, start=1):
    message = bytes(block, 'utf-8')
    hash_obj = SHA256.new(message)

    # 앨리스가 각 블록에 대해 서명
    signer = DSS.new(AliceKey, 'fips-186-3')
    signature = signer.sign(hash_obj)

    print(f"Hash of Block {i}: {hash_obj.hexdigest()}")
    signature_hex = binascii.hexlify(signature)
    print(f"Signature of Block {i}: {signature_hex}")

    pub_key = DSA.construct(AlicePubKey)

    # 블록 서명 검증
    hash_obj = SHA256.new(message)
    verifier = DSS.new(pub_key, 'fips-186-3')
    signature = binascii.unhexlify(signature_hex)

    try:
        verifier.verify(hash_obj, signature)
        print(f"Block {i}: Alice's message is authentic.")
    except ValueError:
        print(f"Block {i}: Alice's message is not authentic.")
