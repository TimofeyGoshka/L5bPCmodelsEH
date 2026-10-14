"""
Thin wrapper around the original Hay et al. 2011 L5b pyramidal cell model.

The original model files live, unmodified, in thirdparty/hay2011/.
Everything we change goes here or in other files under src/.

Requires the compiled mechanisms (thirdparty/hay2011/mod/nrnmech.dll).
Recompile with nrnivmodl in that folder if NEURON is reinstalled or updated.
"""

import os
from contextlib import contextmanager
from pathlib import Path

import numpy as np
from neuron import h

# src/cells/hay_wrapper.py -> parents[0]=cells, [1]=src, [2]=repo root
REPO_ROOT = Path(__file__).resolve().parents[2]
HAY_DIR = REPO_ROOT / "thirdparty" / "hay2011"
MECH_DLL = HAY_DIR / "mod" / "nrnmech.dll"

_files_loaded = False


@contextmanager
def _in_hay_dir():
    """Temporarily switch to the Hay folder.

    The original hoc files and the morphology path are relative to it,
    so this makes loading work no matter where the script is run from.
    """
    previous = os.getcwd()
    os.chdir(HAY_DIR)
    try:
        yield
    finally:
        os.chdir(previous)


def load_model_files():
    """Load mechanisms and hoc files once per Python process.

    Loading the mechanisms twice raises an error, hence the guard.
    """
    global _files_loaded
    if _files_loaded:
        return

    if not MECH_DLL.exists():
        raise FileNotFoundError(
            f"Compiled mechanisms not found: {MECH_DLL}\n"
            "Run nrnivmodl inside thirdparty/hay2011/mod first."
        )

    with _in_hay_dir():
        # as_posix(): forward slashes avoid escape problems in hoc strings
        h.nrn_load_dll(MECH_DLL.as_posix())
        h.load_file("import3d.hoc")
        h.load_file("models/L5PCbiophys3.hoc")
        h.load_file("models/L5PCtemplate.hoc")
        h.load_file("stdrun.hoc")

    _files_loaded = True


class HayNeuron:
    """One Hay L5b pyramidal cell.

    The NEURON cell object is `self.cell`, the same attribute name the old
    scripts used (e.g. cell.cell.soma[0], cell.cell.apic[50]).
    """

    def __init__(self, morphology="cell1.asc"):
        load_model_files()
        with _in_hay_dir():
            self.cell = h.L5PCtemplate(f"morphologies/{morphology}")


def run_soma_current_step(
    neuron,
    amp_nA,
    delay_ms=100.0,
    dur_ms=500.0,
    tstop_ms=700.0,
    v_init=-80.0,
    dt=0.025,
    spike_threshold=0.0,
):
    """Inject a somatic current step and record the somatic voltage.

    Uses a fixed time step (dt) so runs are repeatable.
    Returns (t, v, spike_times) as numpy arrays (ms, mV, ms).
    Spikes are upward crossings of spike_threshold.
    """
    soma = neuron.cell.soma[0](0.5)

    stim = h.IClamp(soma)
    stim.delay = delay_ms
    stim.dur = dur_ms
    stim.amp = amp_nA

    t_vec = h.Vector().record(h._ref_t)
    v_vec = h.Vector().record(soma._ref_v)

    h.CVode().active(0)
    h.dt = dt
    h.tstop = tstop_ms
    h.v_init = v_init
    h.run()

    t = t_vec.as_numpy().copy()
    v = v_vec.as_numpy().copy()

    crossings = np.where((v[:-1] < spike_threshold) & (v[1:] >= spike_threshold))[0] + 1
    return t, v, t[crossings]
