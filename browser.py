import time
import csv

from selenium.webdriver.common.by import By

import settings

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import (TimeoutException,
                                        WebDriverException,
                                        InvalidSessionIdException,
                                        NoSuchElementException)

from random_user_agent.user_agent import UserAgent
from random_user_agent.params import SoftwareName, OperatingSystem

import utils
from utils import hash_url


class Browser():

    def __init__(self):
        # tarayıcı ayarları
        self.chrome_options = Options()
        # chrome bildirim pop-up penceresini devre dışı bırakmak için
        prefs = {"profile.default_content_setting_values.notifications": 2}
        self.chrome_options.add_experimental_option("prefs", prefs)

        self.brw = webdriver.Chrome(settings.BROWSER_DRIVER_DIR,
                                    options=self.chrome_options)
        self.brw.maximize_window()

        # sahte kullanıcı ayarları
        self.software_names = [SoftwareName.CHROME.value]
        self.operating_systems = [OperatingSystem.WINDOWS.value, OperatingSystem.LINUX.value]
        self.user_agent_rotator = UserAgent(software_names=self.software_names,
                                            operating_systems=self.operating_systems,
                                            limit=100)

    def get_url(self, url: str = settings.DEFAULT_PAGE_URL):
        """
        Sahte kullanıcı verileri ile birlikte istenilen URL'e bağlantı sağlar.
        Eğer URL bilgisi iletilmez ise settings dosyasında tanımlanan URL parametresini kullanır.
        :param url: Bağlantı sağlanacak URL
        :return: Bağlantı sağlanan URL
        """
        try:
            self.set_user_agent()
            self.brw.get(url)
            h_url = hash_url(url, save=True)
            try:
                with open(f'{settings.DEFAULT_CONTENT_DIR}/DOM/bot-facebook_{h_url}.csv', 'r',
                          encoding='utf-8') as f:
                    pass

            except FileNotFoundError as e:
                with open(f'{settings.DEFAULT_CONTENT_DIR}/DOM/bot-facebook_{h_url}.csv', 'w',
                          encoding='utf-8') as f:
                    writer = csv.writer(f)
                    writer.writerow(["Begeni", "Yorum", "Paylasim"])

        except TimeoutException as e:
            settings.LOG.error(e.msg)
            self.brw.close()
        except InvalidSessionIdException as e:
            settings.LOG.error(e.msg)
            self.brw.close()
        except WebDriverException as e:
            settings.LOG.error(e.msg)
            self.brw.close()
        finally:
            settings.LOG.error("finally error!")

        return self.brw.current_url

    def take_screenshot(self, url: str = settings.DEFAULT_PAGE_URL):
        md5_url = hash_url(url)
        self.brw.save_screenshot(f"{settings.DEFAULT_MEDIA_DIR}/bot-facebook_{md5_url}.png")

    def get_current_url(self):
        """
        Tarayıcıda açık olan URL değerini verir.
        """
        return self.brw.current_url

    def set_user_agent(self):
        """
        Sahte kullanıcı verisi oluşturur.
        :return: Sahte kullanıcı verisi döndürür.
        """
        user_agent = self.user_agent_rotator.get_random_user_agent()
        self.chrome_options.add_argument(f'user-agent={user_agent}')
        # self.chrome_options.add_argument('--disable-gpu')
        self.chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
        self.chrome_options.add_argument('ignore-certificate-errors')
        self.chrome_options.add_argument("--disable-popup-blocking")
        return user_agent

    def is_required_login(self):
        """
        Görüntülenmek istenen sayfanın giriş gerektirip gerektirmediğini kontrol eder.
        Giriş gerektiriyorsa True, gerektirmiyorsa False döndürür.
        :return: boolean
        """
        try:
            url = self.get_current_url().split('/')
            if url[3] == "login":
                return True
            else:
                tag_text = self.brw.find_element(By.LINK_TEXT, "Yeni Hesap Oluştur")
                tag_text = tag_text.get_attribute("href").split('/')[3]
                if tag_text == "reg":
                    tag_text = self.brw.find_element(By.LINK_TEXT, "Giriş Yap")
                    self.get_url(tag_text.get_attribute("href"))
                    return True

        except AttributeError as e:
            settings.LOG.error(e)
            return False

        except NoSuchElementException as e:
            settings.LOG.error(e.msg)
            return False

    def login(self, use_default: bool = False):
        try:
            self.set_user_agent()

            email = self.brw.find_element(By.ID, 'email')
            _pass = self.brw.find_element(By.ID, 'pass')
            btn = self.brw.find_element(By.ID, 'loginbutton')

            username = settings.DEFAULT_USERNAME
            password = settings.DEFAULT_PASSWORD

            if use_default == False:
                username = input("Lütfen facebook kullanıcı adınızı giriniz: ")
                password = input("Lütfen facebook şifrenizi giriniz: ")

            email.send_keys(username)
            _pass.send_keys(password)
            btn.click()

        except NoSuchElementException as e:
            settings.LOG.error(e)

    def slide_scroll(self):
        # self.brw.execute_script("window.scrollTo(0.5,document.body.scrollHeight)")
        self.brw.execute_script("window.scrollBy(0,350)")

    def get_post_meta(self, date: str = "2021-10"):
        counter = 1
        month = date.split('-')[1]
        while True:
            try:
                find_post = self.brw.find_element(By.XPATH, f"//div[@aria-posinset='{counter}']")
                elements = find_post.text.split('\n')

                if elements[1].split()[1].rstrip(',') == settings.DATE[month]:
                    url = hash_url(self.get_current_url())
                    print('elements', elements)
                else:
                    self.slide_scroll()
                    time.sleep(1)
                    continue

            except IndexError as e:

                settings.LOG.error(e)
                self.slide_scroll()
                counter += 1
                continue

            except NoSuchElementException as e:


                settings.LOG.error(e.msg)
                continue
