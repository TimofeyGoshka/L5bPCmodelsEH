# PROJECT.md

> Entry point for humans and AI assistants. Paste or upload this file at the start of every AI session. At the end of a session, update the **Status** and **Decision log** sections.

## 1. Goal

Model a cortical column in **NEURON**, centred on the layer 5 (LP5/ET) pyramidal neuron, plus a thalamic component, in order to test the hypothesis described in `docs/literature/Hypercontextualisation_NBR_submit.docx` (apical hypercontextualisation under 5-HT2A agonism).

**End product:** _TBD (paper / thesis chapter / learning project / other)_
**Time available per week:** _TBD_

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
- [ ] Create repo structure, pinned environment (`environment.yml`), `.gitignore`
- [ ] Compile NEURON mechanisms (`nrnivmodl`) from a clean checkout
- [ ] Audit existing code: what exists, what runs, what has been validated against a published result
- [ ] Freeze feature additions; move ideas to `docs/backlog.md`
- [ ] Write `docs/DECISIONS.md` (first entry: NEURON throughout)

**Exit when:** a clean checkout runs the baseline L5 cell and reproduces a known behaviour, and this file is up to date.

### Phase 1: Literature research _(timebox: ~3-4 weeks, adjust)_
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
cortical-column-5ht2a/
├── README.md
├── docs/
│   ├── PROJECT.md        # this file
│   ├── DECISIONS.md      # dated log of choices and reasons
│   ├── EXPERIMENTS.md    # question, prediction, result per experiment
│   ├── REVIEW.md         # AI cross-review notes
│   ├── backlog.md        # parked realism ideas
│   └── literature/       # notes per paper, bibliography
├── src/                  # cells, thalamus, network, stimuli
├── mechanisms/           # NEURON .mod files
├── params/               # parameters with source + status
├── configs/              # one file per experiment (seed, params, duration)
├── experiments/          # scripts that run a config and save results
├── analysis/             # metrics and figures
├── tests/                # sanity tests (baseline behaviour)
├── results/              # outputs, mostly git-ignored
├── environment.yml
└── .gitignore
```

Every run saves its config, random seed and git commit hash with its results.

## 8. Status _(update at the end of each session)_

- **Current phase:** 0 (Reset and framework)
- **Last updated:** _YYYY-MM-DD_
- **Done so far:** _..._
- **Blocked / open questions:** _..._
- **Next concrete task:** _..._

## 9. Decision log _(newest first; full detail in `docs/DECISIONS.md`)_

- _YYYY-MM-DD_: Simulator: NEURON throughout (previously undecided between NEURON and Brian2).
- _YYYY-MM-DD_: Literature review precedes scientific scoping and acceptance criteria.

---

## Appendix: Task card template

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
