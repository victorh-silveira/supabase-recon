"""CLI e parser."""

from __future__ import annotations

import pytest

from recon.domain.exceptions import BundleNotFoundError, MissingAnonKeyError
from recon.domain.models import BundleAnalysis, SupabaseProjectConfig
from recon.presentation.cli import build_parser, main


def test_build_parser_human_summary_flag() -> None:
    """Flag --human-summary e --output-root."""
    p = build_parser()
    args = p.parse_args(["--url", "https://a", "--human-summary", "--output-root", "C:\\tmp\\o", "--no-test"])
    assert args.human_summary is True
    assert args.output_root.parts[-1] == "o"


def test_cli_main_success(monkeypatch: pytest.MonkeyPatch) -> None:
    """Main termina sem excepção com orquestrador falso."""
    analysis = BundleAnalysis(
        supabase=SupabaseProjectConfig(
            base_url="https://proj.supabase.co",
            anon_key="eyJh.b.c",
        ),
        auth_endpoints=[],
        tables=["t"],
        rpcs=[],
        edge_functions=[],
    )

    class FakeOrch:
        def run(self, options, output_root=None):
            _ = (options, output_root)
            return analysis

    monkeypatch.setattr(
        "recon.presentation.cli.build_orchestrator",
        lambda **_kwargs: FakeOrch(),
    )
    main(["--url", "https://app.example", "--no-test"])


def test_cli_exits_on_domain_error(monkeypatch: pytest.MonkeyPatch) -> None:
    """MissingAnonKeyError mapeia para SystemExit(1)."""

    class Boom:
        def run(self, *_args: object, **_kwargs: object) -> None:
            raise MissingAnonKeyError("x")

    monkeypatch.setattr(
        "recon.presentation.cli.build_orchestrator",
        lambda **_kwargs: Boom(),
    )
    with pytest.raises(SystemExit) as exc:
        main(["--url", "https://x", "--no-test"])
    assert exc.value.code == 1


def test_cli_exits_on_bundle_not_found(monkeypatch: pytest.MonkeyPatch) -> None:
    """BundleNotFoundError mapeia para SystemExit(1)."""

    class Boom:
        def run(self, *_args: object, **_kwargs: object) -> None:
            raise BundleNotFoundError("nope")

    monkeypatch.setattr(
        "recon.presentation.cli.build_orchestrator",
        lambda **_kwargs: Boom(),
    )
    with pytest.raises(SystemExit) as exc:
        main(["--url", "https://x", "--no-test"])
    assert exc.value.code == 1
