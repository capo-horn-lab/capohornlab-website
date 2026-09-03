"""Backtest artifacts must disclose their non-executable reference-price basis."""

import subprocess
import sys
from pathlib import Path

from research.backtest_engine import BacktestEngine, BacktestStats


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def test_report_carries_machine_readable_non_executable_execution_assumptions():
    engine = BacktestEngine(symbol="NQ")

    report = engine.get_report(stats=BacktestStats())

    assumptions = report["execution_assumptions"]
    assert assumptions["fill_model"] == "bar_reference_only"
    assert assumptions["executable_fills"] is False
    assert assumptions["commission_per_contract_per_side"] == 2.50
    assert assumptions["assumed_slippage_ticks_per_side"] == 1.0
    assert assumptions["costs_are_calibrated"] is False
    assert "not executable fills" in assumptions["limitations"]


def test_declared_reference_costs_drive_engine_commission_and_slippage():
    assumptions = __import__("research.market_data_engine", fromlist=["ExecutionAssumptions"]).ExecutionAssumptions.bar_reference_only(
        commission_per_contract_per_side=3.75,
        assumed_slippage_ticks_per_side=2.0,
    )
    engine = BacktestEngine(symbol="NQ", execution_assumptions=assumptions)

    assert engine._commission_for(quantity=2) == 7.50
    assert engine._slippage_for_bar(quantity=1) == 0.50
    assert engine.slippage_model.assumed_slippage_ticks_per_side == 2.0


def test_backtest_script_can_run_directly_from_project_root():
    result = subprocess.run(
        [sys.executable, "research/backtest_engine.py", "--list"],
        cwd=PROJECT_ROOT,
        text=True,
        capture_output=True,
        check=False,
    )

    assert result.returncode == 0, result.stderr
    assert "OpeningRangeBreakout" in result.stdout
