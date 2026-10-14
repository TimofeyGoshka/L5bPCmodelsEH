   # legacy/

   Early exploratory scripts. Reference only; not validated.

   - hay.py: demo of apical current injection with soma/apical/axon recording.
     Seed for the baseline test.
   - Synapse_test.py: Poisson synaptic input test. Do NOT reuse results:
     Exp2Syn weight is set to 1 (µS), likely far too large; synapses placed by
     list order, not by compartment or distance; no random seeds.
   - network.py: two-cell NetCon plumbing test. Low value.

   Reused elsewhere: hayneuron.py -> src/cells/hay_wrapper.py, tools.py -> src/tools.py.
   Paths in these scripts are relative to the Hay model folder.