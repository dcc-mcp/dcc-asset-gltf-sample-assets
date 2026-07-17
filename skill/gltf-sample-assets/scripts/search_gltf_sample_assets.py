from __future__ import annotations

from pathlib import Path
import sys
from typing import Any

from dcc_mcp_core.skill import skill_entry, skill_exception, skill_success

_SCRIPTS_DIR = Path(__file__).resolve().parent
if str(_SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS_DIR))

from _gltf_samples import LICENSE_NOTICE, search_models  # noqa: E402


@skill_entry
def main(query: str | None = None, limit: int = 20, **_: Any) -> dict[str, Any]:
    try:
        assets = search_models(query, limit)
        return skill_success("glTF sample assets found", assets=assets, count=len(assets), license=LICENSE_NOTICE)
    except Exception as exc:
        return skill_exception(exc, message="Failed to search glTF sample assets")


if __name__ == "__main__":
    from dcc_mcp_core.skill import run_main

    run_main(main)
