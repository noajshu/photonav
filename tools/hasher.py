import hashlib


BUF_SIZE = 65536

def md5(fpath):
    md5 = hashlib.md5()
    with open(fpath, 'rb') as infile:
        while True:
            data = infile.read(BUF_SIZE)
            if not data:
                break
            md5.update(data)

    return md5.hexdigest()
