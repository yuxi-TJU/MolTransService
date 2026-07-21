# Case 2 OPA/OPM Transport Outputs

This directory contains compact L2 transport data for the six OPA/OPM extended-molecule systems and the selected L3 interfacial-orbital outputs for OPA3 and OPM3. The retained files map directly to the reported comparison between `sp` alkynyl and `sp3` methylene contacts.

## Directory layout

- `data/`: processed L2/L3 spectra, conductance summaries, attenuation fits, and MPSH contribution tables.
- `figures/`: static PNG transmission plots.
- `orbital_data/`: primary Molden outputs for the representative OPA3 and OPM3 interfacial analyses.
- `scripts/`: a portable plotting script that reads the included CSV files through relative paths.

## L2 six-system transport comparison

- Spectra: `data/l2_transmission_spectra.csv`
- Conductance summary: `data/l2_conductance_summary.csv`
- Attenuation fits: `data/l2_attenuation_fits.csv`
- Plot: `figures/l2_transmission_spectra.png`
- Script: `scripts/plot_transport_spectra.py`

The spectra table contains OPA2, OPA3, OPA4, OPM2, OPM3, and OPM4 on the common absolute-energy grid used by the EM+Cluster calculations. The summary retains the reference-energy transmission values without the machine-specific source paths present in the original analysis table. The data reproduce the higher OPM conductance and exponential length attenuation described in the text.

## L3 OPA3/OPM3 interfacial diagnosis

- Spectra: `data/l3_transmission_spectra.csv`
- Near-Fermi and selected-peak values: `data/l3_transport_summary.csv`
- Reported MPSH weights: `data/l3_mpsh_contributions.csv`
- OPA3 primary outputs:
  - `orbital_data/opa3/MPSH.molden`
  - `orbital_data/opa3/EC_Abs_-0.98829.molden`
  - `orbital_data/opa3/mpsh_eigenvalues.txt`
- OPM3 primary outputs:
  - `orbital_data/opm3/MPSH.molden`
  - `orbital_data/opm3/EC_Abs_-0.52047.molden`
  - `orbital_data/opm3/mpsh_eigenvalues.txt`

The Molden files contain the orbital and absolute-eigenchannel data needed to inspect the contrasting directional/lobed OPA3 interface state and the more diffuse OPM3 interface state. The static rendered orbital panel is not duplicated here; the underlying numerical visualization files are retained instead.

## Reproduction

From this directory, run:

```bash
python scripts/plot_transport_spectra.py
```

Large raw matrices and intermediate calculation files are intentionally excluded. No SVG files, calculation logs, machine-specific absolute paths, credentials, or private metadata are included.
