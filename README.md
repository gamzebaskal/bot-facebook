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