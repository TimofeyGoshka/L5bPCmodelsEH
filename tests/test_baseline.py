"""
Baseline sanity test for the Hay cell.

This checks that the plumbing works (model loads, cell is quiet without
input, cell fires with a strong somatic step). It does NOT yet compare
against the published Hay et al. 2011 results; that comparison is a
separate step (see the figure folders in thirdparty/hay2011/model sets).

Run from the repo root:  python tests/test_baseline.py
Also works with pytest if you install it later.
"""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.cells.hay_wrapper import HayNeuron, run_soma_current_step  # noqa: E402

_neuron = None


def get_neuron():
    """Create the cell once and reuse it; every run re-initialises it."""
    global _neuron
    if _neuron is None:
        _neuron = HayNeuron()
    return _neuron


def test_model_loads():
    neuron = get_neuron()
    n_sections = len(list(neuron.cell.all))
    assert n_sections > 0
    assert neuron.cell.soma[0].L > 0


def test_quiet_without_input():
    neuron = get_neuron()
    t, v, spikes = run_soma_current_step(neuron, amp_nA=0.0, tstop_ms=300.0)
    assert len(spikes) == 0
    # Wide sanity window for the resting potential, not a published value
    assert -95.0 < v[-1] < -55.0


def test_fires_with_strong_step():
    neuron = get_neuron()
    t, v, spikes = run_soma_current_step(neuron, amp_nA=1.0)
    assert len(spikes) > 0


if __name__ == "__main__":
    neuron = get_neuron()
    print("Sections:", len(list(neuron.cell.all)))

    t, v, spikes = run_soma_current_step(neuron, amp_nA=0.0, tstop_ms=300.0)
    print(f"No input: {len(spikes)} spikes, final soma voltage {v[-1]:.1f} mV")

    t, v, spikes = run_soma_current_step(neuron, amp_nA=1.0)
    print(f"1.0 nA step (500 ms): {len(spikes)} spikes")

    test_model_loads()
    test_quiet_without_input()
    test_fires_with_strong_step()
    print("All baseline checks passed.")
