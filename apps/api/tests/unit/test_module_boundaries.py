from pathlib import Path

from palio.shared.module_boundaries import BoundaryViolation, check_module_boundaries


def test_scaffold_respects_boundary_rules() -> None:
    modules_root = Path(__file__).resolve().parents[2] / "src" / "palio" / "modules"
    assert check_module_boundaries(modules_root) == []


def test_boundary_checker_reports_cross_module_internal_imports(tmp_path: Path) -> None:
    modules_root = tmp_path / "palio" / "modules"
    (modules_root / "identity" / "application").mkdir(parents=True)
    (modules_root / "authorization" / "infrastructure").mkdir(parents=True)

    (modules_root / "identity" / "__init__.py").write_text("")
    (modules_root / "identity" / "application" / "__init__.py").write_text("")
    (modules_root / "identity" / "application" / "service.py").write_text(
        "from palio.modules.authorization.infrastructure.repo import Repo\n"
    )
    (modules_root / "authorization" / "__init__.py").write_text("")
    (modules_root / "authorization" / "infrastructure" / "__init__.py").write_text("")
    (modules_root / "authorization" / "infrastructure" / "repo.py").write_text(
        "class Repo:\n"
        "    pass\n"
    )

    assert check_module_boundaries(modules_root) == [
        BoundaryViolation(
            file=modules_root / "identity" / "application" / "service.py",
            lineno=1,
            import_target="palio.modules.authorization.infrastructure.repo",
            message="Cross-module imports must target another module's facade.py only.",
        )
    ]
