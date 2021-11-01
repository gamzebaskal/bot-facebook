import settings as s
from browser import Browser

brw = Browser()

if s.PARGS.page:
    """
    Eğer kullanıcı uygulamayı çalıştırırken sayfa URL'i gönderdiyse sadece o sayfada 
    işlem yapılacak.
    """

    brw.get_url(s.PARGS.page)

else:
    brw.get_url()