import settings as s

from pathlib import Path

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import (TimeoutException,
                                        WebDriverException,
                                        InvalidSessionIdException,)

from random_user_agent.user_agent import UserAgent
from random_user_agent.params import SoftwareName, OperatingSystem

from utils import hash_url

class Browser():

    def __init__(self):
        # chrome options
        self.chrome_options = Options()

        self.brw = webdriver.Chrome(s.BROWSER_DRIVER_DIR,
                                    options=self.chrome_options)

        # random user agent
        self.software_names = [SoftwareName.CHROME.value]
        self.operating_systems = [OperatingSystem.WINDOWS.value, OperatingSystem.LINUX.value]
        self.user_agent_rotator = UserAgent(software_names=self.software_names,
                                            operating_systems=self.operating_systems,
                                            limit=100)

    def get_url(self, url: str = s.DEFAULT_PAGE_URL):
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
        user_agent = self.user_agent_rotator.get_random_user_agent()
        self.chrome_options.add_argument(f'user-agent={user_agent}')
        # self.chrome_options.add_argument('--disable-gpu')
        self.chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
        self.chrome_options.add_argument('ignore-certificate-errors')
        return user_agent