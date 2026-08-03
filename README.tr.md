# OnlineFix Direct Executor for Linux

[![en](https://img.shields.io/badge/lang-en-blue.svg)](README.md)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)

Linux üzerinde OnlineFix ve diğer crack/multiplayer modifikasyonlarına sahip oyunları **doğrudan `.exe` dosyasına çift tıklayarak** çalıştırmanızı sağlayan bağımsız (standalone), evrensel ve şeffaf bir Linux entegrasyon motorudur.

Bu araç, oyunları başlatmakla kalmaz; arka planda Proton/Wine ve Steam altyapısını oyunun ihtiyaçlarına göre anlık olarak yapılandırır. Hiçbir arayüze ihtiyaç duymadan, Windows ortamındaki orijinal OnlineFix deneyimini Linux'a kayıpsız olarak taşır.

## 🌐 Evrensel Çok Oyunculu (Multiplayer) Desteği

Aracımız sadece oyunu başlatmakla kalmaz, aynı zamanda orijinal OnlineFix'in tüm sunucu ve bağlantı altyapılarını Linux üzerinde kusursuz bir şekilde simüle eder:

- **Resmi OnlineFix Sunucuları & Photon Launcher:** Oyunların kullandığı Photon (PUN) motoru ve resmi OnlineFix Dedicated sunucularına sorunsuz bağlantı kurabilirsiniz. Araç, sunucu bağlantıları için gereken ağ yapılandırmalarını (Network backend) destekler.
- **Steamworks & Spacewar Entegrasyonu (FakeAppId):** Steam üzerinden oynanan oyunlarda arka planda otomatik olarak `FakeAppId` (örn. 480 - Spacewar) maskelemesi yapılır. Steam arkadaşlarınızla sorunsuz bir şekilde davet atabilir ve lobi kurabilirsiniz.
- **Epic Online Services (EOS):** Çapraz platform (Cross-play) desteğine sahip oyunlarda `eos.dll` kancaları (hooks) tespit edilerek sorunsuz EOS sunucu girişi sağlanır.
- **Windows Oyuncularıyla Çapraz Oyun (Cross-Play):** Linux üzerinden oynamanız, Windows kullanan arkadaşlarınızla aynı lobilerde (OnlineFix altyapısında) buluşmanıza kesinlikle engel değildir. Her şey %100 uyumlu çalışır.

## 🚀 Temel Özellikler

- **Tek Tıkla Çalıştırma:** İndirdiğiniz oyun klasöründeki `.exe` dosyasına sağ tıklayın ve **"OnlineFix ile Aç (Proton)"** seçeneğini seçin. Başka hiçbir yapılandırma gerekmez.
- **Dinamik DLL Yönlendirme (Smart Overrides):** Oyun klasöründeki `steamfix.ini`, `onlinefix.ini`, `winmm.dll`, `OnlineFix64.dll` gibi crack dosyalarını otomatik analiz eder ve oyunun ihtiyaç duyduğu `WINEDLLOVERRIDES` (DLL kancalama) parametrelerini anlık olarak oluşturur.
- **Akıllı Proton Motoru (GE-Proton):** Sistemdeki kurulu Proton sürümlerini algılar. Eğer eksikse, sisteminizin mimarisine (x86_64 veya ARM64) en uygun, güncel *GE-Proton* sürümünü GitHub üzerinden otomatik olarak indirir ve Steam'e kurar.
- **Flatpak & Native Steam Desteği:** Steam'i ister Flatpak üzerinden, ister Native olarak kurmuş olun; araç kütüphane yollarınızı otomatik bulur ve senkronize eder.
- **Kayıpsız Arka Plan Uyumluluğu:** (Opsiyonel) Eğer resmi *OnlineFix Linux Launcher* arayüzünü kullanıyorsanız, oynadığınız tüm oyunları, oyun sürelerinizi (Playtime) ve otomatik çekilmiş yüksek çözünürlüklü ikonlarını Launcher'ın veritabanına (`Games.ini`) arka planda sessizce işler.

## ⚙️ Tek Satırda Kurulum

Kurulumu gerçekleştirmek için terminalinizi açın ve aşağıdaki komutu yapıştırın:

```bash
bash -c "$(curl -fsSL https://raw.githubusercontent.com/KadirBerkpolat1/OnlineFix-DirectExecutor/main/install.sh)"
```

### Otomatik Bağımlılıklar
Kurulum betiği işletim sisteminizi (Arch, Fedora, Ubuntu, Debian, Suse) otomatik olarak tanır ve arka planda şu paketleri yükler:
- `zenity` veya `kdialog` (Grafiksel indirme ve bildirim pencereleri için)
- `icoutils` & `imagemagick` (Oyun dosyalarından yüksek kaliteli EXE ikonları çıkartmak için)

## 🗑️ Kaldırma İşlemi

Aracı ve yapılandırmalarını sistemden tamamen ve kalıntısız bir şekilde silmek isterseniz:

```bash
bash -c "$(curl -fsSL https://raw.githubusercontent.com/KadirBerkpolat1/OnlineFix-DirectExecutor/main/uninstall.sh)"
```

## 📜 Lisans & Yasal Bilgilendirme
Bu proje açık kaynaklı bir araç olup **GPL-3.0 Lisansı** (GNU General Public License v3) ile ücretsiz olarak sunulmaktadır. Proje, OnlineFix.me ile resmi bir bağlantıya sahip değildir; yalnızca topluluk odaklı, birlikte çalışabilirlik (interoperability) sağlayan bir uyumluluk (compatibility) katmanıdır.
