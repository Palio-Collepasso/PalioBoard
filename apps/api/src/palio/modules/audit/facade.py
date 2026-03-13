"""Public facade for the audit module."""

from palio.shared.module_facade import ModuleFacade

AuditFacade = ModuleFacade


def build_audit_facade() -> AuditFacade:
    return ModuleFacade(
        module_name="audit",
        purpose="Append-only audit persistence for authoritative changes.",
    )
