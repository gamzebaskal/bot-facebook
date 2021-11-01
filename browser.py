import settings as s

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import (TimeoutException,
                                        WebDriverException,
                                        InvalidSessionIdException,
                                        NoSuchElementException)

from random_user_agent.user_agent import UserAgent
from random_user_agent.params import SoftwareName, OperatingSystem

from utils import hash_url

class Browser():

    def __init__(self):
        # tarayıcı ayarları
        self.chrome_options = Options()

        self.brw = webdriver.Chrome(s.BROWSER_DRIVER_DIR,
                                    options=self.chrome_options)

        # sahte kullanıcı ayarları
        self.software_names = [SoftwareName.CHROME.value]
        self.operating_systems = [OperatingSystem.WINDOWS.value, OperatingSystem.LINUX.value]
        self.user_agent_rotator = UserAgent(software_names=self.software_names,
                                            operating_systems=self.operating_systems,
                                            limit=100)

    def get_url(self, url: str = s.DEFAULT_PAGE_URL):
        """
        Sahte kullanıcı verileri ile birlikte istenilen URL'e bağlantı sağlar.
        Eğer URL bilgisi iletilmez ise settings dosyasında tanımlanan URL parametresini kullanır.
        :param url: Bağlantı sağlanacak URL
        :return: Bağlantı sağlanan URL
        """
        try:
            self.set_user_agent()
            self.brw.get(url)
            hash_url(url)

        except TimeoutException as e:
            s.LOG.error(e)
            self.brw.close()
        except WebDriverException as e:
            s.LOG.error(e)
            self.brw.close()
        except InvalidSessionIdException as e:
            s.LOG.error(e)
            self.brw.close()
        finally:
            s.LOG.error("finally error!")

        return self.brw.current_url

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
                return False

        except AttributeError as e:
            s.LOG.error(e)
            return False

        except NoSuchElementException as e:
            s.LOG.error(e)
            return False