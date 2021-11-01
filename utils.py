import hashlib
import settings as s

def hash_url(url):
    md5_url = hashlib.md5(f"{url}".encode()).hexdigest()
    try:
        with open("url-md5.csv", "r+") as f:
            print("break-")

            for i in f:
                if i.strip() != md5_url:
                    print(md5_url, file=f)
                else:
                    pass

    except FileNotFoundError as e:
        s.LOG.error(e)
        with open("url-md5.csv", "w") as f:
            print(md5_url, file=f)
    return md5_url
