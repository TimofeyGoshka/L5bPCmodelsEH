from neuron import h
from hayneuron import HayNeuron
import tools
import matplotlib.pyplot as plt
import time

start = time.time()

h.nrn_load_dll("mod/nrnmech.dll")
cvode = h.CVode()
cvode.active(1)

cells = []

for i in range(2):
    cell = HayNeuron()
    cells.append(cell)

currents = [
    0.4,
    0.5,
    0.6,
    0.7,
    0.8,
    0.9,
    1.0,
    1.2,
    1.5,
    2.0
]

syn = h.Exp2Syn(cells[1].cell.soma[0](0.5))

syn.tau1 = 0.5
syn.tau2 = 2.0
syn.e = 0

syn_reverse = h.Exp2Syn(cells[0].cell.soma[0](0.5))

syn_reverse.tau1 = 0.5
syn_reverse.tau2 = 2.0
syn_reverse.e = 0

connection = h.NetCon(
    cells[0].cell.soma[0](0.5)._ref_v,
    syn,
    sec=cells[0].cell.soma[0]
)

connection.threshold = 0
connection.weight[0] = 0.1
connection.delay = 1 

connection_reverse = h.NetCon(
    cells[1].cell.soma[0](0.5)._ref_v,
    syn_reverse,
    sec=cells[1].cell.soma[0]
)

connection_reverse.threshold = 0
connection_reverse.weight[0] = 0.1
connection_reverse.delay = 1

# Stimulate and record
stims = []
recordings = []

for cell, current in zip(cells, currents):
    stim = h.IClamp(cell.cell.soma[0](0.5))
    stim.delay = 5
    stim.dur = 100
    stim.amp = current
    stims.append(stim)

    t = h.Vector()
    v = h.Vector()

    t.record(h._ref_t)
    v.record(cell.cell.soma[0](0.5)._ref_v)

    recordings.append((t, v))

# Create spike detectors
spike_recordings = []
netcons = []

for cell in cells:

    spike_times = h.Vector()

    nc = h.NetCon(
        cell.cell.soma[0](0.5)._ref_v,
        None,
        sec=cell.cell.soma[0]
    )

    nc.threshold = 0
    nc.record(spike_times)

    spike_recordings.append(spike_times)
    netcons.append(nc)

print("Cell creation:", time.time() - start, "seconds")

h.tstop = 150
h.v_init = -80

h.finitialize(h.v_init)

run_start = time.time()
h.run()

print("Simulation:", time.time() - run_start, "seconds")
print("Total:", time.time() - start, "seconds")

plt.figure(figsize=(10, 6))

for i, (t, v) in enumerate(recordings):

    plt.plot(
        t,
        v,
        label=f"Neuron {i} ({currents[i]} nA)"
    )

plt.xlabel("Time (ms)")
plt.ylabel("Voltage (mV)")
plt.title("2 Hay Neurons")
plt.legend()
plt.show()

spike_data = []

for spikes in spike_recordings:
    spike_data.append(list(spikes))

tools.plot_raster(spike_data)