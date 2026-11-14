"""Writes pluginmaster.json from the manifests inside plugins/<InternalName>/latest.zip."""

import json
import subprocess
from pathlib import Path
from zipfile import ZipFile

PLUGINS_DIR = Path("plugins")
MASTER_PATH = Path("pluginmaster.json")
DOWNLOAD_URL = (
    "https://raw.githubusercontent.com/AurelienTHOREL/MyDalamudPlugins/master/"
    "plugins/{plugin_name}/latest.zip"
)

DEFAULTS = {
    "IsHide": False,
    "IsTestingExclusive": False,
    "ApplicableVersion": "any",
}

KEPT_KEYS = [
    "Author",
    "Name",
    "Punchline",
    "Description",
    "InternalName",
    "AssemblyVersion",
    "RepoUrl",
    "IconUrl",
    "ApplicableVersion",
    "Tags",
    "DalamudApiLevel",
]


def read_manifest(zip_path: Path) -> dict:
    """Returns the <InternalName>.json manifest stored at the root of a plugin zip."""
    plugin_name = zip_path.parent.name
    manifest_name = f"{plugin_name}.json"
    with ZipFile(zip_path) as archive:
        if manifest_name not in archive.namelist():
            raise SystemExit(f"{zip_path}: no {manifest_name} at the root of the zip")
        manifest = json.loads(archive.read(manifest_name).decode("utf-8-sig"))
    if manifest.get("InternalName") != plugin_name:
        raise SystemExit(
            f"{zip_path}: InternalName {manifest.get('InternalName')!r} "
            f"does not match the folder name {plugin_name!r}"
        )
    return manifest


def last_commit_time(path: Path) -> str:
    """Returns the Unix time of the last commit that touched path."""
    result = subprocess.run(
        ["git", "log", "-1", "--format=%ct", "--", str(path)],
        capture_output=True,
        text=True,
        check=True,
    )
    timestamp = result.stdout.strip()
    if not timestamp:
        raise SystemExit(f"{path} has no commit yet; commit it before regenerating")
    return timestamp


def master_entry(zip_path: Path) -> dict:
    """Builds the pluginmaster entry for one plugin zip."""
    manifest = read_manifest(zip_path)
    entry = {key: manifest[key] for key in KEPT_KEYS if key in manifest}
    for key, value in DEFAULTS.items():
        entry.setdefault(key, value)
    download_url = DOWNLOAD_URL.format(plugin_name=entry["InternalName"])
    entry["DownloadLinkInstall"] = download_url
    entry["DownloadLinkTesting"] = download_url
    entry["DownloadLinkUpdate"] = download_url
    entry["DownloadCount"] = 0
    entry["LastUpdated"] = last_commit_time(zip_path)
    return entry


def main() -> None:
    zips = sorted(PLUGINS_DIR.glob("*/latest.zip"))
    master = [master_entry(zip_path) for zip_path in zips]
    MASTER_PATH.write_text(json.dumps(master, indent=4) + "\n", encoding="utf-8")
    print(f"pluginmaster.json: {len(master)} plugin(s)")


if __name__ == "__main__":
    main()
