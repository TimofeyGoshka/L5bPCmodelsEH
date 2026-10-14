"""
Reproduction check for the Hay et al. 2011 demo protocols (Fig 4A BAC firing,
Fig 4B step current firing).

Two layers of checking:

1. Qualitative checks that always run (BAC beats its parts, firing rises with
   current). These need no reference numbers.
2. Quantitative checks against REFERENCE below. Fill the values in yourself:
   - from the original GUI demo (exact match expected), or
   - from the paper's figure (decide the tolerance yourself).
   None = not filled in yet, so that check is skipped.

Run from the repo root:  python tests/test_hay_protocols.py
Add --plot to see the BAC traces for comparison with Fig 4A.
"""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.cells.hay_wrapper import HayNeuron  # noqa: E402
from src.protocols.hay_protocols import run_bac_protocol, run_step_protocol  # noqa: E402

STEP_AMPLITUDES_NA = (0.619, 0.793, 1.507)

# Fill in from the original demo console ("spike count = N") or from the paper.
REFERENCE = {
    "step_0.619_spikes": None,
    "step_0.793_spikes": None,
    "step_1.507_spikes": None,
}
REFERENCE_TOLERANCE = 0  # 0 = exact match (right for the original-demo count)

_neuron = None


def get_neuron():
    global _neuron
    if _neuron is None:
        _neuron = HayNeuron()
    return _neuron


def test_step_firing_rises_with_current():
    counts = [run_step_protocol(get_neuron(), a).n_spikes for a in STEP_AMPLITUDES_NA]
    assert counts[0] <= counts[1] <= counts[2]
    assert counts[2] > 0


def test_step_matches_reference():
    for amp in STEP_AMPLITUDES_NA:
        expected = REFERENCE[f"step_{amp}_spikes"]
        if expected is None:
            continue
        got = run_step_protocol(get_neuron(), amp).n_spikes
        assert abs(got - expected) <= REFERENCE_TOLERANCE, (amp, got, expected)


def test_bac_beats_its_parts():
    bap = run_bac_protocol(get_neuron(), "BAP")
    epsp = run_bac_protocol(get_neuron(), "EPSP")
    bac = run_bac_protocol(get_neuron(), "BAC")
    assert bac.n_spikes > bap.n_spikes
    assert bac.n_spikes > epsp.n_spikes
    assert bac.max_v_distal > bap.max_v_distal


if __name__ == "__main__":
    neuron = get_neuron()

    print("Step current protocol (2000 ms step at the soma)")
    for amp in STEP_AMPLITUDES_NA:
        r = run_step_protocol(neuron, amp)
        print(f"  {amp} nA: {r.n_spikes} spikes")

    print("\nBAC protocol (distal site 620 um, proximal site 400 um)")
    results = {}
    for kind in ("BAP", "EPSP", "BAC", "CaBurst"):
        r = run_bac_protocol(neuron, kind)
        results[kind] = r
        print(
            f"  {kind:8s} spikes={r.n_spikes}  "
            f"max soma={r.max_v_soma:6.1f} mV  max distal={r.max_v_distal:6.1f} mV"
        )

    test_step_firing_rises_with_current()
    test_step_matches_reference()
    test_bac_beats_its_parts()
    print("\nChecks passed.")

    if "--plot" in sys.argv:
        import matplotlib.pyplot as plt

        fig, axes = plt.subplots(2, 1, sharex=True, figsize=(8, 6))
        for kind in ("BAP", "EPSP", "BAC"):
            r = results[kind]
            axes[0].plot(r.t, r.v_soma, label=kind)
            axes[1].plot(r.t, r.v_distal, label=kind)
        axes[0].set_ylabel("Soma (mV)")
        axes[1].set_ylabel("Distal apical (mV)")
        axes[1].set_xlabel("Time (ms)")
        axes[0].legend()
        plt.show()
