import random
import hashlib



def SALT(H):
    v = random.randint(1000000000,9999999999)
    v=str(v)
    h2 = hashlib.sha512((v+H).encode('utf-8')).hexdigest()
    return v,h2

