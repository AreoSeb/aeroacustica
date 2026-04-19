"""
Figure didattiche per paper sui criteri di convergenza
Stile coerente con make_figures.py / make_figures_v2.py del progetto Huawei
Palette: huaweiblue #1A365D, midblue #2C5282, lightblue #EBF4FF
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Rectangle
from matplotlib.lines import Line2D
import os

OUTDIR = os.path.join(os.path.dirname(__file__), "figs_conv")
os.makedirs(OUTDIR, exist_ok=True)

HUAWEIBLUE = "#1A365D"
MIDBLUE = "#2C5282"
LIGHTBLUE = "#EBF4FF"
TABLEHEAD = "#D6E4F7"
ACCENT_GREEN = "#2F855A"
ACCENT_ORANGE = "#C05621"
ACCENT_RED = "#9B2C2C"
ACCENT_GREY = "#4A5568"

plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "font.size": 10,
    "axes.titlesize": 11,
    "axes.labelsize": 10,
    "axes.titleweight": "bold",
    "axes.edgecolor": ACCENT_GREY,
    "axes.linewidth": 0.8,
    "axes.grid": True,
    "grid.color": "#CBD5E0",
    "grid.linewidth": 0.5,
    "grid.alpha": 0.6,
    "legend.fontsize": 9,
    "legend.framealpha": 0.95,
    "legend.edgecolor": ACCENT_GREY,
    "savefig.bbox": "tight",
    "savefig.dpi": 180,
})


# ==========================================================
# FIG 1 — Storia residui RMS: 4 casi tipici (good/plateau/oscillating/divergent)
# ==========================================================
def fig_residual_history():
    fig, axes = plt.subplots(2, 2, figsize=(11, 7.5))
    iters = np.arange(1, 1001)

    # (a) Buona convergenza
    ax = axes[0, 0]
    rms_p = 10 ** (-0.5 * np.log10(iters) - 0.5 + 0.05 * np.sin(iters / 30))
    rms_u = 10 ** (-0.55 * np.log10(iters) - 0.4 + 0.04 * np.sin(iters / 25))
    rms_t = 10 ** (-0.6 * np.log10(iters) - 0.3 + 0.03 * np.sin(iters / 20))
    ax.semilogy(iters, rms_p, color=HUAWEIBLUE, label="RMS pressione")
    ax.semilogy(iters, rms_u, color=MIDBLUE, label="RMS velocità-x")
    ax.semilogy(iters, rms_t, color=ACCENT_GREEN, label="RMS turbolenza")
    ax.axhline(1e-6, color=ACCENT_RED, linestyle="--", linewidth=1.0,
               label="Target $10^{-6}$")
    ax.set_title("(a) Convergenza monotona — buona")
    ax.set_xlabel("Iterazione")
    ax.set_ylabel("Residuo RMS")
    ax.set_ylim(1e-7, 1e0)
    ax.legend(loc="upper right")

    # (b) Plateau (mesh poor o CFL alto)
    ax = axes[0, 1]
    rms_p2 = 10 ** np.where(iters < 200,
                            -0.5 * np.log10(iters) - 0.3,
                            -1.5 + 0.05 * np.sin(iters / 40))
    rms_u2 = 10 ** np.where(iters < 250,
                            -0.5 * np.log10(iters) - 0.3,
                            -1.7 + 0.04 * np.sin(iters / 35))
    ax.semilogy(iters, rms_p2, color=HUAWEIBLUE, label="RMS pressione")
    ax.semilogy(iters, rms_u2, color=MIDBLUE, label="RMS velocità-x")
    ax.axhline(1e-6, color=ACCENT_RED, linestyle="--", linewidth=1.0,
               label="Target $10^{-6}$")
    ax.axhspan(1e-2, 1e-1, color=ACCENT_ORANGE, alpha=0.15)
    ax.text(500, 5e-2, "PLATEAU\nresidui bloccati",
            ha="center", color=ACCENT_ORANGE, fontweight="bold", fontsize=9)
    ax.set_title("(b) Plateau — mesh skewness o BC sbagliata")
    ax.set_xlabel("Iterazione")
    ax.set_ylabel("Residuo RMS")
    ax.set_ylim(1e-7, 1e0)
    ax.legend(loc="lower left")

    # (c) Oscillazioni LCO (Limit Cycle Oscillation, naturale instationary)
    ax = axes[1, 0]
    decay = np.exp(-iters / 200)
    base = 1e-3 + 1e-4 * decay
    osc = 5e-4 * np.sin(iters / 8) * (1 - 0.7 * np.exp(-iters / 100))
    rms_p3 = base + osc
    rms_u3 = (1e-3 + 8e-5 * decay) + 4e-4 * np.sin(iters / 9 + 0.5)
    ax.semilogy(iters, np.abs(rms_p3), color=HUAWEIBLUE, label="RMS pressione")
    ax.semilogy(iters, np.abs(rms_u3), color=MIDBLUE, label="RMS velocità-x")
    ax.axhline(1e-6, color=ACCENT_RED, linestyle="--", linewidth=1.0,
               label="Target $10^{-6}$")
    ax.text(500, 5e-3, "Oscillazioni — flusso\nintrinsecamente non stazionario\n(passare a URANS)",
            ha="center", color=ACCENT_ORANGE, fontweight="bold", fontsize=9,
            bbox=dict(boxstyle="round,pad=0.3", facecolor="white",
                      edgecolor=ACCENT_ORANGE))
    ax.set_title("(c) Oscillazioni LCO — fisica instazionaria")
    ax.set_xlabel("Iterazione")
    ax.set_ylabel("Residuo RMS")
    ax.set_ylim(1e-7, 1e0)
    ax.legend(loc="upper right")

    # (d) Divergente
    ax = axes[1, 1]
    rms_p4 = np.zeros_like(iters, dtype=float)
    rms_p4[:300] = 10 ** (-0.3 * np.log10(iters[:300]) - 0.5)
    rms_p4[300:] = 10 ** (0.005 * (iters[300:] - 300) - 1.0)
    rms_u4 = np.zeros_like(iters, dtype=float)
    rms_u4[:280] = 10 ** (-0.3 * np.log10(iters[:280]) - 0.4)
    rms_u4[280:] = 10 ** (0.006 * (iters[280:] - 280) - 0.9)
    ax.semilogy(iters, rms_p4, color=HUAWEIBLUE, label="RMS pressione")
    ax.semilogy(iters, rms_u4, color=MIDBLUE, label="RMS velocità-x")
    ax.axhline(1e-6, color=ACCENT_RED, linestyle="--", linewidth=1.0,
               label="Target $10^{-6}$")
    ax.axvspan(280, 1000, color=ACCENT_RED, alpha=0.10)
    ax.annotate("Divergenza:\nridurre CFL\no migliorare mesh",
                xy=(500, 1e2), xytext=(700, 5e-3),
                ha="center", color=ACCENT_RED, fontweight="bold", fontsize=9,
                arrowprops=dict(arrowstyle="->", color=ACCENT_RED, lw=1.2))
    ax.set_title("(d) Divergenza — CFL troppo alto")
    ax.set_xlabel("Iterazione")
    ax.set_ylabel("Residuo RMS")
    ax.set_ylim(1e-7, 1e4)
    ax.legend(loc="upper left")

    fig.suptitle("Storia dei residui RMS: quattro scenari tipici nella RANS stazionaria",
                 fontsize=12, fontweight="bold", color=HUAWEIBLUE, y=1.00)
    plt.tight_layout()
    out = os.path.join(OUTDIR, "fig_residual_history.png")
    plt.savefig(out)
    plt.close()
    print(f"✓ {out}")


# ==========================================================
# FIG 2 — Effetto del numero di CFL
# ==========================================================
def fig_cfl_effect():
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.6))

    # Sx: storia residui per 4 CFL
    iters = np.arange(1, 2001)
    cfl_curves = {
        0.5: (HUAWEIBLUE, 0.18, "CFL = 0.5 — robusto, lento"),
        5: (MIDBLUE, 0.42, "CFL = 5 — bilanciato"),
        50: (ACCENT_GREEN, 0.82, "CFL = 50 — adattivo, veloce"),
        500: (ACCENT_RED, -0.005, "CFL = 500 — divergente"),
    }
    ax = axes[0]
    for cfl, (color, slope, label) in cfl_curves.items():
        if slope > 0:
            rms = 10 ** (-slope * np.log10(iters) - 0.4)
            rms = np.clip(rms, 1e-9, None)
        else:
            base = 10 ** (-0.4 * np.log10(iters[:400]) - 0.4)
            div = 10 ** (slope * (iters[400:] - 400) ** 1.3 - 0.4 + 0.001 * (iters[400:] - 400))
            div = 10 ** (0.004 * (iters[400:] - 400) - 0.4)
            rms = np.concatenate([base, div])
        ax.semilogy(iters, rms, color=color, label=label, linewidth=1.4)
    ax.axhline(1e-6, color="black", linestyle=":", linewidth=0.8)
    ax.text(1900, 1.5e-6, "target $10^{-6}$", ha="right",
            fontsize=8, color="black")
    ax.set_xlabel("Iterazione")
    ax.set_ylabel("Residuo RMS pressione")
    ax.set_title("(a) Effetto del CFL sulla velocità di convergenza")
    ax.set_ylim(1e-9, 1e2)
    ax.legend(loc="upper right", fontsize=8)

    # Dx: trade-off chart (CPU time vs robustezza)
    ax = axes[1]
    cfl_vals = np.array([0.5, 1, 2, 5, 10, 20, 50, 100, 200, 500])
    iters_to_conv = np.array([3500, 1900, 1100, 480, 250, 145, 95, 110, np.nan, np.nan])
    risk = np.array([1, 1, 1, 1, 1.5, 2, 2.5, 4, 7, 10])

    ax.set_xscale("log")
    ax.set_yscale("log")
    valid = ~np.isnan(iters_to_conv)
    ax.plot(cfl_vals[valid], iters_to_conv[valid],
            "o-", color=HUAWEIBLUE, linewidth=1.6,
            label="Iterazioni a $\\mathrm{RMS}=10^{-6}$")
    ax.axvspan(0.5, 5, color=ACCENT_GREEN, alpha=0.10, label="zona robusta")
    ax.axvspan(5, 100, color=ACCENT_ORANGE, alpha=0.10, label="zona ottimale (CFL adapt)")
    ax.axvspan(100, 1000, color=ACCENT_RED, alpha=0.10, label="zona pericolosa")
    ax.set_xlabel("Numero di CFL")
    ax.set_ylabel("Iterazioni necessarie")
    ax.set_title("(b) Trade-off CFL: velocità vs robustezza")
    ax.legend(loc="upper right", fontsize=8)
    ax.set_xlim(0.4, 600)

    fig.suptitle("Numero di CFL nella RANS stazionaria: scelta del valore",
                 fontsize=12, fontweight="bold", color=HUAWEIBLUE, y=1.02)
    plt.tight_layout()
    out = os.path.join(OUTDIR, "fig_cfl_effect.png")
    plt.savefig(out)
    plt.close()
    print(f"✓ {out}")


# ==========================================================
# FIG 3 — GCI Richardson extrapolation
# ==========================================================
def fig_gci_richardson():
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.8))

    # Dati esempio: tre mesh L1=coarse, L2=medium, L3=fine; QoI = u_z al centro
    # h è la dimensione caratteristica della cella (mm)
    h_vals = np.array([0.300, 0.150, 0.075])  # coarse → fine
    phi_vals = np.array([8.42, 9.18, 9.41])   # m/s
    r = h_vals[0] / h_vals[1]  # = 2

    # Ordine di convergenza apparente (Celik 2008)
    eps32 = phi_vals[1] - phi_vals[0]
    eps21 = phi_vals[2] - phi_vals[1]
    p = np.log(np.abs(eps32 / eps21)) / np.log(r)
    phi_ext = phi_vals[2] + (phi_vals[2] - phi_vals[1]) / (r ** p - 1)
    GCI_fine = 1.25 * np.abs((phi_vals[2] - phi_vals[1]) / phi_vals[2]) / (r ** p - 1) * 100

    # Sx: extrapolation curve
    ax = axes[0]
    h_dense = np.linspace(0, 0.35, 400)
    # phi(h) ≈ phi_ext - C h^p
    C_fit = (phi_ext - phi_vals[2]) / h_vals[2] ** p
    phi_curve = phi_ext - C_fit * h_dense ** p

    ax.plot(h_dense, phi_curve, "-", color=MIDBLUE, linewidth=1.6,
            label=f"Richardson, $p={p:.2f}$")
    ax.scatter(h_vals, phi_vals, s=80, color=HUAWEIBLUE, zorder=5,
               label="Soluzioni CFD (L1, L2, L3)")
    ax.scatter([0], [phi_ext], s=140, marker="*", color=ACCENT_RED, zorder=6,
               label=f"$\\phi_{{ext}} = {phi_ext:.3f}$ m/s")
    for hv, pv, lab in zip(h_vals, phi_vals, ["L1", "L2", "L3"]):
        ax.annotate(lab, xy=(hv, pv), xytext=(8, -12),
                    textcoords="offset points", fontsize=9,
                    fontweight="bold", color=HUAWEIBLUE)
    # Banda incertezza GCI sulla mesh fine
    band = phi_vals[2] * GCI_fine / 100
    ax.axhspan(phi_vals[2] - band, phi_vals[2] + band,
               color=ACCENT_GREEN, alpha=0.15,
               label=f"banda GCI = ±{GCI_fine:.2f}%")
    ax.set_xlabel("Dimensione cella $h$ (mm)")
    ax.set_ylabel("$\\bar u_z$ al centro del jet (m/s)")
    ax.set_title("(a) Estrapolazione di Richardson")
    ax.legend(loc="lower right", fontsize=8)
    ax.set_xlim(-0.02, 0.35)

    # Dx: convergenza percentuale
    ax = axes[1]
    err_obs = np.abs(phi_vals - phi_ext) / phi_ext * 100
    bars = ax.bar(["L1\n(coarse)", "L2\n(medium)", "L3\n(fine)"], err_obs,
                  color=[ACCENT_RED, ACCENT_ORANGE, ACCENT_GREEN],
                  edgecolor=HUAWEIBLUE, linewidth=1.0)
    for bar, val in zip(bars, err_obs):
        ax.text(bar.get_x() + bar.get_width() / 2, val + 0.15,
                f"{val:.2f}%", ha="center", fontsize=9, fontweight="bold")
    ax.axhline(3, color=ACCENT_RED, linestyle="--", linewidth=1.0,
               label="soglia GCI accettabile (3%)")
    ax.set_ylabel("Errore relativo a $\\phi_{ext}$ (%)")
    ax.set_title("(b) Errore residuo per livello di mesh")
    ax.legend(loc="upper right", fontsize=8)

    fig.suptitle("Grid Convergence Index — esempio numerico (Celik et al. 2008)",
                 fontsize=12, fontweight="bold", color=HUAWEIBLUE, y=1.02)
    plt.tight_layout()
    out = os.path.join(OUTDIR, "fig_gci_richardson.png")
    plt.savefig(out)
    plt.close()
    print(f"✓ {out}")


# ==========================================================
# FIG 4 — Inner residuals nel dual time-stepping (URANS/DDES/LES)
# ==========================================================
def fig_dual_time_inner():
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.8))

    # Sx: residui inner per 5 outer step consecutivi (zoom)
    ax = axes[0]
    n_inner = 30
    iters = np.arange(1, n_inner + 1)
    colors = plt.cm.viridis(np.linspace(0.1, 0.85, 5))
    for k, col in enumerate(colors):
        # Ogni outer step: residuo iniziale ~1e-2, decade ~3 ordini
        start = 10 ** (-2.0 - 0.05 * k)
        rms = start * 10 ** (-0.13 * iters + 0.02 * np.sin(iters))
        ax.semilogy(iters, rms, "o-", color=col, markersize=3,
                    label=f"Outer step n+{k}", linewidth=1.0)
    ax.axhline(1e-5, color=ACCENT_RED, linestyle="--", linewidth=1.0,
               label="Target inner $10^{-5}$")
    ax.axvline(20, color=ACCENT_ORANGE, linestyle=":", linewidth=1.0,
               label="N$_{inner}$ massimo = 20")
    ax.set_xlabel("Iterazione interna (entro un outer step)")
    ax.set_ylabel("Residuo RMS pressione (interno)")
    ax.set_title("(a) Convergenza interna per outer step")
    ax.legend(loc="upper right", fontsize=8)
    ax.set_xlim(1, n_inner)

    # Dx: inviluppo finale per ogni outer step (long-term stability)
    ax = axes[1]
    n_outer = 200
    outer = np.arange(1, n_outer + 1)
    # Residuo finale all'ultima inner iter di ogni outer step
    final_in = 10 ** (-5.0 + 0.3 * np.sin(outer / 8) - 0.0005 * outer)
    # Residuo iniziale di ogni outer step (≈ unsteady)
    init_in = 10 ** (-2.0 + 0.15 * np.sin(outer / 10))
    ax.semilogy(outer, init_in, color=MIDBLUE, label="Residuo iniziale",
                linewidth=1.2)
    ax.semilogy(outer, final_in, color=HUAWEIBLUE, label="Residuo finale",
                linewidth=1.2)
    ax.fill_between(outer, init_in, final_in, color=LIGHTBLUE, alpha=0.5)
    ax.axhline(1e-5, color=ACCENT_RED, linestyle="--", linewidth=1.0,
               label="target inner $10^{-5}$")
    ax.set_xlabel("Outer step (avanzamento temporale)")
    ax.set_ylabel("Residuo RMS pressione")
    ax.set_title("(b) Inviluppo iniziale–finale lungo il tempo fisico")
    ax.legend(loc="upper right", fontsize=8)

    fig.suptitle("Dual time-stepping: convergenza delle iterazioni interne",
                 fontsize=12, fontweight="bold", color=HUAWEIBLUE, y=1.02)
    plt.tight_layout()
    out = os.path.join(OUTDIR, "fig_dual_time_inner.png")
    plt.savefig(out)
    plt.close()
    print(f"✓ {out}")


# ==========================================================
# FIG 5 — Vincoli sul time step (versione didattica con annotazioni)
# ==========================================================
def fig_timestep_constraints():
    fig, ax = plt.subplots(figsize=(11, 5.5))

    constraints = [
        ("CFL conv. ($\\Delta x=30\\,\\mu$m, CFL=0.5)", 1.5, MIDBLUE,
         "stabilità schema esplicito"),
        ("Nyquist a 20 kHz",                              25.0, ACCENT_GREEN,
         "evita aliasing"),
        ("20 punti / periodo a 20 kHz",                   2.5, ACCENT_ORANGE,
         "rappresenta spettro acustico"),
        ("Kolmogorov $\\tau_\\eta/10$",                   0.34, ACCENT_RED,
         "risolve scale dissipative LES"),
    ]
    labels = [c[0] for c in constraints]
    vals = [c[1] for c in constraints]
    colors = [c[2] for c in constraints]
    motivs = [c[3] for c in constraints]

    y_pos = np.arange(len(labels))
    bars = ax.barh(y_pos, vals, color=colors, edgecolor=HUAWEIBLUE,
                   alpha=0.85, height=0.55)
    ax.set_xscale("log")
    ax.set_yticks(y_pos)
    ax.set_yticklabels(labels)
    ax.invert_yaxis()
    for bar, v, m in zip(bars, vals, motivs):
        ax.text(v * 1.15, bar.get_y() + bar.get_height() / 2,
                f"$\\Delta t \\leq {v}\\,\\mu$s   — {m}",
                va="center", fontsize=9)

    chosen = 0.5
    ax.axvline(chosen, color="black", linestyle="--", linewidth=1.5)
    ax.text(chosen, -0.7, f"$\\Delta t$ scelto WRLES = {chosen}$\\,\\mu$s",
            ha="center", fontsize=10, fontweight="bold", color="black")

    ax.set_xlabel("Limite superiore su $\\Delta t$ ($\\mu$s) — scala log")
    ax.set_title("Vincoli fisici e numerici sul passo temporale (mesh L5)",
                 color=HUAWEIBLUE, pad=12)
    ax.set_xlim(0.1, 80)
    ax.grid(axis="y", alpha=0.0)
    plt.tight_layout()
    out = os.path.join(OUTDIR, "fig_timestep_constraints.png")
    plt.savefig(out)
    plt.close()
    print(f"✓ {out}")


# ==========================================================
# FIG 6 — Convergenza statistica LES: running mean & first/second half
# ==========================================================
def fig_running_mean():
    np.random.seed(42)
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.8))

    # Genera segnale velocità con turbolenza + mean ~3 m/s
    dt = 0.5e-6  # 0.5 us
    n = 100000
    t = np.arange(n) * dt * 1e3  # ms
    u_mean_true = 3.0
    u_rms_true = 0.85
    # autocorrelato (Ornstein-Uhlenbeck like)
    tau_int = 5e-5  # 50 us
    alpha = np.exp(-dt / tau_int)
    sigma = u_rms_true * np.sqrt(1 - alpha ** 2)
    u = np.zeros(n)
    u[0] = u_mean_true
    noise = np.random.normal(0, sigma, n)
    for i in range(1, n):
        u[i] = u_mean_true + alpha * (u[i - 1] - u_mean_true) + noise[i]

    # Aggiungi transitorio iniziale (preflush 10 ms)
    transient = (u_mean_true - 1.5) * np.exp(-t / 3.0)
    u_obs = u - transient

    # running mean
    cumsum = np.cumsum(u_obs)
    run_mean = cumsum / np.arange(1, n + 1)

    ax = axes[0]
    # Sample-down per chiarezza grafica
    step = 200
    ax.plot(t[::step], u_obs[::step], color=LIGHTBLUE, linewidth=0.5,
            label="$u_z(t)$ raw")
    ax.plot(t, run_mean, color=HUAWEIBLUE, linewidth=1.6,
            label="$\\bar u_z(t)$ running mean")
    ax.axhline(u_mean_true, color=ACCENT_RED, linestyle="--", linewidth=1.0,
               label=f"valore vero = {u_mean_true} m/s")
    ax.axvspan(0, 10, color=ACCENT_ORANGE, alpha=0.15)
    ax.text(5, 4.2, "PREFLUSH\n(scarta)",
            ha="center", fontsize=9, color=ACCENT_ORANGE, fontweight="bold")
    ax.set_xlabel("Tempo (ms)")
    ax.set_ylabel("$u_z$ al sensore (m/s)")
    ax.set_title("(a) Running mean: convergenza al valore stazionario")
    ax.legend(loc="upper right", fontsize=8)
    ax.set_ylim(0.5, 5.0)

    # Test stationarity: confronto media 1° e 2° semi-intervallo
    ax = axes[1]
    # Skip preflush
    skip_idx = int(10e-3 / (dt * 1e3) * 1e3)  # 10 ms in idx
    skip_idx = int(10 / (dt * 1e3))
    u_after = u_obs[skip_idx:]
    t_after = t[skip_idx:] - t[skip_idx]
    half = len(u_after) // 2

    half_lengths = np.array([2, 4, 8, 16, 24, 32, 40])  # ms
    means_1st = []
    means_2nd = []
    for L in half_lengths:
        n_L = int(L / (dt * 1e3))
        n_L = min(n_L, half)
        m1 = u_after[:n_L].mean()
        m2 = u_after[n_L:2 * n_L].mean() if 2 * n_L < len(u_after) else np.nan
        means_1st.append(m1)
        means_2nd.append(m2)
    means_1st = np.array(means_1st)
    means_2nd = np.array(means_2nd)
    diff = np.abs(means_1st - means_2nd) / u_mean_true * 100

    ax.plot(half_lengths * 2, diff, "o-", color=HUAWEIBLUE, linewidth=1.5,
            markersize=8, label="$|\\bar u_{1^{st}} - \\bar u_{2^{nd}}| / \\bar u$ (%)")
    ax.axhline(2.0, color=ACCENT_RED, linestyle="--", linewidth=1.0,
               label="soglia 2%")
    ax.fill_betweenx([0, 25], 0, 16, color=ACCENT_ORANGE, alpha=0.10)
    ax.fill_betweenx([0, 25], 16, 80, color=ACCENT_GREEN, alpha=0.10)
    ax.text(8, 10, "non\nconvergente", ha="center",
            color=ACCENT_ORANGE, fontweight="bold", fontsize=9)
    ax.text(48, 10, "convergente\n(≥ 8 $t_{FT}$)", ha="center",
            color=ACCENT_GREEN, fontweight="bold", fontsize=9)
    ax.set_xlabel("Durata totale dell'intervallo statistico (ms)")
    ax.set_ylabel("Discrepanza tra semi-intervalli (%)")
    ax.set_title("(b) Test di stazionarietà — first vs second half")
    ax.legend(loc="upper right", fontsize=8)
    ax.set_ylim(0, 22)

    fig.suptitle("Convergenza statistica nelle simulazioni LES",
                 fontsize=12, fontweight="bold", color=HUAWEIBLUE, y=1.02)
    plt.tight_layout()
    out = os.path.join(OUTDIR, "fig_running_mean.png")
    plt.savefig(out)
    plt.close()
    print(f"✓ {out}")


# ==========================================================
# FIG 7 — Convergenza spettrale (Welch): effetto del numero di finestre
# ==========================================================
def fig_welch_convergence():
    np.random.seed(7)
    from scipy.signal import welch

    fs = 1 / 0.5e-6  # 2 MHz sampling
    n = 200000
    t = np.arange(n) / fs
    # Segnale sintetico: tono a 670 Hz (Strouhal) + tono a 4 kHz + rumore -5/3
    sig = (0.4 * np.sin(2 * np.pi * 670 * t)
           + 0.15 * np.sin(2 * np.pi * 4000 * t + 0.7))
    # Aggiungi rumore -5/3 (filtro semplice 1/f^(5/6) in ampiezza)
    white = np.random.normal(0, 1.0, n)
    F = np.fft.rfft(white)
    f_axis = np.fft.rfftfreq(n, 1 / fs)
    f_axis_safe = np.where(f_axis < 1, 1, f_axis)
    F_filt = F / (f_axis_safe ** (5 / 6))
    noise = np.fft.irfft(F_filt, n)
    noise *= 0.35 / noise.std()
    sig = sig + noise

    fig, axes = plt.subplots(1, 2, figsize=(11, 4.8))

    # Sx: PSD per diversi numeri di finestre
    ax = axes[0]
    nperseg_list = [2048, 8192, 32768]
    labels = ["1 finestra (n=2048)", "8 finestre (n=8192)", "32 finestre"]
    cmap = [ACCENT_RED, ACCENT_ORANGE, HUAWEIBLUE]
    for nperseg, lab, c in zip(nperseg_list, labels, cmap):
        f, P = welch(sig, fs=fs, nperseg=nperseg, noverlap=nperseg // 2,
                     window="hann")
        ax.loglog(f, P, color=c, linewidth=1.0, label=lab, alpha=0.9)
    # Slope -5/3 reference
    f_ref = np.array([100, 50000])
    P_ref = 1e-2 * (f_ref / 100) ** (-5 / 3)
    ax.loglog(f_ref, P_ref, "--", color="black", linewidth=1.0,
              label="slope $-5/3$")
    ax.set_xlim(100, 1e5)
    ax.set_ylim(1e-9, 1e-2)
    ax.set_xlabel("Frequenza (Hz)")
    ax.set_ylabel("PSD pressione")
    ax.set_title("(a) Welch: trade-off risoluzione vs varianza")
    ax.legend(loc="lower left", fontsize=8)

    # Dx: bias / varianza schematic
    ax = axes[1]
    nperseg_grid = np.array([1024, 2048, 4096, 8192, 16384, 32768, 65536])
    n_seg = (n // nperseg_grid * 2 - 1).clip(min=1)
    # var ~ 1/nseg, df ~ fs/nperseg
    df = fs / nperseg_grid
    var_norm = 1 / np.sqrt(n_seg)
    ax2 = ax.twinx()
    l1 = ax.semilogx(nperseg_grid, df, "o-", color=HUAWEIBLUE,
                     linewidth=1.5, label="risoluzione $\\Delta f$")
    l2 = ax2.semilogx(nperseg_grid, var_norm, "s-", color=ACCENT_RED,
                      linewidth=1.5, label="incertezza statistica $\\propto 1/\\sqrt{N_{seg}}$")
    ax.set_xlabel("Lunghezza segmento $n_{perseg}$ (campioni)")
    ax.set_ylabel("Risoluzione $\\Delta f$ (Hz)", color=HUAWEIBLUE)
    ax2.set_ylabel("Errore standard relativo", color=ACCENT_RED)
    ax.set_title("(b) Bias-variance trade-off")
    lines = l1 + l2
    ax.legend(lines, [l.get_label() for l in lines], loc="upper center",
              fontsize=8)
    ax.tick_params(axis="y", labelcolor=HUAWEIBLUE)
    ax2.tick_params(axis="y", labelcolor=ACCENT_RED)
    ax.grid(True, alpha=0.6)
    ax2.grid(False)

    fig.suptitle("Convergenza dello spettro Welch nel post-processing FW-H",
                 fontsize=12, fontweight="bold", color=HUAWEIBLUE, y=1.02)
    plt.tight_layout()
    out = os.path.join(OUTDIR, "fig_welch_convergence.png")
    plt.savefig(out)
    plt.close()
    print(f"✓ {out}")


# ==========================================================
# FIG 8 — Istogramma y+ sul chip: criterio di qualità mesh
# ==========================================================
def fig_yplus_histogram():
    np.random.seed(11)
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.6))

    # Sx: istogramma WMLES (target y+ ~30) e WRLES (target y+ < 0.5)
    ax = axes[0]
    yp_wmles = np.random.lognormal(mean=np.log(28), sigma=0.25, size=8000)
    yp_wrles = np.random.lognormal(mean=np.log(0.35), sigma=0.30, size=8000)
    bins = np.logspace(-2, 2.5, 60)
    ax.hist(yp_wrles, bins=bins, color=HUAWEIBLUE, alpha=0.8,
            edgecolor="white", label="WRLES L5 — target $y^+<0.5$")
    ax.hist(yp_wmles, bins=bins, color=ACCENT_ORANGE, alpha=0.7,
            edgecolor="white", label="WMLES L4 — target $y^+\\sim 30$")
    ax.axvline(0.5, color=HUAWEIBLUE, linestyle="--", linewidth=1.2)
    ax.axvline(30, color=ACCENT_ORANGE, linestyle="--", linewidth=1.2)
    ax.axvline(5, color=ACCENT_RED, linestyle=":", linewidth=1.0)
    ax.text(0.5 * 1.1, 600, "$y^+=0.5$", color=HUAWEIBLUE, fontsize=8,
            rotation=90, va="bottom")
    ax.text(30 * 1.1, 600, "$y^+=30$", color=ACCENT_ORANGE, fontsize=8,
            rotation=90, va="bottom")
    ax.text(5 * 1.05, 1100, "limite buffer", color=ACCENT_RED, fontsize=8,
            rotation=90, va="bottom")
    ax.set_xscale("log")
    ax.set_xlabel("$y^+$ sul chip")
    ax.set_ylabel("Numero di celle")
    ax.set_title("(a) Distribuzione $y^+$: WMLES vs WRLES")
    ax.legend(loc="upper right", fontsize=8)
    ax.set_xlim(1e-2, 3e2)

    # Dx: cumulativo, frazione celle within target
    ax = axes[1]
    sorted_wm = np.sort(yp_wmles)
    sorted_wr = np.sort(yp_wrles)
    cdf_wm = np.arange(len(sorted_wm)) / len(sorted_wm) * 100
    cdf_wr = np.arange(len(sorted_wr)) / len(sorted_wr) * 100
    ax.semilogx(sorted_wr, cdf_wr, color=HUAWEIBLUE, linewidth=1.6,
                label="WRLES L5")
    ax.semilogx(sorted_wm, cdf_wm, color=ACCENT_ORANGE, linewidth=1.6,
                label="WMLES L4")
    # Frazione celle WRLES con y+ < 1
    frac_wr1 = (sorted_wr < 1).sum() / len(sorted_wr) * 100
    frac_wm_target = ((sorted_wm > 20) & (sorted_wm < 50)).sum() / len(sorted_wm) * 100
    ax.axhline(95, color=ACCENT_RED, linestyle="--", linewidth=1.0,
               label="target ≥ 95%")
    ax.set_xlabel("$y^+$")
    ax.set_ylabel("Percentuale celle (%)")
    ax.set_title("(b) CDF — frazione celle entro target")
    ax.legend(loc="lower right", fontsize=8)
    ax.set_xlim(1e-2, 3e2)
    ax.set_ylim(0, 105)

    fig.suptitle("Convergenza della qualità mesh a parete: $y^+$ sul chip",
                 fontsize=12, fontweight="bold", color=HUAWEIBLUE, y=1.02)
    plt.tight_layout()
    out = os.path.join(OUTDIR, "fig_yplus_histogram.png")
    plt.savefig(out)
    plt.close()
    print(f"✓ {out}")


# ==========================================================
# FIG 9 — Flowchart decisionale per la convergenza
# ==========================================================
def fig_flowchart():
    fig, ax = plt.subplots(figsize=(11.5, 8.5))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 11)
    ax.axis("off")

    def box(x, y, w, h, text, color=LIGHTBLUE, edge=HUAWEIBLUE, fs=9, weight="normal"):
        b = FancyBboxPatch((x - w / 2, y - h / 2), w, h,
                           boxstyle="round,pad=0.08,rounding_size=0.18",
                           facecolor=color, edgecolor=edge, linewidth=1.3)
        ax.add_patch(b)
        ax.text(x, y, text, ha="center", va="center",
                fontsize=fs, fontweight=weight, color=HUAWEIBLUE)

    def diamond(x, y, w, h, text, color="#FFF7E6", edge=ACCENT_ORANGE, fs=9):
        d = mpatches.Polygon([[x, y + h / 2], [x + w / 2, y],
                              [x, y - h / 2], [x - w / 2, y]],
                             closed=True, facecolor=color, edgecolor=edge,
                             linewidth=1.3)
        ax.add_patch(d)
        ax.text(x, y, text, ha="center", va="center",
                fontsize=fs, color=HUAWEIBLUE)

    def arrow(x1, y1, x2, y2, label="", color=HUAWEIBLUE):
        a = FancyArrowPatch((x1, y1), (x2, y2),
                            arrowstyle="->", mutation_scale=15,
                            color=color, linewidth=1.4)
        ax.add_patch(a)
        if label:
            ax.text((x1 + x2) / 2 + 0.1, (y1 + y2) / 2,
                    label, fontsize=8, color=color, fontweight="bold")

    # Title
    ax.text(6, 10.5, "Workflow decisionale per la convergenza CFD",
            ha="center", fontsize=13, fontweight="bold", color=HUAWEIBLUE)

    # Step boxes
    box(6, 9.6, 4.0, 0.7, "1. Avvia simulazione (RANS / URANS / LES)",
        color=TABLEHEAD, weight="bold")
    arrow(6, 9.25, 6, 8.8)

    box(6, 8.5, 4.5, 0.6, "2. Monitor: residui RMS, monitor points, CFL",
        color=LIGHTBLUE)
    arrow(6, 8.2, 6, 7.8)

    diamond(6, 7.5, 4.5, 0.6,
            "Residui scendono di ≥ 4 ordini?", fs=9)
    arrow(8.2, 7.5, 9.7, 7.5, label="sì")
    arrow(3.8, 7.5, 2.3, 7.5, label="no")

    # NO branch
    box(2.3, 6.8, 3.5, 0.6, "Riduci CFL ×2 oppure\nattiva CFL_ADAPT",
        color="#FFF5F5", edge=ACCENT_RED)
    arrow(2.3, 6.5, 2.3, 5.9)
    diamond(2.3, 5.5, 3.5, 0.6, "Migliora?", fs=9)
    arrow(2.3, 5.2, 2.3, 4.6, label="no")
    box(2.3, 4.2, 3.5, 0.65, "Verifica mesh\n(skewness, BC, $y^+$)",
        color="#FFF5F5", edge=ACCENT_RED)
    arrow(4.0, 5.5, 5.5, 5.5, label="sì")

    # SI branch
    box(9.7, 6.8, 3.5, 0.7,
        "Stazionario?\nCheck monitor points\n(< 0.5% drift)",
        color=LIGHTBLUE, fs=8)
    arrow(9.7, 6.4, 9.7, 5.85)

    diamond(9.7, 5.5, 3.5, 0.6, "URANS / LES?", fs=9)
    arrow(9.7, 5.2, 9.7, 4.6, label="sì")

    # LES branch
    box(9.7, 4.1, 4.5, 0.85,
        "3. Inner residuals\ndecadono ≥ 3 ordini\nentro N$_{inner}$ massimo?",
        color="#F0FFF4", edge=ACCENT_GREEN, fs=9)
    arrow(9.7, 3.7, 9.7, 3.2)

    diamond(9.7, 2.85, 4.5, 0.65, "Statistiche convergenti?\n(8 $t_{FT}$, $|m_1-m_2|<2\\%$)", fs=8)
    arrow(7.45, 2.85, 5.5, 2.85, label="no: estendi simulazione")
    arrow(9.7, 2.55, 9.7, 2.0, label="sì")

    box(9.7, 1.6, 4.5, 0.7,
        "4. GCI < 3% sulla QoI\n(3 mesh, Celik 2008)",
        color="#F0FFF4", edge=ACCENT_GREEN, weight="bold", fs=9)
    arrow(9.7, 1.25, 9.7, 0.7)

    box(9.7, 0.4, 4.5, 0.55, "✓ SIMULAZIONE CONVERGENTE",
        color=ACCENT_GREEN, edge=HUAWEIBLUE, fs=10, weight="bold")

    # back arrows for fix loops (left side)
    arrow(2.3, 3.85, 4.0, 5.0, color=ACCENT_RED)

    # Legend
    legend_elements = [
        mpatches.Patch(facecolor=TABLEHEAD, edgecolor=HUAWEIBLUE,
                       label="Step procedurale"),
        mpatches.Patch(facecolor="#FFF7E6", edgecolor=ACCENT_ORANGE,
                       label="Decisione"),
        mpatches.Patch(facecolor="#FFF5F5", edgecolor=ACCENT_RED,
                       label="Azione correttiva"),
        mpatches.Patch(facecolor="#F0FFF4", edgecolor=ACCENT_GREEN,
                       label="Verifica di accettazione"),
    ]
    ax.legend(handles=legend_elements, loc="lower left",
              bbox_to_anchor=(0.0, -0.02), fontsize=8, ncol=4)

    out = os.path.join(OUTDIR, "fig_flowchart.png")
    plt.savefig(out)
    plt.close()
    print(f"✓ {out}")


# ==========================================================
# Main
# ==========================================================
if __name__ == "__main__":
    print("Genero figure didattiche convergenza in", OUTDIR)
    fig_residual_history()
    fig_cfl_effect()
    fig_gci_richardson()
    fig_dual_time_inner()
    fig_timestep_constraints()
    fig_running_mean()
    fig_welch_convergence()
    fig_yplus_histogram()
    fig_flowchart()
    print("\nTutte le figure generate con successo.")
