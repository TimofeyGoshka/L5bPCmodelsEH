## 2026-10-10: No separate audit document
Only five small scripts; a full audit table was overkill. Warnings (synaptic
weight units, arbitrary synapse placement, no seeds, relative paths) are
recorded in the notes file in legacy/.

## 2026-10-10: Hay model stays unmodified in thirdparty/hay2011/
Keeps our changes separate from the original and lets us compare against it
if results look wrong.

## 2026-10-10: Pinned environment via requirements.txt
No conda installed; plain Python 3.12.7. NEURON 9.0.1 recorded because
mechanism behaviour can differ between versions.

## 2026-10-10: NEURON throughout
Simulator: NEURON for the whole project (previously undecided between NEURON
and Brian2). Reason: the Hay model is native NEURON; multicompartment L5 cell
is the core of the project.

## 2026-10-10: Literature review before scientific scoping
Scientific claims and acceptance criteria are defined only after Phase 1
(literature research).