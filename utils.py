import hashlib

import settings
import settings as s


def hash_url(url: str, save: bool = False):
    """
    Bağlantı sağlanacak URL değerini alır, md5 algoritması ile şifreleyip
    url-md5.csv dosyasına kaydeder.
    :param url: md5 ile şifrelenecek URL adresi
    :return: md5 ile şifrelenmiş URL değeri
    """
    md5_url = hashlib.md5(f"{url}".encode()).hexdigest()
    if save:
        try:
            with open(f"{settings.DEFAULT_CONTENT_DIR}/url-md5.csv", "r+") as f:

                for i in f:
                    if i.strip() != md5_url:
                        print(md5_url, file=f)
                    else:
                        pass

        except FileNotFoundError as e:
            s.LOG.error(e)
            with open(f"{settings.DEFAULT_CONTENT_DIR}/url-md5.csv", "w") as f:
                print(md5_url, file=f)
    return md5_url


