# OnlineFix Direct Executor - Linux

[![en](https://img.shields.io/badge/lang-en-blue.svg)](README.md)

Linux üzerinde OnlineFix oyunlarını (Proton aracılığıyla) doğrudan `.exe` dosyasına çift tıklayarak çalıştırmanızı sağlayan hafif ve evrensel bir araçtır. 

Oyunları başlatmakla kalmaz, arka planda resmi [OnlineFix Linux Launcher](https://github.com/ZzEdovec/onlinefix-linux) ile tam entegre çalışır. Oynadığınız oyunları otomatik olarak Launcher'ın kütüphanesine ekler, oynama sürenizi kaydeder ve oyun ikonlarını çıkarır.

## Özellikler
- **Tek Tıkla Çalıştırma:** Herhangi bir `.exe` dosyasına sağ tıklayın -> "OnlineFix ile Aç (Proton)" diyerek direkt oyuna girin.
- **Akıllı DLL Algılama:** Oyun klasöründeki `steamfix.ini`, `winmm.txt` gibi dosyaları okuyarak gerekli `WINEDLLOVERRIDES` ayarlarını otomatik yapar.
- **Evrensel Steam Desteği:** Sistemdeki Steam'in Flatpak mi yoksa Native mi kurulu olduğunu otomatik algılar.
- **Otomatik Kütüphane Kaydı:** Çalıştırılan her oyunu arayüzün `Games.ini` dosyasına otomatik yazar. 
- **Süre Kaydı (Time Tracking):** Oyunda geçirdiğiniz süreyi (Time in game) hesaplar ve arayüzde günceller.
- **İkon Çıkartma:** Oyunun `.exe` dosyasından resmi ikonunu otomatik çıkarır ve Launcher kütüphanesinde kapak fotoğrafı ve ikon olarak ayarlar.
- **Çoklu Dil ve Logo Desteği:** Sağ tık menüsü sistem dilinize (İngilizce / Türkçe) göre adapte olur ve resmi OnlineFix logosunu barındırır.

## Tek Satırda Kurulum

Aracı doğrudan `curl` ile tek komutta sisteminize kurabilirsiniz:

```bash
bash -c "$(curl -fsSL https://raw.githubusercontent.com/KadirBerkpolat1/OnlineFix-DirectExecutor/main/install.sh)"
```

*Kurulum sırasında, isteğe bağlı olarak resmi `onlinefix-linux-launcher` arayüzünü de otomatik kurup kurmamak istediğiniz sorulacaktır.*

### İsteğe Bağlı Gereksinimler (İkon Çıkartma İçin)
Eğer aracın oyun `.exe` dosyalarından ikonları otomatik çıkarıp Launcher arayüzüne eklemesini istiyorsanız sisteminizde şu paketlerin kurulu olduğundan emin olun:
- **Arch/CachyOS:** `sudo pacman -S icoutils imagemagick`
- **Ubuntu/Mint:** `sudo apt install icoutils imagemagick`
- **Fedora:** `sudo dnf install icoutils ImageMagick`

## Kaldırma İşlemi

Aracı sisteminizden tamamen kaldırmak isterseniz:
```bash
bash -c "$(curl -fsSL https://raw.githubusercontent.com/KadirBerkpolat1/OnlineFix-DirectExecutor/main/uninstall.sh)"
```
