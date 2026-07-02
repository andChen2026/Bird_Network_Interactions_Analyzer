# Project Context Summary — Probabilistic Acoustic Interaction Networks for Ovenbirds
*For continuation in a new chat session — Updated end of Week 6*

---

## Who I Am
Andrew Chen (acy23), recent CS graduate from University of Pittsburgh, completing a 10-week MCSI Summer Sustainability Research Training Program (May 18 – July 26, 2026). In the Responsible Data Science (HAIL) Cohort.

**Advisors:**
- Dr. Justin Kitzes (Kitzes Lab, computational ecology, co-creator of OpenSoundscape)
- Dr. Amin Rahimian (Industrial Engineering, network science and Bayesian inference)

**Collaborators:**
- Sam Lapp — postdoc/PhD, author of foundational Ovenbird individual identification pipeline
- Louis Freeland — lab member, dataset access and technical guidance
- Tessa Rhinehart — co-author on Lapp et al., recommended as contact for alternative datasets

**Deliverables due ~July 26:**
- 5-page written report
- 8-minute PowerPoint presentation
- 2-minute advisor-approved video

**Long-term goal:** MS in Biomedical Informatics at Stony Brook University (SBU-BNL partnership), with PhD ambitions in computational biology/ML applied to genomics.

---

## Core Research Question
**"Does temporal co-occurrence mean countersinging or coincidence?"**

This extends Lapp et al. (2025) by adding a third stage — interaction validity — to their existing individual identification pipeline.

**Null hypothesis:** Acoustic events between two individuals occur completely at random in time with no interaction effects. Real data is tested against this null via P(observed events | completely random events).

---

## Scope Decisions Made This Week — CRITICAL

### Countersinging Definition (Fixed)
Countersinging is defined deterministically: **if S (spatial) AND T (temporal) criteria are both met → countersinging event.** H (historical) criterion dropped for now to keep the scope attainable in 4 remaining weeks.

### GP/Hawkes Architecture — Deferred to Future Work
GP and Hawkes process implementation is explicitly scoped as **future work**. They will be discussed in the paper as a natural extension but not implemented this summer. The GP framing (probabilistic edge weights, uncertainty quantification) remains the long-term vision and is worth mentioning in the discussion/conclusion.

### Temporal Focus (Kitzes Input)
Kitzes confirmed that **temporal analysis is more meaningful than spatial** because Ovenbirds sing from consistent fixed posts. The null model is purely temporal — completely random event timing with no interaction effects. The spatial simulation (territory circles, radial sampling) is deprioritized; territory placement remains in the design but the primary signal is temporal.

### Simulator Reframing
The Simulator class was reframed from a spatial distribution generator to a **temporal null simulator**:
- Generates random acoustic events with start times drawn from a specified sampling distribution
- Each event has fixed duration of 3 seconds (start, end = start + 3)
- Null: events are completely random in time with no interaction effects
- Tests P(observed events | completely random events)
- Distribution can be specified; no commitment to Poisson yet pending data inspection

---

## Software Architecture

Class definitions moved out of Jupyter notebooks into `.py` modules. Notebooks serve only as the analysis/visualization layer.

**Filter ABC pattern:**
```python
from abc import ABC, abstractmethod

class Filter(ABC):
    def __init__(self, threshold: float):
        self.threshold = threshold

    @abstractmethod
    def apply(self, events: list) -> list:
        pass

class ProximityFilter(Filter):
    def apply(self, events: list) -> list:
        pass  # stubbed

class TemporalFilter(Filter):
    def apply(self, events: list) -> list:
        pass  # stubbed
```

`Filter` is an abstract base class (Python equivalent of a Java interface). Concrete subclasses must implement `apply`. Instantiate as `ProximityFilter(threshold=2.0)`, never `Filter(threshold=2.0)` directly.

**Simulator stub:**
```python
def generateRandomAcousticEvents(self, SamplingDistribution, n: int) -> list:
    # Stubbed — generates random AcousticEvents with temporal coordinates (start, end)
    # Each event duration fixed at 3 seconds
    # Distribution can be specified; implement after pipeline produces real data
    pass
```

---

## Pipeline Status — End of Week 6

### Completed Steps
1. **HawkEars species detection** — all 14 arrays complete
   - Outputs: `/media/auk/projects/acy23/outputs/1_species_detection/1_detect_hawkears/`
   - ~71K Ovenbird detections across all arrays
   - Top species: Red-eyed Vireo (493K), White-throated Sparrow (91K), Ovenbird (71K)

2. **Detection selection** (`2_select_detections_to_localize.ipynb`) — complete
   - Threshold: `-1` (intentionally permissive, Sam's original setting)
   - Sparse binary detection pickles saved at `/media/auk/projects/acy23/outputs/1_species_detection/2_select_detections/`
   - ~4.75 days of effective recording per array (~65-70 array-days total)

3. **Acoustic localization** (`1_localize_ovenbird.py`) — complete
   - Ovenbird frequency range hardcoded to 2000–7000 Hz
   - Outputs: `/media/auk/projects/acy23/outputs/2_acoustic_localization/1_localize_ovenbird/`
   - JSON format: bird position, contributing recorders, TDOA values
   - Species counts per array: `/media/auk/projects/acy23/outputs/2_acoustic_localization/det_cnts/`
   - Runs with non-fatal TDOA warnings (discriminant clamped to zero for geometrically inconsistent delays)

### Next Step
4. **Individual classifier** — identify individual Ovenbirds from localized events
   - Notebook TBD (likely in Sam's pipeline)
   - This is the next pipeline stage to get running

### Path Reference
```
/media/auk/projects/acy23/
  SBT/2016/V1/                          # raw audio (14 arrays)
  outputs/
    1_species_detection/
      1_detect_hawkears/                 # HawkEars CSVs
      2_select_detections/               # sparse binary pickles (thresh=-1)
    2_acoustic_localization/
      1_localize_ovenbird/               # JSON localization outputs
      det_cnts/                          # species counts per array
```

### Common Fixes Applied to Sam's Pipeline
- Kernel mismatch: VS Code was using Python 3.8 system kernel instead of `ovenbird_classification` (Python 3.10) — fix by selecting correct kernel in VS Code top-right
- `~/.local` package leakage: use `PYTHONNOUSERSITE=1` if needed
- Hardcoded paths pointing to `/home/sml161/` need to be updated to `/media/auk/projects/acy23/`
- Missing directories: always `mkdir -p` before running scripts that write output
- `species_freq_ranges.csv` not accessible — hardcoded Ovenbird range 2000–7000 Hz instead

---

## Null Simulation Design

### Handwritten Notes (Page 1)
- p(x) is a probability distribution over a territory
- Null: p(x) is uniform (cylinder for circular territory)
- As r → 0: clumping (polar coordinate bias)
- As r → R: empty space near edge
- Need radial transformation to correct for polar sampling bias: sample r with p(r) ∝ r

### Handwritten Notes (Page 2)
Algorithm for territory event simulation:
1. Pick territory center (x₀, y₀)
2. Sample radius r from a distribution
3. Sample θ from 0 to 2π uniformly
4. Convert: x = r·cosθ + x₀, y = r·sinθ + y₀
5. Run convex hull over generated points to approximate territory boundary

**Note:** Spatial simulation deprioritized per Kitzes — temporal analysis is primary. Radial correction math still needed if spatial simulation is revisited.

**Parameters needed from literature:**
- Ovenbird territory sizes (distribution, not just mean)
- Breeding density (territories per hectare)
- Singing rate per individual (feeds into μ)

---

## Literature

| Paper | Relevance | Priority |
|-------|-----------|----------|
| Lapp et al. (2025) | Individual ID pipeline, Bayesian priors (0.97, 0.99) | Essential |
| Grames et al. 2022 | Hawkes process for acoustic event modeling | Essential |
| Searcy & Beecher 2009 | S, T, H aggressive signal criteria | Essential |
| Weeden & Falls 1959 | Ovenbird neighbor recognition | Essential |
| Wiegand & Moloney — Ch. 4.2 | Spatial point pattern analysis, CSR null | Read tomorrow |
| Bishop PRML Ch. 6 | GP framework | Future work reference |
| Rahimian et al. "Seeding with Costly Network Information" | Active learning / uncertainty sampling | Background |
| Social learning and culture in birds (Royal Society B) | Bird social behavior context | Skim |
| Cognitive adaptations of social bonding in birds (PMC) | Bird social intelligence | Low priority |
| Costs and benefits in bird flocks (Nature Eco & Evo) | Collective behavior | Low priority |
| Effect of sociality on competitive interactions (Proc B) | Competitive interactions | Skim |
| Song as aggressive signal in songbirds | S, T, H justification | Essential |
| Countersinging chapter (Advances in Study of Behavior) | Direct countersinging framing | High priority |

**Reading plan:** 6 behavior articles (~20 min skim each) → Wiegand & Moloney introduction today → Chapter 4.2 rigorously tomorrow

---

## Key Principles Learned This Summer

- **Statistics before implementation** — understand the problem before reaching for tools
- **Temporal null is the right null** — Ovenbirds sing from fixed posts; spatial randomness is not the meaningful baseline
- **Read documentation before running pipelines** — caught Day 1 dataset flaw before wasting compute
- **Precision over recall** — FP edges corrupt network metrics, FN just makes network sparser
- **P(S,T,H) ≠ P(S)P(T)P(H)** — joint dependence requires joint model (GP) — future work
- **Bayesian uncertainty quantification not optional** — sparse data regime requires it — future work
- **Research ≠ classes** — question must be found; failure signals are noisy
- **Premature implementation hurts research** — tool-first thinking is a CS habit to break
- **Unused directions aren't wasted** — they narrow the space and document the process
- **Attainable scope > perfect scope** — 4 weeks remaining; deterministic pipeline first, GP later
- **More was found than could be implemented** — normal in research; future work section handles the rest

---

## One-Sentence Contribution

*"We extend Lapp et al.'s individual identification pipeline by building a countersinging interaction network using deterministic spatial and temporal criteria, validated against a temporal null model of completely random acoustic events, laying the empirical foundation for a future probabilistic GP/Hawkes framework."*

---

*Last updated: June 25, 2026 | End of Week 6 | MCSI Summer Research Program | University of Pittsburgh*
