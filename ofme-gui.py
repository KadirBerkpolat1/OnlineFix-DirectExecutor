#!/usr/bin/env python3
import os
import sys
import subprocess
import configparser
import json
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                             QHBoxLayout, QGridLayout, QLabel, QPushButton,
                             QScrollArea, QDialog, QLineEdit, QCheckBox,
                             QComboBox, QFileDialog, QMessageBox, QTabWidget, QFormLayout, QFrame, QSpacerItem, QSizePolicy, QInputDialog)
from PyQt5.QtGui import QPixmap, QIcon, QFont, QPalette, QColor, QCursor
from PyQt5.QtCore import Qt, QSize, QThread, pyqtSignal
from ofme_hubcap import HubcapManager
from ofme_autocracker import AutoCracker

class WorkerThread(QThread):
    progress = pyqtSignal(int, str)
    finished = pyqtSignal(bool, str)

    def __init__(self, task_func, *args, **kwargs):
        super().__init__()
        self.task_func = task_func
        self.args = args
        self.kwargs = kwargs

    def run(self):
        try:
            self.kwargs['progress_callback'] = self.progress.emit
            res = self.task_func(*self.args, **self.kwargs)
            self.finished.emit(True, "Success")
        except Exception as e:
            self.finished.emit(False, str(e))

CONFIG_DIR = os.path.expanduser("~/.config/OFME-Linux")
GAMES_INI = os.path.join(CONFIG_DIR, "Games.ini")
IMAGES_DIR = os.path.join(CONFIG_DIR, "images")
EXECUTOR_BIN = os.path.expanduser("~/.local/bin/onlinefix-executor")

# Modern Stylesheet (Catppuccin Mocha inspired for sleek dark mode)
MODERN_THEME = """
QMainWindow, QDialog {
    background-color: #1e1e2e;
}
QScrollArea, QScrollArea > QWidget > QWidget {
    background-color: transparent;
    border: none;
}
QTabWidget::pane {
    border: none;
    background-color: #1e1e2e;
}
QTabBar::tab {
    background-color: #181825;
    color: #a6adc8;
    padding: 12px 30px;
    font-size: 15px;
    font-weight: 600;
    border: none;
    border-bottom: 3px solid transparent;
}
QTabBar::tab:selected {
    color: #89b4fa;
    border-bottom: 3px solid #89b4fa;
    background-color: #1e1e2e;
}
QTabBar::tab:hover:!selected {
    background-color: #313244;
}
QLineEdit {
    background-color: #11111b;
    color: #cdd6f4;
    border: 2px solid #45475a;
    padding: 12px;
    border-radius: 8px;
    font-size: 14px;
}
QLineEdit:focus {
    border: 2px solid #89b4fa;
}
QPushButton {
    background-color: #89b4fa;
    color: #11111b;
    border: none;
    padding: 12px 24px;
    border-radius: 8px;
    font-size: 14px;
    font-weight: bold;
}
QPushButton:hover {
    background-color: #b4befe;
}
QPushButton:pressed {
    background-color: #74c7ec;
}
QPushButton#SecondaryBtn {
    background-color: #313244;
    color: #cdd6f4;
    border: 1px solid #45475a;
}
QPushButton#SecondaryBtn:hover {
    background-color: #45475a;
}
QLabel {
    color: #cdd6f4;
}
QFrame#Card {
    background-color: #313244;
    border-radius: 12px;
}
QCheckBox {
    color: #cdd6f4;
    font-size: 14px;
}
QCheckBox::indicator {
    width: 20px;
    height: 20px;
    border-radius: 4px;
    border: 2px solid #45475a;
    background-color: #11111b;
}
QCheckBox::indicator:checked {
    background-color: #89b4fa;
    border: 2px solid #89b4fa;
}
QComboBox {
    background-color: #11111b;
    color: #cdd6f4;
    border: 2px solid #45475a;
    padding: 8px;
    border-radius: 8px;
}
"""

class GameConfigDialog(QDialog):
    # Keep similar logic but styled
    def __init__(self, game_name, game_exe, game_dir, parent=None):
        super().__init__(parent)
        self.game_name = game_name
        self.game_exe = game_exe
        self.game_dir = game_dir
        self.config_path = os.path.join(game_dir, ".ofme-config.json")
        self.setWindowTitle(f"Configure - {game_name}")
        self.setMinimumWidth(450)
        self.init_ui()
        self.load_config()

    def init_ui(self):
        layout = QFormLayout()
        layout.setSpacing(15)

        title = QLabel(f"Settings for {self.game_name}")
        title.setStyleSheet("font-size: 18px; font-weight: bold; color: #89b4fa; margin-bottom: 10px;")
        layout.addRow(title)

        self.proton_combo = QComboBox()
        self.proton_combo.addItem("auto")
        # Load protons...
        protons_dir1 = os.path.expanduser("~/.config/OFME-Linux/protons")
        steam_paths = [
            os.path.expanduser("~/.local/share/Steam/compatibilitytools.d"),
            os.path.expanduser("~/.steam/steam/compatibilitytools.d"),
            os.path.expanduser("~/.var/app/com.valvesoftware.Steam/data/Steam/compatibilitytools.d")
        ]
        candidates = set()
        if os.path.isdir(protons_dir1): candidates.update(os.listdir(protons_dir1))
        for sp in steam_paths:
            if os.path.isdir(sp): candidates.update(os.listdir(sp))
        for c in sorted(list(candidates)): self.proton_combo.addItem(c)
        layout.addRow("Proton Version:", self.proton_combo)

        self.chk_gamemode = QCheckBox("Enable GameMode (Feral)")
        layout.addRow("Performance:", self.chk_gamemode)

        self.chk_mangohud = QCheckBox("Enable MangoHud (FPS Counter)")
        layout.addRow("HUD:", self.chk_mangohud)

        self.chk_gamescope = QCheckBox("Enable Gamescope")
        self.txt_gamescope_args = QLineEdit("-W 1920 -H 1080 -f")
        layout.addRow("Gamescope:", self.chk_gamescope)
        layout.addRow("Args:", self.txt_gamescope_args)

        self.txt_dlls = QLineEdit()
        self.txt_dlls.setPlaceholderText("path/to/mod.dll, path/to/trainer.dll")
        layout.addRow("Inject DLLs:", self.txt_dlls)

        btn_box = QHBoxLayout()
        btn_save = QPushButton("Save Config")
        btn_save.clicked.connect(self.save_config)
        btn_cancel = QPushButton("Cancel")
        btn_cancel.setObjectName("SecondaryBtn")
        btn_cancel.clicked.connect(self.reject)
        
        btn_box.addWidget(btn_cancel)
        btn_box.addWidget(btn_save)

        layout.addRow("", btn_box)
        self.setLayout(layout)

    def load_config(self):
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, 'r') as f: data = json.load(f)
                idx = self.proton_combo.findText(data.get("proton_version", "auto"))
                if idx >= 0: self.proton_combo.setCurrentIndex(idx)
                self.chk_gamemode.setChecked(data.get("use_gamemode", False))
                self.chk_mangohud.setChecked(data.get("use_mangohud", False))
                self.chk_gamescope.setChecked(data.get("use_gamescope", False))
                self.txt_gamescope_args.setText(data.get("gamescope_args", "-W 1920 -H 1080 -f"))
                self.txt_dlls.setText(",".join(data.get("injected_dlls", [])))
            except: pass

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
            with open(self.config_path, 'w') as f: json.dump(data, f, indent=4)
            self.accept()
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

class GameCard(QFrame):
    def __init__(self, name, exe, main_path, parent=None):
        super().__init__(parent)
        self.name = name
        self.exe = exe
        self.main_path = main_path
        self.setObjectName("Card")
        self.setFixedSize(280, 260)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(15, 15, 15, 15)

        img_label = QLabel()
        img_label.setAlignment(Qt.AlignCenter)
        header_path = os.path.join(IMAGES_DIR, f"{self.name}_header.png")
        icon_path = os.path.join(IMAGES_DIR, f"{self.name}_icon.png")

        pixmap = None
        if os.path.exists(header_path):
            pixmap = QPixmap(header_path).scaled(250, 120, Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)
        elif os.path.exists(icon_path):
            pixmap = QPixmap(icon_path).scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        else:
            pixmap = QPixmap(250, 120)
            pixmap.fill(QColor("#45475a"))

        if pixmap: img_label.setPixmap(pixmap)
        layout.addWidget(img_label)

        title = QLabel(self.name)
        title.setAlignment(Qt.AlignCenter)
        title.setWordWrap(True)
        title.setStyleSheet("font-size: 16px; font-weight: bold; margin-top: 10px;")
        layout.addWidget(title)
        
        layout.addStretch()

        btn_layout = QHBoxLayout()
        btn_play = QPushButton("Play Game")
        btn_play.setCursor(QCursor(Qt.PointingHandCursor))
        btn_play.setStyleSheet("background-color: #a6e3a1; color: #11111b;") # Green
        btn_play.clicked.connect(self.play_game)

        btn_config = QPushButton("⚙️")
        btn_config.setObjectName("SecondaryBtn")
        btn_config.setFixedWidth(45)
        btn_config.setCursor(QCursor(Qt.PointingHandCursor))
        btn_config.clicked.connect(self.open_config)

        btn_layout.addWidget(btn_play)
        btn_layout.addWidget(btn_config)
        layout.addLayout(btn_layout)

        self.setLayout(layout)

    def play_game(self):
        if not os.path.exists(EXECUTOR_BIN): return
        subprocess.Popen([EXECUTOR_BIN, self.exe], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    def open_config(self):
        GameConfigDialog(self.name, self.exe, self.main_path, self).exec_()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("OFME - Game Manager")
        self.resize(1100, 750)
        self.setStyleSheet(MODERN_THEME)

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
        self.grid.setSpacing(20)
        self.grid.setContentsMargins(30, 30, 30, 30)

        self.load_games()
        scroll.setWidget(container)
        self.tabs.addTab(scroll, "My Library")

    def init_hubcap_tab(self):
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        widget = QWidget()
        
        # Main layout for the tab
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignTop | Qt.AlignHCenter)
        layout.setSpacing(30)
        layout.setContentsMargins(50, 40, 50, 40)
        
        header = QLabel("Discover & Unlock Games")
        header.setStyleSheet("font-size: 28px; font-weight: 800; color: #89b4fa;")
        header.setAlignment(Qt.AlignCenter)
        layout.addWidget(header)
        
        subtitle = QLabel("Use your Hubcap API to fetch manifests, download directly from Steam, and auto-crack games.")
        subtitle.setStyleSheet("font-size: 15px; color: #a6adc8; margin-bottom: 20px;")
        subtitle.setAlignment(Qt.AlignCenter)
        layout.addWidget(subtitle)

        # --- Card 1: API Configuration ---
        card1 = QFrame()
        card1.setObjectName("Card")
        card1.setMaximumWidth(800)
        c1_layout = QVBoxLayout(card1)
        c1_layout.setContentsMargins(25, 25, 25, 25)
        
        c1_title = QLabel("1. API Authentication")
        c1_title.setStyleSheet("font-size: 18px; font-weight: bold; color: #f38ba8;") # Red/Pink
        c1_layout.addWidget(c1_title)
        
        self.api_input = QLineEdit()
        self.api_input.setPlaceholderText("Paste your HubcapManifest API Key here...")
        c1_layout.addWidget(self.api_input)
        layout.addWidget(card1)

        # --- Card 2: Actions (Search & Install) ---
        card2 = QFrame()
        card2.setObjectName("Card")
        card2.setMaximumWidth(800)
        c2_layout = QVBoxLayout(card2)
        c2_layout.setSpacing(15)
        c2_layout.setContentsMargins(25, 25, 25, 25)
        
        c2_title = QLabel("2. Game Downloader & Unlocker")
        c2_title.setStyleSheet("font-size: 18px; font-weight: bold; color: #a6e3a1;")
        c2_layout.addWidget(c2_title)

        c2_desc = QLabel("Search for a game to download manifests. Install the Steam Hook once to enable playing locked games.")
        c2_desc.setStyleSheet("color: #bac2de;")
        c2_layout.addWidget(c2_desc)
        
        btn_box2 = QHBoxLayout()
        btn_search = QPushButton("🔍 Search & Download Game")
        btn_search.setCursor(QCursor(Qt.PointingHandCursor))
        btn_search.clicked.connect(self.search_hubcap)
        
        btn_install_hook = QPushButton("🛠️ Install Steam Hook (SLSteam)")
        btn_install_hook.setObjectName("SecondaryBtn")
        btn_install_hook.setCursor(QCursor(Qt.PointingHandCursor))
        btn_install_hook.clicked.connect(self.install_steam_hook)
        
        btn_box2.addWidget(btn_search)
        btn_box2.addWidget(btn_install_hook)
        c2_layout.addLayout(btn_box2)
        layout.addWidget(card2)
        
        # --- Card 3: Auto-Cracker ---
        card3 = QFrame()
        card3.setObjectName("Card")
        card3.setMaximumWidth(800)
        c3_layout = QVBoxLayout(card3)
        c3_layout.setSpacing(15)
        c3_layout.setContentsMargins(25, 25, 25, 25)
        
        c3_title = QLabel("3. OnlineFix Auto-Cracker")
        c3_title.setStyleSheet("font-size: 18px; font-weight: bold; color: #f9e2af;")
        c3_layout.addWidget(c3_title)
        
        c3_desc = QLabel("Automatically fetch and apply multiplayer fixes (OnlineFix) to an existing downloaded game.")
        c3_desc.setStyleSheet("color: #bac2de;")
        c3_layout.addWidget(c3_desc)
        
        btn_fix = QPushButton("⚡ Auto-Find & Apply Fix")
        btn_fix.setCursor(QCursor(Qt.PointingHandCursor))
        btn_fix.setStyleSheet("background-color: #f9e2af; color: #11111b;")
        btn_fix.clicked.connect(self.auto_fix_game)
        
        c3_layout.addWidget(btn_fix, alignment=Qt.AlignLeft)
        layout.addWidget(card3)

        # --- Status Bar / Log ---
        self.lbl_status = QLabel("Status: Ready to work.")
        self.lbl_status.setStyleSheet("font-size: 15px; font-weight: bold; color: #89b4fa; padding: 15px; background-color: #181825; border-radius: 8px;")
        self.lbl_status.setMaximumWidth(800)
        self.lbl_status.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.lbl_status)

        layout.addStretch()
        widget.setLayout(layout)
        scroll.setWidget(widget)
        self.tabs.addTab(scroll, "Discover & Unlock")

    def search_hubcap(self):
        api_key = self.api_input.text().strip()
        if not api_key:
            QMessageBox.warning(self, "Warning", "Please enter a Hubcap API Key in step 1.")
            return
            
        query, ok = QInputDialog.getText(self, "Search Game", "Enter game name to search:")
        if not ok or not query.strip(): return
            
        self.lbl_status.setText(f"Status: Searching Steam for '{query}'...")
        self.hubcap = HubcapManager(api_key)
        try:
            games = self.hubcap.search_game(query.strip())
            selected = games[0]
            self.lbl_status.setText(f"Status: Downloading manifest for {selected['name']}...")
            
            self.thread = WorkerThread(self.hubcap.download_manifests, selected['app_id'])
            self.thread.progress.connect(self.update_status)
            self.thread.finished.connect(self.task_finished)
            self.thread.start()
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))
            self.lbl_status.setText("Status: Error encountered.")

    def install_steam_hook(self):
        self.lbl_status.setText("Status: Installing enter-the-wired hook...")
        self.hubcap = HubcapManager()
        self.thread = WorkerThread(self.hubcap.install_enter_the_wired)
        self.thread.progress.connect(self.update_status)
        self.thread.finished.connect(self.task_finished)
        self.thread.start()

    def auto_fix_game(self):
        game_dir = QFileDialog.getExistingDirectory(self, "Select Game Directory to Crack")
        if not game_dir: return
            
        self.lbl_status.setText("Status: Searching OnlineFix database...")
        self.autocrack = AutoCracker()
        try:
            results = self.autocrack.search_fix("Selected Game")
            fix_url = results[0]['download_url']
            self.lbl_status.setText("Status: Downloading and applying fix...")
            self.thread = WorkerThread(self.autocrack.download_and_apply, fix_url, game_dir)
            self.thread.progress.connect(self.update_status)
            self.thread.finished.connect(self.task_finished)
            self.thread.start()
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))
            self.lbl_status.setText("Status: Error encountered.")

    def update_status(self, percent, message):
        self.lbl_status.setText(f"Status: {message} ({percent}%)")

    def task_finished(self, success, message):
        if success:
            QMessageBox.information(self, "Success", "Operation completed successfully!")
            self.lbl_status.setText("Status: Ready.")
        else:
            QMessageBox.critical(self, "Error", f"Operation failed: {message}")
            self.lbl_status.setText("Status: Error.")

    def load_games(self):
        for i in reversed(range(self.grid.count())):
            self.grid.itemAt(i).widget().setParent(None)

        if not os.path.exists(GAMES_INI):
            lbl = QLabel("No games found.\n\nRight click any Windows .exe file on your system and select\n'Open with OnlineFix' to automatically add it to this library.")
            lbl.setStyleSheet("color: #a6adc8; font-size: 16px; font-weight: 500;")
            lbl.setAlignment(Qt.AlignCenter)
            self.grid.addWidget(lbl, 0, 0)
            return

        config = configparser.ConfigParser(strict=False)
        config.optionxform = str
        try: config.read(GAMES_INI, encoding='utf-8')
        except: return

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

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
