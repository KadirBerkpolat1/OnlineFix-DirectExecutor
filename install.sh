#!/bin/bash

# OnlineFix Direct Executor - Universal Install Script (TUI Edition)
# Can be run via: bash -c "$(curl -fsSL https://raw.githubusercontent.com/KadirBerkpolat1/OnlineFix-DirectExecutor/main/install.sh)"

set -e

# Ensure whiptail is available (part of libnewt/newt)
if ! command -v whiptail &> /dev/null; then
    echo "Whiptail is not installed. Falling back to simple installation..."
    if [ -f /etc/arch-release ]; then sudo pacman -S --noconfirm --needed libnewt; fi
    if [ -f /etc/debian_version ]; then sudo apt-get update && sudo apt-get install -y whiptail; fi
    if [ -f /etc/fedora-release ]; then sudo dnf install -y newt; fi
    if [ -f /etc/SUSE-brand ] || [ -f /etc/SuSE-release ]; then sudo zypper install -y newt; fi
fi

# Fallback if whiptail still fails to install
if ! command -v whiptail &> /dev/null; then
    echo "Error: Could not install whiptail. Please install it manually and try again."
    exit 1
fi

TITLE="OnlineFix Direct Executor Setup"

# Welcome Screen
whiptail --title "$TITLE" --msgbox "Welcome to the OnlineFix Direct Executor & Game Manager Setup.\n\nThis tool allows you to run cracked/multiplayer Windows games natively on Linux with a single click. \n\nWe will now install the necessary dependencies and integrate the engine into your desktop environment." 15 65

# Step 1: Dependencies & Core Files
{
    echo "10"; echo "XXX"; echo "Checking package manager for dependencies..."; echo "XXX"
    sleep 1

    if ! command -v wrestool &> /dev/null || ! command -v convert &> /dev/null || ! command -v zenity &> /dev/null || ! command -v aria2c &> /dev/null; then
        echo "30"; echo "XXX"; echo "Installing dependencies (icoutils, imagemagick, zenity, aria2)..."; echo "XXX"

        if [ -f /etc/arch-release ]; then
            sudo pacman -S --noconfirm --needed icoutils imagemagick zenity aria2 > /dev/null 2>&1 || true
        elif [ -f /etc/debian_version ]; then
            sudo apt-get update > /dev/null 2>&1 && sudo apt-get install -y icoutils imagemagick zenity aria2 > /dev/null 2>&1 || true
        elif [ -f /etc/fedora-release ]; then
            sudo dnf install -y icoutils ImageMagick zenity aria2 > /dev/null 2>&1 || true
        elif [ -f /etc/SUSE-brand ] || [ -f /etc/SuSE-release ]; then
            sudo zypper install -y icoutils ImageMagick zenity aria2 > /dev/null 2>&1 || true
        fi
    fi
    echo "50"; echo "XXX"; echo "Dependencies verified."; echo "XXX"
    sleep 0.5

    # Paths
    BIN_DIR="$HOME/.local/bin"
    APP_DIR="$HOME/.local/share/applications"
    ICON_DIR="$HOME/.local/share/icons/hicolor/256x256/apps"

    mkdir -p "$BIN_DIR" "$APP_DIR" "$ICON_DIR"

    # Step 2: Download Executor
    echo "70"; echo "XXX"; echo "Downloading Execution Engine (onlinefix-executor)..."; echo "XXX"
    curl -sSL https://raw.githubusercontent.com/KadirBerkpolat1/OnlineFix-DirectExecutor/main/onlinefix-executor.py -o "$BIN_DIR/onlinefix-executor"
    chmod +x "$BIN_DIR/onlinefix-executor"

    # Step 3: Download Icons & Desktop Entry
    echo "90"; echo "XXX"; echo "Setting up Desktop Integration..."; echo "XXX"
    curl -sSL https://raw.githubusercontent.com/ZzEdovec/onlinefix-linux/main/src/.data/img/oflogo.png -o "$ICON_DIR/onlinefix-logo.png"

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

    update-desktop-database "$APP_DIR" 2>/dev/null || true

    echo "100"; echo "XXX"; echo "Base Installation Complete!"; echo "XXX"
    sleep 1

} | whiptail --title "$TITLE" --gauge "Installing Core Components..." 8 60 0

# Optional Component: Official ZzEdovec Launcher
if whiptail --title "$TITLE" --yesno "Would you also like to install the 'Legacy Official OnlineFix Launcher' (v2.7.1)?\n\n(Note: Direct Executor works completely standalone without it, but you can install it if you prefer the classic library interface.)" 12 65 --defaultno; then
    {
        echo "20"; echo "XXX"; echo "Downloading installer..."; echo "XXX"
        TMP_INSTALLER="/tmp/onlinefix_launcher_installer"
        curl -sL https://github.com/ZzEdovec/onlinefix-linux/releases/download/v2.7.1/onlinefix_launcher_installer -o "$TMP_INSTALLER"
        chmod +x "$TMP_INSTALLER"

        echo "60"; echo "XXX"; echo "Running ZzEdovec's Installer..."; echo "XXX"
        "$TMP_INSTALLER" > /dev/null 2>&1 || true
        rm -f "$TMP_INSTALLER"

        echo "100"; echo "XXX"; echo "Legacy Launcher Installed."; echo "XXX"
        sleep 1
    } | whiptail --title "$TITLE" --gauge "Installing Legacy Launcher..." 8 60 0
fi

# End Screen
whiptail --title "$TITLE" --msgbox "🎉 Installation Completed Successfully!\n\nYou can now right-click any Windows .exe file in your file manager and select:\n\n-> 'Open with OnlineFix (Proton)'\n\nThe executor will automatically detect your Steam paths, crack files, and apply the correct patches." 15 65

clear
echo "================================================="
echo "  INSTALLATION COMPLETED SUCCESSFULLY!"
echo "================================================="
echo "Right-click any .exe file to get started."
