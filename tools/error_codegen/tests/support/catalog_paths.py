"""Path helpers for error_codegen test fixtures and snapshots.

Keep file-system plumbing here only for the tool suite.
"""

import shutil
import sys
from importlib import util
from pathlib import Path
from types import ModuleType

TESTS_ROOT = Path(__file__).resolve().parents[1]
REPOSITORY_ROOT = Path(__file__).resolve().parents[4]
FIXTURES_ROOT = TESTS_ROOT / "fixtures" / "catalogs"
SNAPSHOTS_ROOT = TESTS_ROOT / "snapshots"
API_SRC_DIR = REPOSITORY_ROOT / "apps" / "api" / "src"


def materialize_catalog_fixture(
    fixture_name: str,
    *,
    kind: str,
    output_dir: Path,
) -> Path:
    catalog_root = output_dir / "catalog"
    shutil.copytree(FIXTURES_ROOT / "base", catalog_root)
    overlay_root = FIXTURES_ROOT / kind / fixture_name
    for source_path in sorted(overlay_root.rglob("*")):
        if source_path.is_dir():
            continue
        target_path = catalog_root / source_path.relative_to(overlay_root)
        target_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source_path, target_path)
    return catalog_root / "index.yaml"


def snapshot_path(*parts: str) -> Path:
    return SNAPSHOTS_ROOT.joinpath(*parts)


def load_module_from_path(path: Path, *, module_name: str) -> ModuleType:
    api_src = str(API_SRC_DIR)
    if api_src not in sys.path:
        sys.path.insert(0, api_src)

    spec = util.spec_from_file_location(module_name, path)
    assert spec is not None
    assert spec.loader is not None
    module = util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module
