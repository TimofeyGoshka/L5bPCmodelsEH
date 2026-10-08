from neuron import h
import tools
from hayneuron import HayNeuron
import matplotlib.pyplot as plt


# =========================
# Initialize model
# =========================

cell = HayNeuron()

cvode = h.CVode()
cvode.active(1)

soma = cell.cell.soma[0](0.5)
apical = cell.cell.apic[50](0.5)
axon = cell.cell.axon[0](0.5)


# =========================
# Stimulus
# =========================

stim = h.IClamp(cell.cell.apic[50](0.5))

stim.delay = 100
stim.dur = 500
stim.amp = 1.0


# =========================
# Recording
# =========================

t_soma, v_soma = tools.record_voltage(soma)
t_apic, v_apic = tools.record_voltage(apical)
t_axon, v_axon = tools.record_voltage(axon)



# =========================
# Run simulation
# =========================

h.tstop = 700
h.v_init = -80

h.finitialize(h.v_init)
h.run()


# =========================
# Store result
# =========================

result_soma = tools.SimulationResult(
    time=list(t_soma),
    voltage=list(v_soma),
    spikes=None,
    label="1.0 nA"
)

result_apic = tools.SimulationResult(
    time=list(t_apic),
    voltage=list(v_apic),
    spikes=None,
    label="1.0 nA"
)

result_axon = tools.SimulationResult(
    time=list(t_axon),
    voltage=list(v_axon),
    spikes=None,
    label="1.0 nA"
)


# =========================
# Analysis
# =========================

result_soma.summary()
result_apic.summary()
result_axon.summary()


# =========================
# Plot
# =========================

plt.figure(figsize=(10, 6))

plt.plot(
    result_soma.time,
    result_soma.voltage,
    label="Soma"
)

plt.plot(
    result_apic.time,
    result_apic.voltage,
    label="Apical"
)

plt.plot(
    result_axon.time,
    result_axon.voltage,
    label="Axon"
)


plt.xlabel("Time (ms)") 
plt.ylabel("Voltage (mV)") 
plt.legend()

plt.show()