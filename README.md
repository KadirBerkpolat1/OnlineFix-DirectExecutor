# OnlineFix Direct Executor for Linux

Linux üzerinde OnlineFix oyunlarını (Proton aracılığıyla) doğrudan `.exe` dosyasına çift tıklayarak çalıştırmanızı sağlayan hafif ve evrensel bir araçtır. 

Oyunları başlatmakla kalmaz, arka planda [OnlineFix Linux Launcher](https://github.com/ZzEdovec/onlinefix-linux) ile tam entegre çalışır. Oynadığınız oyunları Launcher'ın kütüphanesine otomatik ekler ve oynama sürenizi (Time in game) kaydeder.

## Özellikler

- **Evrensel Çalışma:** Ubuntu, Fedora, Arch Linux, Linux Mint ve diğer tüm dağıtımlarda çalışır.
- **Flatpak & Native Steam Desteği:** Sistemdeki Steam'in Flatpak mi yoksa Native mi kurulu olduğunu otomatik algılar ve Proton'u doğru dizinlerden bulur.
- **Otomatik Kütüphane Kaydı:** Çalıştırılan her oyunu `Games.ini` dosyasına otomatik yazar. 
- **Oynama Süresi (Time Tracking):** Oyunda geçirdiğiniz süreyi hesaplar ve Launcher arayüzündeki oynama sürenizi günceller.
- **Hızlı Masaüstü Entegrasyonu:** Kurulumdan sonra herhangi bir dosya yöneticisinde (Dolphin, Nautilus vb.) `.exe` dosyalarına sağ tıklayıp "OnlineFix ile Aç (Proton)" diyerek oyuna girebilirsiniz.
- **Akıllı DLL Algılama:** Oyun klasöründeki `steamfix.ini`, `winmm.txt` gibi dosyaları okuyarak gerekli `WINEDLLOVERRIDES` ayarlarını sizin yerinize otomatik yapar.

## Kurulum

Sisteminize kurmak için terminalde şu komutları çalıştırmanız yeterlidir:

```bash
git clone https://github.com/KULLANICI_ADINIZ/OnlineFix-DirectExecutor.git
cd OnlineFix-DirectExecutor
chmod +x install_universal.sh
./install_universal.sh
```

Kurulum bittikten sonra oyunlarınızın `.exe` dosyalarına sağ tıklayarak **OnlineFix ile Aç (Proton)** seçeneğini kullanabilirsiniz.

## Gereksinimler
- Python 3 (Tüm Linux dağıtımlarında varsayılan olarak gelir)
- Steam (Native veya Flatpak)
- Herhangi bir Proton sürümü (Steam üzerinden veya GE-Proton)
