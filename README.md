# İHA Telemetri CSV Senaryo Üretici

İHA yer kontrol istasyonları ve telemetri analiz sistemlerini test etmek için geliştirilmiş, 14 farklı uçuş ve hata senaryosunu simüle edebilen bağımsız masaüstü uygulaması.

---

## 🚀 Özellikler

- **14 Farklı Test Senaryosu:**
  1. %100 Geçerli Uçuş Verisi
  2. Zaman Boşluğu / Kesintili Uçuş (Data Drop Anomaly)
  3. Karışık / Kısmi Hatalı Veri
  4. Negatif Hız Değerleri
  5. Batarya Sınır İhlalleri (< %0 veya > %100)
  6. Geçersiz Enlem/Boylam (WGS84 dışı)
  7. Sayısal Alanda Metin İçeren Veri
  8. Zorunlu Alanı Boş Bırakılmış Satırlar
  9. Çözümlenemeyen / Bozuk Zaman Damgaları
  10. Açısal Sınır İhlalleri (Pitch/Roll/Yaw)
  11. Gerekli Sütunları Eksik CSV
  12. Sıfır Geçerli Kayıt (Tüm satırlar hatalı)
  13. Boş Dosya (0 bayt)
  14. Bozuk Biçimli CSV Sözdizimi
- **Canlı Önizleme:** Üretilen telemetri satırlarını kaydetmeden önce doğrudan arayüz tablosunda inceleme.
- **Parametre Özelleştirme:** Satır sayısı, kesinti süresi (sn), başlangıç irtifası, hızı ve batarya seviyesini belirleme.

---

## 💻 Çalıştırma

1. **Tek Tıkla Başlatma:**
   `Baslat.bat` dosyasına çift tıklayarak doğrudan çalıştırabilirsiniz.

2. **Python ile Başlatma:**
   ```bash
   pip install customtkinter pandas
   python app.py
   ```
