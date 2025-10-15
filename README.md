# 🧠 Zihinsel Sağlık Asistanı

Bu uygulama, kullanıcıların zihinsel sağlık konularında destek alabilecekleri bir sohbet asistanıdır. Google'ın Gemini API'si kullanılarak geliştirilmiştir.

🌍 **Deploy Link:** 

https://zihinsel-asistan.streamlit.app/

![Adobe Express - Ekran Kaydı 2025-10-15 00 24 03](https://github.com/user-attachments/assets/82655191-a980-492c-adae-7f23fe94eebe)


## 🚀 Hızlı Başlangıç

### Ön Koşullar
- Python 3.8+
- Google Gemini API anahtarı

### Kurulum

1️⃣ Gerekli paketleri yükleyin:
   ```bash
   pip install -r requirements.txt
   ```

2️⃣ `.env` dosyası oluşturun ve Google API anahtarınızı ekleyin:
   ```env
   GOOGLE_API_KEY=your_google_api_key_here
   ```

3️⃣ Uygulamayı çalıştırın:
   ```bash
   # Yöntem 1: Doğrudan çalıştırma (tercih edilen)
   streamlit run app.py
   
   # Yöntem 2: Python modülü olarak çalıştırma
   python -m streamlit run app.py
   ```

## 🎯 Kullanım

1. Uygulamayı başlattıktan sonra tarayıcınızda otomatik olarak açılacaktır
2. Alt kısımdaki metin kutusuna mesajınızı yazın ve "Gönder" butonuna tıklayın
3. Asistanınız yanıt verecektir

## ✨ Özellikler

- 🤖 Akıllı sohbet asistanı
- 🧠 Zihinsel sağlık odaklı yanıtlar
- 🔒 Gizlilik odaklı (sohbet geçmişi kaydedilmez)

## 🛠️ Kullanılan Teknolojiler

- **Python** - Programlama Dili
- **Streamlit** - Web Arayüzü
- **Google Gemini API** - Yapay Zeka Modeli
- **python-dotenv** - Ortam Değişkenleri Yönetimi
- **Streamlit-chat** - Sohbet Arayüzü Bileşenleri
- **Pillow** - Görüntü İşleme
- **Google-GenerativeAI** - Google'ın Yapay Zeka API'si

## 📁 Repo Yapısı

```
zihinsel-kisisel-asistan--chatbot/
├── app.py                 # Streamlit uygulama dosyası
├── requirements.txt       # Gerekli Python paketleri
├── .env                  # Çevresel değişkenler (git'te takip edilmez)
├── .gitignore            # Git tarafından yok sayılacak dosyalar
└── README.md             # Bu dosya
```

## 📊 Veri Seti ve Metodoloji

Bu projede, Google'ın güçlü yapay zeka modeli **Gemini** kullanılmıştır. Model, geniş bir veri kümesi üzerinde eğitilmiş olup, kullanıcı etkileşimlerinden öğrenerek sürekli kendini geliştirmektedir.

### Veri Kaynakları
- **Genel İnternet Verileri**: Çeşitli güvenilir kaynaklardan toplanan geniş kapsamlı metin verileri
- **Bilimsel Yayınlar**: Psikoloji ve zihinsel sağlık alanındaki akademik çalışmalar
- **Lisanslı Veri Setleri**: Eğitim sürecinde kullanılan özel lisanslı veri kümeleri

### Gizlilik ve Etik
- Kullanıcı sohbet verileri kaydedilmemekte veya saklanmamaktadır
- Tüm etkileşimler anonim olarak işlenmektedir
- Tıbbi teşhis veya tedavi önerisi sunulmamaktadır

## 📝 Gereksinimler

Gerekli tüm paketler `requirements.txt` dosyasında listelenmiştir.

## 🤝 Katkıda Bulunma

Katkıda bulunmaktan çekinmeyin! Lütfen önce bir konu açın ve değişikliklerinizi tartışın.

> **Not:** Bu proje Cascade AI asistanından alınan yardımla geliştirilmiştir.

## 📜 Lisans

Bu proje [MIT](LICENSE) lisansı altında lisanslanmıştır.

## 📞 İletişim

Sorularınız veya geri bildirimleriniz için lütfen bir konu açın.
- Email : aysankkotan@gmail.com
- GitHub: https://github.com/aysankkotan
- LinkedIn: https://www.linkedin.com/in/aysankotan/

## Gereksinimler

- Python 3.8 veya üzeri
- Google API anahtarı
- İnternet bağlantısı
