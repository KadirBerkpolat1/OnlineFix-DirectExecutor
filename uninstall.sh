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
echo "[2/2] Proton Cleanup"
read -p "Do you want to delete auto-downloaded GE-Proton files from Steam's compatibilitytools.d to free up space? (y/N) [Default: N]: " delete_proton
if [[ "$delete_proton" =~ ^[Yy]$ ]]; then
    echo "Scanning Steam directories for GE-Proton..."
    for steam_path in "$HOME/.local/share/Steam" "$HOME/.steam/steam" "$HOME/.var/app/com.valvesoftware.Steam/data/Steam" "$HOME/.var/app/com.valvesoftware.Steam/.local/share/Steam"; do
        if [ -d "$steam_path/compatibilitytools.d" ]; then
            find "$steam_path/compatibilitytools.d" -maxdepth 1 -type d -name "GE-Proton*" -exec rm -rf {} + 2>/dev/null || true
        fi
    done
    echo "GE-Proton files removed."
fi

update-desktop-database "$APP_DIR" 2>/dev/null

echo ""
echo "================================================="
echo "  UNINSTALLATION COMPLETED!"
echo "================================================="
