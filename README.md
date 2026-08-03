# OnlineFix Direct Executor for Linux

[![tr](https://img.shields.io/badge/lang-tr-red.svg)](README.tr.md)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)

A standalone, universal, and seamless Linux integration engine that allows you to run OnlineFix and other crack/multiplayer-modified games **by directly double-clicking the `.exe` file**.

This tool doesn't just launch games; it dynamically configures Proton/Wine and the Steam infrastructure in the background based on the specific needs of the game. It ports the authentic OnlineFix experience from Windows to Linux losslessly, without requiring any intermediate GUI launcher.

## 🌐 Universal Multiplayer & Server Support

Our executor goes beyond just launching the game—it flawlessly simulates the entire server and networking backend required for modified games on Linux:

- **Official OnlineFix Servers & Photon Launcher:** Seamlessly connect to games utilizing the Photon (PUN) engine and official OnlineFix Dedicated servers. The required networking backend is fully supported.
- **Steamworks & Spacewar Integration:** The tool automatically reads your configuration files to mask the `FakeAppId` (usually 480 - Spacewar) natively in the background. You can send Steam invites, create lobbies, and play with your Steam friends effortlessly.
- **Epic Online Services (EOS):** For cross-play supported games, the engine accurately detects and hooks `eos.dll` variants, ensuring smooth Epic servers authentication.
- **Cross-Play with Windows:** Playing on Linux via this executor does not isolate you. You can play, join, and host lobbies with your friends on Windows seamlessly within the OnlineFix infrastructure.

## 🚀 Key Features

- **One-Click Execution:** Simply right-click any `.exe` file inside your downloaded game folder and select **"Open with OnlineFix (Proton)"**. No manual prefixes or DLL setups required.
- **Dynamic DLL Overrides:** Intelligently scans the game directory for crack files such as `steamfix.ini`, `onlinefix.ini`, `winmm.dll`, or `OnlineFix64.dll`. It then generates and injects the exact `WINEDLLOVERRIDES` the game needs to bypass DRM and enable multiplayer.
- **Smart Proton Engine (GE-Proton):** Automatically detects installed Proton versions. If none are found, it identifies your system architecture (x86_64 or ARM64) and automatically downloads the latest *GE-Proton* directly from GitHub, installing it into Steam.
- **Flatpak & Native Steam Support:** Whether you use Native Steam or the Flatpak version, the tool reliably resolves your library paths and handles them interchangeably.
- **Lossless Background Interoperability:** (Optional) If you use the official *OnlineFix Linux Launcher* GUI, this tool silently registers every game you play, updates your "Time in game," and extracts high-resolution icons from the `.exe` into the launcher's `Games.ini` database.

## ⚙️ One-Line Installation

To install the tool on your system, open your terminal and run:

```bash
bash -c "$(curl -fsSL https://raw.githubusercontent.com/KadirBerkpolat1/OnlineFix-DirectExecutor/main/install.sh)"
```

### Auto-Resolved Dependencies
The installation script automatically detects your distribution (Arch, Fedora, Ubuntu, Debian, Suse) and securely installs the following dependencies via your package manager:
- `zenity` or `kdialog` (For native GUI download progress and notification dialogues)
- `icoutils` & `imagemagick` (For extracting high-quality icons from Windows executables)

## 🗑️ Uninstallation

If you wish to completely remove the tool and clean up its configurations:

```bash
bash -c "$(curl -fsSL https://raw.githubusercontent.com/KadirBerkpolat1/OnlineFix-DirectExecutor/main/uninstall.sh)"
```

## 📜 License & Disclaimer
This project is an open-source tool provided freely under the **GPL-3.0 License** (GNU General Public License v3). This project is NOT officially affiliated with OnlineFix.me; it is a community-driven compatibility layer designed to provide interoperability on Linux.
