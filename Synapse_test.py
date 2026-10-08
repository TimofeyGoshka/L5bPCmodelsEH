from neuron import h
from hayneuron import HayNeuron
import tools
import matplotlib.pyplot as plt

h.nrn_load_dll("mod/nrnmech.dll")

cvode = h.CVode()
cvode.active(1)

cell = HayNeuron()


# ============================================================
# Synapse parameters
# ============================================================

NUM_BASAL = 40
NUM_APICAL = 30
NUM_TUFT = 30

POISSON_RATE = 5       # Hz

EPSP_WEIGHT = 0.001    # nA

EPSP_TAU0 = 0.2        # ms
EPSP_TAU1 = 3.0        # ms


# ============================================================
# Find dendritic sections
# ============================================================

basal_sections = []
apical_sections = []
tuft_sections = []

for section in cell.cell.all:

    name = section.name()

    if "dend" in name:
        basal_sections.append(section)

    elif "apic" in name:
        apical_sections.append(section)


# For now, use distal apical sections as tuft candidates
tuft_sections = apical_sections[-30:]


# ============================================================
# Create synapses
# ============================================================

synapses = []
netstims = []
netcons = []


def add_excitatory_synapse(section, location=0.5):

    # -------------------------
    # EPSP synapse
    # -------------------------

    synapse = h.Exp2Syn(section(location))

    synapse.tau1 = EPSP_TAU0
    synapse.tau2 = EPSP_TAU1
    synapse.e = 0  # Reversal potential
    


    # -------------------------
    # Poisson source
    # -------------------------

    stim = h.NetStim()

    stim.interval = 1000 / POISSON_RATE
    stim.number = 1e9
    stim.start = 0
    stim.noise = 1


    # -------------------------
    # Connect source → synapse
    # -------------------------

    nc = h.NetCon(
        stim,
        synapse
    )

    nc.weight[0] = 1


    # -------------------------
    # Keep references
    # -------------------------

    synapses.append(synapse)
    netstims.append(stim)
    netcons.append(nc)


# ============================================================
# Place synapses
# ============================================================

for section in basal_sections[:NUM_BASAL]:
    add_excitatory_synapse(section)


for section in apical_sections[:NUM_APICAL]:
    add_excitatory_synapse(section)


for section in tuft_sections[:NUM_TUFT]:
    add_excitatory_synapse(section)


# ============================================================
# Record voltage
# ============================================================

t, v = tools.record_voltage(
    cell.cell.soma[0](0.5)
)


# ============================================================
# Record spikes
# ============================================================

spikes, spike_detector = tools.record_spikes(
    cell.cell.soma[0](0.5)
)


# ============================================================
# Run simulation
# ============================================================

h.tstop = 1000
h.v_init = -80

h.finitialize(h.v_init)
h.run()



# ============================================================
# Results
# ============================================================

print("Simulation finished")
print(f"Synapses: {len(synapses)}")
print(f"Poisson rate: {POISSON_RATE} Hz")
print(f"Spikes: {len(spikes)}")

print(
    f"Firing rate: "
    f"{tools.firing_rate(spikes, h.tstop):.2f} Hz"
)


# ============================================================
# Plot
# ============================================================

tools.plot_voltage(
    t,
    v,
    title="Hay neuron with Poisson excitatory input"
)