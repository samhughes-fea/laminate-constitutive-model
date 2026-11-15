"""Laminate stages report on the shared logger."""

from __future__ import annotations

import pytest

from laminate_constitutive_model.stage_log import (
    LOGGER_NAME,
    StageCollector,
    StageReport,
    collecting,
    fold_reports,
    stage,
)


def test_a_stage_records_seconds_and_an_error_keeps_its_time() -> None:
    with collecting() as sink:
        with stage("laminate_constitutive_model", "kept"):
            pass
        with pytest.raises(RuntimeError):
            with stage("laminate_constitutive_model", "failed"):
                raise RuntimeError("stage failed")
    folded = fold_reports(sink.take())
    assert folded["kept"] >= 0.0
    failed = folded["failed"]
    assert isinstance(failed, dict)
    assert failed["seconds"] >= 0.0
    assert failed["error"] == "stage failed"


def test_public_contract() -> None:
    import dataclasses
    import logging

    assert LOGGER_NAME == "blade.stage"
    assert [item.name for item in dataclasses.fields(StageReport)] == [
        "package", "stage", "seconds", "error", "depth", "started",
        "cpu_seconds", "measures"]
    assert callable(stage) and callable(fold_reports)
    assert issubclass(StageCollector, logging.Handler)


def test_generalized_section_reports_laminate_mechanics(cfrp) -> None:
    from laminate_constitutive_model.laminate_kinematics import FSDTModel, generalized_section
    from laminate_constitutive_model.laminate_mechanics import Laminate

    laminate = Laminate.from_angles(cfrp, [0, 90], 0.001)
    with collecting() as sink:
        generalized_section(FSDTModel(), laminate)
    reports = sink.take()
    assert reports[0].measures["stations"] == 1
    folded = fold_reports(reports)
    assert folded["laminate_mechanics"] >= 0.0
