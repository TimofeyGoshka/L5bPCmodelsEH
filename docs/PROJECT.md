# PROJECT.md

> Entry point for humans and AI assistants. Paste or upload this file at the start of every AI session. At the end of a session, update the **Status** and **Decision log** sections.

## 1. Goal

Model a cortical column in **NEURON**, centred on the layer 5 (LP5/ET) pyramidal neuron, plus a thalamic component, in order to test the hypothesis described in `docs/literature/Hypercontextualisation_NBR_submit.docx.txt` (apical hypercontextualisation under 5-HT2A agonism).

**End product:** Paper
**Time available per week:** 3 hours

## 2. Hypothesis (as stated in the source paper, not yet scoped)

The paper proposes that 5-HT2A agonism:

1. amplifies apical-dendrite responses in a subset of extratelencephalic (ET) layer 5 cells, and
2. boosts presynaptic glutamate release from thalamocortical afferents onto those apical dendrites,

together sustaining a cortex → thalamus → apical-tuft loop with more bursting and broader broadcast of cortical information.

Open points the paper itself leaves unresolved: the location of the postsynaptic effect (tuft, integration zone, oblique dendrites, intracellular receptors), the role of interneurons, and layers 2/3 and 6.

**Scientific claims, model variants and acceptance criteria are deliberately NOT defined yet.** They are fixed in Phase 2, after the literature review.

## 3. Principles

- **The repo is the memory.** AI chats are disposable; decisions and plans live in files.
- **Spec before code.** Every coding task has a task card (appendix) with an acceptance test.
- **Realism budget.** A new biological detail is added only if a specific experiment needs it. Everything else goes to `docs/backlog.md`.
- **Every claim and parameter traces to a source.** Params carry a status: `from paper`, `estimated`, or `guess`. AI summaries are never a source on their own.
- **Truth comes from tests and sources, not model agreement.** Two AIs agreeing is not evidence.
- **Small steps, committed often.** One task per branch/chat; run sanity tests after every change.
- **Simulator:** NEURON throughout (decision logged below).

## 4. Phases

### Phase 0: Reset and framework _(timebox: ~1 week, adjust)_
-- [x] Create repo structure, requirements.txt, .gitignore
- [x] Compile NEURON mechanisms (nrnivmodl in thirdparty/hay2011/mod)
- [x] Review existing code (notes in legacy/README.md)
- [x] Freeze feature additions; ideas go to docs/backlog.md
- [x] Write docs/DECISIONS.md
- [x] Hay wrapper (src/cells/hay_wrapper.py) and sanity test
- [x] Reproduce original demos in Python (src/protocols/hay_protocols.py);
      step count at 0.793 nA matches the original GUI demo exactly (27)
- [x] Fresh-clone test: clone the repo into a new folder, compile the
      mechanisms, run both tests

**Exit when:** a clean checkout runs the baseline L5 cell and reproduces a known behaviour, and this file is up to date.

### Phase 1: Literature research _(timebox: 10.16.26 to 08.11.26)_
Organized by questions. No conclusions drawn yet.

1. **L5 cell models:** What does the Hay et al. model reproduce about apical-basal coupling and burst firing, and where does it fall short? How do ET cells differ from other L5 types? Are there better-suited models?
2. **5-HT2A effects on L5 cells:** Which cell types, compartments, magnitudes, currents/receptors? Extract numbers into the params table with source and confidence.
3. **Thalamic side:** Which populations are relevant (higher-order, intralaminar)? What models exist for thalamic relay cells? What is known about their synapses onto layer 1 and about presynaptic 5-HT2A effects?
4. **Existing computational work:** What has already been modelled on apical drive and thalamocortical loops? What can be reused rather than built?
5. **Scale needed:** How many cells and synapses does a meaningful column or loop require?

**Outputs:** a note per paper in `docs/literature/`, a params table with sources and confidence, a gap list, and a one-page answer to *"what can this model test that isn't already known?"*

**Exit when:** that one-page answer can be stated in your own words.

### Phase 2: Scientific scoping _(timebox: ~1 week, adjust)_
- [ ] Define the exact question and predictions
- [ ] Define model variants (e.g. candidate sites of the postsynaptic effect)
- [ ] Define observables and acceptance criteria
- [ ] Define the staged ladder of levels (single cell → cell + thalamic loop → column) and the test for each
- [ ] Set the realism budget
- [ ] Cross-critique by two AIs; review with a domain expert if possible

**Exit when:** the scope document is written and reviewed.

### Phase 3: Staged implementation in NEURON
Levels and tests are defined in Phase 2. Do not move up a level until the current one meets its criteria.

### Phase 4: Experiments and analysis
Run configured experiments, record in `docs/EXPERIMENTS.md`, compare against predictions, including failed predictions.

### Phase 5: Review and write-up
Decide whether to iterate, extend, or write up.

## 5. Working with AI

| Use | Suggested tool (swap if it works poorly) |
|---|---|
| Planning, architecture, code, code review | Claude |
| Digesting long papers / many files at once | Gemini |
| Cross-review | Each critiques the other's plan or diff; write results to `docs/REVIEW.md` |

**Session start prompt (template):**
> Context: `PROJECT.md` (attached). Today's task: _[task card]_. Constraints: follow the Principles section. Ask me if anything is ambiguous before writing code.

**Session end prompt (template):**
> Draft updates to the Status and Decision log sections of PROJECT.md based on this session. List open questions and the next concrete task.

**Free-tier habits:** short chats, one task each; upload files rather than long pastes; never rely on chat history.

## 6. Weekly review (15 min)
- What moved? What is blocked?
- Was anything added without an experiment that needs it? (move it to the backlog)
- Is the current phase's exit criterion closer?
- Have both AIs critique this file's Status section.

## 7. Repo structure

```
L5bPCmodelsEH/
├── README.md
├── requirements.txt
├── docs/                  # PROJECT.md, DECISIONS.md, backlog.md, literature/
├── thirdparty/hay2011/    # original Hay model, unmodified
├── legacy/                # old scripts, reference only
├── src/
│   ├── cells/hay_wrapper.py
│   └── protocols/hay_protocols.py
└── tests/                 # test_baseline.py, test_hay_protocols.py

```

Every run saves its config, random seed and git commit hash with its results.

## 8. Status _(update at the end of each session)_

- Current phase: 0 (Reset and framework), finishing
- Last updated: 2026-10-14
- Done so far: repo, environment, Hay wrapper, step and BAC protocols
  reproduced in Python; step count matches the original demo exactly
- Blocked / open questions: end product and time per week still TBD (section 1)
- Next concrete task: compare with paper Fig 4, fresh-clone test, then Phase 1

## 9. Decision log _(newest first; full detail in `docs/DECISIONS.md`)_

- **Current phase:** 1 (Literature research), just started
- **Last updated:** 16.10.2026
- **Phase 0:** complete. Wrapper and protocols reproduce the original Hay
  demos (step at 0.793 nA = 27 spikes, exact match; BAC plots look like
  paper Fig 4A); a fresh clone builds and passes both tests.
- **Phase 1 progress** (details in docs/literature/):
  1. L5 cell models (Hay et al. 2011 and alternatives): not started
  2. 5-HT2A effects on L5 cells (numbers for params table): not started
  3. Thalamic side (relay cell models, layer 1 synapses): not started
  4. Existing computational work on apical drive / thalamocortical loops: not started
  5. Scale needed (cells, synapses): not started
- **Timebox for Phase 1:** until <date you choose>
- **Blocked / open questions:** -
- **Next concrete task:** read Hay et al. 2011 and write
  docs/literature/hay2011.md using the paper template (group 1)

## Appendix: Task card template and Glossary

```
# Task: <short name>
Phase / level: 
Goal (one sentence): 
Inputs (files, params, papers): 
Out of scope (what NOT to add): 
Acceptance test (how we know it's done): 
Params touched and their source/status: 
Branch: 
Notes / result: 
```

```
Glossary and key context (read this first, AI assistants, ask for any context or files if needed)

- Hay et al. 2011: published model of a layer 5b pyramidal cell (ModelDB
  3343), used unmodified in thirdparty/hay2011/. Our code loads it through
  src/cells/hay_wrapper.py.
- BAC firing (Hay Fig 4A): a 5 ms somatic pulse (1.9 nA) paired 5 ms later
  with an EPSP-like current (0.5 nA) at a distal apical site (620 um from
  the soma) produces a burst with a dendritic calcium spike. In Python:
  run_bac_protocol (src/protocols/hay_protocols.py). Our result: pulse
  alone 1 spike, current alone 0, both 3.
- Step-current firing (Hay Fig 4B): a 2000 ms somatic step. Amplitudes
  0.619 / 0.793 / 1.507 nA gave 22 / 27 / 39 spikes in our reproduction;
  the 0.793 nA count (27) matches the original GUI demo exactly.
- ET cells: extratelencephalic layer 5 pyramidal cells, the cell type
  the hypothesis is about.
- The hypothesis paper is docs/literature/Hypercontextualisation_NBR_submit.docx.
- Tests: tests/test_baseline.py and tests/test_hay_protocols.py.

```