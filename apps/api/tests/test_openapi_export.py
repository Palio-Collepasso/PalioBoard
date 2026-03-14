from pathlib import Path

import yaml

from palio.app.export_openapi import export_openapi


def test_export_openapi_writes_current_contract(tmp_path: Path) -> None:
    output_path = export_openapi(tmp_path / "openapi.yaml")

    specification = yaml.safe_load(output_path.read_text(encoding="utf-8"))

    assert output_path.exists()
    assert specification["info"]["title"] == "PalioBoard API"
    assert specification["paths"].keys() >= {
        "/api/admin/health",
        "/api/public/health",
        "/healthz",
        "/realtime/health",
    }
