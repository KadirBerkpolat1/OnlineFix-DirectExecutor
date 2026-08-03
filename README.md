# OnlineFix Direct Executor for Linux

[![tr](https://img.shields.io/badge/lang-tr-red.svg)](README.tr.md)

A lightweight and universal tool that allows you to run OnlineFix patched Windows games natively on Linux (via Proton) simply by double-clicking the `.exe` file.

It completely bypasses the need for an intermediate GUI to launch games, but works fully integrated in the background with the official [OnlineFix Linux Launcher](https://github.com/ZzEdovec/onlinefix-linux). It automatically adds launched games to the launcher's library, tracks your play time, and extracts game icons.

## Features
- **One-Click Execution:** Right-click any `.exe` file -> "Open with OnlineFix (Proton)" to jump straight into the game.
- **Smart DLL Overrides:** Automatically scans the game directory for `steamfix.ini`, `winmm.txt`, and necessary DLLs to inject `WINEDLLOVERRIDES`.
- **Universal Steam Pathing:** Automatically detects and utilizes Proton from both Native Steam and Flatpak Steam installations.
- **Library Integration:** Every game you launch is silently registered into the official launcher's `Games.ini`.
- **Time Tracking:** Tracks your "Time in game" and syncs it with the launcher's UI.
- **Icon Extraction:** Automatically extracts the game's icon from the `.exe` file and uses it as the banner and icon in the launcher.
- **Bilingual Desktop Integration:** The "Open with" context menu adapts to your system language (English / Turkish) and features the official OnlineFix logo.

## One-Line Installation

You can install the tool directly using `curl`:

```bash
bash -c "$(curl -fsSL https://raw.githubusercontent.com/KadirBerkpolat1/OnlineFix-DirectExecutor/main/install.sh)"
```

*During the installation, you will be prompted if you optionally want to download and install the official `onlinefix-linux-launcher` GUI as well.*

### Optional Dependencies (For Icon Extraction)
If you want the tool to automatically extract game icons from `.exe` files and add them to the launcher's UI, please install these packages:
- **Arch/CachyOS:** `sudo pacman -S icoutils imagemagick`
- **Ubuntu/Mint:** `sudo apt install icoutils imagemagick`
- **Fedora:** `sudo dnf install icoutils ImageMagick`

## Uninstallation

If you ever wish to remove the tool from your system:
```bash
bash -c "$(curl -fsSL https://raw.githubusercontent.com/KadirBerkpolat1/OnlineFix-DirectExecutor/main/uninstall.sh)"
```
