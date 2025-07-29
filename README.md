#  Motivasyonum

**Motivasyonum**, gün içindeki ruh halini yazan kullanıcıların duygularını analiz ederek, onların psikolojik durumlarına uygun mesajlar ve alıntılar öneren yapay zekâ destekli bir Streamlit uygulamasıdır.

Bu proje, modern yapay zekâ araçları ile pozitif psikolojiyi bir araya getirerek kullanıcıya hem içsel bir destek sağlar, hem de özelleştirilmiş öneriler sunar. 

Amacımız: _“Kendini yalnız hissettiğin anlarda bile, seni anlayan bir yapay zekâ dostun olsun.”_


## Özellikler

- 🧠 **Duygu Analizi**: Kullanıcının yazdığı metinden pozitif, negatif veya nötr duygu durumunu tahmin eder.
- 💬 **AI Destekli Öneri Sistemi**: Tahmin edilen duyguya göre MongoDB'den uygun motivasyon mesajlarını getirir.
- 📈 **Ruh Hali Takibi**: Kullanıcının ruh hali zaman içinde grafikle görselleştirilir.
- 📖 **Günün Hadisi**: Tek tıkla rastgele hadis getirerek manevi destek sunar.
- 💖 **Favori Alıntılar**: Beğenilen alıntılar tek tıkla kaydedilir ve sonraki oturumlarda görüntülenebilir.
- 🎨 **Tema Seçimi**: Kullanıcı, gündüz/gece modunu sidebar üzerinden değiştirebilir.
- 🛠️ **Yönetici Paneli** (Gizli): Sidebar üzerinden öneri veritabanına yeni kayıt eklenebilir.
- 🌐 **MongoDB Atlas ile Bağlantı**: Veritabanı işlemleri modern bulut altyapısıyla sağlanır.



Kurulum ve Çalıştırma (Installation & Usage)
Bu adımlar, Motivasyonum.AI uygulamasını yerel ortamınızda kurup çalıştırmak için gereklidir.

1. Repoyu Klonlayın
git clone https://github.com/kullanici-adiniz/motivasyonum-ai.git
cd motivasyonum-ai
2. Ortamı Hazırlayın
Python 3.8+ yüklü olduğundan emin olun.
python -m venv venv
source venv/bin/activate  # Windows için: venv\Scripts\activate
3. Gerekli Kütüphaneleri Kurun
pip install -r requirements.txt
4. .env Dosyasını Oluşturun
Proje kök dizinine .env adlı bir dosya oluşturun ve içine aşağıdaki bilgileri girin:
MONGO_URI=mongodb+srv://kullanici:sifre@cluster0.mongodb.net/?retryWrites=true&w=majority
DB_NAME=veri_seti
COLLECTION_ADI=motivasyon_onerileri
❗️ Güvenlik nedeniyle .env dosyasını .gitignore içinde gizlemeyi unutmayın.

5. Uygulamayı Başlatın
--> streamlit run motivasyonum_app.py
Tarayıcıda http://localhost:8501 adresinde uygulama açılacaktır.



## 📸 Ekran Görüntüleri

[(Ana Sayfa)(C:\Users\monster\Desktop\motivasyonum\screenshots\image1.png) (C:\Users\monster\Desktop\motivasyonum\screenshots\image2.png)]

### Günün Hadisi
(C:\Users\monster\Desktop\motivasyonum\screenshots\image3.png)

### Duygu Tespiti ve Tavsiye
(C:\Users\monster\Desktop\motivasyonum\screenshots\image4.png)

### Favorilerim
(C:\Users\monster\Desktop\motivasyonum\screenshots\image5.png)

### Tema Seçimi
(C:\Users\monster\Desktop\motivasyonum\screenshots\image6.png)

### Öneri Ekleme
(C:\Users\monster\Desktop\motivasyonum\screenshots\image7.png)


2. Nasıl Kullanılır? (Usage)
Uygulamayı çalıştırma komutu (örneğin: streamlit run app.py)

Giriş yapmaya gerek var mı?

Tavsiye almak için ne yapılmalı?

Örnek:
##  Nasıl Kullanılır?
1. Terminalden aşağıdaki komutu çalıştırın:
streamlit run app.py
2. Uygulama arayüzü açıldığında, günlük ruh halinizi yazın ve "💡 Tavsiye Al" butonuna tıklayın.
3. Günlük önerinizi alın ve dilediğiniz takdirde alıntıları favorilerinize ekleyin!

## 🛠️ Kullanılan Teknolojiler
- Python 🐍
- Streamlit 📊
- MongoDB 🌿
- dotenv (.env yapılandırması)
- Custom CSS 🎨


🙋4. Katkıda Bulunmak (Contributing)
## Katkıda Bulunmak
Katkılarınızı memnuniyetle karşılıyoruz!

1. Bu repoyu forklayın.
2. Yeni bir branch oluşturun.
3. Geliştirmeleri yapın ve commit'leyin.
4. Pull Request gönderin.
5. Lisans (License)


**Uygulama Yapısı ve Kod Açıklamaları:**

motivasyonum_app.py: Uygulamanın ana akışını kontrol eder. Streamlit ile arayüz oluşturur, temaları ve kullanıcı girişlerini yönetir.

model.py: Duygu analizi modeli içerir. Kullanıcının yazdığı metni sınıflandırır (Pozitif, Negatif, Nötr).

utils.py: Yardımcı fonksiyonlar içerir. Arka plan ayarı, MongoDB işlemleri, rastgele hadis ve alıntı gösterimi gibi işlevleri barındırır.

.env: Gizli anahtarlar (MongoDB bağlantısı gibi) burada tutulur.

assets/: Tema görselleri burada bulunur.
