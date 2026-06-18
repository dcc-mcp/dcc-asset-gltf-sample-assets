from __future__ import annotations

from typing import Any

from dcc_mcp_core.skill import skill_entry, skill_exception, skill_success

from _gltf_samples import download


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
