from pathlib import Path

from tests.support import postgres


def test_load_local_stack_postgres_defaults_reads_compose_values(
    tmp_path: Path,
    monkeypatch,
) -> None:
    compose_file = tmp_path / "docker-compose.yml"
    compose_file.write_text(
        """
services:
  db:
    image: postgres:17-alpine
    environment:
      POSTGRES_DB: palio
      POSTGRES_USER: palio
      POSTGRES_PASSWORD: palio
""".strip(),
        encoding="utf-8",
    )
    monkeypatch.setattr(postgres, "LOCAL_STACK_COMPOSE_FILE", compose_file)
    postgres.load_local_stack_postgres_defaults.cache_clear()

    defaults = postgres.load_local_stack_postgres_defaults()

    assert defaults.image == "postgres:17-alpine"
    assert defaults.user == "palio"
    assert defaults.password == "palio"
    assert defaults.database == "palio"
    assert defaults.admin_url == "postgresql+psycopg://palio:palio@127.0.0.1:5432/palio"
