#!/usr/bin/env python3
import os
import sys
import subprocess
import configparser
import json
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                             QHBoxLayout, QGridLayout, QLabel, QPushButton,
                             QScrollArea, QDialog, QLineEdit, QCheckBox,
                             QComboBox, QFileDialog, QMessageBox, QTabWidget, QFormLayout)
from PyQt5.QtGui import QPixmap, QIcon, QFont, QPalette, QColor
from PyQt5.QtCore import Qt, QSize

CONFIG_DIR = os.path.expanduser("~/.config/OFME-Linux")
GAMES_INI = os.path.join(CONFIG_DIR, "Games.ini")
IMAGES_DIR = os.path.join(CONFIG_DIR, "images")
EXECUTOR_BIN = os.path.expanduser("~/.local/bin/onlinefix-executor")

class GameConfigDialog(QDialog):
    def __init__(self, game_name, game_exe, game_dir, parent=None):
        super().__init__(parent)
        self.game_name = game_name
        self.game_exe = game_exe
        self.game_dir = game_dir
        self.config_path = os.path.join(game_dir, ".ofme-config.json")
        self.setWindowTitle(f"{game_name} - Configuration")
        self.setMinimumWidth(400)
        self.init_ui()
        self.load_config()

    def init_ui(self):
        layout = QFormLayout()

        self.proton_combo = QComboBox()
        self.proton_combo.addItem("auto")
        # Populate with installed protons
        protons_dir1 = os.path.expanduser("~/.config/OFME-Linux/protons")
        steam_paths = [
            os.path.expanduser("~/.local/share/Steam/compatibilitytools.d"),
            os.path.expanduser("~/.steam/steam/compatibilitytools.d"),
            os.path.expanduser("~/.var/app/com.valvesoftware.Steam/data/Steam/compatibilitytools.d")
        ]

        candidates = set()
        if os.path.isdir(protons_dir1):
            candidates.update(os.listdir(protons_dir1))
        for sp in steam_paths:
            if os.path.isdir(sp):
                candidates.update(os.listdir(sp))

        for c in sorted(list(candidates)):
            self.proton_combo.addItem(c)

        layout.addRow("Proton Version:", self.proton_combo)

        self.chk_gamemode = QCheckBox("Enable GameMode")
        layout.addRow("Performance:", self.chk_gamemode)

        self.chk_mangohud = QCheckBox("Enable MangoHud")
        layout.addRow("HUD:", self.chk_mangohud)

        self.chk_gamescope = QCheckBox("Enable Gamescope")
        self.txt_gamescope_args = QLineEdit("-W 1920 -H 1080 -f")
        layout.addRow("Gamescope:", self.chk_gamescope)
        layout.addRow("Gamescope Args:", self.txt_gamescope_args)

        self.txt_dlls = QLineEdit()
        self.txt_dlls.setPlaceholderText("Comma separated paths to DLLs to inject")
        layout.addRow("Injected DLLs:", self.txt_dlls)

        btn_box = QHBoxLayout()
        btn_save = QPushButton("Save")
        btn_save.clicked.connect(self.save_config)
        btn_cancel = QPushButton("Cancel")
        btn_cancel.clicked.connect(self.reject)

        btn_box.addWidget(btn_save)
        btn_box.addWidget(btn_cancel)

        layout.addRow(btn_box)
        self.setLayout(layout)

    def load_config(self):
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, 'r') as f:
                    data = json.load(f)

                proton = data.get("proton_version", "auto")
                idx = self.proton_combo.findText(proton)
                if idx >= 0:
                    self.proton_combo.setCurrentIndex(idx)

                self.chk_gamemode.setChecked(data.get("use_gamemode", False))
                self.chk_mangohud.setChecked(data.get("use_mangohud", False))
                self.chk_gamescope.setChecked(data.get("use_gamescope", False))
                self.txt_gamescope_args.setText(data.get("gamescope_args", "-W 1920 -H 1080 -f"))

                dlls = data.get("injected_dlls", [])
                self.txt_dlls.setText(",".join(dlls))
            except Exception as e:
                print(f"Failed to load config: {e}")

    def save_config(self):
        data = {
            "proton_version": self.proton_combo.currentText(),
            "use_gamemode": self.chk_gamemode.isChecked(),
            "use_mangohud": self.chk_mangohud.isChecked(),
            "use_gamescope": self.chk_gamescope.isChecked(),
            "gamescope_args": self.txt_gamescope_args.text(),
            "injected_dlls": [d.strip() for d in self.txt_dlls.text().split(",") if d.strip()]
        }
        try:
            with open(self.config_path, 'w') as f:
                json.dump(data, f, indent=4)
            self.accept()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Could not save config: {e}")

class GameCard(QWidget):
    def __init__(self, name, exe, main_path, parent=None):
        super().__init__(parent)
        self.name = name
        self.exe = exe
        self.main_path = main_path
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        img_label = QLabel()
        img_label.setAlignment(Qt.AlignCenter)

        # Determine image
        header_path = os.path.join(IMAGES_DIR, f"{self.name}_header.png")
        icon_path = os.path.join(IMAGES_DIR, f"{self.name}_icon.png")

        pixmap = None
        if os.path.exists(header_path):
            pixmap = QPixmap(header_path).scaled(300, 140, Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)
        elif os.path.exists(icon_path):
            pixmap = QPixmap(icon_path).scaled(128, 128, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        else:
            # Fallback placeholder
            pixmap = QPixmap(300, 140)
            pixmap.fill(QColor("#2a2a2a"))

        if pixmap:
            img_label.setPixmap(pixmap)

        layout.addWidget(img_label)

        title = QLabel(self.name)
        title.setAlignment(Qt.AlignCenter)
        font = QFont()
        font.setBold(True)
        font.setPointSize(11)
        title.setFont(font)
        layout.addWidget(title)

        btn_layout = QHBoxLayout()
        btn_play = QPushButton("Play")
        btn_play.setStyleSheet("background-color: #27ae60; color: white; font-weight: bold; padding: 5px;")
        btn_play.clicked.connect(self.play_game)

        btn_config = QPushButton("⚙️")
        btn_config.setFixedWidth(40)
        btn_config.clicked.connect(self.open_config)

        btn_layout.addWidget(btn_play)
        btn_layout.addWidget(btn_config)
        layout.addLayout(btn_layout)

        self.setLayout(layout)
        self.setStyleSheet("""
            QWidget {
                background-color: #1e1e1e;
                border-radius: 8px;
            }
            QLabel {
                color: white;
            }
        """)

    def play_game(self):
        if not os.path.exists(EXECUTOR_BIN):
            QMessageBox.critical(self, "Error", "onlinefix-executor not found. Please run install.sh.")
            return

        # Launch in background
        subprocess.Popen([EXECUTOR_BIN, self.exe], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    def open_config(self):
        dlg = GameConfigDialog(self.name, self.exe, self.main_path, self)
        dlg.exec_()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("OFME - OnlineFix Game Manager")
        self.resize(1000, 700)

        # Dark Theme
        self.setStyleSheet("""
            QMainWindow {
                background-color: #121212;
            }
            QScrollArea {
                border: none;
                background-color: transparent;
            }
            QTabWidget::pane {
                border: 0px;
                background-color: #121212;
            }
            QTabBar::tab {
                background-color: #2a2a2a;
                color: white;
                padding: 10px 20px;
                margin-right: 2px;
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
            }
            QTabBar::tab:selected {
                background-color: #3a3a3a;
                font-weight: bold;
            }
            QPushButton {
                background-color: #2c3e50;
                color: white;
                border: none;
                padding: 8px 15px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #34495e;
            }
        """)

        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        self.init_library_tab()
        self.init_hubcap_tab()

    def init_library_tab(self):
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)

        container = QWidget()
        self.grid = QGridLayout(container)
        self.grid.setAlignment(Qt.AlignTop | Qt.AlignLeft)

        self.load_games()

        scroll.setWidget(container)
        self.tabs.addTab(scroll, "My Library")

    def init_hubcap_tab(self):
        # Placeholder for Hubcap / enter-the-wired integration
        widget = QWidget()
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignTop)

        title = QLabel("Hubcap Downloader & Auto-Cracker")
        title.setStyleSheet("font-size: 18px; font-weight: bold; color: white;")
        layout.addWidget(title)

        desc = QLabel("Enter your HubcapManifest API Key to search and download games directly from Steam CDN.")
        desc.setStyleSheet("color: #aaaaaa;")
        layout.addWidget(desc)

        form = QFormLayout()
        self.api_input = QLineEdit()
        self.api_input.setPlaceholderText("Enter Hubcap API Key...")
        form.addRow("API Key:", self.api_input)
        layout.addLayout(form)

        btn_box = QHBoxLayout()
        btn_search = QPushButton("Search Games (Coming Soon)")
        btn_search.setDisabled(True)
        btn_box.addWidget(btn_search)

        btn_fix = QPushButton("Auto-find Fix for Existing Game")
        btn_fix.clicked.connect(self.auto_fix_placeholder)
        btn_box.addWidget(btn_fix)

        layout.addLayout(btn_box)
        widget.setLayout(layout)

        self.tabs.addTab(widget, "Discover & Unlock")

    def load_games(self):
        # Clear grid
        for i in reversed(range(self.grid.count())):
            self.grid.itemAt(i).widget().setParent(None)

        if not os.path.exists(GAMES_INI):
            lbl = QLabel("No games found. Right click a game's .exe and select 'Open with OnlineFix' to add it here.")
            lbl.setStyleSheet("color: #aaaaaa; font-size: 14px;")
            self.grid.addWidget(lbl, 0, 0)
            return

        config = configparser.ConfigParser(strict=False)
        config.optionxform = str
        try:
            config.read(GAMES_INI, encoding='utf-8')
        except Exception as e:
            lbl = QLabel(f"Error reading Games.ini: {e}")
            self.grid.addWidget(lbl, 0, 0)
            return

        row, col = 0, 0
        max_cols = 3

        for section in config.sections():
            exe = config.get(section, 'executable', fallback="")
            main_path = config.get(section, 'mainPath', fallback="")

            if exe and os.path.exists(exe):
                card = GameCard(section, exe, main_path)
                self.grid.addWidget(card, row, col)

                col += 1
                if col >= max_cols:
                    col = 0
                    row += 1

    def auto_fix_placeholder(self):
        QMessageBox.information(self, "Auto-Cracker", "The Auto-Cracker engine will scan your selected folder and download the corresponding OnlineFix files via Torrent/Direct automatically in a future update.")

if __name__ == '__main__':
    app = QApplication(sys.argv)

    # Try to set application style
    app.setStyle("Fusion")

    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
