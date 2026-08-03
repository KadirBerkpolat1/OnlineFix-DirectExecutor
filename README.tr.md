<div align="center">
  <img src="https://raw.githubusercontent.com/ZzEdovec/onlinefix-linux/main/src/.data/img/oflogo.png" alt="OnlineFix Linux Logo" width="150" />
  <h1>OnlineFix Direct Executor</h1>
  <p><b>Linux için Evrensel ve Bağımsız Çevrimiçi Oyun Entegrasyon Motoru</b></p>

  [![en](https://img.shields.io/badge/Language-English-blue.svg)](README.md)
  [![License: GPL v3](https://img.shields.io/badge/License-GPLv3-green.svg)](https://www.gnu.org/licenses/gpl-3.0)
  [![Platform: Linux](https://img.shields.io/badge/Platform-Linux-orange.svg)](https://kernel.org)
  [![Environment: Steam/Proton](https://img.shields.io/badge/Environment-Proton%20%7C%20Wine-blueviolet.svg)](https://github.com/ValveSoftware/Proton)
</div>

<br/>

**OnlineFix Direct Executor**, Windows için hazırlanmış olan OnlineFix, Empress, Goldberg ve diğer Crack/Multiplayer modifikasyonlarına sahip oyunları **doğrudan `.exe` dosyasına çift tıklayarak** Linux üzerinde sorunsuz bir şekilde çalıştırmanızı sağlayan bağımsız (standalone) bir entegrasyon aracıdır.

Hiçbir arayüze ihtiyaç duymadan arka planda çalışır, oyunun yapılandırmasını anlık olarak analiz eder, gerekli ağ kancalarını (Network Hooks) atar ve Steam/Proton ortamını dinamik olarak oyun için hazırlar.

---

## 📑 İçindekiler
- [Özellikler](#-özellikler)
- [Çok Oyunculu ve Sunucu Desteği](#-çok-oyunculu-ve-sunucu-desteği)
- [Nasıl Çalışır? (Kaputun Altında)](#-nasıl-çalışır-kaputun-altında)
- [Kurulum](#-kurulum)
- [Kaldırma İşlemi](#-kaldırma-işlemi)
- [Lisans ve Yasal Uyarı](#-lisans-ve-yasal-uyarı)

---

## ✨ Özellikler

- **🔥 Tek Tıkla Çalıştırma:** İndirdiğiniz oyun klasöründeki `.exe` dosyasına sağ tıklayıp **"OnlineFix ile Aç (Proton)"** diyerek anında oyuna girin. 
- **🧠 Dinamik DLL Yönlendirme (Smart Overrides):** Oyun klasöründeki özel crack dosyalarını (`steamfix.ini`, `onlinefix.ini`, `winmm.dll` vb.) otomatik tespit eder ve Proton için en kusursuz `WINEDLLOVERRIDES` konfigürasyonunu anlık üretir.
- **⚙️ Otonom Proton Motoru (GE-Proton):** Sisteminizi ve Steam sürümünüzü tarar. Uygun Proton bulunamazsa, işlemci mimarinize (x86_64 veya ARM64) göre en güncel *GE-Proton* sürümünü GitHub üzerinden otomatik olarak indirip sisteme entegre eder.
- **🐧 Flatpak & Native Steam Desteği:** Steam'i nasıl kurmuş olursanız olun (Flatpak veya sistem paketi), araç tüm kütüphane yollarını otomatik bularak senkronize olur.
- **📊 Şeffaf Arka Plan Entegrasyonu (Opsiyonel):** Eğer sisteminizde resmi *OnlineFix Linux Launcher* kuruluysa; oynadığınız tüm oyunları, oyun sürelerinizi (Playtime) ve otomatik oluşturulan yüksek çözünürlüklü ikonlarını sessizce Launcher'ın veritabanına işler.

---

## 🌐 Çok Oyunculu ve Sunucu Desteği

Aracımız sadece bir "başlatıcı" değildir. Ağ katmanlarını ve çok oyunculu (multiplayer) altyapıları eksiksiz simüle eder:

- **Resmi OnlineFix Sunucuları & Photon (PUN):** Oyunların ihtiyaç duyduğu Photon sunucu bağlantılarına engel olmaz; orijinal **OnlineFix Dedicated** sunucularına doğrudan katılmanıza olanak tanır.
- **Steamworks & Spacewar Entegrasyonu:** Arka planda `onlinefix.ini` ve diğer ayar dosyalarını (UTF-8/UTF-16 fark etmeksizin) okuyarak Steam ağını maskeler (`FakeAppId`). Steam arkadaş listeniz üzerinden davet atabilir, lobi kurabilir ve Windows oyuncularıyla birlikte oynayabilirsiniz.
- **Epic Online Services (EOS):** Çapraz platform destekli oyunlardaki Epic `eos.dll` kancalarını tespit ederek sorunsuz sunucu girişi sağlar.

---

## 🛠️ Nasıl Çalışır? (Kaputun Altında)

1. **Bağlam Menüsü (Context Menu):** Bir oyunu açtığınızda Linux masaüstü ortamınız (KDE/GNOME vb.) argüman olarak EXE dosya yolunu doğrudan Python motorumuza iletir.
2. **Ortam Analizi:** Motor, oyun klasörünü tarar. Çatlak (Crack) dosyalarını eşleştirerek bağımlılık listesi çıkartır.
3. **Steam & Prefix Hazırlığı:** Oyun için izole edilmiş bir WINEPREFIX (Sanal Windows C: Sürücüsü) yaratılır ve Flatpak/Native Steam kütüphaneleri buraya bağlanır.
4. **Enjeksiyon:** Bulunan tüm özel DLL'ler sisteme *Native* olarak tanımlanarak oyunun orijinal DRM veya ağ servislerini atlaması/yönlendirmesi sağlanır.
5. **Yürütme (Execution):** İlgili GE-Proton sürümü, doğru ortam değişkenleriyle (Environment Variables) tetiklenir ve oyun tam performansla başlar.

---

## 📦 Kurulum

Kurulum tek satırlık bir komut ile gerçekleştirilir. Terminalinizi açın ve aşağıdaki kodu yapıştırın:

```bash
bash -c "$(curl -fsSL https://raw.githubusercontent.com/KadirBerkpolat1/OnlineFix-DirectExecutor/main/install.sh)"
```

> **Not:** Kurulum betiği; işletim sisteminizi otomatik algılayarak (Arch, Fedora, Ubuntu, vb.) indirme barları için `zenity`/`kdialog` ve ikon çıkartma motorları için `icoutils`, `imagemagick` gibi paketleri sisteminize güvenle kurar.

---

## 🗑️ Kaldırma İşlemi

Aracı ve yapılandırmalarını sistemden tamamen silmek ve arka planda indirilen geçici GE-Proton dosyalarından kurtularak yer açmak isterseniz:

```bash
bash -c "$(curl -fsSL https://raw.githubusercontent.com/KadirBerkpolat1/OnlineFix-DirectExecutor/main/uninstall.sh)"
```

---

## 📜 Lisans ve Yasal Uyarı

Bu yazılım **GPL-3.0 Lisansı** (GNU General Public License v3) altında dağıtılan özgür ve açık kaynaklı bir araçtır. Kodları dilediğiniz gibi okuyabilir, paylaşabilir ve geliştirebilirsiniz. 

*Yasal Uyarı: Bu proje, bağımsız ve topluluk odaklı bir uyumluluk (compatibility) katmanıdır. OnlineFix.me veya başka herhangi bir grupla doğrudan resmi bir bağı yoktur. Sadece kullanıcıların yasal donanımlarında özgür yazılım çalıştırma haklarını (interoperability) kolaylaştırmak amacıyla geliştirilmiştir.*

---


## 📦 Bağımlılıklar (Dependencies)

Aracı kullanmadan önce sisteminizde aşağıdaki paketlerin kurulu olduğundan emin olun:

- `steam` (Zorunlu) – Oyunların Steamworks üzerinden (Spacewar) çalışabilmesi için.
- `zenity` veya `kdialog` (Zorunlu) – İndirme pencereleri ve hata bildirimleri için.
- `icoutils` & `imagemagick` (İsteğe Bağlı) – Oyun `.exe` dosyalarından kaliteli ikon çıkartabilmek için (`icoextract` yerine daha evrensel bir çözümdür).

> **‼️ ÖNEMLİ NOT:** Orijinal *OnlineFix Linux Launcher* aksine, **bizim yazdığımız Direct Executor Flatpak Steam sürümlerini %100 destekler!** Arka plandaki akıllı tarama motorumuz, Steam'i ister yerel (Native) ister Flatpak (`com.valvesoftware.Steam`) olarak kurmuş olun kütüphane yollarınızı sorunsuz bulur. Snap desteği ise şu an için mevcut değildir.

## 🧩 Uyumluluk Tablosu (Compatibility Matrix)

Farklı crack/fix türleri ve gruplar için aracımızın sunduğu destek durumu aşağıdaki gibidir:

| Fix Türü | Grup | Durum | Notlar |
| :--- | :--- | :--- | :--- |
| **SteamFix** | **OnlineFix** | 🟢 Tam Destek | 64-bit oyunlarda kusursuz çalışır. Eski 32-bit oyunlarda sorun yaşanabilir. |
| **SteamFix** | **FreeTP** | 🟡 Kısmi Destek | Sadece 2026 öncesine ait (eski) fix sürümleri desteklenmektedir. |
| **Özel Sunucular** | **OnlineFix** | 🟢 Tam Destek | Photon Launcher altyapılı özel sunuculara (Custom Servers) tam erişim. |
| **SteamFix + EOSFix** | **OnlineFix** | 🟢 Tam Destek | Her iki DRM'i birleştiren (Combined) oyunlarda sorunsuz giriş. |
| **SteamFix + EOSFix** | **FreeTP** | 🔴 Desteklenmiyor | FreeTP'nin birleşik çözümlerinde çalışmamaktadır (Tamamen kırık). |
| **EOSFix** | **OnlineFix** | 🟡 Kısmi Destek | `EOSAuthHooker` ile tam uyumludur ancak eski "Legacy" mod henüz test edilmemiştir. |
| **EOSFix** | **FreeTP** | 🔴 Desteklenmiyor | FreeTP'nin EOS çözümleri desteklenmemektedir (Tamamen kırık). |

