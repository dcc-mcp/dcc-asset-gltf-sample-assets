from __future__ import annotations

import json
import os
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any


REPO = "KhronosGroup/glTF-Sample-Assets"
BRANCH = "main"
API = f"https://api.github.com/repos/{REPO}"
RAW = f"https://raw.githubusercontent.com/{REPO}/{BRANCH}"
LICENSE_NOTICE = {
    "repository": f"https://github.com/{REPO}",
    "usage_notice": "Sample assets have per-model licenses and credits. Keep model README.md or LICENSE.md with downloaded files.",
}


def _headers() -> dict[str, str]:
    headers = {"User-Agent": "dcc-mcp-gltf-sample-assets/0.1"}
    if os.environ.get("GITHUB_TOKEN"):
        headers["Authorization"] = f"Bearer {os.environ['GITHUB_TOKEN']}"
    return headers


def tree() -> list[dict[str, Any]]:
    url = f"{API}/git/trees/{BRANCH}?recursive=1"
    req = urllib.request.Request(url, headers=_headers())
    with urllib.request.urlopen(req, timeout=60) as resp:
        return json.loads(resp.read().decode("utf-8")).get("tree", [])


def model_files(model_name: str) -> list[dict[str, Any]]:
    prefix = f"Models/{model_name.strip('/')}/"
    return [item for item in tree() if item.get("type") == "blob" and item.get("path", "").startswith(prefix)]


def search_models(query: str | None = None, limit: int = 20) -> list[dict[str, Any]]:
    needle = (query or "").lower()
    models: dict[str, dict[str, Any]] = {}
    for item in tree():
        path = item.get("path", "")
        parts = path.split("/")
        if len(parts) < 3 or parts[0] != "Models":
            continue
        name = parts[1]
        if needle and needle not in name.lower() and needle not in path.lower():
            continue
        rec = models.setdefault(name, {"name": name, "variants": set(), "license_files": [], "sample_files": []})
        if len(parts) > 3:
            rec["variants"].add(parts[2])
        if parts[-1].lower() in {"license.md", "readme.md"}:
            rec["license_files"].append(path)
        if path.lower().endswith((".glb", ".gltf")) and len(rec["sample_files"]) < 6:
            rec["sample_files"].append(path)
    out = []
    for rec in models.values():
        rec["variants"] = sorted(rec["variants"])
        out.append(rec)
        if len(out) >= limit:
            break
    return out


def raw_url(path: str) -> str:
    return f"{RAW}/{urllib.parse.quote(path.strip('/'), safe='/')}"


def download(path: str, output_dir: str) -> dict[str, Any]:
    safe_path = path.strip("/")
    if not safe_path.startswith("Models/"):
        raise ValueError("path must be under Models/")
    target = Path(output_dir) / Path(safe_path).name
    target.parent.mkdir(parents=True, exist_ok=True)
    req = urllib.request.Request(raw_url(safe_path), headers={"User-Agent": "dcc-mcp-gltf-sample-assets/0.1"})
    with urllib.request.urlopen(req, timeout=180) as resp:
        target.write_bytes(resp.read())
    return {"file": str(target), "source_path": safe_path, "source_url": raw_url(safe_path), **LICENSE_NOTICE}
