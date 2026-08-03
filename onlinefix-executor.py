#!/usr/bin/env python3
import os
import sys
import re
import subprocess
import configparser


import urllib.request
import json
import tarfile

def download_latest_proton_ge():
    try:
        # En güncel GE-Proton sürümünü GitHub API'sinden çek
        api_url = "https://api.github.com/repos/GloriousEggroll/proton-ge-custom/releases/latest"
        req = urllib.request.Request(api_url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode())
            download_url = next(asset['browser_download_url'] for asset in data['assets'] if asset['name'].endswith('.tar.gz'))
            version_name = data['tag_name']
            
        # Determine where to install
        steam_compat = os.path.join(get_active_steam_path(), "compatibilitytools.d")
        os.makedirs(steam_compat, exist_ok=True)
        tar_path = os.path.join(steam_compat, f"{version_name}.tar.gz")
        
        # Create a Live Download Progress Bar with Zenity
        has_zenity = subprocess.run(["which", "zenity"], stdout=subprocess.DEVNULL).returncode == 0
        
        if has_zenity:
            zenity = subprocess.Popen([
                "zenity", "--progress", 
                "--title", "OnlineFix - Proton Installation", 
                "--text", f"Downloading missing Proton version:\n{version_name} (Approx. 400MB)...", 
                "--percentage=0", "--auto-close", "--auto-kill", "--width=400"
            ], stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, universal_newlines=True)
            
            def reporthook(block_num, block_size, total_size):
                if total_size > 0:
                    percent = int(block_num * block_size * 100 / total_size)
                    if percent > 100: percent = 100
                    try:
                        zenity.stdin.write(f"{percent}\n")
                        zenity.stdin.flush()
                    except:
                        pass
                        
            urllib.request.urlretrieve(download_url, tar_path, reporthook)
            
            # Set progress bar to 100 and close when download finishes
            try:
                zenity.stdin.write("100\n")
                zenity.stdin.flush()
                zenity.stdin.close()
                zenity.wait()
            except:
                pass
                
            subprocess.run(["zenity", "--info", "--text", f"Download complete!\n\nExtracting {version_name} files to the system, your game will launch shortly...", "--title", "OnlineFix - Proton Installation", "--timeout", "4"], stderr=subprocess.DEVNULL)
        else:
            # If zenity is not on the system, just use curl
            print(f"{version_name} is downloading (Approx. 400MB)...")
            subprocess.run(["curl", "-L", download_url, "-o", tar_path], check=True)
        
        print("Extracting files...")
        with tarfile.open(tar_path, "r:gz") as tar:
            tar.extractall(path=steam_compat)
            
        os.remove(tar_path)
        print("Proton installed successfully!")
        return True
    except Exception as e:
        print(f"Proton auto-download error: {e}")
        if 'tar_path' in locals() and os.path.exists(tar_path):
            os.remove(tar_path)
        return False

def get_steam_paths():
    home = os.path.expanduser("~")
    # List of Native and Flatpak Steam paths
    return [
        os.path.join(home, ".local/share/Steam"),
        os.path.join(home, ".steam/steam"),
        os.path.join(home, ".var/app/com.valvesoftware.Steam/data/Steam"),
        os.path.join(home, ".var/app/com.valvesoftware.Steam/.local/share/Steam")
    ]

def get_latest_proton():
    proton_candidates = []

    # 1. OFME-Linux Proton Folder
    ofme_protons = os.path.expanduser("~/.config/OFME-Linux/protons")
    if os.path.isdir(ofme_protons):
        for d in os.listdir(ofme_protons):
            p_bin = os.path.join(ofme_protons, d, "proton")
            if os.path.isfile(p_bin):
                proton_candidates.append(p_bin)

    # 2. Native & Flatpak Steam Folders
    for steam_path in get_steam_paths():
        steam_compat = os.path.join(steam_path, "compatibilitytools.d")
        if os.path.isdir(steam_compat):
            for d in os.listdir(steam_compat):
                p_bin = os.path.join(steam_compat, d, "proton")
                if os.path.isfile(p_bin):
                    proton_candidates.append(p_bin)

        steam_common = os.path.join(steam_path, "steamapps/common")
        if os.path.isdir(steam_common):
            for d in os.listdir(steam_common):
                if d.lower().startswith("proton"):
                    p_bin = os.path.join(steam_common, d, "proton")
                    if os.path.isfile(p_bin):
                        proton_candidates.append(p_bin)

    if not proton_candidates:
        return None

    # Select the most recent one based on modification date
    return max(proton_candidates, key=os.path.getmtime)

def get_active_steam_path():
    for p in get_steam_paths():
        if os.path.exists(p):
            return p
    return os.path.expanduser("~/.steam/steam")

def add_to_ofme_launcher(game_exe, game_dir, prefix_path, custom_overrides, fake_app_id, proton_bin_path):
    ini_path = os.path.expanduser("~/.config/OFME-Linux/Games.ini")
    os.makedirs(os.path.dirname(ini_path), exist_ok=True)

    config = configparser.ConfigParser(strict=False)
    config.optionxform = str  # Büyük/küçük harf duyarlılığını koru

    if os.path.exists(ini_path):
        try:
            config.read(ini_path, encoding='utf-8')
        except:
            pass

    game_name = os.path.basename(game_dir)
    if not game_name:
        game_name = "Unknown Game"

    # If there is another game with the same name but different paths, add a number to the name
    original_name = game_name
    counter = 1
    while config.has_section(game_name):
        if config.has_option(game_name, 'executable') and config.get(game_name, 'executable') == game_exe:
            # Game is already registered, update the current record and exit
            break
        game_name = f"{original_name} ({counter})"
        counter += 1

    if not config.has_section(game_name):
        config.add_section(game_name)

    config.set(game_name, 'executable', game_exe)
    config.set(game_name, 'mainPath', game_dir)
    config.set(game_name, 'prefixPath', prefix_path)

    # Find the name of the Proton folder
    proton_name = "GE-Proton Latest"
    if proton_bin_path:
        proton_name = os.path.basename(os.path.dirname(proton_bin_path))

    config.set(game_name, 'proton', proton_name)
    config.set(game_name, 'overrides', custom_overrides)
    config.set(game_name, 'steamOverlay', '1')
    if fake_app_id:
        config.set(game_name, 'fakeSteamID', fake_app_id)

    # Save to file
    with open(ini_path, 'w', encoding='utf-8') as f:
        config.write(f)
        
    # Icon extraction process (requires wrestool and imagemagick)
    images_dir = os.path.expanduser("~/.config/OFME-Linux/images")
    os.makedirs(images_dir, exist_ok=True)
    
    icon_path = os.path.join(images_dir, f"{game_name}_icon.png")
    header_path = os.path.join(images_dir, f"{game_name}_header.png")
    
    if not os.path.exists(icon_path):
        import subprocess
        try:
            # 1. Extract icons from EXE as .ico
            ico_out = os.path.join(images_dir, f"{game_name}.ico")
            subprocess.run(["wrestool", "-x", "-t", "14", game_exe, "-o", ico_out], stderr=subprocess.DEVNULL)
            
            if os.path.exists(ico_out):
                # 2. Convert .ico file to .png using imagemagick (take the largest one)
                subprocess.run(["convert", f"{ico_out}[0]", icon_path], stderr=subprocess.DEVNULL)
                os.remove(ico_out)
                
            # If there is no header and the icon was extracted, temporarily use the icon as the header too
            if os.path.exists(icon_path) and not os.path.exists(header_path):
                import shutil
                shutil.copy2(icon_path, header_path)
                
        except Exception:
            pass # If tools are not installed or icon is missing, fail silently

def main():
    if len(sys.argv) < 2:
        print("Usage: onlinefix-executor <oyun.exe>")
        sys.exit(1)

    game_exe = os.path.abspath(sys.argv[1])
    game_dir = os.path.dirname(game_exe)

    if not os.path.exists(game_exe):
        print(f"Error: File not found -> {game_exe}")
        sys.exit(1)

    dx_overrides = "d3d11=n;d3d10=n;d3d10core=n;dxgi=n;openvr_api_dxvk=n;d3d12=n;d3d12core=n;d3d9=n;d3d8=n;"
    overrides = []

    dll_pattern = re.compile(r'(?i)^(emp|custom)\.dll$|^win.*\.dll$|^(online|steam).*\.(dll|ini|json)$|^eos.*\.dll$|^epicfix.*\.dll$|^(winmm|dlllist)\.txt$|^launch_data\.of.*$')
    fake_app_id = "480"

    for f in os.listdir(game_dir):
        if not dll_pattern.match(f):
            continue

        filepath = os.path.join(game_dir, f)

        if re.match(r'(?i)^(winmm|dlllist)\.txt$', f):
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as txt:
                for line in txt:
                    line = line.strip()
                    if line.lower().endswith('.dll'):
                        dll_name = os.path.splitext(os.path.basename(line.replace('\\', '/')))[0].lower()
                        if dll_name not in [o.split('=')[0] for o in overrides]:
                            overrides.append(f"{dll_name}=n")
            continue

        if re.match(r'(?i)^(online|steam)fix\.ini$', f):
            try:
                with open(filepath, 'r', encoding='utf-8', errors='ignore') as inifile:
                    for line in inifile:
                        if line.strip().lower().startswith("fakeappid"):
                            parts = line.split("=")
                            if len(parts) > 1:
                                fake_app_id = parts[1].strip()
            except:
                pass
            continue

        if re.match(r'(?i)^launch_data\.of.*$|^onlinefix\.json$', f):
            continue

        if f.lower().endswith('.dll'):
            dll_name = os.path.splitext(f)[0].lower()
            if dll_name not in [o.split('=')[0] for o in overrides]:
                if re.match(r'(?i)^win.*\.dll$', f):
                    overrides.append(f"{dll_name}=n,b")
                else:
                    overrides.append(f"{dll_name}=n")

    custom_overrides_str = ";".join(overrides)
    if custom_overrides_str:
        custom_overrides_str += ";"

    final_overrides = dx_overrides + custom_overrides_str

    proton_bin = get_latest_proton()
    if not proton_bin:
        # Instead of visual error, directly download GE-Proton and retry!
        success = download_latest_proton_ge()
        if success:
            proton_bin = get_latest_proton()
            
        if not proton_bin:
            error_msg = "Auto Proton download failed!\n\nPlease download a Proton version via Steam or install GE-Proton manually."
            if subprocess.run(["which", "zenity"], stdout=subprocess.DEVNULL).returncode == 0:
                subprocess.run(["zenity", "--error", "--text", error_msg, "--title", "OnlineFix Executor"], stderr=subprocess.DEVNULL)
            sys.exit(1)

    prefix_path = os.path.join(game_dir, "OFME_Prefix")
    os.makedirs(prefix_path, exist_ok=True)

    steam_path = get_active_steam_path()

    # Integrate this game into the Launcher's interface (Games.ini)
    add_to_ofme_launcher(game_exe, game_dir, prefix_path, custom_overrides_str, fake_app_id, proton_bin)

    env = os.environ.copy()
    env["WINEDLLOVERRIDES"] = final_overrides
    env["STEAM_COMPAT_DATA_PATH"] = prefix_path
    env["STEAM_COMPAT_CLIENT_INSTALL_PATH"] = steam_path

    # Steam overlay
    env["LD_PRELOAD"] = f"{steam_path}/ubuntu12_32/gameoverlayrenderer.so:{steam_path}/ubuntu12_64/gameoverlayrenderer.so"
    env["ENABLE_VK_LAYER_VALVE_steam_overlay_1"] = "1"
    env["SteamOverlayGameId"] = fake_app_id

    # Check if Steam is running and start it (Native or Flatpak)
    steam_check = subprocess.run(["pidof", "steam"], stdout=subprocess.DEVNULL)
    if steam_check.returncode != 0:
        print("Steam is not running. Starting in the background...")
        if "com.valvesoftware.Steam" in steam_path:
            subprocess.Popen(["flatpak", "run", "com.valvesoftware.Steam", "-silent"])
        else:
            subprocess.Popen(["steam", "-silent"])

    import time
    cmd = [proton_bin, "run", game_exe]
    
    print(f"Launching game: {game_exe}")
    start_time = time.time()
    
    try:
        # Start the game and wait for it to finish
        process = subprocess.Popen(cmd, env=env)
        process.wait()
    except KeyboardInterrupt:
        process.terminate()
        
    end_time = time.time()
    elapsed_seconds = int(end_time - start_time)
    
    # Save the playtime to Games.ini
    if elapsed_seconds > 0:
        ini_path = os.path.expanduser("~/.config/OFME-Linux/Games.ini")
        if os.path.exists(ini_path):
            config = configparser.ConfigParser(strict=False)
            config.optionxform = str
            try:
                config.read(ini_path, encoding='utf-8')
                
                # Find the name of the game (matching executable path)
                target_section = None
                for section in config.sections():
                    if config.has_option(section, 'executable') and config.get(section, 'executable') == game_exe:
                        target_section = section
                        break
                
                if target_section:
                    current_time = 0
                    if config.has_option(target_section, 'timeSpent'):
                        try:
                            current_time = int(config.get(target_section, 'timeSpent'))
                        except ValueError:
                            pass
                    
                    config.set(target_section, 'timeSpent', str(current_time + elapsed_seconds))
                    
                    with open(ini_path, 'w', encoding='utf-8') as f:
                        config.write(f)
                    print(f"Playtime updated: +{elapsed_seconds} seconds.")
            except Exception as e:
                print(f"Error occurred while saving playtime: {e}")

if __name__ == "__main__":
    main()
