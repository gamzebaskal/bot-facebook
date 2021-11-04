# bot-facebook
 Facebook sayfaları için web kazıyıcı

# <b>Projenin Amacı</b><br/>
Bu proje facebook sayfaları ve profilleri için ücretsiz veri toplama aracıdır. Sayfa içerisindeki belirtilen aya ait tüm girdileri alıp, csv dosyası olarak kaydeder. Eğitim amaçlı kullanılmak üzere geliştirildi ve dolayısıyla tüm sorumluluk kullanıcıya aittir. Yasal olmayacak şekilde veri toplama veya paylaşma gibi bir amacı yoktur.

Temel olarak bu proje, istenilen Facebook sayfasından istenilen aya ait tüm gönderileri çekebilir, her gönderinin beğeni, yorum, paylaşım gibi verilerini toplar ve bunları ekran görüntüleri ile birlikte şifrelenmiş bir biçimde kayıt edebilir. Örneğin https://m.facebook.com/besiktasbelediyesi sayfası içerisinden Eylül ayı için gönderiler toplanabilir. Veri ortaya çıktıktan sonra üzerine başka analizler yapmak da mümkün. Toplanan ekran görüntüleri üzerinden metinleri ayıklayabilmek için OCR aracı uygulamanın içinde mevcut. IP bloklanmasının önüne geçmek için önlemler alınmış olsa da yine de eser miktarda kullanmakta fayda var.

# <b>Proje Özellikleri</b><br/>
1) Değer olarak verilen facebook sayfasına bağlantı sağlar ve ekran görüntüsünü kaydeder.
2) md5 algoritmasını kullanarak bağlantı sağlanan URL bilgisini kaydeder.
3) Bağlanılan sayfadan, parametre olarak iletilen aya ait postları kaydeder.
4) Giriş gerektiren sayfalar için kullanıcı bilgileri iletilerek facebook'a giriş yapılabilir.
5) Facebook'un user-agent bilgilerini kullanarak cihaz tespiti yapmasını önlemek için sahte cihaz bilgileri üretir ve gönderir.

# <b>Nasıl Kurulur?</b><br/>
Öncelikle projeyi aşağıdaki komut ile bilgisayarınıza indirmelisiniz.

    git clone https://github.com/gamzebaskal/bot-facebook

Bilgisayarınızda python sanal ortamı oluşturun.

    python -m virtualenv venv

Sanal ortamı aktif edin.
    
    venv\Scripts\activate.bat

Daha sonra bağımlılıkları yükleyin.

    python -m pip install -r requirements.txt


# <b>Nasıl Çalıştırılır?</b><br/>
Uygulama iki farklı şekilde çalıştırılabilir:<br/>
    <b>Varsayılan Ayarlar İle</b><br/>
        Settings.py dosyası içerisindeki DEFAULT_PAGE_URL, DEFAULT_USERNAME, DEFAULT_PASSWORD değişkenleri ayarlanmalıdır.<br/>
        Örneğin;<br/>
            DEFAULT_PAGE_URL = "https://www.facebook.com/besiktasbelediyesi"
            DEFAULT_USERNAME = "{facebook_kullanici_adiniz}"
            DEFAULT_PASSWORD = "{facebook_sifreniz}"<br/>
    <b>Konsol İle</b><br/>
        Uygulama çalıştırılırken, konsol üzerinden gerekli parametreler gönderilmelidir. python main.py -p {facebook_sayfa_adresi} -m {post_tarihi} <br/>
        Örneğin;<br/>

            python main.py -p "https://www.facebook.com/besiktasbelediyesi" -m 2021-10