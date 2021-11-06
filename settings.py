import argparse
import logging

from pathlib import Path

#Proje yolu
BASE_DIR = Path(__file__).resolve().parent

# İçerik ayarları
DEFAULT_CONTENT_DIR = Path.joinpath(BASE_DIR, 'content')
DEFAULT_MEDIA_DIR = Path.joinpath(DEFAULT_CONTENT_DIR, 'media')


# Tarayıcı parametreleri
BROWSER_DRIVER_DIR = Path.joinpath(BASE_DIR, "drivers/chromedriver.exe")

DATE = {
    "01": "Ocak", "02": "Şubat",
    "03": "Mart", "04": "Nisan",
    "05": "Mayıs", "06": "Haziran",
    "07": "Temmuz", "08": "Ağustos",
    "09": "Eylül", "10": "Ekim",
    "11": "Kasım", "12": "Aralık",
}

# Log parametreleri
LOG = logging
LOG.basicConfig(filename=f'{DEFAULT_CONTENT_DIR}/logs.log', filemode='a',
                           format="%(asctime)s %(message)s",
                           level=logging.DEBUG)

# Konsol parametreleri
ARGS = argparse.ArgumentParser(exit_on_error=False)
ARGS.add_argument('-p', '--page', required=False, type=str, help='Facebook sayfa adresi')
ARGS.add_argument('-o', '--output', required=False, type=str, help='Çıktı dosyası türü')
ARGS.add_argument('-f', '--file', required=False, type=str, help='Facebook adreslerini dosyadan alın')
ARGS.add_argument('-m', '--month', required=False, type=int, help='Gönderinin alınacağı ay')

PARGS = ARGS.parse_args()

# Facebook parametreleri
DEFAULT_PAGE_URL = "https://www.facebook.com/SultanbeyliBel"
DEFAULT_USERNAME = "bb.baskal" # facebook kullanıcı adı
DEFAULT_PASSWORD = "Gb14062014" # facebook şifresi

