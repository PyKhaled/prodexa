import platform
import webbrowser
import requests
from prodexa.__version__ import __version__

GITHUB_REPO = "pykhaled/prodexa"
GITHUB_API = f"https://api.github.com/repos/{GITHUB_REPO}/releases/latest"


def is_newer_version(latest: str, current: str) -> bool:
    def normalize(v):
        return [int(x) for x in v.lstrip("v").split(".")]
    return normalize(latest) > normalize(current)


def check_for_update():
    try:
        response = requests.get(GITHUB_API, timeout=5)
        response.raise_for_status()
        data = response.json()

        latest_version = data["tag_name"]
        assets = data.get("assets", [])

        if not is_newer_version(latest_version, __version__):
            return None

        asset = select_asset(assets)
        if not asset:
            return None

        return {
            "version": latest_version,
            "url": asset["browser_download_url"],
            "name": asset["name"],
        }

    except Exception:
        return None


def select_asset(assets):
    system = platform.system().lower()

    for asset in assets:
        name = asset["name"].lower()

        if system == "darwin" and name.endswith(".dmg"):
            return asset
        if system == "windows" and name.endswith(".exe"):
            return asset
        if system == "linux" and not name.endswith((".exe", ".dmg")):
            return asset

    return None


def open_download(url: str):
    webbrowser.open(url)
