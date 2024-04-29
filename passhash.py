import hashlib

def hash_password(password):
    sha256_hash = hashlib.new('sha256')
    data = password.encode()
    sha256_hash.update(data)
    return sha256_hash.hexdigest()
