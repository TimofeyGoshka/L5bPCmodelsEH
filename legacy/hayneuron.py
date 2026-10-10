from neuron import h

class HayNeuron:
    def __init__(self):

       
        h.load_file("import3d.hoc")
        h.load_file("models/L5PCbiophys3.hoc")
        h.load_file("models/L5PCtemplate.hoc")
        h.load_file("stdrun.hoc")

        self.cell = h.L5PCtemplate(
            "morphologies/cell1.asc"
        )