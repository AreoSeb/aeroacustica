"""Generate figures for the SU2 aeroacoustic jet-impingement paper."""

import matplotlib

matplotlib.use("Agg")
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyArrowPatch, Rectangle

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

OUT = "/root/su2_paper/figs"
import os

os.makedirs(OUT, exist_ok=True)


def fig_domain():
    """Fig. 1 — Domain schematic (nuova geometria: camera D=20mm×H=3mm + tubo inlet D=1.5mm×H=1mm sopra)."""
    # Scala di visualizzazione: mantieni proporzioni orizzontali reali,
    # ingrandisci verticalmente x5 per leggibilità (dominio piatto H/D = 0.15).
    # Tutte le misure sono in mm (unità di disegno).
    # Scala verticale: 1 unità grafica = 0.5 mm reale (quindi H_cam=3mm → 6 u.g.)
    VSCALE = 2.0  # ingrandimento verticale

    D_cam = 20.0   # mm, diametro camera principale
    H_cam = 3.0    # mm, altezza camera principale
    D_jet = 1.5    # mm, diametro tubo inlet
    H_jet = 1.0    # mm, altezza tubo inlet
    # Coordinate in unità grafiche (y moltiplicato per VSCALE)
    H_cam_v = H_cam * VSCALE   # 6
    H_jet_v = H_jet * VSCALE   # 2
    D_fwh = 12.0   # mm, diametro FW-H surface
    H_fwh = 2.5    # mm, altezza FW-H surface (da 1 mm sopra chip)
    H_fwh_v = H_fwh * VSCALE
    fwh_y0 = 1.0 * VSCALE  # 1mm sopra chip

    fig, ax = plt.subplots(figsize=(7.5, 6.0))

    # --- Camera principale (y=0 chip, y=H_cam_v top camera) ---
    ax.add_patch(
        Rectangle(
            (-D_cam / 2, 0), D_cam, H_cam_v,
            fill=False, edgecolor="black", linewidth=1.8
        )
    )

    # --- Tubo inlet: SOPRA la camera, al centro, attaccato al top della camera ---
    # y_base_tubo = H_cam_v, altezza = H_jet_v
    tube_x0 = -D_jet / 2
    tube_y0 = H_cam_v
    ax.add_patch(
        Rectangle(
            (tube_x0, tube_y0), D_jet, H_jet_v,
            facecolor="#4A90D9", edgecolor="black", linewidth=1.4, alpha=0.75
        )
    )

    # Top del tubo = velocity inlet (linea rossa spessa + freccia)
    ax.plot(
        [-D_jet / 2, D_jet / 2], [tube_y0 + H_jet_v, tube_y0 + H_jet_v],
        color="#C23B3B", linewidth=2.5, solid_capstyle="round"
    )
    # Freccia flusso in ingresso (verso il basso)
    ax.annotate(
        "",
        xy=(0, tube_y0 + H_jet_v * 0.25),
        xytext=(0, tube_y0 + H_jet_v * 0.85),
        arrowprops=dict(arrowstyle="->", color="#C23B3B", lw=2.0),
    )
    ax.annotate(
        "Velocity inlet\n(U = 10 m/s ↓, T = 293 K)",
        xy=(D_jet / 2, tube_y0 + H_jet_v),
        xytext=(4.5, tube_y0 + H_jet_v + 1.5),
        fontsize=9, ha="left", color="#C23B3B",
        arrowprops=dict(arrowstyle="->", color="#C23B3B"),
    )

    # Label tubo inlet
    ax.annotate(
        "Tubo inlet\nD=1.5 mm\nH=1 mm\n(pareti no-slip)",
        xy=(-D_jet / 2, tube_y0 + H_jet_v / 2),
        xytext=(-8.5, tube_y0 + H_jet_v / 2),
        fontsize=8.5, ha="right", va="center",
        arrowprops=dict(arrowstyle="->", color="#333"),
    )

    # --- Top camera: parete no-slip (tranne il foro D=1.5mm al centro) ---
    # Linea sinistra: da -D_cam/2 a -D_jet/2
    ax.plot(
        [-D_cam / 2, -D_jet / 2], [H_cam_v, H_cam_v],
        color="#555", linewidth=2.8, solid_capstyle="butt"
    )
    # Linea destra: da D_jet/2 a D_cam/2
    ax.plot(
        [D_jet / 2, D_cam / 2], [H_cam_v, H_cam_v],
        color="#555", linewidth=2.8, solid_capstyle="butt"
    )
    ax.text(
        7, H_cam_v + 0.3, "Top camera: no-slip\n(tranne foro centrale D=1.5 mm)",
        fontsize=8.0, ha="left", color="#555"
    )

    # --- Chip (fondo camera, y=0) ---
    ax.add_patch(
        Rectangle(
            (-4, -0.9 * VSCALE), 8, 0.9 * VSCALE,
            facecolor="#444", edgecolor="black", hatch="//", linewidth=1.2,
        )
    )
    ax.text(0, -1.1 * VSCALE, "Chip (no-slip, adiabatico)", ha="center", fontsize=9, color="#222")

    # --- Outlet laterale (superficie cilindrica D=20mm) ---
    # Frecce verso l'esterno, a metà altezza camera
    y_out = H_cam_v / 2
    ax.annotate(
        "",
        xy=(D_cam / 2 + 4.0, y_out),
        xytext=(D_cam / 2 + 0.1, y_out),
        arrowprops=dict(arrowstyle="->", color="#E07B00", lw=2.0),
    )
    ax.annotate(
        "",
        xy=(-D_cam / 2 - 4.0, y_out),
        xytext=(-D_cam / 2 - 0.1, y_out),
        arrowprops=dict(arrowstyle="->", color="#E07B00", lw=2.0),
    )
    ax.text(
        D_cam / 2 + 4.2, y_out + 0.3,
        "Outlet laterale\n(p = 0)",
        color="#E07B00", fontsize=9, ha="left"
    )

    # --- Getto (colonna di flusso nell'interno della camera) ---
    for y_top in np.linspace(H_cam_v - 0.2, 0.3, 14):
        alpha = max(0.15, 0.55 - (H_cam_v - y_top) * 0.03)
        ax.add_patch(
            Rectangle(
                (-D_jet / 2 * 0.9, y_top), D_jet * 0.9, 0.25,
                facecolor="#88BBE0", alpha=alpha, lw=0
            )
        )

    # Frecce di impingement radiale
    for x_frac in [-0.7, -0.4, 0.4, 0.7]:
        x_end = x_frac * D_cam / 2 * 0.55
        ax.annotate(
            "",
            xy=(x_end, 0.18),
            xytext=(x_end * 0.3, 1.1),
            arrowprops=dict(arrowstyle="->", color="#6A9EC4", lw=1.2, alpha=0.8),
        )

    # --- FW-H permeable surface ---
    fwh_r = D_fwh / 2  # 6 mm
    ax.add_patch(
        Rectangle(
            (-fwh_r, fwh_y0), 2 * fwh_r, H_fwh_v,
            fill=False, edgecolor="#D08500", linestyle="--", linewidth=1.5,
        )
    )
    ax.text(
        -fwh_r - 0.3, fwh_y0 + H_fwh_v + 0.4,
        "FW-H superficie permeabile\n(D=12 mm × H=2.5 mm, 1 mm sopra chip)",
        color="#D08500", fontsize=8.5, ha="left"
    )

    # --- Quote dimensionali ---
    # Larghezza camera
    dim_y = -2.8 * VSCALE
    ax.annotate(
        "",
        xy=(-D_cam / 2, dim_y), xytext=(D_cam / 2, dim_y),
        arrowprops=dict(arrowstyle="<->", color="black"),
    )
    ax.text(0, dim_y - 0.5, "D = 20 mm", ha="center", fontsize=9)

    # Altezza camera (asse destro)
    dim_x_right = D_cam / 2 + 7.5
    ax.annotate(
        "",
        xy=(dim_x_right, 0), xytext=(dim_x_right, H_cam_v),
        arrowprops=dict(arrowstyle="<->", color="black"),
    )
    ax.text(dim_x_right + 0.4, H_cam_v / 2, "H = 3 mm",
            rotation=90, fontsize=9, va="center")

    # Altezza tubo inlet (asse sinistro)
    dim_x_left = -D_cam / 2 - 5.0
    ax.annotate(
        "",
        xy=(dim_x_left, H_cam_v), xytext=(dim_x_left, H_cam_v + H_jet_v),
        arrowprops=dict(arrowstyle="<->", color="black"),
    )
    ax.text(dim_x_left - 0.4, H_cam_v + H_jet_v / 2, "H_inlet = 1 mm",
            rotation=90, fontsize=8.5, va="center")

    # Gap totale chip→top inlet
    dim_x_gap = D_cam / 2 + 7.5
    ax.annotate(
        "",
        xy=(dim_x_gap + 2.0, 0), xytext=(dim_x_gap + 2.0, H_cam_v + H_jet_v),
        arrowprops=dict(arrowstyle="<->", color="#8E44AD"),
    )
    ax.text(dim_x_gap + 2.5, (H_cam_v + H_jet_v) / 2,
            "Gap\ntot = 4 mm",
            rotation=90, fontsize=8.5, va="center", color="#8E44AD")

    # Quote D_jet
    ax.annotate(
        "",
        xy=(-D_jet / 2, H_cam_v + H_jet_v + 1.0),
        xytext=(D_jet / 2, H_cam_v + H_jet_v + 1.0),
        arrowprops=dict(arrowstyle="<->", color="black"),
    )
    ax.text(0, H_cam_v + H_jet_v + 1.5,
            "D_j = 1.5 mm", ha="center", fontsize=8.5)

    # --- Note Re e aspetto ---
    ax.text(
        -D_cam / 2, -3.6 * VSCALE,
        "Re = 1000  (D_j = 1.5 mm, U = 10 m/s, aria std)   |   "
        "Scala verticale ×2 per leggibilità  (H/D reale = 0.15)",
        fontsize=8, color="#555", ha="left"
    )

    ax.set_xlim(-18, 20)
    ax.set_ylim(-4.5 * VSCALE, H_cam_v + H_jet_v + 5.0)
    ax.axis("off")
    ax.set_title("Fig. 1 — Dominio cilindrico: camera D=20×H=3 mm + tubo inlet D=1.5×H=1 mm (scala v ×2)")
    plt.tight_layout()
    plt.savefig(f"{OUT}/fig_domain.png", dpi=180, bbox_inches="tight")
    plt.close()


def fig_scales():
    """Fig. 2 — Turbulent length scales (log). Valori aggiornati alla geometria compatta."""
    fig, ax = plt.subplots(figsize=(7.5, 3.8))

    scales = [
        ("Kolmogorov η", 7e-6, "#C23B3B"),      # aggiornato: 7 μm
        ("Taylor λ", 13e-6, "#E07B00"),           # aggiornato: 13 μm
        ("Integral L₀", 7.5e-4, "#1E73BE"),       # aggiornato: 750 μm = 0.75 mm
        ("Jet D_j", 1.5e-3, "#2E7D32"),
        ("Domain D", 2e-2, "#555"),
    ]
    x_pos = np.arange(len(scales))
    vals = [s[1] for s in scales]
    colors = [s[2] for s in scales]
    labels = [s[0] for s in scales]

    bars = ax.bar(x_pos, vals, color=colors, edgecolor="black", linewidth=0.8)
    ax.set_yscale("log")
    ax.set_xticks(x_pos)
    ax.set_xticklabels(labels)
    ax.set_ylabel("Scala di lunghezza [m]")
    ax.set_title("Fig. 2 — Gerarchia delle scale di lunghezza (Re=1000, U=10 m/s, D_j=1.5 mm)")

    for bar, val in zip(bars, vals):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            val * 1.5,
            f"{val*1e6:.0f} μm" if val < 1e-3 else f"{val*1e3:.1f} mm",
            ha="center",
            fontsize=9,
        )

    ax.axhspan(5e-6, 20e-6, alpha=0.15, color="green", label="Δ_min LES consigliato")
    ax.set_ylim(1e-6, 1e-1)
    ax.legend(loc="upper left")
    plt.tight_layout()
    plt.savefig(f"{OUT}/fig_scales.png", dpi=180)
    plt.close()


def fig_timestep():
    """Fig. 3 — Timestep constraints. Aggiornato: τ_η/10 = 3.4e-7 s."""
    fig, ax = plt.subplots(figsize=(7.5, 3.8))
    constraints = [
        ("CFL convettivo\n(Δx/U, CFL=0.5)", 1e-6, "#1E73BE"),
        ("CFL acustico\n(Δx/c, compress.)", 6e-8, "#C23B3B"),
        ("Nyquist @ 20 kHz", 2.5e-5, "#E07B00"),
        ("20 pts/periodo\n@ 20 kHz", 2.5e-6, "#8E44AD"),
        ("τ_η / 10\n(Kolmogorov, τ_η=3.4μs)", 3.4e-7, "#2E7D32"),  # aggiornato
    ]
    xs = np.arange(len(constraints))
    vals = [c[1] for c in constraints]
    cols = [c[2] for c in constraints]
    labs = [c[0] for c in constraints]
    bars = ax.bar(xs, vals, color=cols, edgecolor="black", linewidth=0.8)
    ax.set_yscale("log")
    ax.set_xticks(xs)
    ax.set_xticklabels(labs, fontsize=8.5)
    ax.set_ylabel("Δt max [s]")
    ax.axhline(5e-7, color="red", linestyle="--", lw=1.8, label="Δt scelto = 5·10⁻⁷ s")
    ax.set_title("Fig. 3 — Vincoli sul passo temporale (τ_η=3.4 μs, τ_jet=0.15 ms, t_FT≈4 ms)")
    for bar, val in zip(bars, vals):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            val * 1.3,
            f"{val:.1e}",
            ha="center",
            fontsize=8,
        )
    ax.legend(loc="lower right")
    ax.set_ylim(1e-8, 1e-4)
    plt.tight_layout()
    plt.savefig(f"{OUT}/fig_timestep.png", dpi=180)
    plt.close()


def fig_cell_count():
    """Fig. 4 — Cell count breakdown per zona (dominio compatto 4.5× più piccolo)."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4.2))

    zones = [
        "Prism wall\n(chip)",
        "Prism wall\n(top + tubo inlet)",
        "Jet core +\nshear layer",
        "Impingement\nnear-wall",
        "Transizione",
        "Dominio\nesterno",
    ]
    vals = [4.2, 4.0, 0.2, 0.8, 2.0, 0.8]  # Mcells — target WRLES ~12M totali
    cols = ["#C23B3B", "#E07B00", "#1E73BE", "#8E44AD", "#2E7D32", "#666"]

    # Stacked bar
    bottoms = np.cumsum([0] + vals[:-1])
    for z, v, c, b in zip(zones, vals, cols, bottoms):
        ax1.bar(0, v, bottom=b, color=c, edgecolor="white", label=f"{z} ({v:.1f} M)")
    ax1.set_ylabel("Celle [milioni]")
    ax1.set_xticks([])
    total = sum(vals)
    ax1.text(0, total + 0.3, f"Totale ≈ {total:.0f} M", ha="center", fontsize=10, fontweight="bold")
    ax1.set_title("Fig. 4a — Cell count per zona (tet+prism)\nDominio compatto: camera 3 mm × tubo 1 mm")
    ax1.legend(loc="center left", bbox_to_anchor=(1.02, 0.5), fontsize=8.0)

    # Comparison multi-fase
    variants = ["RANS\nvalidazione", "URANS", "DDES/IDDES", "WMLES", "WRLES\n(target)"]
    counts = [0.5, 1.5, 3.0, 6.0, 12.0]
    bar_cols = ["#aaa", "#888", "#E07B00", "#1E73BE", "#C23B3B"]
    bars = ax2.bar(variants, counts, color=bar_cols, edgecolor="black", linewidth=0.8)
    ax2.set_ylabel("Celle [milioni]")
    ax2.set_title("Fig. 4b — Dimensione mesh per fase di validazione")
    for bar, v in zip(bars, counts):
        ax2.text(
            bar.get_x() + bar.get_width() / 2,
            v + 0.2,
            f"{v:.1f} M",
            ha="center",
            fontsize=9,
        )
    plt.tight_layout()
    plt.savefig(f"{OUT}/fig_cells.png", dpi=180)
    plt.close()


def fig_pipeline():
    """Fig. 5 — Validation pipeline flowchart. Aggiornati Δt per Fasi 3, 4, 5."""
    fig, ax = plt.subplots(figsize=(9.5, 5))
    steps = [
        ("Fase 1\nRANS SST\n(~0.5 M)", 0.5, 0.7, "#d4e6f1"),
        ("Fase 2\nGCI Celik\n(3 mesh)", 0.5, 0.55, "#d1f2eb"),
        ("Fase 3\nURANS SST\n(~1.5 M)\nΔt=1×10⁻⁵ s", 0.5, 0.4, "#fdebd0"),   # aggiornato
        ("Fase 4\nDDES SA\n(~3 M)\nΔt=5×10⁻⁶ s", 0.5, 0.25, "#fadbd8"),       # aggiornato
        ("Fase 5\nLES WALE\n(~12 M)\nΔt=5×10⁻⁷ s", 0.5, 0.1, "#e8daef"),      # aggiornato
        ("Fase 6\nFW-H post\n(permeable)", 0.87, 0.1, "#ffe9a8"),
    ]
    for txt, x, y, c in steps:
        ax.add_patch(
            mpatches.FancyBboxPatch(
                (x - 0.1, y - 0.06),
                0.2,
                0.12,
                boxstyle="round,pad=0.02",
                facecolor=c,
                edgecolor="black",
            )
        )
        ax.text(x, y, txt, ha="center", va="center", fontsize=8.5)

    # Vertical arrows
    for (_, _, y1, _), (_, _, y2, _) in zip(steps[:-2], steps[1:-1]):
        ax.annotate(
            "",
            xy=(0.5, y2 + 0.06),
            xytext=(0.5, y1 - 0.06),
            arrowprops=dict(arrowstyle="->", color="black", lw=1.4),
        )
    # Side arrow
    ax.annotate(
        "",
        xy=(0.77, 0.1),
        xytext=(0.6, 0.1),
        arrowprops=dict(arrowstyle="->", color="black", lw=1.4),
    )

    # Criteria on the right
    criteria = [
        (0.75, 0.7, "Res<1e-5, ṁ conservata"),
        (0.75, 0.55, "GCI<5%, p>1.8"),
        (0.75, 0.4, "Picco spettrale\nSt≈0.3"),
        (0.75, 0.25, "Pendenza −5/3\nnella shear layer"),
        (0.28, 0.1, "Pope M(x)≥0.80\nCelik LES_IQ≥0.80"),
    ]
    for x, y, t in criteria:
        ax.text(x, y, t, fontsize=8.5, va="center", color="#333", style="italic")

    ax.set_xlim(0, 1)
    ax.set_ylim(0, 0.85)
    ax.axis("off")
    ax.set_title("Fig. 5 — Pipeline di validazione multi-fedeltà (6 fasi)")
    plt.tight_layout()
    plt.savefig(f"{OUT}/fig_pipeline.png", dpi=180)
    plt.close()


def fig_spectra_expected():
    """Fig. 6 — Expected energy spectrum with -5/3 slope (schematic)."""
    fig, ax = plt.subplots(figsize=(7, 4))
    k = np.logspace(2, 5.5, 300)
    # Synthetic spectrum: plateau then -5/3 then dissipation
    k_e = 3e3
    k_d = 1.5e5
    E = 1e-5 * (k / k_e) ** (-5 / 3) * np.exp(-((k / k_d) ** 2))
    E[k < k_e] = E[k >= k_e][0] * (k[k < k_e] / k_e) ** (-1)  # approx L-shape
    ax.loglog(k, E, "-", color="#1E73BE", lw=2, label="Target spettro risolto LES")
    # Filter cutoff zone
    k_cut = 1e5
    ax.axvline(k_cut, color="red", ls="--", lw=1.4, label="Filtro LES (Δ)")
    ax.axvspan(k_cut, 1e6, alpha=0.12, color="red")
    # Annotate -5/3
    ax.text(1e4, 2e-8, "pendenza −5/3", color="#1E73BE", fontsize=11, rotation=-22)
    ax.set_xlabel("k [1/m]")
    ax.set_ylabel("E(k) [m³/s²]")
    ax.set_title("Fig. 6 — Spettro di energia atteso (inertial range)")
    ax.legend(loc="lower left")
    plt.tight_layout()
    plt.savefig(f"{OUT}/fig_spectra.png", dpi=180)
    plt.close()


def fig_hardware():
    """Fig. 7 — Confronto hardware: Laptop vs CINECA vs AWS."""
    fig, ax = plt.subplots(figsize=(11, 5.5))

    # Dati piattaforme
    platforms = [
        {
            "name": "Laptop\nRyzen 9 AI 370 HX",
            "details": "12 core Zen 5 | 32 GB RAM\n~0.3 TFlops FP64 eff.\n(Turbo 5.1 GHz)",
            "max_cells_M": 3.0,
            "cost_eur_h": 0.0,
            "suitable": "RANS ≤ 3 M\nURANS ≤ 1.5 M",
            "color": "#2E7D32",
            "bar_color": "#A8D5A2",
        },
        {
            "name": "CINECA\nGalileo100 / Leonardo",
            "details": "fino 512 core EPYC/Xeon\nStorage Lustre | InfiniBand HDR\n€ 0.02 / core-h",
            "max_cells_M": 12.0,
            "cost_eur_h": 0.02 * 128,   # 128 core tipici, costo=€2.56/h
            "suitable": "DDES / WMLES\nWRLES 12 M",
            "color": "#1E73BE",
            "bar_color": "#A0C4E8",
        },
        {
            "name": "AWS\nhpc7a.96xlarge",
            "details": "192 core EPYC 9R14 | 768 GB RAM\nEFA network | Savings Plan\n$7.20/h on-demand",
            "max_cells_M": 12.0,
            "cost_eur_h": 7.20 * 0.92,  # $/h on-demand → EUR approx
            "suitable": "DDES / WMLES\nWRLES (alternativa commerciale)",
            "color": "#E07B00",
            "bar_color": "#F4C98A",
        },
    ]

    n = len(platforms)
    x = np.arange(n)
    col_centers = x * 3.5  # spaziatura colonne

    # Asse principale: max mesh cells (barre)
    width = 1.4
    bars = ax.bar(
        col_centers, [p["max_cells_M"] for p in platforms],
        width=width,
        color=[p["bar_color"] for p in platforms],
        edgecolor=[p["color"] for p in platforms],
        linewidth=1.8,
        zorder=3,
    )

    # Etichette max cells
    for bar, p in zip(bars, platforms):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + 0.25,
            f"max ≈ {p['max_cells_M']:.0f} M celle",
            ha="center", fontsize=9, fontweight="bold",
        )

    # Etichette nome piattaforma
    ax.set_xticks(col_centers)
    ax.set_xticklabels([p["name"] for p in platforms], fontsize=10, fontweight="bold")
    ax.set_ylabel("Capacità max mesh [milioni di celle]", fontsize=10)
    ax.set_ylim(0, 16)

    # Testo dettagli tecnici (sotto il grafico)
    for i, p in enumerate(platforms):
        ax.text(
            col_centers[i], -2.5,
            p["details"],
            ha="center", va="top", fontsize=8.0, color=p["color"],
            linespacing=1.4,
        )
        # Adatta simulazione
        ax.text(
            col_centers[i], 14.0,
            f"Adatto per:\n{p['suitable']}",
            ha="center", va="top", fontsize=8.0,
            bbox=dict(boxstyle="round,pad=0.3", facecolor=p["bar_color"], edgecolor=p["color"], alpha=0.8),
        )

    # Asse secondario: costo orario (linea + punti)
    ax2 = ax.twinx()
    ax2.spines["right"].set_visible(True)
    costs = [p["cost_eur_h"] for p in platforms]
    ax2.plot(col_centers, costs, "D--", color="#8E44AD", lw=1.8, ms=9, zorder=5, label="Costo/ora [€]")
    ax2.set_ylabel("Costo orario [€/h]", color="#8E44AD", fontsize=10)
    ax2.tick_params(axis="y", colors="#8E44AD")
    for xc, c in zip(col_centers, costs):
        if c > 0:
            ax2.text(xc + 0.8, c + 0.2, f"€{c:.1f}/h", color="#8E44AD", fontsize=8.5)
        else:
            ax2.text(xc + 0.8, 0.5, "€ 0 (locale)", color="#2E7D32", fontsize=8.5)
    ax2.set_ylim(0, 12)
    ax2.legend(loc="upper right", fontsize=9)

    ax.set_xlim(-1.5, col_centers[-1] + 2.0)
    ax.set_title(
        "Fig. 7 — Confronto piattaforme hardware: capacità mesh e costi operativi",
        fontsize=11, pad=14
    )
    ax.grid(axis="y", alpha=0.3, zorder=0)

    plt.tight_layout(rect=[0, 0.15, 1, 1])
    plt.savefig(f"{OUT}/fig_hardware.png", dpi=180, bbox_inches="tight")
    plt.close()


def fig_costs():
    """Fig. 8 — Costi totali per le 5 simulazioni target (CINECA vs AWS, scala log)."""
    fig, ax = plt.subplots(figsize=(9.5, 5.0))

    # Dati costi per simulazione
    # Formato: (label, costo_CINECA_EUR, costo_AWS_USD)
    sims = [
        ("RANS fine\n(0.5 M celle)", 0.0, 0.0),         # laptop, gratis
        ("URANS\n(1.5 M celle)", 15.0, 0.0),             # CINECA €15 (laptop fallback €0)
        ("DDES\n(3 M celle)", 36.0, 75.0),
        ("WMLES\n(6 M celle)", 300.0, 600.0),
        ("WRLES\n(12 M celle)", 1220.0, 2100.0),          # AWS Savings / on-demand $3500
    ]

    labels = [s[0] for s in sims]
    costs_cineca = np.array([s[1] for s in sims], dtype=float)
    costs_aws = np.array([s[2] for s in sims], dtype=float)

    x = np.arange(len(sims))
    width = 0.35

    # Barre CINECA (blu) — sostituisce 0 con NaN per log scale
    c_cineca_plot = np.where(costs_cineca == 0, np.nan, costs_cineca)
    c_aws_plot = np.where(costs_aws == 0, np.nan, costs_aws)

    bars_c = ax.bar(
        x - width / 2, c_cineca_plot, width,
        color="#4A90D9", edgecolor="#1E73BE", linewidth=1.2,
        label="CINECA (€)", zorder=3
    )
    bars_a = ax.bar(
        x + width / 2, c_aws_plot, width,
        color="#F4A56A", edgecolor="#E07B00", linewidth=1.2,
        label="AWS hpc7a (US$, Savings Plan)", zorder=3
    )

    # Etichette valore sulle barre
    for bar, val in zip(bars_c, costs_cineca):
        if val > 0:
            ax.text(
                bar.get_x() + bar.get_width() / 2,
                val * 1.45,
                f"€{val:.0f}",
                ha="center", fontsize=8.5, color="#1E73BE", fontweight="bold"
            )
        else:
            ax.text(
                x[list(costs_cineca).index(val)] - width / 2,
                2.5,
                "laptop\n€ 0",
                ha="center", fontsize=7.5, color="#2E7D32"
            )

    for bar, val in zip(bars_a, costs_aws):
        if val > 0:
            ax.text(
                bar.get_x() + bar.get_width() / 2,
                val * 1.45,
                f"${val:.0f}",
                ha="center", fontsize=8.5, color="#E07B00", fontweight="bold"
            )
        else:
            ax.text(
                x[list(costs_aws).index(val)] + width / 2,
                2.5,
                "laptop\n€ 0",
                ha="center", fontsize=7.5, color="#2E7D32"
            )

    # Nota on-demand AWS WRLES
    ax.annotate(
        "AWS on-demand\n≈ $3 500",
        xy=(x[-1] + width / 2, 2100),
        xytext=(x[-1] + width / 2 + 0.5, 3200),
        fontsize=8, color="#C23B3B",
        arrowprops=dict(arrowstyle="->", color="#C23B3B", lw=1.2),
    )

    ax.set_yscale("log")
    ax.set_ylim(1, 8000)
    ax.set_xticks(x)
    ax.set_xticklabels(labels, fontsize=9)
    ax.set_ylabel("Costo stimato [€ o US$]", fontsize=10)
    ax.set_title(
        "Fig. 8 — Costi totali per simulazione: CINECA vs AWS hpc7a (scala logaritmica)",
        fontsize=11
    )
    ax.legend(loc="upper left", fontsize=9)

    # Linea di riferimento budget
    ax.axhline(100, color="#555", linestyle=":", lw=1.2, label="Budget €100")
    ax.text(len(sims) - 0.4, 120, "Budget €100", fontsize=8, color="#555")

    ax.grid(axis="y", alpha=0.3, zorder=0)
    plt.tight_layout()
    plt.savefig(f"{OUT}/fig_costs.png", dpi=180)
    plt.close()


if __name__ == "__main__":
    fig_domain()
    print("  fig_domain.png OK")
    fig_scales()
    print("  fig_scales.png OK")
    fig_timestep()
    print("  fig_timestep.png OK")
    fig_cell_count()
    print("  fig_cells.png OK")
    fig_pipeline()
    print("  fig_pipeline.png OK")
    fig_spectra_expected()
    print("  fig_spectra.png OK")
    fig_hardware()
    print("  fig_hardware.png OK")
    fig_costs()
    print("  fig_costs.png OK")
    print("\nTutte le figure scritte in", OUT)
