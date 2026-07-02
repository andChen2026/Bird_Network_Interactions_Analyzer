"""
Law of Large Numbers demo, extended to 10 individual birds:
each bird independently draws its own song times from the same underlying
process (constant rate or non-constant rate). Events are stacked in a
histogram, colored by bird ID, so you can see both:
  (1) the aggregate distribution converging to the theoretical density
      as N (per-bird sample size) grows, and
  (2) each bird's individual contribution to that total, by color.
"""

import os
import glob
import numpy as np
import matplotlib.pyplot as plt

rng = np.random.default_rng(seed=7)

# ---------------------------------------------------------------------------
# Time window: 6:30 AM - 8:00 AM
# ---------------------------------------------------------------------------
T_START, T_END = 6.5, 8.0
WINDOW = T_END - T_START

# ---------------------------------------------------------------------------
# Rate function (non-constant case): dawn chorus, highest at 6:30, tapering off
# ---------------------------------------------------------------------------
def lambda_noncost(t_abs):
    baseline = 1.5
    dawn_decay = 11.0 * np.exp(-2.2 * (t_abs - T_START))
    return baseline + dawn_decay

_grid = np.linspace(T_START, T_END, 5000)
_norm_const = np.trapezoid(lambda_noncost(_grid), _grid) if hasattr(np, "trapezoid") \
    else np.trapz(lambda_noncost(_grid), _grid) # pyright: ignore[reportAttributeAccessIssue]

def noncost_density(t_abs):
    return lambda_noncost(t_abs) / _norm_const

UNIFORM_DENSITY = 1.0 / WINDOW

# ---------------------------------------------------------------------------
# Samplers
# ---------------------------------------------------------------------------
def sample_uniform(n, rng):
    return T_START + rng.uniform(0, WINDOW, size=n)

def sample_from_rate(rate_fn, n, rng, n_grid=5000):
    grid = np.linspace(T_START, T_END, n_grid)
    rate_max = rate_fn(grid).max()
    accepted = np.empty(0)
    batch = max(2000, n * 4)
    while len(accepted) < n:
        candidates = T_START + rng.uniform(0, WINDOW, size=batch)
        u = rng.uniform(0, rate_max, size=batch)
        mask = u < rate_fn(candidates)
        accepted = np.concatenate([accepted, candidates[mask]])
    return accepted[:n]

# ---------------------------------------------------------------------------
# 10 birds, each with its own color
# ---------------------------------------------------------------------------
N_BIRDS = 10
BIRD_COLORS = plt.cm.tab10.colors  # pyright: ignore[reportAttributeAccessIssue] # 10 distinct colors
BIRD_LABELS = [f"Bird {i+1}" for i in range(N_BIRDS)]

N_VALUES = [10, 100, 1000, 10000]  # per-bird sample size
N_BINS = 20

fig, axes = plt.subplots(2, len(N_VALUES), figsize=(17, 7.5), sharey="row")

def clock_ticks(ax):
    tick_hours = np.linspace(T_START, T_END, 4)
    labels = []
    for h in tick_hours:
        hh, mm = int(h), int(round((h - int(h)) * 60))
        labels.append(f"{hh}:{mm:02d}")
    ax.set_xticks(tick_hours)
    ax.set_xticklabels(labels, fontsize=8)

t_line = np.linspace(T_START, T_END, 500)
legend_handles = None

for col, n in enumerate(N_VALUES):
    # --- Row 0: constant rate, 10 birds stacked ---
    ax = axes[0, col]
    events_by_bird = [sample_uniform(n, rng) for _ in range(N_BIRDS)]
    _, _, patches = ax.hist(events_by_bird, bins=N_BINS, range=(T_START, T_END),
                             density=True, stacked=True, color=BIRD_COLORS,
                             edgecolor="white", linewidth=0.3)
    if legend_handles is None:
        legend_handles = [p[0] for p in patches]
    ax.axhline(UNIFORM_DENSITY, color="black", lw=2, linestyle="--")
    ax.set_title(f"N = {n:,} per bird", fontsize=11, fontweight="bold")
    ax.set_xlim(T_START, T_END)
    clock_ticks(ax)
    if col == 0:
        ax.set_ylabel("Constant rate\n(stacked density)", fontsize=10)

    # --- Row 1: non-constant rate, 10 birds stacked ---
    ax = axes[1, col]
    events_by_bird_v = [sample_from_rate(lambda_noncost, n, rng) for _ in range(N_BIRDS)]
    ax.hist(events_by_bird_v, bins=N_BINS, range=(T_START, T_END),
             density=True, stacked=True, color=BIRD_COLORS,
             edgecolor="white", linewidth=0.3)
    ax.plot(t_line, noncost_density(t_line), color="black", lw=2, linestyle="--")
    ax.set_xlim(T_START, T_END)
    clock_ticks(ax)
    if col == 0:
        ax.set_ylabel("Non-constant rate\n(stacked density)", fontsize=10)

fig.legend(legend_handles, BIRD_LABELS, loc="upper center", ncol=10, # pyright: ignore[reportArgumentType]
           bbox_to_anchor=(0.5, 1.06), fontsize=9, frameon=False)

fig.suptitle(
    "Law of Large Numbers across 10 birds: stacked song-time distributions converge to theory\n"
    "dashed line = true density   |   color = bird ID   |   bars = 10 birds pooled together",
    fontsize=13, fontweight="bold", y=1.14
)
fig.tight_layout(rect=[0, 0, 1, 0.90]) # pyright: ignore[reportArgumentType]

output_dir = os.path.expanduser("~/Desktop/Mascaro Summer Training Program - Learning Bird Soundscapes/Computing/files")
os.makedirs(output_dir, exist_ok=True)

existing = glob.glob(os.path.join(output_dir, "poisson_rate_comparison_stacked*"))
count = len(existing)
filename = f"poisson_rate_comparison_stacked_{count}.png"

fig.savefig(os.path.join(output_dir, filename), dpi=200, bbox_inches="tight")
print(f"Saved figure as {filename}")
