import hashlib
import settings
import csv

def hash_url(url: str, save: bool = False):
    """
    Bağlantı sağlanacak URL değerini alır, md5 algoritması ile şifreleyip
    url-md5.csv dosyasına kaydeder.
    :param url: md5 ile şifrelenecek URL adresi
    :param save: Eğer şifrelenen url aynı zamanda md5-url dosyasına kaydedilecekse True yapılır.
    :return: md5 ile şifrelenmiş URL değeri
    """
    md5_url = hashlib.md5(f"{url}".encode()).hexdigest()
    if save:
        try:
            with open(f"{settings.DEFAULT_CONTENT_DIR}/url-md5.csv", "r+",
                      encoding='utf-8') as f:

                for i in f:
                    if i.strip() != md5_url:
                        print(md5_url, file=f)
                    else:
                        pass

        except FileNotFoundError as e:
            settings.LOG.error(e)
            with open(f"{settings.DEFAULT_CONTENT_DIR}/url-md5.csv", "w",
                      encoding='utf-8') as f:
                print(md5_url, file=f)
    return md5_url


def save_post_meta(data, file):
    with open(f"{settings.DEFAULT_CONTENT_DIR}/{file}", "a", encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(data)


def create_dom_file(url):
    h_url = hash_url(url)
    try:
        # csv dosya varsa işlem yapmaz, yok ise oluşturur ve başlıkları içine kaydeder.
        with open(f'{settings.DEFAULT_CONTENT_DIR}/DOM/bot-facebook_{h_url}.csv', 'r',
                  encoding='utf-8') as f:
            pass

    except FileNotFoundError as e:
        settings.LOG.error(e)
        with open(f'{settings.DEFAULT_CONTENT_DIR}/DOM/bot-facebook_{h_url}.csv', 'w',
                  encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(["Begeni", "Yorum", "Paylasim"])
