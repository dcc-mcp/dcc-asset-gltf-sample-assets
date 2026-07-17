from __future__ import annotations

from pathlib import Path
import sys
from typing import Any

from dcc_mcp_core.skill import skill_entry, skill_exception, skill_success

_SCRIPTS_DIR = Path(__file__).resolve().parent
if str(_SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS_DIR))

from _gltf_samples import download  # noqa: E402


@skill_entry
def main(path: str, output_dir: str, **_: Any) -> dict[str, Any]:
    try:
        result = download(path, output_dir)
        return skill_success("glTF sample file downloaded", **result)
    except Exception as exc:
        return skill_exception(exc, message="Failed to download glTF sample file")


if __name__ == "__main__":
    from dcc_mcp_core.skill import run_main

    run_main(main)
