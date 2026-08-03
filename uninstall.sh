#!/bin/bash

# OnlineFix Direct Executor - Universal Uninstaller
# Can be run via: bash -c "$(curl -fsSL https://raw.githubusercontent.com/KadirBerkpolat1/OnlineFix-DirectExecutor/main/uninstall.sh)"

echo "================================================="
echo "  Uninstalling OnlineFix Direct Executor"
echo "================================================="

BIN_DIR="$HOME/.local/bin"
APP_DIR="$HOME/.local/share/applications"
ICON_DIR="$HOME/.local/share/icons/hicolor/256x256/apps"

echo "Removing execution engine..."
rm -f "$BIN_DIR/onlinefix-executor"

echo "Removing desktop integration..."
rm -f "$APP_DIR/onlinefix-executor.desktop"

echo "Removing icon files..."
rm -f "$ICON_DIR/onlinefix-logo.png"

echo "Updating desktop database..."
update-desktop-database "$APP_DIR" 2>/dev/null

echo "================================================="
echo "  UNINSTALLATION COMPLETED!"
echo "================================================="
