# Case 1 Conformational Transport Outputs

This directory contains the compact processed output for the biphenyl-diamine conformational scan. The retained grid and plots correspond to the reported 19 × 19 scan: 19 values of the inter-ring torsion angle `theta` from 0° to 90° and 19 values of the amine torsion angle `phi` from 0° to 180°, for 361 conformations in total.

## Directory layout

- `data/`: the processed transmission matrix used in the reported conformational maps.
- `figures/`: static PNG plots corresponding to the reported heatmap and selected fixed-`phi` trends.
- `scripts/`: a portable plotting script that reads the included CSV through paths relative to this directory.

## Data and output mapping

### Two-dimensional conformational map

- Data: `data/transmission_grid.csv`
- Plot: `figures/transmission_heatmap_log10.png`
- Script: `scripts/plot_conformational_transport.py`

Rows of the wide CSV are `phi` values and columns are `theta` values. Each cell is the processed transmission value used in the reported plots. The post-processing averaged `T(E)` over the interval centered at -9.05 eV with a half-width of 0.10 eV. The resulting map contains the low-transmission band near `phi = 60°` described in the text.

### Fixed-`phi` torsion trends

- Data: `data/transmission_grid.csv`
- Plot: `figures/transmission_vs_cos2_theta.png`
- Script: `scripts/plot_conformational_transport.py`

The selected slices are `phi = 0°, 30°, 60°, 120°, 150°, 180°`. They are plotted against `cos²(theta)` and use the same matrix as the heatmap.

## Related structure inputs

The initial structure and the script used to generate the 361-point torsion grid are retained in `../input_structures/`. The scan uses `theta = 0°` to `90°` in 5° steps and `phi = 0°` to `180°` in 10° steps.

## Reproduction

From this directory, run:

```bash
python scripts/plot_conformational_transport.py
```

The large collection of per-conformation calculation directories and raw transmission spectra is intentionally excluded. No SVG files, machine-specific paths, credentials, or private metadata are included.
