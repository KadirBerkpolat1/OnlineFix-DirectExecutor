import os
import subprocess
import tempfile
import urllib.parse

class AutoCracker:
    def __init__(self):
        # Base url for searching
        self.search_url = "https://onlinefix.me/index.php?do=search"

    def search_fix(self, game_name):
        """
        Mock search function for OnlineFix.
        In a real scenario, this would bypass CF, log in, and scrape the download links.
        """
        # Simulated response
        return [
            {
                "title": f"{game_name} - Online Multiplayer Fix",
                "download_url": "https://example.com/dummy_fix.rar",
                "type": "steam_fix"
            }
        ]

    def download_and_apply(self, download_url, target_game_dir, progress_callback=None):
        """
        Downloads the fix using aria2c and extracts it to the game directory.
        """
        if not os.path.exists(target_game_dir):
            raise FileNotFoundError(f"Target game directory not found: {target_game_dir}")

        with tempfile.TemporaryDirectory() as temp_dir:
            file_name = os.path.basename(urllib.parse.urlparse(download_url).path)
            if not file_name:
                file_name = "fix_archive.rar"

            out_path = os.path.join(temp_dir, file_name)

            if progress_callback:
                progress_callback(10, f"Starting download with aria2c...")

            # 1. Download using aria2c
            try:
                cmd = [
                    "aria2c",
                    "--max-connection-per-server=4",
                    "--split=4",
                    "--dir", temp_dir,
                    "--out", file_name,
                    download_url
                ]

                # Mocking the download since we use a dummy URL
                if "example.com" in download_url:
                    if progress_callback:
                        progress_callback(50, "Simulating download of fix archive...")
                    with open(out_path, 'w') as f:
                        f.write("DUMMY ARCHIVE CONTENT")
                else:
                    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
                    for line in process.stdout:
                        if progress_callback and "Download Progress" in line: # Basic filtering
                            progress_callback(50, line.strip())
                    process.wait()

                    if process.returncode != 0:
                        raise Exception("aria2c download failed.")

            except Exception as e:
                raise Exception(f"Download error: {e}")

            if progress_callback:
                progress_callback(70, "Download complete. Extracting files...")

            # 2. Extract Archive
            # Assuming it's a RAR or ZIP. In Linux, 7z or unrar is often used.
            try:
                # If it's a dummy file, we just simulate extraction
                if "example.com" in download_url:
                    dummy_fix = os.path.join(target_game_dir, "OnlineFix64.dll")
                    dummy_ini = os.path.join(target_game_dir, "OnlineFix.ini")
                    with open(dummy_fix, 'w') as f: f.write("DUMMY DLL")
                    with open(dummy_ini, 'w') as f: f.write("[OnlineFix]\nSteamId=123456")
                else:
                    # Attempt 7z extraction (requires p7zip)
                    extract_cmd = ["7z", "x", "-y", f"-o{target_game_dir}", out_path]
                    subprocess.run(extract_cmd, check=True, stdout=subprocess.DEVNULL)
            except Exception as e:
                raise Exception(f"Extraction error (Ensure 7z/unrar is installed): {e}")

            if progress_callback:
                progress_callback(100, "Fix applied successfully! Steam configuration updated.")

            return True
