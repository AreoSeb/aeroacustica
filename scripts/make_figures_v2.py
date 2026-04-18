"""Generate figures for FW-H vs APE aeroacoustic comparison paper (v2)."""

import matplotlib

matplotlib.use("Agg")
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch, Rectangle

plt.rcParams.update(
    {
        "font.family": "DejaVu Sans",
        "font.size": 10,
        "axes.grid": True,
        "grid.alpha": 0.3,
        "axes.spines.top": False,
        "axes.spines.right": False,
    }
)

OUT = "/root/su2_paper/figs_v2"
import os

os.makedirs(OUT, exist_ok=True)

# Palette coerente
BLU       = "#1A365D"
AZZURRO   = "#2C5282"
ARANCIO   = "#E07B00"
VERDE     = "#2E7D32"
ROSSO     = "#C23B3B"
VIOLA     = "#8E44AD"
GRIGIO    = "#555555"
GRIGIO_LT = "#AAAAAA"
GRIGIO_FG = "#DDDDDD"


# ─────────────────────────────────────────────────────────────────────────────
# Fig. 1 — Conceptual diagram FW-H vs APE
# ─────────────────────────────────────────────────────────────────────────────
def fig_fwh_vs_ape_concept():
    """Fig. 1 — Diagramma concettuale: analogia integrale FW-H vs APE."""
    fig, (ax_l, ax_r) = plt.subplots(1, 2, figsize=(12, 5.5))
    fig.suptitle(
        "Fig. 1 — Confronto concettuale: analogia integrale vs propagazione risolta",
        fontsize=11, fontweight="bold", y=1.01,
    )

    rng = np.random.default_rng(42)

    # ── Pannello sinistro: FW-H ──────────────────────────────────────────────
    ax = ax_l
    ax.set_xlim(-4, 8)
    ax.set_ylim(-4, 4)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_title("FW-H (Analogia Integrale)", fontsize=10.5, fontweight="bold", color=AZZURRO)

    # Turbolent region (cerchio grigio)
    turb_circle = plt.Circle((0, 0), 1.3, color=GRIGIO_FG, ec=GRIGIO, lw=1.5, zorder=2)
    ax.add_patch(turb_circle)
    ax.text(0, -1.55, "turbolent region", ha="center", fontsize=8, color=GRIGIO)

    # Sorgenti CFD (dots verdi)
    for _ in range(22):
        xd = rng.uniform(-1.1, 1.1)
        yd = rng.uniform(-1.1, 1.1)
        if xd**2 + yd**2 < 1.1**2:
            ax.plot(xd, yd, "o", color=VERDE, ms=4, zorder=3, alpha=0.85)

    # Superficie permeabile FW-H (ellisse tratteggiata arancio)
    fwh_ell = mpatches.Ellipse(
        (0.1, 0), width=4.2, height=3.4,
        fill=False, edgecolor=ARANCIO, linestyle="--", linewidth=2.0, zorder=4,
    )
    ax.add_patch(fwh_ell)
    ax.text(
        0.1, 1.8, "superficie permeabile\nFW-H  $\\mathcal{S}$",
        ha="center", fontsize=8.5, color=ARANCIO,
    )

    # Punto sulla superficie → osservatore
    s_x, s_y = 1.85, 1.2
    obs_x, obs_y = 6.5, 2.2
    ax.plot(s_x, s_y, "s", color=ARANCIO, ms=7, zorder=5)
    ax.annotate(
        "",
        xy=(obs_x, obs_y),
        xytext=(s_x, s_y),
        arrowprops=dict(arrowstyle="->", color=BLU, lw=1.6),
        zorder=5,
    )
    # etichetta r
    mid_x = (s_x + obs_x) / 2
    mid_y = (s_y + obs_y) / 2
    ax.text(mid_x - 0.1, mid_y + 0.22, "$r$", fontsize=10, color=BLU)

    # Osservatore (punto rosso)
    ax.plot(obs_x, obs_y, "o", color=ROSSO, ms=9, zorder=6)
    ax.text(obs_x + 0.15, obs_y + 0.18, "Osservatore\n$\\mathbf{x}$", fontsize=8.5, color=ROSSO)

    # Formula
    ax.text(
        2.0, -3.5,
        r"$p'(\mathbf{x},t)=\int_{\mathcal{S}} G(\mathbf{x}-\mathbf{y})\,[Q]\,dS(\mathbf{y})$",
        ha="center", fontsize=9, color=BLU,
        bbox=dict(boxstyle="round,pad=0.4", facecolor="#EBF4FF", edgecolor=AZZURRO, alpha=0.9),
    )

    # ── Pannello destro: APE ─────────────────────────────────────────────────
    ax = ax_r
    ax.set_xlim(-4, 8)
    ax.set_ylim(-4, 4)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_title("APE (Eq. Perturbazione Acustica)", fontsize=10.5, fontweight="bold", color=VERDE)

    # Turbolent region
    turb_circle2 = plt.Circle((0, 0), 1.3, color=GRIGIO_FG, ec=GRIGIO, lw=1.5, zorder=2)
    ax.add_patch(turb_circle2)
    ax.text(0, -1.55, "turbolent region", ha="center", fontsize=8, color=GRIGIO)

    # Sorgenti CFD
    rng2 = np.random.default_rng(7)
    for _ in range(22):
        xd = rng2.uniform(-1.1, 1.1)
        yd = rng2.uniform(-1.1, 1.1)
        if xd**2 + yd**2 < 1.1**2:
            ax.plot(xd, yd, "o", color=VERDE, ms=4, zorder=3, alpha=0.85)

    # Mesh acustica (griglia di nodi blu)
    xs_mesh = np.linspace(-3.5, 7.0, 18)
    ys_mesh = np.linspace(-3.5, 3.5, 12)
    for xm in xs_mesh:
        for ym in ys_mesh:
            dist = xm**2 + ym**2
            if dist > 1.0:
                ax.plot(xm, ym, ".", color=AZZURRO, ms=2.5, alpha=0.55, zorder=2)

    # Linee di griglia orizzontali/verticali leggere
    for ym in ys_mesh[::2]:
        ax.plot(xs_mesh[[0, -1]], [ym, ym], "-", color=AZZURRO, lw=0.3, alpha=0.25, zorder=1)
    for xm in xs_mesh[::2]:
        ax.plot([xm, xm], ys_mesh[[0, -1]], "-", color=AZZURRO, lw=0.3, alpha=0.25, zorder=1)

    ax.text(
        3.0, 3.6, "mesh acustica APE\n(nodi blu)",
        ha="center", fontsize=8.5, color=AZZURRO,
    )

    # Onde (sinusoidi piccole che si propagano dalla sorgente)
    t_vals = np.linspace(0, np.pi, 100)
    for r_wave in [1.8, 2.6, 3.5, 4.5]:
        xw = r_wave * np.cos(t_vals)
        yw = r_wave * np.sin(t_vals)
        # solo parte non coperta dalla turbolent region
        mask = xw**2 + yw**2 > 1.4**2
        xw[~mask] = np.nan
        yw[~mask] = np.nan
        ax.plot(xw, yw, "-", color=ROSSO, lw=0.9, alpha=0.55, zorder=4)

    # Osservatore
    obs_x2, obs_y2 = 6.5, 2.2
    ax.plot(obs_x2, obs_y2, "o", color=ROSSO, ms=9, zorder=6)
    ax.text(obs_x2 + 0.15, obs_y2 + 0.18, "Osservatore\n$\\mathbf{x}$", fontsize=8.5, color=ROSSO)

    # Freccia da onda verso osservatore
    ax.annotate(
        "",
        xy=(obs_x2 - 0.6, obs_y2 - 0.4),
        xytext=(obs_x2 - 1.8, obs_y2 - 1.1),
        arrowprops=dict(arrowstyle="->", color=ROSSO, lw=1.5),
        zorder=5,
    )
    ax.text(obs_x2 - 2.6, obs_y2 - 1.5, "onde risolte", fontsize=7.5, color=ROSSO)

    # Formula APE
    ax.text(
        2.0, -3.5,
        r"$\dfrac{\partial p'}{\partial t}+c^{2}\nabla\cdot\mathbf{u}'=S_{\mathrm{APE}}(\mathbf{y},t)$",
        ha="center", fontsize=9, color=VERDE,
        bbox=dict(boxstyle="round,pad=0.4", facecolor="#E8F5E9", edgecolor=VERDE, alpha=0.9),
    )

    plt.tight_layout()
    plt.savefig(f"{OUT}/fig_fwh_vs_ape_concept.png", dpi=180, bbox_inches="tight")
    plt.close()


# ─────────────────────────────────────────────────────────────────────────────
# Fig. 2 — Cost vs Accuracy scatter
# ─────────────────────────────────────────────────────────────────────────────
def fig_cost_accuracy_tradeoff():
    """Fig. 2 — Trade-off accuratezza vs costo per metodi CAA."""
    fig, ax = plt.subplots(figsize=(8.5, 5.5))

    methods = [
        {
            "label": "FW-H rigido\n(solo sup. solida)",
            "cost": 1.0,
            "acc": 60,
            "color": GRIGIO_LT,
            "marker": "o",
            "size": 120,
        },
        {
            "label": "FW-H permeabile",
            "cost": 1.3,
            "acc": 78,
            "color": ARANCIO,
            "marker": "o",
            "size": 150,
        },
        {
            "label": "LEE\n(Linearized Euler)\n[instabilità idrodina.]",
            "cost": 8.0,
            "acc": 85,
            "color": ROSSO,
            "marker": "^",
            "size": 160,
        },
        {
            "label": "APE\n(Ewert-Schröder)\n★ sweet spot",
            "cost": 5.0,
            "acc": 92,
            "color": VERDE,
            "marker": "*",
            "size": 280,
        },
        {
            "label": "DNS acustico diretto\n(riferimento)",
            "cost": 30.0,
            "acc": 99,
            "color": BLU,
            "marker": "D",
            "size": 170,
        },
    ]

    # Pareto-front line: FW-H perm → APE → DNS
    pareto_pts = [(1.3, 78), (5.0, 92), (30.0, 99)]
    px, py = zip(*pareto_pts)
    ax.plot(
        px, py, "-", color=GRIGIO, lw=1.5, alpha=0.6, zorder=1,
        label="Pareto-front appross.",
    )

    # Scatter
    for m in methods:
        ax.scatter(
            m["cost"], m["acc"],
            c=m["color"], marker=m["marker"], s=m["size"],
            edgecolors="black", linewidths=0.7, zorder=4,
        )
        # offset label
        dy = 2.5
        dx = 0.0
        if "DNS" in m["label"]:
            dy = -5.5
            dx = 0.5
        if "LEE" in m["label"]:
            dx = 0.3
        ax.annotate(
            m["label"],
            xy=(m["cost"], m["acc"]),
            xytext=(m["cost"] * 1.05 + dx, m["acc"] + dy),
            fontsize=8.5,
            color=m["color"] if m["color"] != GRIGIO_LT else GRIGIO,
            arrowprops=dict(arrowstyle="-", color=GRIGIO_LT, lw=0.8),
        )

    # Zona "sweet spot" APE
    ax.axvspan(3.5, 7.0, alpha=0.07, color=VERDE, zorder=0)
    ax.text(5.2, 65, "zona\nsweet spot", ha="center", fontsize=8, color=VERDE, alpha=0.75)

    ax.set_xscale("log")
    ax.set_xlabel("Costo relativo  (FW-H rigido = 1)", fontsize=10)
    ax.set_ylabel("Accuratezza far-field in regime confinato [%]", fontsize=10)
    ax.set_title(
        "Fig. 2 — Trade-off accuratezza vs costo per metodi CAA",
        fontsize=11, fontweight="bold",
    )
    ax.set_xlim(0.7, 70)
    ax.set_ylim(45, 103)
    ax.legend(loc="lower right", fontsize=8.5)

    plt.tight_layout()
    plt.savefig(f"{OUT}/fig_cost_accuracy_tradeoff.png", dpi=180, bbox_inches="tight")
    plt.close()


# ─────────────────────────────────────────────────────────────────────────────
# Fig. 3 — Refraction comparison
# ─────────────────────────────────────────────────────────────────────────────
def fig_refraction_comparison():
    """Fig. 3 — FW-H non cattura diffrazione/rifrazione da ostacoli."""
    fig, (ax_l, ax_r) = plt.subplots(
        1, 2, figsize=(11, 4.8), sharey=True,
        gridspec_kw={"wspace": 0.08},
    )
    fig.suptitle(
        "Fig. 3 — FW-H non cattura diffrazione/rifrazione da ostacoli",
        fontsize=11, fontweight="bold",
    )

    # ── Sinistra: FW-H free-space ────────────────────────────────────────────
    ax = ax_l
    ax.set_xlim(-1, 7)
    ax.set_ylim(-1, 5)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_title("FW-H — Propagazione free-space", fontsize=10, color=AZZURRO)

    # Sorgente
    ax.plot(0, 2, "r*", ms=14, zorder=5, label="Sorgente")
    ax.text(0.15, 2.35, "Sorgente", fontsize=8.5, color=ROSSO)

    # Onde sferiche concentriche
    theta = np.linspace(0, 2 * np.pi, 360)
    for r in [0.6, 1.2, 1.9, 2.7, 3.6, 4.6]:
        ax.plot(
            r * np.cos(theta), 2 + r * np.sin(theta),
            "--", color=GRIGIO_LT, lw=0.9, alpha=0.7, zorder=2,
        )

    # Osservatore
    obs_x, obs_y = 5.5, 3.5
    ax.plot(obs_x, obs_y, "ko", ms=8, zorder=5)
    ax.text(obs_x + 0.12, obs_y + 0.15, "Osservatore", fontsize=8.5)

    # Retta sorgente-osservatore
    ax.plot([0, obs_x], [2, obs_y], "-", color=AZZURRO, lw=1.4, alpha=0.7, zorder=3)
    ax.text(2.5, 3.15, "propagazione\nretta", fontsize=8, color=AZZURRO, rotation=14)

    ax.text(3.0, 0.1, "nessun ostacolo", ha="center", fontsize=8.5, color=GRIGIO,
            style="italic")

    # ── Destra: APE con ostacolo ─────────────────────────────────────────────
    ax = ax_r
    ax.set_xlim(-1, 7)
    ax.set_ylim(-1, 5)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_title("APE — Con ostacolo e rifrazione", fontsize=10, color=VERDE)

    # Sorgente
    ax.plot(0, 2, "r*", ms=14, zorder=5)
    ax.text(0.15, 2.35, "Sorgente", fontsize=8.5, color=ROSSO)

    # Ostacolo rettangolare
    obs_rect = Rectangle(
        (2.0, 1.2), 1.5, 1.6,
        facecolor=GRIGIO_FG, edgecolor=GRIGIO, linewidth=1.5, zorder=4,
    )
    ax.add_patch(obs_rect)
    ax.text(2.75, 2.0, "ostacolo\n(mesh cubica)", ha="center", fontsize=7.5, color=GRIGIO)

    # Onde deformate (non circolari) attorno all'ostacolo
    theta_full = np.linspace(0, 2 * np.pi, 720)
    for r in [0.6, 1.2, 1.9, 2.8, 3.8]:
        xw = r * np.cos(theta_full)
        yw = 2 + r * np.sin(theta_full)
        # schiaccia le onde verso l'ostacolo
        in_obstacle_zone = (xw > 1.8) & (xw < 3.7) & (yw > 1.0) & (yw < 3.0)
        # deflect
        yw_def = yw.copy()
        xw_def = xw.copy()
        mask_top = in_obstacle_zone & (yw >= 2.0)
        mask_bot = in_obstacle_zone & (yw < 2.0)
        yw_def[mask_top] = 3.0 + (yw[mask_top] - 3.0) * 0.4
        yw_def[mask_bot] = 1.0 + (yw[mask_bot] - 1.0) * 0.4
        ax.plot(xw_def, yw_def, "--", color=GRIGIO_LT, lw=0.9, alpha=0.65, zorder=2)

    # Osservatore
    obs_x2, obs_y2 = 5.5, 3.5
    ax.plot(obs_x2, obs_y2, "ko", ms=8, zorder=5)
    ax.text(obs_x2 + 0.12, obs_y2 + 0.15, "Osservatore", fontsize=8.5)

    # Percorso curvato attorno all'ostacolo
    t_arc = np.linspace(0, 1, 80)
    path_x = t_arc * 5.5
    path_y = 2 + 1.2 * np.sin(np.pi * t_arc) + 0.5 * np.sin(2 * np.pi * t_arc)
    ax.plot(path_x, path_y, "-", color=VERDE, lw=1.6, alpha=0.8, zorder=3)
    # freccia sul percorso
    idx = 60
    ax.annotate(
        "",
        xy=(path_x[idx + 3], path_y[idx + 3]),
        xytext=(path_x[idx - 3], path_y[idx - 3]),
        arrowprops=dict(arrowstyle="->", color=VERDE, lw=1.5),
        zorder=5,
    )
    ax.text(4.5, 4.3, "percorso\ncurvato", fontsize=8, color=VERDE)

    plt.tight_layout()
    plt.savefig(f"{OUT}/fig_refraction_comparison.png", dpi=180, bbox_inches="tight")
    plt.close()


# ─────────────────────────────────────────────────────────────────────────────
# Fig. 4 — APE workflow flowchart
# ─────────────────────────────────────────────────────────────────────────────
def fig_ape_workflow():
    """Fig. 4 — Workflow hybrid LES + APE (flowchart verticale)."""
    fig, ax = plt.subplots(figsize=(10, 6.5))
    ax.set_xlim(0, 10)
    ax.set_ylim(-0.5, 7.5)
    ax.axis("off")
    ax.set_title(
        "Fig. 4 — Workflow hybrid LES + APE",
        fontsize=11, fontweight="bold", pad=10,
    )

    steps = [
        {
            "n": 1,
            "label": "1. SU2 LES",
            "detail": "campo CFD fluttuante\n$p(\\mathbf{x},t)$, $\\mathbf{u}(\\mathbf{x},t)$",
            "tool": "SU2 + LES WALE",
            "color": AZZURRO,
            "fc": "#EBF4FF",
            "y": 6.5,
        },
        {
            "n": 2,
            "label": "2. Estrazione sorgenti",
            "detail": "vettore di Lamb $\\mathbf{L}=\\boldsymbol{\\omega}\\times\\mathbf{u}$\npressione fluttuante $p'$",
            "tool": "pyvista / paraview",
            "color": VERDE,
            "fc": "#E8F5E9",
            "y": 5.2,
        },
        {
            "n": 3,
            "label": "3. Mesh APE",
            "detail": "griglia acustica (più grossolana della CFD)\nstrutturata o non-strutturata",
            "tool": "Gmsh / CGAL",
            "color": ARANCIO,
            "fc": "#FFF3E0",
            "y": 3.9,
        },
        {
            "n": 4,
            "label": "4. Interpolazione sorgenti",
            "detail": "proietta $S_{\\mathrm{APE}}$ da CFD-mesh\na APE-mesh",
            "tool": "scipy.interpolate / RBF",
            "color": VIOLA,
            "fc": "#F3E5F5",
            "y": 2.6,
        },
        {
            "n": 5,
            "label": "5. Solver APE",
            "detail": "integra sistema 4 PDE linearizzate\n$\\partial_t \\mathbf{q} + \\mathbf{A}\\cdot\\nabla\\mathbf{q} = \\mathbf{S}$",
            "tool": "PIANO DLR / custom Python",
            "color": ROSSO,
            "fc": "#FFEBEE",
            "y": 1.3,
        },
        {
            "n": 6,
            "label": "6. Post-processing",
            "detail": "SPL, spettri $E(f)$,\ndirettività $D(\\theta)$",
            "tool": "matplotlib / pandas",
            "color": "#B7950B",
            "fc": "#FFFDE7",
            "y": 0.0,
        },
    ]

    box_w = 5.0
    box_h = 0.85
    cx = 4.0  # centro x delle box

    for s in steps:
        # Box step
        ax.add_patch(
            FancyBboxPatch(
                (cx - box_w / 2, s["y"] - box_h / 2),
                box_w, box_h,
                boxstyle="round,pad=0.08",
                facecolor=s["fc"],
                edgecolor=s["color"],
                linewidth=1.8,
                zorder=3,
            )
        )
        # Testo label principale
        ax.text(
            cx, s["y"] + 0.18,
            s["label"],
            ha="center", va="center", fontsize=9.5, fontweight="bold",
            color=s["color"], zorder=4,
        )
        # Dettaglio
        ax.text(
            cx, s["y"] - 0.18,
            s["detail"],
            ha="center", va="center", fontsize=7.5, color=GRIGIO, zorder=4,
        )
        # Annotazione tool (a destra)
        ax.text(
            cx + box_w / 2 + 0.25, s["y"],
            f"⚙  {s['tool']}",
            ha="left", va="center", fontsize=8, color=s["color"], zorder=4,
        )

    # Frecce tra steps
    for i in range(len(steps) - 1):
        y_from = steps[i]["y"] - box_h / 2
        y_to   = steps[i + 1]["y"] + box_h / 2
        ax.annotate(
            "",
            xy=(cx, y_to),
            xytext=(cx, y_from),
            arrowprops=dict(arrowstyle="-|>", color=GRIGIO, lw=1.5),
            zorder=5,
        )

    plt.tight_layout()
    plt.savefig(f"{OUT}/fig_ape_workflow.png", dpi=180, bbox_inches="tight")
    plt.close()


# ─────────────────────────────────────────────────────────────────────────────
# Fig. 5 — Implementation options (Gantt-style)
# ─────────────────────────────────────────────────────────────────────────────
def fig_implementation_options():
    """Fig. 5 — Opzioni implementative APE: confronto tempi e rischio."""
    fig, ax = plt.subplots(figsize=(12, 5.5))

    options = [
        {
            "label": "Opzione A\nlibAcoustics (OpenFOAM)",
            "t_min": 2,
            "t_max": 4,
            "risk_color": VERDE,
            "risk": "basso",
            "pro": "affidabile, community attiva",
            "contra": "richiede export/import CFD→OF",
            "y": 2.0,
        },
        {
            "label": "Opzione B\nSolver APE custom Python/NumPy",
            "t_min": 6,
            "t_max": 8,
            "risk_color": ARANCIO,
            "risk": "medio",
            "pro": "pieno controllo, flessibile",
            "contra": "serve validazione vs. benchmark",
            "y": 1.0,
        },
        {
            "label": "Opzione C\nFork SU2 + solver APE C++",
            "t_min": 12,
            "t_max": 24,
            "risk_color": ROSSO,
            "risk": "alto",
            "pro": "integrazione nativa SU2",
            "contra": "padronanza C++ SU2 richiesta",
            "y": 0.0,
        },
    ]

    bar_h = 0.55
    for opt in options:
        duration = opt["t_max"] - opt["t_min"]
        # Barra principale
        ax.barh(
            opt["y"], duration,
            left=opt["t_min"], height=bar_h,
            color=opt["risk_color"], alpha=0.75,
            edgecolor="black", linewidth=1.2,
            zorder=3,
        )
        # Label sulla barra
        cx_bar = opt["t_min"] + duration / 2
        ax.text(
            cx_bar, opt["y"],
            f"{opt['t_min']}–{opt['t_max']} settimane",
            ha="center", va="center", fontsize=9, fontweight="bold",
            color="white", zorder=4,
        )
        # Label opzione a sinistra
        ax.text(
            opt["t_min"] - 0.3, opt["y"],
            opt["label"],
            ha="right", va="center", fontsize=9, color=opt["risk_color"],
        )
        # Rischio
        ax.text(
            opt["t_max"] + 0.4, opt["y"] + 0.16,
            f"Rischio: {opt['risk'].upper()}",
            ha="left", va="center", fontsize=8.5, color=opt["risk_color"],
            fontweight="bold",
        )
        # Pro/contro
        ax.text(
            opt["t_max"] + 0.4, opt["y"] - 0.16,
            f"✔ {opt['pro']}   |   ✘ {opt['contra']}",
            ha="left", va="center", fontsize=7.5, color=GRIGIO,
        )

    # Linee verticali di riferimento
    for t in [4, 8, 12, 16, 20, 24]:
        ax.axvline(t, color=GRIGIO_FG, lw=0.8, zorder=1)

    # Fascia "pianificabile in 1 sprint"
    ax.axvspan(0, 4, alpha=0.06, color=VERDE, zorder=0)
    ax.text(2.0, 2.65, "1 sprint\n(4 sett.)", ha="center", fontsize=8, color=VERDE, alpha=0.8)

    # Tabella riassuntiva sotto i grafici
    table_y = -0.75
    col_x  = [3, 10, 17, 24]
    headers = ["", "Tempo stimato", "Rischio", "Pro (breve)"]
    rows = [
        ["Opzione A", "2–4 sett.",    "BASSO",  "affidabile, rapido"],
        ["Opzione B", "6–8 sett.",    "MEDIO",  "pieno controllo"],
        ["Opzione C", "3–6 mesi",     "ALTO",   "nativa SU2"],
    ]
    row_cols = [GRIGIO_FG, "#E8F5E9", "#FFF3E0", "#FFEBEE"]
    col_colors = [GRIGIO, VERDE, ARANCIO, ROSSO]

    for ci, (hdr, cx_t) in enumerate(zip(headers, col_x)):
        ax.text(cx_t, table_y - 0.05, hdr, ha="center", fontsize=8.5,
                fontweight="bold", color=col_colors[ci])

    for ri, row in enumerate(rows):
        dy = table_y - 0.45 - ri * 0.38
        for ci, (cell, cx_t) in enumerate(zip(row, col_x)):
            ax.text(cx_t, dy, cell, ha="center", fontsize=8.0, color=GRIGIO)

    # Linea separatrice tabella
    ax.axhline(table_y + 0.12, color=GRIGIO_LT, lw=0.8, xmin=0.0, xmax=1.0)

    ax.set_xlim(-12, 30)
    ax.set_ylim(-1.85, 3.0)
    ax.set_xlabel("Tempo [settimane]", fontsize=10)
    ax.set_yticks([])
    ax.spines["left"].set_visible(False)
    ax.set_title(
        "Fig. 5 — Opzioni implementative APE: confronto tempi e rischio",
        fontsize=11, fontweight="bold",
    )

    # Legenda rischi
    legend_patches = [
        mpatches.Patch(color=VERDE,   label="Rischio basso"),
        mpatches.Patch(color=ARANCIO, label="Rischio medio"),
        mpatches.Patch(color=ROSSO,   label="Rischio alto"),
    ]
    ax.legend(handles=legend_patches, loc="upper right", fontsize=9)

    plt.tight_layout()
    plt.savefig(f"{OUT}/fig_implementation_options.png", dpi=180, bbox_inches="tight")
    plt.close()


# ─────────────────────────────────────────────────────────────────────────────
# Entry point
# ─────────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    fig_fwh_vs_ape_concept()
    print("  fig_fwh_vs_ape_concept.png OK")
    fig_cost_accuracy_tradeoff()
    print("  fig_cost_accuracy_tradeoff.png OK")
    fig_refraction_comparison()
    print("  fig_refraction_comparison.png OK")
    fig_ape_workflow()
    print("  fig_ape_workflow.png OK")
    fig_implementation_options()
    print("  fig_implementation_options.png OK")
    print(f"\nTutte le figure scritte in {OUT}")
