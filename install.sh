#!/bin/bash

# OnlineFix Direct Executor - Universal Install Script
# Can be run via: bash -c "$(curl -fsSL https://raw.githubusercontent.com/KadirBerkpolat1/OnlineFix-DirectExecutor/main/install.sh)"

echo "================================================="
echo "  OnlineFix Direct Executor Installation"
echo "================================================="
echo ""

# Paket Yöneticisini Algıla ve Gerekli Paketleri Kur
echo "[1/5] Checking and installing dependencies (icoutils, imagemagick, zenity)..."
if ! command -v wrestool &> /dev/null || ! command -v convert &> /dev/null; then
    echo "Dependencies are missing. Attempting to install automatically (may require sudo password)..."
    if [ -f /etc/arch-release ]; then
        sudo pacman -S --noconfirm --needed icoutils imagemagick zenity
    elif [ -f /etc/debian_version ]; then
        sudo apt-get update && sudo apt-get install -y icoutils imagemagick zenity
    elif [ -f /etc/fedora-release ]; then
        sudo dnf install -y icoutils ImageMagick zenity
    elif [ -f /etc/SUSE-brand ] || [ -f /etc/SuSE-release ]; then
        sudo zypper install -y icoutils ImageMagick zenity
    else
        echo "Warning: Could not auto-detect package manager. Please install 'icoutils', 'imagemagick', and 'zenity' manually for icon extraction to work."
    fi
else
    echo "Dependencies are already installed."
fi
echo ""

BIN_DIR="$HOME/.local/bin"
APP_DIR="$HOME/.local/share/applications"
ICON_DIR="$HOME/.local/share/icons/hicolor/256x256/apps"

mkdir -p "$BIN_DIR"
mkdir -p "$APP_DIR"
mkdir -p "$ICON_DIR"

# 1. Download the Python script
echo "[2/5] Downloading execution engine..."
curl -fsSL https://raw.githubusercontent.com/KadirBerkpolat1/OnlineFix-DirectExecutor/main/onlinefix-executor.py -o "$BIN_DIR/onlinefix-executor"
chmod +x "$BIN_DIR/onlinefix-executor"

# 2. Download the OnlineFix icon
echo "[3/5] Downloading OnlineFix icon..."
curl -fsSL https://raw.githubusercontent.com/ZzEdovec/onlinefix-linux/main/src/.data/img/oflogo.png -o "$ICON_DIR/onlinefix-logo.png"

# 3. Create the .desktop file with localization
echo "[4/5] Creating desktop integration..."
cat <<DESK > "$APP_DIR/onlinefix-executor.desktop"
[Desktop Entry]
Name=Open with OnlineFix (Proton)
Comment=Launch EXE files with OnlineFix patches via Proton
Exec=sh -c '"$HOME/.local/bin/onlinefix-executor" "%f"'
Icon=$ICON_DIR/onlinefix-logo.png
Terminal=false
Type=Application
Categories=Game;
MimeType=application/x-ms-dos-executable;application/x-executable;
DESK

update-desktop-database "$APP_DIR" 2>/dev/null

# 5. Optional: Install official OnlineFix Linux Launcher
echo ""
echo "[5/5] Official Launcher Integration"
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
echo "-> Open with OnlineFix (Proton)"
