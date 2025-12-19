import hashlib

def hash_kyc_ref(ref: str) -> str:
    return hashlib.sha256(ref.strip().encode()).hexdigest()
