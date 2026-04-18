# Aeroacustica — Jet Impingente su Chip

Simulazione SU2 CFD del raffreddamento per jet impingement di un chip (commessa Huawei Research Center Finland, ex Nokia). Progetto UniGe, Prof. A. Bottaro.

## Obiettivo

Riprodurre al CFD il setup sperimentale Huawei per validare il solutore SU2 su getto impingente a Re=1000. Obiettivo: se i risultati sono comparabili ai dati sperimentali, seguiranno commesse di ottimizzazione geometrica per ridurre il rumore udibile (jet diretto → buon raffreddamento, alto rumore; mesh a celle cubiche → rumore basso, peggior raffreddamento).

## Caso

- Camera cilindrica D=20 mm × H=3 mm, chip sul fondo (no-slip, adiabatico)
- Tubo inlet D=1.5 mm × H=1 mm sopra la camera, centrato
- Velocità jet U=10 m/s verso il chip, Re=1000, Mach=0.029
- Outlet laterale (pressure-outlet)
- Fluido: aria standard 20 °C

## Contenuto repo

```
aeroacustica/
├── main.pdf              # Documento tecnico completo (34 pagine)
├── main.tex              # Sorgente LaTeX del paper
├── figs/                 # Figure PNG (8 figure, 180 DPI)
├── configs/              # Template SU2 v8 .cfg per ogni fase
│   ├── rans_baseline.cfg # RANS k-omega SST (L1-L3)
│   ├── urans_sst.cfg     # URANS SST (L2, Δt=1e-5 s)
│   ├── ddes_sa.cfg       # DDES Spalart-Allmaras (L3, Δt=5e-6 s)
│   └── les_wrles.cfg     # LES wall-resolved WALE (L5, Δt=5e-7 s, FW-H)
├── scripts/
│   └── make_figures.py   # Rigenera le 8 figure matplotlib
└── LICENSE               # MIT
```

## Pipeline di validazione (6 fasi)

1. **RANS k-omega SST** — mesh L1 (500k), check topologia e conservazione massa
2. **GCI Celik** — tre mesh L1/L2/L3 (0.5/1.5/3M), ordine convergenza ≥1.8
3. **URANS SST** — mesh L2 (1.5M), FFT pressione → Strouhal St≈0.3
4. **DDES SA** — mesh L3 (3M), pendenza -5/3 shear layer
5. **LES WRLES (WALE)** — mesh L5 (12M), Pope M≥0.80, Celik LES_IQ≥0.80
6. **FW-H post-processing** — propagazione far-field, confronto con misure Huawei

## Mesh progression

| Livello | N celle | Δx wall | y+_max | Uso | Hardware |
|---------|---------|---------|--------|-----|----------|
| L0 | 150k | 200 μm | ~5 | Debug | Laptop |
| L1 | 500k | 80 μm | ~2 | RANS coarse | Laptop (8-10h) |
| L2 | 1.5M | 50 μm | ~1.5 | RANS medium + URANS | Laptop (1-3 gg) |
| L3 | 3M | 30 μm | ~1 | RANS fine + DDES | Laptop border / HPC |
| L4 | 6M | 25 μm | 30 (model) | WMLES | HPC 128-256c |
| L5 | 12M | 20 μm | <0.5 | **WRLES target** | HPC 256-512c |
| L6 | 20M | 15 μm | <0.3 | WRLES check | HPC 512c+ |

## Stima costi (path minimo fino L5)

| HW | Compute cost |
|----|--------------|
| CINECA Leonardo (accademico €0.020/core-h) | ~**€1 590** |
| AWS hpc7a.96xlarge (spot ~$2.30/h) | ~**$2 740** |
| AWS hpc7a.96xlarge (on-demand $7.20/h) | ~$5 730 |

Dettagli e analisi nel `main.pdf` (sezioni 9-10).

## Ricompilare il PDF

```bash
# Dipendenze: texlive-latex-extra texlive-fonts-recommended texlive-science
#             texlive-lang-italian texlive-pictures lmodern
cd /root/aeroacustica
pdflatex main.tex && pdflatex main.tex
```

## Rigenerare le figure

```bash
python3 -m pip install matplotlib numpy
python3 scripts/make_figures.py
# Output: figs/*.png (8 file PNG, 180 DPI)
```

## Contatti

- **Autore del paper**: Prof. A. Bottaro, Università di Genova
- **Responsabile simulazione**: Sebastiano ([AreoSeb](https://github.com/AreoSeb))
- **Cliente**: Huawei Research Center, Finlandia

## Licenza

MIT — vedi [LICENSE](LICENSE).
