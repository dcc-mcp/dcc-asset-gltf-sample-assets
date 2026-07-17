from __future__ import annotations

import importlib.util
import os
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skill" / "gltf-sample-assets"
SCRIPTS = SKILL / "scripts"


def load(name: str):
    script_dir = str(SCRIPTS)
    sys.path[:] = [entry for entry in sys.path if entry != script_dir]
    sys.modules.pop("_gltf_samples", None)
    spec = importlib.util.spec_from_file_location(name, SCRIPTS / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    return module


def validate_skill() -> None:
    from dcc_mcp_core import validate_skill

    report = validate_skill(str(SKILL))
    assert not report.has_errors, report


def validate_direct_imports() -> None:
    """Maya's legacy file executor does not add the script directory to sys.path."""
    for name in (
        "search_gltf_sample_assets",
        "list_gltf_sample_files",
        "download_gltf_sample_file",
    ):
        assert callable(load(name).main)


def live_gltf_smoke() -> None:
    if os.environ.get("RUN_LIVE_API_SMOKE") != "true":
        print("skip live glTF sample assets smoke")
        return
    search = load("search_gltf_sample_assets").main(query="Avocado", limit=1)
    assert search["success"], search
    files = load("list_gltf_sample_files").main(model_name="Avocado")
    assert files["success"], files
    assert files["context"]["files"], files


def main() -> None:
    validate_direct_imports()
    validate_skill()
    live_gltf_smoke()


if __name__ == "__main__":
    main()
