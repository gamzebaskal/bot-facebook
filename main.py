import time

import settings
import utils
from browser import Browser

brw = Browser()

if settings.PARGS.page:
    """
    Eğer kullanıcı uygulamayı çalıştırırken sayfa URL'i gönderdiyse sadece o sayfada 
    işlem yapılacak.
    """

    brw.get_url(settings.PARGS.page)
    brw.take_screenshot(settings.PARGS.page)

else:
    brw.get_url()
while True:

    if brw.is_required_login() == True:
        if brw.login(use_default=True):
            continue


    elif brw.is_required_login() == False:
        time.sleep(3)
        utils.create_dom_file(brw.get_current_url())
        brw.take_screenshot(file=f'bot-facebook_{brw.get_current_url()}')
        brw.get_post_meta()
        break
