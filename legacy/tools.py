import matplotlib.pyplot as plt
from neuron import h


# =========================
# Recording tools
# =========================

def record_voltage(section):
    """
    Record membrane voltage from a NEURON section.
    Returns time and voltage vectors.
    """

    t = h.Vector()
    v = h.Vector()

    t.record(h._ref_t)
    v.record(section._ref_v)

    return t, v


def record_spikes(section, threshold=0):
    """
    Detect spikes using NEURON NetCon.
    Returns spike times and the NetCon object.
    """

    spike_times = h.Vector()

    nc = h.NetCon(
        section._ref_v,
        None,
        sec=section.sec
    )

    nc.threshold = threshold
    nc.record(spike_times)

    return spike_times, nc


# =========================
# Analysis tools
# =========================

def firing_rate(spike_times, duration_ms):
    """
    Calculate firing rate in Hz.
    """

    return len(spike_times) / (duration_ms / 1000)


# =========================
# Plotting tools
# =========================

def plot_voltage(time, voltage, title="Voltage trace"):
    """
    Plot one voltage trace.
    """

    plt.figure(figsize=(8, 4))

    plt.plot(time, voltage)

    plt.xlabel("Time (ms)")
    plt.ylabel("Voltage (mV)")
    plt.title(title)

    plt.show()


def plot_traces(results):
    """
    Plot multiple voltage traces.

    Format:
    [
        ("Neuron 1", time, voltage),
        ("Neuron 2", time, voltage)
    ]
    """

    plt.figure(figsize=(8, 4))

    for name, time, voltage in results:
        plt.plot(
            time,
            voltage,
            label=name
        )

    plt.xlabel("Time (ms)")
    plt.ylabel("Voltage (mV)")
    plt.legend()

    plt.show()


def plot_raster(spike_data):
    """
    Plot spike raster.

    Format:
    [
        [spike times neuron 1],
        [spike times neuron 2],
        ...
    ]
    """

    plt.figure(figsize=(8, 4))

    for neuron_id, spikes in enumerate(spike_data):
        plt.scatter(
            spikes,
            [neuron_id] * len(spikes),
            s=5
        )

    plt.xlabel("Time (ms)")
    plt.ylabel("Neuron")

    plt.show()


class SimulationResult:

    def __init__(self, time, voltage, spikes=None, label=None):
        self.time = time
        self.voltage = voltage
        self.spikes = spikes
        self.label = label

    def firing_rate(self, duration_ms):
        if self.spikes is None:
            return 0

        return len(self.spikes) / ((self.time[-1] - self.time[0]) / 1000)


    def summary(self):
        print(f"Simulation: {self.label}")

        if self.spikes is not None:
            print(f"Spikes: {len(self.spikes)}")
            print(f"Firing rate: {self.firing_rate(self.time[-1]):.2f} Hz")