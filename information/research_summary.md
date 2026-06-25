# Research Summary — Probabilistic Acoustic Interaction Networks for Ovenbirds

## Core Research Question

**"Does temporal co-occurrence mean counter-singing or coincidence?"**

This is the central question the entire framework is designed to answer. It extends Lapp et al. (2024) by adding a third stage — interaction validity — to the existing individual identification pipeline.

Implement a bird network analyzer that assigns confidence based on data availability using Gaussian Process Models and Hawkes Processes as the underlying foundation.

---

## The Three-Stage Pipeline

The contribution formalizes a three-stage false positive framework:

**Stage 1 — Species Classification (HawkEars)**
- Precision: 0.97 at threshold 1.0
- False positives here propagate through every downstream stage

**Stage 2 — Individual Identification (Lapp et al.)**
- Accuracy: 0.94 validation, 0.99 test set
- End-to-end recall: 0.16 — 84% of real songs filtered out by design
- Precision over recall is correct — false positive edges corrupt network metrics

**Stage 3 — Interaction Validity (my novel contribution)**
- Does temporal co-occurrence represent counter-singing or coincidence?
- Not addressed anywhere in Lapp et al.
- This is the gap the GP framework fills

**End-to-end precision:** 0.97 × 0.99 ≈ 0.96 baseline before observing S, T, H

---

## Key Mathematical Framework

**Tweak if needed for fixed constants and variables**

**Edge weight model:**

$$P_{ab}(\text{Interaction} \mid S=s_0, T=t_0, H=h_0)$$

Where:
- **S** — spatial proximity between birds
- **T** — temporal proximity of vocalizations
- **H** — historical interaction count between the pair
- **I** ∈ {0,1} — binary interaction outcome
- S, T, H ∈ ℝ — continuous valued features

**Network-level marginal:**

$$P(\text{Interaction}) = \iiint_{S\,T\,H} P(\text{Interaction} \mid S,T,H)\, ds\, dt\, dh$$

This is the average interaction rate across all edges or bird interactions — useful as a network summary statistic and null model validation.

**Critical independence violation:**

$$P(S,T,H) \neq P(S)P(T)P(H)$$

Therefore:

$$P(I \mid S,T,H) \neq P(I \mid S) + P(I \mid T) + P(I \mid H)$$

Features are not independent — spatial and temporal proximity interact synergistically. This is the mathematical justification for the GP over simpler additive models.

---

## Why Gaussian Process Models

The GP is mathematically necessary, not optional, because:

- P(S,T) ≠ P(S)P(T) — joint dependence cannot be modeled additively
- GP models a continuous function over the entire S,T,H space jointly
- Provides full posterior distribution over interaction intensity surface — not just a point estimate
- Naturally incorporates Bayesian priors from Lapp et al.
- Captures multimodal interaction landscape — different types of counter-singing regimes
- Uncertainty quantification varies by data density — honest about sparse data

**GP vs alternatives:**

| Model | Bias | Uncertainty | Prior | Interpretable |
|-------|------|-------------|-------|---------------|
| Uniform prior | Very high | None | No | Yes |
| Sigmoid | Medium | None | No | Yes |
| Neural network | Low | None | No | No |
| GP | Low | Full posterior | Yes | Yes |

**Computational cost:** O(N³) — requires HPC (Snowy/Screech). Sparse GP approximations available for large datasets.

**Bayesian consistency:** As N→∞, posterior concentrates around true value and point predictions become valid approximations. GP is essential in the current sparse data regime.

---

## Feature Justification

S, T, H are not arbitrary — they map directly onto the three established criteria for aggressive acoustic signaling (Searcy & Beecher 2009):

- **S → Context criterion** — signal increases in aggressive contexts (spatial proximity defines territorial context)
- **T → Response criterion** — receivers respond to the signal (temporal proximity as evidence of response)
- **H → Predictive criterion** — signal predicts aggressive escalation (interaction history indicates established rivalry)

**Combinatorial explosion constraint:** Adding more features expands the integral dimensionality and requires exponentially more data. Three ecologically justified features is the principled choice.

---

## Hawkes Process — Temporal Excitation Model

The Hawkes process formally distinguishes counter-singing from coincidence through a rate function λ(t):

$$\lambda(t) = \mu + \sum_{t_i < t} \alpha \cdot g(t - t_i)$$

Where:
- **μ** — background rate: baseline singing independent of other birds (coincidence)
- **α** — excitation: how much bird A's singing increases bird B's rate (counter-singing)
- **β** — decay: how quickly excitation fades after a song
- **g(t - tᵢ)** — decay kernel: response probability decreases as time since song increases

**Key distinction from GP:**
- Hawkes models **when** interactions happen temporally — the rate function
- GP models **how confident** we are given S, T, H jointly — the probability surface
- Hawkes does NOT give a point estimate — it gives a continuous rate function over time
- Together: temporal dynamics + spatiotemporal uncertainty quantification

**Directly estimable from loca26 day 1 data:**

| Hawkes Parameter | Data Column Required |
|-----------------|---------------------|
| Background rate μ | `start_timestamp` + total observation window |
| Excitation α | Pairwise `start_timestamp` comparisons between individuals |
| Decay β | Time differences between A's song and B's response |
| Spatial decay | `event_position_x/y` distances between pairs |

**No additional data collection needed** — all parameters estimable from `loca2024grid1_clips_day1_strict_reviewed.csv`

**Estimated background rate from day 1:**
~495 events / (240 minutes × 104 individuals) ≈ 0.02 songs per bird per minute baseline

**Why Hawkes works in sparse data regime:**
- Designed specifically for point process data — not large matrices
- Parameters estimable from relatively few events
- Significant advantage over GP in sparse observation setting

---

## Dataset — loca26 2024

| Metric | Lapp et al. | loca26 grid1 day1 | Notes |
|--------|-------------|-------------------|-------|
| Individuals | 45 (13 arrays) | 104 (1 grid) | 2.3x more from one grid |
| Events | 717 (all arrays) | 495 (day1 only) | Day 1 only reliable |
| Recorder spacing | ~34m | ~18-20m | 2x denser |
| Area | ~9 ha per array | ~3.4 ha | 8x individual density |
| Days recorded | 1-5 per array | 1 reliable day | Hardware failure after day 1 |
| Classifier | HawkEars | HawkEars | Same prior valid (0.97) |
| Verified | Yes | Machine-labeled only | Requires Bayesian framework |

**Spatial structure:**

| Level | Dimension | Notes |
|-------|-----------|-------|
| Recorder spacing | ~18-19m | Denser than Lapp et al. (~34m) |
| Full grid footprint | 226×152m (~3.4 ha) | Total array area |
| Ovenbird territory | ~0.5-1 ha typical | From literature |
| Individuals per grid | 104 | Extremely dense |
| Distance filter | 100m radius | Connects most individuals |

**Critical hardware failure finding:**
Sam Lapp's readme documents that rubber bands securing recorders to trees degraded from UV exposure after day 1:
- 60% of high recorders fell on the ground
- 10% of low recorders fell
- 5 recorders never recorded at all (MSD-2422, MSD-2019, MSD-1371, MSD-2050, MSD-0428)
- Sam's explicit recommendation: only analyze day 1 (May 16, 2024)
- Days 2-13 exist as raw audio (759 GB) but spatial positions are unreliable — localization would be invalid

**This was not discovered by running the pipeline — it was discovered by reading the readme before processing.** Reading documentation before executing prevented a week of wasted compute time on spatially corrupted data.

**Ground truth available:**
Field observers tracked actual bird singing positions on 5/16 and 5/28. Stored in `loca2024grid1_observed_bird_singing_events.csv`. Provides partial ecological validation for network edges — rare in PAM research.

**Lapp et al. as Bayesian prior:** Empirically measured precision values (0.97, 0.99) serve as informed priors for the unverified loca26 dataset.

---

## Network Analysis Approach

**Structure:**
- Nodes — machine-assigned individual Ovenbirds
- Edges — potential countersinging interactions
- Directed — A→B means A.start > B.end (A responded to B)
- Weighted — GP-derived P(Interaction | S,T,H) with confidence interval

**Scope:** Counter-singing interactions only — not general social behavior

**Dynamic systems modeling** — primary analytical approach:
- Network evolves across 13 recording days
- Edge weights update as new observations arrive
- Captures temporal arc of breeding season — territory establishment → stable phase → late breeding

**Community detection** — identifies interaction clusters within the grid

**Scale guidance from Louis:** Realistic network scale is ~10-20 individuals per local area with 500+ events — guides method selection

---

## Potential Issues

### Primary Limitation — Insufficient Data Points

**The number of data points is the fundamental constraint of this research.** With ~10-20 individuals per local area and only day 1 reliable due to hardware failures, the network is too small and sparse to confidently compute most standard network metrics. This limits:

- Which metrics can be reported with statistical confidence
- How strongly ecological conclusions can be stated
- The generalizability of any findings beyond this specific dataset

Unlike social networks (Facebook, Instagram — millions of nodes, thousands of events per second), biological interaction networks are inherently data-sparse due to ecological constraints on population density, territory size, and physical field equipment limitations. This is not a failure of the approach — it is the biological reality that Bayesian uncertainty quantification is specifically designed to address.

Every other limitation below is secondary to this one. The Bayesian GP + Hawkes framework is designed to be honest about this — reporting wide confidence intervals where data is sparse rather than false precision. Processing days 2-13 is not viable due to recorder failures — day 1 is the reliable dataset.

**1. Small network size**
~10-20 individuals per local area limits meaningful network metric computation. Centrality and clustering require sufficient nodes. Method selection must account for small network scale — confirmed question for Monday meeting.

**2. Sparse data — hardware failure compounding pipeline filtering**
Low recall arises from two compounding sources:
- **By design:** Pipeline filtering (precision 1.00, recall 0.17) — deliberate precision-over-recall tradeoff
- **By necessity:** Recorder failures after day 1 — 60% high moths, 10% low moths fell; localization invalid for days 2-13
- Combined effect: true end-to-end recall lower than 0.16
- Bayesian framework explicitly models this sparsity.

**3. Machine-labeled data — no human verification**
104 individuals are machine-assigned clusters, not human-verified. Bayesian framework handles this via informed priors but introduces uncertainty at Stage 2. Precision may be lower than 0.99 in practice for unverified data.

**4. P(S,T) not separable — identifiability problem**
Joint effect of S and T can be measured but individual contributions cannot be cleanly untangled. Must claim joint effects, not independent contributions. Cov(S,T) ≠ 0 — the synergistic joint condition is the countersinging signal.

**5. Unobserved confounders**
S, T, H don't capture everything. Dominance hierarchies, weather, habitat features may drive interaction probability but aren't in the data — omitted variable bias. Residual GP uncertainty partially captures this but doesn't resolve it.

**6. TN unobservable**
True negatives — confirmed non-interactions — don't exist in PAM data. Precision is the only valid metric. This constrains what claims can be made.

**7. Low end-to-end recall (0.16)**
84% of real interactions filtered out by pipeline design plus hardware failures. Network is necessarily sparse. Must acknowledge as limitation — precision-over-recall tradeoff by design and by necessity.

**8. DTW not directly useful**
Dynamic Time Warping measures acoustic content similarity. Ovenbirds don't need acoustically similar songs to countersing — DTW is a potential future feature extension, not a core component.

**9. Computational complexity**
GP inference is O(N³). Sparse GP approximations needed. Strategy to be determined with Rahimian Monday.

**10. Days 2-13 not processable**
Hardware failures render spatial positions unreliable after day 1. Sam Lapp's explicit recommendation: day 1 only. Confirmed before running pipeline — saved a week of wasted compute time.

---

## Questions 

- Hawkes process vs GP vs hybrid — which approach given 495 events and ~10-20 individuals per local area?
- Which network metrics are meaningful for small sparse networks at this scale?
- How to formally specify GP prior distributions from Lapp et al. precision values (0.97, 0.99)?
- What is the computational budget and GP approximation strategy?
- Can observed singing events (5/16, 5/28) be used to validate edge weights?
- Can any days 2-13 be salvaged using only the recorders confirmed not to have fallen?
- Is community detection meaningful at this network scale?
- Does the newer HawkEars v1.0.8 (used in loca26) change the 0.97 precision prior from Lapp et al. (v0.1.0)?

---

## Key Literature

| Paper | Relevance |
|-------|-----------|
| Lapp et al. (2024) | Individual identification pipeline, source of Bayesian priors (0.97, 0.99) |
| Grames et al. (2022) | Hawkes process for acoustic event modeling — excitation vs background rate |
| Searcy & Beecher (2009) | Three criteria for aggressive acoustic signaling — justifies S, T, H features |
| Weeden & Falls (1959) | Ovenbird neighbor recognition — ecological context |
| Bishop PRML Chapter 6 | GP framework — kernel methods, posterior inference |
| Oxford Network Science | Community detection, dynamic systems modeling |
| Song as Aggressive Signal | Context, predictive, response criteria — validates edge definition |

---

## Contribution

*"We extend Lapp et al.'s individual identification pipeline by proposing a Gaussian Process and Hawkes Process framework that jointly models the spatiotemporal excitation structure of acoustic co-occurrence events to assign probabilistic edge weights to a counter-singing interaction network, explicitly quantifying uncertainty from three compounding sources of false positives and the inherent data sparsity of field PAM deployments."*

---

## Research Statement

*"Build a bird network analyzer that assigns confidence based on data availability using Gaussian Process Models and Hawkes Processes as the underlying foundation."*

---

*Last updated: June 18, 2026 | MCSI Summer Research Program | University of Pittsburgh*
