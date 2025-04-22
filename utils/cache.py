import hashlib, os

CACHE = "cache/hash.txt"

def is_new_data(df):
    s = df.to_csv(index=False).encode()
    h = hashlib.sha256(s).hexdigest()
    os.makedirs(os.path.dirname(CACHE), exist_ok=True)
    old = None
    if os.path.exists(CACHE):
        old = open(CACHE).read().strip()
    if h == old:
        return False
    open(CACHE, "w").write(h)
    return True