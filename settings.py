import argparse
import logging

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent # proje dizini

log = logging
_log = logging.basicConfig(filename='logs.log', filemode='a', format="%(asctime)s %(message)s",
                    encoding='utf-8', level=logging.DEBUG)

# Console arguments
_args = argparse.ArgumentParser(exit_on_error=False)
_args.add_argument('-p', '--page', required=False, type=str, help='Facebook sayfa adresi')
_args.add_argument('-o', '--output', required=False, type=str, help='Çıktı dosyası türü')
_args.add_argument('-f', '--file', required=False, type=str, help='Facebook adreslerini dosyadan alın')
_args.add_argument('-m', '--month', required=False, type=int, help='Gönderinin alınacağı ay')

pargs = _args.parse_args()
