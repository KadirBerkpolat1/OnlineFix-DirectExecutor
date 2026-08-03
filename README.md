<div align="center">
  <img src="https://raw.githubusercontent.com/ZzEdovec/onlinefix-linux/main/src/.data/img/oflogo.png" alt="OnlineFix Linux Logo" width="150" />
  <h1>OnlineFix Direct Executor</h1>
  <p><b>Universal and Standalone Multiplayer Integration Engine for Linux</b></p>

  [![tr](https://img.shields.io/badge/Language-Turkish-red.svg)](README.tr.md)
  [![License: GPL v3](https://img.shields.io/badge/License-GPLv3-green.svg)](https://www.gnu.org/licenses/gpl-3.0)
  [![Platform: Linux](https://img.shields.io/badge/Platform-Linux-orange.svg)](https://kernel.org)
  [![Environment: Steam/Proton](https://img.shields.io/badge/Environment-Proton%20%7C%20Wine-blueviolet.svg)](https://github.com/ValveSoftware/Proton)
</div>

<br/>

**OnlineFix Direct Executor** is a standalone integration tool that allows you to run games modified with OnlineFix, Empress, Goldberg, and other multiplayer cracks on Linux effortlessly—**simply by double-clicking the `.exe` file.**

It works entirely in the background without requiring an intermediate GUI launcher. It analyzes the game configuration on the fly, applies the necessary network hooks, and dynamically prepares the Steam/Proton environment for a seamless launch.

---

## 📑 Table of Contents
- [Features](#-features)
- [Multiplayer & Server Support](#-multiplayer--server-support)
- [How It Works (Under the Hood)](#-how-it-works-under-the-hood)
- [Installation](#-installation)
- [Uninstallation](#-uninstallation)
- [License & Disclaimer](#-license--disclaimer)

---

## ✨ Features

- **🔥 One-Click Execution:** Simply right-click any `.exe` file inside your game directory and select **"Open with OnlineFix (Proton)"** to jump straight into the action.
- **🧠 Dynamic DLL Overrides:** Intelligently detects specialized crack files (`steamfix.ini`, `onlinefix.ini`, `winmm.dll`, etc.) and instantly generates the perfect `WINEDLLOVERRIDES` configuration for Proton.
- **⚙️ Autonomous Proton Engine (GE-Proton):** Scans your system for installed Proton versions. If none are found, it identifies your CPU architecture (x86_64 or ARM64) and automatically downloads the latest *GE-Proton* directly from GitHub.
- **🐧 Flatpak & Native Steam Support:** Whether you use Native Steam or the Flatpak version, the engine flawlessly resolves and synchronizes your library paths.
- **📊 Silent Background Interoperability (Optional):** If you have the official *OnlineFix Linux Launcher* installed on your system, this tool silently registers every game you play, tracks your playtime, and extracts high-resolution icons straight into the Launcher's database.

---

## 🌐 Multiplayer & Server Support

Our executor is far more than a basic "launcher." It comprehensively simulates network layers and multiplayer infrastructures:

- **Official OnlineFix Servers & Photon (PUN):** Allows unobstructed connection to games relying on the Photon engine, enabling you to join official **OnlineFix Dedicated** servers natively.
- **Steamworks & Spacewar Integration:** Silently reads `onlinefix.ini` configuration files (safely parsing UTF-8/UTF-16 encoding) to mask your network presence via `FakeAppId`. Send Steam invites, create lobbies, and play cross-platform with Windows users seamlessly.
- **Epic Online Services (EOS):** Detects `eos.dll` hooks in cross-play supported games to ensure smooth Epic servers authentication.

---

## 🛠️ How It Works (Under the Hood)

1. **Context Menu Execution:** When a game is launched, your Linux Desktop Environment (KDE/GNOME) passes the absolute EXE path directly to our Python engine.
2. **Environment Analysis:** The engine scans the directory, matches known crack signatures, and extracts a dependency list.
3. **Steam & Prefix Preparation:** An isolated WINEPREFIX (Virtual Windows C: Drive) is created for the game, linking up natively with your Flatpak or System Steam libraries.
4. **Injection:** The discovered custom DLLs are declared as *Native* overrides, allowing the game to bypass original DRM and reroute network services.
5. **Execution:** The correct GE-Proton version is triggered alongside the specifically crafted Environment Variables, launching the game with maximum performance.

---

## 📦 Installation

Installation is completed using a single terminal command. Open your terminal and paste the following:

```bash
bash -c "$(curl -fsSL https://raw.githubusercontent.com/KadirBerkpolat1/OnlineFix-DirectExecutor/main/install.sh)"
```

> **Note:** The installation script auto-detects your distribution (Arch, Fedora, Ubuntu, etc.) and safely installs required packages like `zenity`/`kdialog` (for GUI progress bars) and `icoutils`/`imagemagick` (for high-quality icon extraction).

---

## 🗑️ Uninstallation

If you ever wish to completely remove the tool and its configurations, as well as clear up disk space by deleting auto-downloaded GE-Proton versions:

```bash
bash -c "$(curl -fsSL https://raw.githubusercontent.com/KadirBerkpolat1/OnlineFix-DirectExecutor/main/uninstall.sh)"
```

---

## 📜 License & Disclaimer

This software is a free and open-source tool distributed under the **GPL-3.0 License** (GNU General Public License v3). You are free to read, modify, and distribute the code as you see fit.

*Disclaimer: This project is an independent, community-driven compatibility layer. It has no direct official affiliation with OnlineFix.me or any other release groups. It is designed solely to facilitate users' interoperability rights to run free software on their legal hardware.*

---


## 📦 Dependencies

Before using the executor, make sure the following packages are installed on your system:

- `steam` (Required) – To run games over Steamworks network (Spacewar).
- `zenity` or `kdialog` (Required) – For download progress bars and notifications.
- `icoutils` & `imagemagick` (Optional) – For automatic, high-quality icon extraction from Windows `.exe` files (a more universal alternative to `icoextract`).

> **‼️ IMPORTANT NOTE:** Unlike the official *OnlineFix Linux Launcher*, **our Direct Executor 100% supports Flatpak Steam versions!** Our smart engine automatically detects and adapts to your paths whether you installed Steam natively or via Flatpak (`com.valvesoftware.Steam`). However, Snap versions are currently not supported.

## 🧩 Compatibility Matrix

The current support status for various fix types and release groups using our integration engine:

| Fix Type | Group | Status | Notes |
| :--- | :--- | :--- | :--- |
| **SteamFix** | **OnlineFix** | 🟢 Full Support | Seamless on 64-bit games. 32-bit games may experience issues. |
| **SteamFix** | **FreeTP** | 🟡 Partial Support | Only supports older fixes released before 2026. |
| **Custom Servers** | **OnlineFix** | 🟢 Full Support | Complete access to custom OnlineFix servers utilizing Photon Launcher. |
| **SteamFix + EOSFix** | **OnlineFix** | 🟢 Full Support | Flawless execution on combined DRM solutions. |
| **SteamFix + EOSFix** | **FreeTP** | 🔴 Broken | FreeTP's combined solutions are currently entirely broken. |
| **EOSFix** | **OnlineFix** | 🟡 Partial Support | Fully compatible via `EOSAuthHooker`. Legacy mode remains untested. |
| **EOSFix** | **FreeTP** | 🔴 Broken | FreeTP's EOS solutions are currently entirely broken. |

