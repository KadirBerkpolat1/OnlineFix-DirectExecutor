import os
import json
import urllib.request
import urllib.parse
import subprocess

class HubcapManager:
    def __init__(self, api_key=None):
        self.api_key = api_key
        
        # Determine steam paths
        self.steam_paths = [
            os.path.expanduser("~/.local/share/Steam"),
            os.path.expanduser("~/.steam/steam"),
            os.path.expanduser("~/.var/app/com.valvesoftware.Steam/data/Steam")
        ]

    def set_api_key(self, api_key):
        self.api_key = api_key

    def search_game(self, query):
        """
        Search for a game using Steam Store API to get the AppID.
        """
        encoded_query = urllib.parse.quote(query)
        url = f"https://store.steampowered.com/api/storesearch/?term={encoded_query}&l=english&cc=US"
        
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode())
        
        results = []
        for item in data.get("items", []):
            results.append({
                "app_id": str(item["id"]),
                "name": item["name"],
                "type": "game"
            })
            
        if not results:
            raise Exception("No games found on Steam matching this query.")
            
        return results

    def get_app_depots(self, app_id):
        """
        Fetch depot information from SteamCMD API.
        """
        url = f"https://api.steamcmd.net/v1/info/{app_id}"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode())
            
        if data.get("status") != "success":
            raise Exception("Failed to fetch app info from SteamCMD API.")
            
        app_data = data.get("data", {}).get(app_id, {})
        depots = app_data.get("depots", {})
        
        depot_manifests = []
        for depot_id, depot_info in depots.items():
            # Skip branches, just get public manifest
            if not isinstance(depot_info, dict):
                continue
                
            manifests = depot_info.get("manifests", {})
            public_manifest = manifests.get("public", {})
            
            if "gid" in public_manifest:
                depot_manifests.append({
                    "depot_id": depot_id,
                    "manifest_id": public_manifest["gid"]
                })
                
        return depot_manifests

    def download_manifests(self, app_id, progress_callback=None):
        """
        Downloads manifest and depot keys for the specified app_id
        and places them in the Steam depotcache directory using Hubcap API.
        """
        if not self.api_key:
            raise ValueError("API Key is required to download manifests.")

        if progress_callback:
            progress_callback(10, f"Fetching depot info for AppID: {app_id}...")

        try:
            depots = self.get_app_depots(app_id)
        except Exception as e:
            raise Exception(f"Failed to get depots: {str(e)}")

        if not depots:
            raise Exception("No public depots found for this game.")

        total_depots = len(depots)
        
        for steam_path in self.steam_paths:
            if not os.path.exists(steam_path):
                continue
                
            depot_path = os.path.join(steam_path, "steamapps", "depotcache")
            os.makedirs(depot_path, exist_ok=True)

            for idx, depot in enumerate(depots):
                depot_id = depot["depot_id"]
                manifest_id = depot["manifest_id"]
                
                pct = int(10 + (idx / total_depots) * 80)
                if progress_callback:
                    progress_callback(pct, f"Downloading manifest for depot {depot_id}...")

                # Hubcap API URL
                hubcap_url = f"https://hubcapmanifest.com/api/v1/generate/manifest?depot_id={depot_id}&manifest_id={manifest_id}&api_key={self.api_key}"
                manifest_file = os.path.join(depot_path, f"{depot_id}_{manifest_id}.manifest")
                
                try:
                    req = urllib.request.Request(hubcap_url, headers={'User-Agent': 'Mozilla/5.0'})
                    with urllib.request.urlopen(req) as response:
                        manifest_data = response.read()
                        with open(manifest_file, 'wb') as f:
                            f.write(manifest_data)
                except Exception as e:
                    print(f"Warning: Failed to download manifest {depot_id}: {e}")
                    # In a real app we might retry, or show warning.
                    
            if progress_callback:
                progress_callback(95, "Triggering Steam Install protocol...")
            
            # Optionally trigger steam://install/APP_ID to kickstart Steam
            try:
                subprocess.Popen(["xdg-open", f"steam://install/{app_id}"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            except:
                pass
                
            break # Only need to do it for the first valid steam path

        if progress_callback:
            progress_callback(100, "Manifests installed successfully. Steam should start downloading shortly.")

        return True

    def install_enter_the_wired(self, progress_callback=None):
        if progress_callback:
            progress_callback(10, "Downloading enter-the-wired installer...")
        try:
            cmd = 'curl -fsSL https://raw.githubusercontent.com/ciscosweater/enter-the-wired/main/enter-the-wired | bash'
            process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
            for line in process.stdout:
                if progress_callback:
                    progress_callback(50, f"Installer: {line.strip()}")
            process.wait()
            if process.returncode == 0:
                if progress_callback:
                    progress_callback(100, "enter-the-wired installed successfully.")
                return True
            else:
                raise Exception(f"Installer exited with code {process.returncode}")
        except Exception as e:
            if progress_callback:
                progress_callback(100, f"Error installing enter-the-wired: {str(e)}")
            raise e
