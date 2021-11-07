import time

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


class Browser:

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

    def take_screenshot(self, file):
        self.brw.save_screenshot(f"{settings.DEFAULT_MEDIA_DIR}/{file}")

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
            if url[3] != "login":
                tag_text = self.brw.find_element(By.LINK_TEXT, "Yeni Hesap Oluştur")
                tag_text = tag_text.get_attribute("href").split('/')[3]
                if tag_text == "reg":
                    tag_text = self.brw.find_element(By.LINK_TEXT, "Giriş Yap")
                    self.get_url(tag_text.get_attribute("href"))
                    return True
            else:
                return True

        except AttributeError as e:
            print("attribute_error: ", e)
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
        self.brw.execute_script("window.scrollBy(0,300)")

    def get_post_meta(self, date: str = "2021-11"):
        counter = 1
        month = date.split('-')[1]
        while True:
            try:
                find_post = self.brw.find_element(By.XPATH, f"//div[@aria-posinset='{counter}']")
                elements = find_post.text.split('\n')
                ref_item = elements.index("Beğen")
                like_count = None
                comment_count = None
                share_count = None
                if elements[ref_item - 1].split()[1] == "Paylaşım":
                    like_count = elements[ref_item - 3]  # beğeni sayısı
                    if elements[ref_item - 2].split()[1] == 'Yorum':
                        comment_count = elements[ref_item - 2].split()[0]  # yorum sayısı
                    else:
                        pass
                    share_count = elements[ref_item - 1].split()[0]
                elif elements[ref_item - 1].split()[1] == "Yorum":
                    like_count = elements[ref_item - 3]
                else:
                    like_count = elements[ref_item - 1]
                if elements[1].split()[1].rstrip(',') == settings.DATE[month]:
                    url = hash_url(self.get_current_url())
                    time.sleep(2)
                    self.take_screenshot(file=f'OCR/bot-facebook_{month}_{counter}_{url}.png')
                    utils.save_post_meta(data=[like_count,
                                               comment_count,
                                               share_count
                                               ],
                                         file=f'DOM/bot-facebook_{url}.csv')
                    counter += 1
                    self.slide_scroll()
                    continue
                else:
                    counter += 1
                    self.slide_scroll()
                    time.sleep(1)
                    continue

            except IndexError as e:
                """
                Eğer sayfada hiç post bulunamaz ise buraya düşecektir.
                """
                print("IndexError")
                settings.LOG.error(e)
                self.slide_scroll()
                counter += 1
                continue

            except NoSuchElementException as e:
                print("NoSuchElementExp", counter)
                settings.LOG.error(e.msg)
                time.sleep(2)
                self.slide_scroll()
                continue
