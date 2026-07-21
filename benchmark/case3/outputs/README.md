# Case 3 Rectification Benchmark Data

This directory contains compact processed data, analysis scripts, static plots, and interactive visualizations for the Case 3 molecular-rectification study.

Large raw calculation outputs are intentionally excluded, including `Field_*` directories, complete `Transmission.txt` and `voltage_current.txt` files, and generated `.out`, `.hsd`, `.bin`, and `.dat` files. The processed tables retain the numerical values needed to inspect and reproduce the included plots.

## Directory layout

- `data/`: processed numerical data and clustering summaries.
- `figures/`: static PNG plots.
- `interactive/`: browser-based three-dimensional visualizations.
- `scripts/`: data-processing, clustering, and plotting scripts.

## Data and output mapping

### Current-voltage comparison

- Data: `data/iv_curves_two_junctions.csv`
- Plot: `figures/iv_curves_two_junctions.png`
- Script: `scripts/plot_iv_curves.py`

The table contains the calculated current-voltage curves for the symmetric tetraphenyl control and the asymmetric DPDP junction.

### Conformation-dependent rectification clustering

- Data: `data/transport_metrics_with_rr_clusters.csv`
- Summary: `data/rectification_cluster_summary.txt`
- Interactive views:
  - `interactive/rectification_clusters_k2_envelope_interactive.html`
  - `interactive/rectification_clusters_k4_envelope_interactive.html`
- Scripts:
  - `scripts/cluster_rectification_regions.py`
  - `scripts/generate_interactive_rectification_html_from_csv.py`

The transport table contains 343 conformations defined by the three torsion angles `A_deg`, `B_deg`, and `C_deg`. It reports zero-bias transmission, currents at ±1.718 V, rectification ratios, and the k=2 and k=4 cluster assignments. Calculation-file references are stored as relative paths rather than machine-specific absolute paths.

Running the clustering script also produces the following static views:

- `figures/rectification_clusters_k2.png`
- `figures/rectification_clusters_k4.png`
- `figures/rectification_clusters_k4_envelope.png`

### Rectification-current performance

- Data: `data/transport_metrics_with_rr_clusters.csv`
- Plot: `figures/rr_vs_current_by_cluster.png`
- Script: `scripts/plot_rr_vs_current_by_cluster.py`

The current magnitude is defined as the larger absolute current under positive or negative bias at 1.718 V. Colors identify the k=4 rectification clusters.

### Bias-dependent transmission spectra

- Selected-point metrics: `data/selected_points_metrics.csv`
- Processed spectra: `data/selected_transmission_spectra.csv`
- Plot: `figures/selected_rectification_transmission_spectra.png`
- Script: `scripts/plot_selected_transmission_spectra.py`

The processed spectra table contains three bias conditions for each of four representative conformations. The plotting script reads these compact CSV files directly and does not require the excluded raw `Transmission.txt` files.

### Interactive zero-bias transmission map

- Data: `data/transport_metrics_with_rr_clusters.csv`
- Interactive view: `interactive/transmission_tef0_interactive.html`
