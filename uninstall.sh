#!/bin/bash

# OnlineFix Direct Executor - Universal Uninstaller
# Can be run via: bash -c "$(curl -fsSL https://raw.githubusercontent.com/KadirBerkpolat1/OnlineFix-DirectExecutor/main/uninstall.sh)"

echo "================================================="
echo "  Uninstalling OnlineFix Direct Executor"
echo "================================================="

BIN_DIR="$HOME/.local/bin"
APP_DIR="$HOME/.local/share/applications"
ICON_DIR="$HOME/.local/share/icons/hicolor/256x256/apps"

echo "[1/2] Removing Direct Executor files..."
rm -f "$BIN_DIR/onlinefix-executor"
rm -f "$APP_DIR/onlinefix-executor.desktop"
rm -f "$ICON_DIR/onlinefix-logo.png"

echo ""
echo "[2/2] Official Launcher Uninstallation"
read -p "Do you also want to uninstall the official 'onlinefix-linux-launcher'? (y/N) [Default: N]: " uninstall_launcher
if [[ "$uninstall_launcher" =~ ^[Yy]$ ]]; then
    echo "Removing official launcher files..."
    rm -rf "$HOME/.local/share/OnlineFix Linux Launcher"
    rm -f "$HOME/.local/share/applications/OnlineFix Linux Launcher.desktop"
    
    read -p "Do you want to delete all launcher data (Game settings, downloaded Protons, images)? (y/N) [Default: N]: " delete_data
    if [[ "$delete_data" =~ ^[Yy]$ ]]; then
        echo "Removing launcher data..."
        rm -rf "$HOME/.config/OFME-Linux"
    else
        echo "Launcher data kept in ~/.config/OFME-Linux"
    fi
    echo "Official launcher uninstalled successfully!"
fi

update-desktop-database "$APP_DIR" 2>/dev/null

echo ""
echo "================================================="
echo "  UNINSTALLATION COMPLETED!"
echo "================================================="
