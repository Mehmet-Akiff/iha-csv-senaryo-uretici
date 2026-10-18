# 🧪 İHA Telemetri CSV Senaryo Üretici (v1.4.0)

[![Version](https://img.shields.io/badge/Sürüm-v1.4.0-2bda72?style=for-the-badge)](https://github.com/Mehmet-Akiff/iha-csv-senaryo-uretici/releases/tag/v1.4.0)
[![Platform](https://img.shields.io/badge/Platform-Windows%2010%2F11-0078D6?style=for-the-badge)](https://github.com/Mehmet-Akiff/iha-csv-senaryo-uretici/releases)
[![Security](https://img.shields.io/badge/Güvenlik-DigiCert%20İmzalı%20Motor-2b8a3e?style=for-the-badge)](https://github.com/Mehmet-Akiff/iha-csv-senaryo-uretici/releases/tag/v1.4.0)

**İHA Telemetri CSV Senaryo Üretici**, İHA yer kontrol istasyonlarını ve telemetri analiz yazılımlarını uçtan uca test etmek amacıyla geliştirilmiş, **14 farklı uçuş, sensör arızası ve veri bozulması senaryosunu** üretebilen bağımsız bir masaüstü simülasyon uygulamasıdır.

---

## 🌟 Öne Çıkan Özellikler (v1.4.0)

* **🚁 Özel Taktik Drone İkonu & 1.8 Saniye Animasyonlu Açılış Ekranı (Splash Screen):** Uygulama başlatıldığında kullanıcıyı bilgilendiren ilerleme çubuklu İHA yükleme ekranı ve yumuşak **Fade-In** pencere açılışı.
* **🗂️ Otomatik Sıralı ve Tarihli Periyot Klasörleme:** Toplu senaryo üretiminde dosyaların birbirine karışmasını önlemek için her üretim periyodu otomatik olarak `01_Uretim_YYYY-AA-GG_SS-dd-sn/`, `02_Uretim_...` şeklinde numaralandırılmış ve tarih damgalı izole klasörlere kaydedilir.
* **✨ Sayfa Geçiş ve Sayaç Animasyonları:**
  * `📋 Tablo Görünümü`, `📄 Ham CSV İçeriği (Raw)` ve `ℹ️ Senaryo Rehberi` sekmeleri arasında geçiş yaparken **Zümrüt Yeşili Parlama (Glow Pulse)** animasyonu.
  * Veri üretildiğinde canlı satır sayacı animasyonu.
* **🛡️ %100 DigiCert İmzalı Çalışma Zamanı:** Paket içerisindeki çalıştırılabilir dosyalar (`pythonw.exe`, `python.exe`) resmi **Python Software Foundation (DigiCert)** imzasına sahiptir; Avast ve Windows Defender tarafından %100 güvenli olarak tanınır.

---

## 📥 Doğrudan İndir ve Çalıştır (Python Gerektirmez!)

1. **[GitHub Releases (v1.4.0) Sayfasına Gidin](https://github.com/Mehmet-Akiff/iha-csv-senaryo-uretici/releases/tag/v1.4.0)**
2. **`CSV_Senaryo_Uretici_DigiCert_Signed_v1.4.0.zip`** arşivini indirin ve bir klasöre çıkartın.
3. Klasör içerisindeki **`CSV_Senaryo_Uretici Baslat.vbs`** (veya `.bat`) dosyasına çift tıklayarak uygulamayı hemen başlatın!

---

## 🧪 Desteklenen 14 Telemetri Senaryosu

| # | Senaryo Kodu | Senaryo Açıklaması ve Test Amacı |
| :--- | :--- | :--- |
| **01** | `valid` | **%100 Geçerli Uçuş Verisi:** Kusursuz, gerçekçi tırmanış/seyir telemetri kaydı. |
| **02** | `with_gaps` | **Zaman Boşluğu (Kesintili Uçuş):** Belirtilen saniye kadar haberleşme kesintisi (data drop) içerir. |
| **03** | `mixed_errors` | **Karışık / Kısmi Hatalı Veri:** Geçerli verilerin arasına serpiştirilmiş 5 farklı tipte hatalı satır (Kısmi kurtarma testi). |
| **04** | `negative_speed` | **Negatif Hız Hatası:** Fiziksel olarak imkansız negatif hız (`-12.5 m/s` vb.) içeren satırlar. |
| **05** | `battery_out_of_bounds` | **Batarya Sınır İhlali:** `%0`'ın altında (`-15%`) veya `%100`'ün üzerinde (`125%`) batarya değerleri. |
| **06** | `lat_lon_out_of_bounds` | **Coğrafi Koordinat İhlali:** WGS-84 sınırları dışında enlem (`>90°`) ve boylam (`>180°`) değerleri. |
| **07** | `text_in_numeric` | **Sayısal Alanda Metin:** İrtifa, hız ve batarya sütunlarında bozuk metin (`"YUKSEK"`, `"HATA"`) ifadeleri. |
| **08** | `empty_mandatory_fields` | **Boş Zorunlu Hücreler:** Zorunlu telemetri sütunlarında eksik (`NaN`/boş) bırakılmış hücreler. |
| **09** | `invalid_timestamps` | **Çözümlenemeyen Zaman Damgası:** Bozuk tarih/saat formatları (`"BOZUK_TARIH"`). |
| **10** | `angle_out_of_bounds` | **Açısal Sınır İhlalleri:** Pitch, Roll ve Yaw açılarında fiziksel sınır dışı değerler. |
| **11** | `missing_columns` | **Eksik Zorunlu Sütunlar:** `speed` ve `battery_pct` sütunları eksik bırakılmış CSV yapısı. |
| **12** | `zero_valid_rows` | **Sıfır Geçerli Kayıt:** Başlıkları doğru ancak içindeki tüm satırları hatalı olan dosya. |
| **13** | `empty_file` | **Boş Dosya (0 Bayt):** Tamamen boş dosya sınır durumu testi. |
| **14** | `corrupted_format` | **Bozuk CSV Sözdizimi:** Sütun sayısı tutarsız, ayrıştırılamayan bozuk metin yapısı. |

---

## 💻 Geliştirici Kurulumu (Kaynak Koddan Çalıştırma)

```bash
pip install -r requirements.txt
python app.py
```

---

## 📁 Proje Dizin Yapısı

```text
iha-csv-senaryo-uretici/
├── app.py                  # CustomTkinter Masaüstü Arayüzü (v1.4.0 - Splash & Animasyonlu)
├── scenario_engine.py      # 14 Senaryolu Telemetri Veri Üretim ve Klasörleme Motoru
├── README.md               # Kapsamlı Kullanım ve Senaryo Kılavuzu
├── requirements.txt        # Python Bağımlılıkları
└── assets/                 # Özel İHA/Drone İkonları (generator_icon.ico / .png)
```
