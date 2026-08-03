#!/bin/bash

# OnlineFix Direct Executor - Universal Install Script
# Can be run via: bash -c "$(curl -fsSL https://raw.githubusercontent.com/KadirBerkpolat1/OnlineFix-DirectExecutor/main/install.sh)"

echo "================================================="
echo "  OnlineFix Direct Executor Installation"
echo "================================================="
echo ""

BIN_DIR="$HOME/.local/bin"
APP_DIR="$HOME/.local/share/applications"
ICON_DIR="$HOME/.local/share/icons/hicolor/256x256/apps"

mkdir -p "$BIN_DIR"
mkdir -p "$APP_DIR"
mkdir -p "$ICON_DIR"

# 1. Download the Python script
echo "[1/4] Downloading execution engine..."
curl -fsSL https://raw.githubusercontent.com/KadirBerkpolat1/OnlineFix-DirectExecutor/main/onlinefix-executor.py -o "$BIN_DIR/onlinefix-executor"
chmod +x "$BIN_DIR/onlinefix-executor"

# 2. Download the OnlineFix icon
echo "[2/4] Downloading OnlineFix icon..."
curl -fsSL https://raw.githubusercontent.com/ZzEdovec/onlinefix-linux/main/src/res/.data/img/icon.png -o "$ICON_DIR/onlinefix-logo.png"

# 3. Create the .desktop file with localization
echo "[3/4] Creating desktop integration..."
cat <<'DESK' > "$APP_DIR/onlinefix-executor.desktop"
[Desktop Entry]
Name=Open with OnlineFix (Proton)
Name[tr]=OnlineFix ile Aç (Proton)
Comment=Launch EXE files with OnlineFix patches via Proton
Comment[tr]=Exe dosyalarını OnlineFix yamaları uygulanmış şekilde Proton ile başlatır
Exec=sh -c '"$HOME/.local/bin/onlinefix-executor" "%f"'
Icon=onlinefix-logo
Terminal=false
Type=Application
Categories=Game;
MimeType=application/x-ms-dos-executable;application/x-executable;
DESK

update-desktop-database "$APP_DIR" 2>/dev/null

# 4. Optional: Install official OnlineFix Linux Launcher
echo ""
echo "[4/4] Official Launcher Integration"
read -p "Do you want to also install the official 'onlinefix-linux' launcher? (y/N) [Default: N]: " install_launcher
if [[ "$install_launcher" =~ ^[Yy]$ ]]; then
    echo "Downloading official installer (v2.7.1)..."
    TMP_INSTALLER="/tmp/onlinefix_launcher_installer"
    curl -L https://github.com/ZzEdovec/onlinefix-linux/releases/download/v2.7.1/onlinefix_launcher_installer -o "$TMP_INSTALLER"
    chmod +x "$TMP_INSTALLER"
    echo "Running official installer..."
    "$TMP_INSTALLER"
    rm -f "$TMP_INSTALLER"
    echo "Official launcher installed successfully!"
fi

echo ""
echo "================================================="
echo "  INSTALLATION COMPLETED SUCCESSFULLY!"
echo "================================================="
echo "You can now right-click any .exe file and select:"
echo "-> Open with OnlineFix (Proton) / OnlineFix ile Aç"
echo ""
echo "Note: If you want automatic EXE icon extraction, ensure 'icoutils' and 'imagemagick' are installed on your system."
echo "Arch: sudo pacman -S icoutils imagemagick"
echo "Ubuntu: sudo apt install icoutils imagemagick"
