"""
Python versions of the original Hay et al. 2011 demo protocols:

  thirdparty/hay2011/simulationcode/Step_current_firing.hoc  (Fig 4B)
  thirdparty/hay2011/simulationcode/BAC_firing.hoc           (Fig 4A)

Settings (amplitudes, timings, sites) are copied from the hoc files so the
results can be compared with the original GUI demo and with the paper.
The original files are never modified.

Both protocols use the variable time step (CVode active), like the originals.
"""

from dataclasses import dataclass

import numpy as np
from neuron import h

SPIKE_THRESHOLD_MV = -10.0  # same as the APCount threshold in the original step demo


# ---------------------------------------------------------------------------
# Step current (Step_current_firing.hoc)
# ---------------------------------------------------------------------------

@dataclass
class StepResult:
    step_amp_nA: float
    t: np.ndarray
    v_soma: np.ndarray
    spike_times: np.ndarray

    @property
    def n_spikes(self):
        return len(self.spike_times)


def run_step_protocol(
    neuron,
    step_amp_nA=0.793,
    delay_ms=700.0,
    dur_ms=2000.0,
    tstop_ms=3000.0,
    v_init=-80.0,
):
    """Somatic current step. The original comments list three amplitudes:
    step 1 = 0.619 nA, step 2 = 0.793 nA (the file default), step 3 = 1.507 nA.
    """
    soma = neuron.cell.soma[0](0.5)

    stim = h.IClamp(soma)
    stim.delay = delay_ms
    stim.dur = dur_ms
    stim.amp = step_amp_nA

    t_vec = h.Vector().record(h._ref_t)
    v_vec = h.Vector().record(soma._ref_v)

    apc = h.APCount(soma)
    apc.thresh = SPIKE_THRESHOLD_MV
    spike_vec = h.Vector()
    apc.record(spike_vec)

    h.CVode().active(1)
    h.tstop = tstop_ms
    h.v_init = v_init
    h.run()

    return StepResult(
        step_amp_nA=step_amp_nA,
        t=t_vec.as_numpy().copy(),
        v_soma=v_vec.as_numpy().copy(),
        spike_times=np.array(spike_vec),
    )


# ---------------------------------------------------------------------------
# BAC firing (BAC_firing.hoc)
# ---------------------------------------------------------------------------

PULSE_DELAY_MS = 295.0
PULSE_DUR_MS = 5.0


def find_apical_site(cell, distance_um):
    """Apical site at a given path distance from the soma.

    Same rule as the original: among the sites the template returns for that
    distance, take the one with the largest diameter.
    """
    sites = cell.locateSites("apic", distance_um)
    best = None
    best_diam = 0.0
    for i in range(int(sites.count())):
        site = sites.o(i)
        sec_idx = int(site[0])
        loc = site[1]
        diam = cell.apic[sec_idx](loc).diam
        if diam > best_diam:
            best_diam = diam
            best = (sec_idx, loc)
    if best is None:
        raise RuntimeError(f"No apical site found at {distance_um} um")
    return best


@dataclass
class BACResult:
    experiment_type: str
    t: np.ndarray
    v_soma: np.ndarray
    v_distal: np.ndarray
    v_proximal: np.ndarray
    i_epsp: np.ndarray
    spike_times: np.ndarray
    distal_site: tuple
    proximal_site: tuple

    @property
    def n_spikes(self):
        return len(self.spike_times)

    @property
    def max_v_distal(self):
        return float(self.v_distal.max())

    @property
    def max_v_soma(self):
        return float(self.v_soma.max())


def run_bac_protocol(
    neuron,
    experiment_type="BAC",
    bac_dt_ms=5.0,
    square_amp_nA=1.9,
    imax_nA=0.5,
    rise_tau_ms=0.5,
    decay_tau_ms=5.0,
    proximal_um=400.0,
    distal_um=620.0,
    tstop_ms=600.0,
    v_init=-80.0,
):
    """Somatic 5 ms pulse plus an EPSP-like current injected in the distal apical dendrite.

    experiment_type: 'BAP' (pulse only), 'EPSP' (dendritic current only),
    'CaBurst' (3x dendritic current only), or 'BAC' (both).
    The 'EPSP' current is the epsp point process from the original mod folder
    (a current injection, not a conductance synapse).
    """
    amplitudes = {
        "BAP": (square_amp_nA, 0.0),
        "CaBurst": (0.0, imax_nA * 3),
        "BAC": (square_amp_nA, imax_nA),
        "EPSP": (0.0, imax_nA),
    }
    if experiment_type not in amplitudes:
        raise ValueError(f"experiment_type must be one of {list(amplitudes)}")
    soma_amp, epsp_amp = amplitudes[experiment_type]

    cell = neuron.cell
    soma = cell.soma[0](0.5)

    pulse = h.IClamp(soma)
    pulse.delay = PULSE_DELAY_MS
    pulse.dur = PULSE_DUR_MS
    pulse.amp = soma_amp

    distal_site = find_apical_site(cell, distal_um)
    proximal_site = find_apical_site(cell, proximal_um)
    distal = cell.apic[distal_site[0]](distal_site[1])
    proximal = cell.apic[proximal_site[0]](proximal_site[1])

    epsp = h.epsp(distal)
    epsp.tau0 = rise_tau_ms
    epsp.tau1 = decay_tau_ms
    epsp.onset = PULSE_DELAY_MS + bac_dt_ms
    epsp.imax = epsp_amp

    t_vec = h.Vector().record(h._ref_t)
    v_soma = h.Vector().record(soma._ref_v)
    v_distal = h.Vector().record(distal._ref_v)
    v_proximal = h.Vector().record(proximal._ref_v)
    i_epsp = h.Vector().record(epsp._ref_i)

    apc = h.APCount(soma)
    apc.thresh = SPIKE_THRESHOLD_MV
    spike_vec = h.Vector()
    apc.record(spike_vec)

    h.CVode().active(1)
    h.tstop = tstop_ms
    h.v_init = v_init
    h.run()

    return BACResult(
        experiment_type=experiment_type,
        t=t_vec.as_numpy().copy(),
        v_soma=v_soma.as_numpy().copy(),
        v_distal=v_distal.as_numpy().copy(),
        v_proximal=v_proximal.as_numpy().copy(),
        i_epsp=i_epsp.as_numpy().copy(),
        spike_times=np.array(spike_vec),
        distal_site=distal_site,
        proximal_site=proximal_site,
    )
