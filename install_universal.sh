#!/bin/bash

# OnlineFix Direct Executor - Evrensel Kurulum Betiği

echo "Kurulum başlatılıyor..."

# Hedef dizinleri oluştur
mkdir -p "$HOME/.local/bin"
mkdir -p "$HOME/.local/share/applications"

# Çalıştırılabilir python betiğini evrensel bin dizinine kopyala
cp onlinefix-executor.py "$HOME/.local/bin/onlinefix-executor"
chmod +x "$HOME/.local/bin/onlinefix-executor"

# Masaüstü entegrasyonu (Kısayol dosyası)
DESKTOP_FILE="$HOME/.local/share/applications/onlinefix-executor.desktop"

cat <<EOF > "$DESKTOP_FILE"
[Desktop Entry]
Name=OnlineFix ile Aç (Proton)
Comment=Exe dosyalarını OnlineFix yamaları uygulanmış şekilde Proton ile başlatır
Exec="$HOME/.local/bin/onlinefix-executor" %f
Icon=steam
Terminal=false
Type=Application
Categories=Game;
MimeType=application/x-ms-dos-executable;application/x-executable;
EOF

# Masaüstü veritabanını güncelle
update-desktop-database "$HOME/.local/share/applications"

echo ""
echo "=== KURULUM TAMAMLANDI ==="
echo ""
echo "Araç ~/.local/bin/onlinefix-executor yoluna yüklendi."
echo "İki büyük özellik başarıyla aktifleşti:"
echo " 1) Flatpak veya Normal Steam'in Kurulu olduğu yerler otomatik taranacak."
echo " 2) Çalıştırdığınız her oyun otomatik olarak 'onlinefix-linux' Launcher'ın (Games.ini) listesine kaydedilecek!"
echo ""
echo "Not: ~/.local/bin dizininin PATH ortam değişkeninde olduğundan emin olun."
echo "Artık herhangi bir .exe dosyasına sağ tıklayıp aracı kullanabilirsiniz."