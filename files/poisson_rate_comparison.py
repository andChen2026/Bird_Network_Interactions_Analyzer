"""
Law of Large Numbers demo: as sample size N grows, the empirical distribution
of a focal bird's song times converges to the underlying theoretical
distribution -- uniform for a constant-rate (homogeneous Poisson) process,
and rate-shaped for a non-constant-rate (inhomogeneous Poisson) process.

Row 1: constant rate      -> empirical histogram should flatten toward uniform
Row 2: non-constant rate  -> empirical histogram should sharpen toward the
                              normalized rate curve (dawn chorus taper)
"""

import os
import glob
import numpy as np
import matplotlib.pyplot as plt

rng = np.random.default_rng()

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

# Normalize into a proper probability density over the window (integrates to 1)
_grid = np.linspace(T_START, T_END, 5000)
_norm_const = np.trapezoid(lambda_noncost(_grid), _grid) if hasattr(np, "trapezoid") \
    else np.trapz(lambda_noncost(_grid), _grid) # pyright: ignore[reportAttributeAccessIssue]

def noncost_density(t_abs):
    return lambda_noncost(t_abs) / _norm_const

UNIFORM_DENSITY = 1.0 / WINDOW  # theoretical density for the constant-rate case

# ---------------------------------------------------------------------------
# Samplers -- both conditioned on drawing exactly N event times
# ---------------------------------------------------------------------------
def sample_uniform(n, rng):
    """Constant-rate case: N events land uniformly at random in the window."""
    return T_START + rng.uniform(0, WINDOW, size=n)

def sample_from_rate(rate_fn, n, rng, n_grid=5000):
    """Non-constant-rate case: N events land according to the rate function's
    shape, via vectorized rejection sampling."""
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
# Sample sizes to show convergence across
# ---------------------------------------------------------------------------
N_VALUES = [10, 100, 1000, 10000]
N_BINS = 20

COLOR_CONST = "#3b6fa0"
COLOR_VAR = "#c9622f"

fig, axes = plt.subplots(2, len(N_VALUES), figsize=(16, 7), sharey="row")

def clock_ticks(ax):
    tick_hours = np.linspace(T_START, T_END, 4)
    labels = []
    for h in tick_hours:
        hh, mm = int(h), int(round((h - int(h)) * 60))
        labels.append(f"{hh}:{mm:02d}")
    ax.set_xticks(tick_hours)
    ax.set_xticklabels(labels, fontsize=8)

t_line = np.linspace(T_START, T_END, 500)

for col, n in enumerate(N_VALUES):
    # --- Row 0: constant rate ---
    ax = axes[0, col]
    events = sample_uniform(n, rng)
    ax.hist(events, bins=N_BINS, range=(T_START, T_END), density=True,
            color=COLOR_CONST, alpha=0.6, edgecolor="white", linewidth=0.4)
    ax.axhline(UNIFORM_DENSITY, color=COLOR_CONST, lw=2, linestyle="--")
    ax.set_title(f"N = {n:,}", fontsize=11, fontweight="bold")
    ax.set_xlim(T_START, T_END)
    clock_ticks(ax)
    if col == 0:
        ax.set_ylabel("Constant rate\n(density)", fontsize=10)

    # --- Row 1: non-constant rate ---
    ax = axes[1, col]
    events_v = sample_from_rate(lambda_noncost, n, rng)
    ax.hist(events_v, bins=N_BINS, range=(T_START, T_END), density=True,
            color=COLOR_VAR, alpha=0.6, edgecolor="white", linewidth=0.4)
    ax.plot(t_line, noncost_density(t_line), color=COLOR_VAR, lw=2, linestyle="--")
    ax.set_xlim(T_START, T_END)
    clock_ticks(ax)
    if col == 0:
        ax.set_ylabel("Non-constant rate\n(density)", fontsize=10)

fig.suptitle(
    "Law of Large Numbers: empirical song-time distribution converges to theory\n"
    "dashed line = true density   |   bars = empirical histogram from N samples",
    fontsize=13, fontweight="bold", y=1.04
)
fig.tight_layout(rect=[0, 0, 1, 0.94]) # pyright: ignore[reportArgumentType]

output_dir = os.path.expanduser("~/Desktop/Mascaro Summer Training Program - Learning Bird Soundscapes/Computing/files")
os.makedirs(output_dir, exist_ok=True)

existing = glob.glob(os.path.join(output_dir, "poisson_rate_comparison*"))
count = len(existing)
filename = f"poisson_rate_comparison_{count}.png"

fig.savefig(os.path.join(output_dir, filename), dpi=200, bbox_inches="tight")
print(f"Saved figure as {filename}")
