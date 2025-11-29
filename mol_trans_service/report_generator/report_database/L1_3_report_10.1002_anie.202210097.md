# 0\. Metadata

  - Title: Fano Resonance in Single-Molecule Junctions
  - DOI: (Omit this part)

# 1\. Literature Summary

This is an experiment + computation study. The authors investigate the emergence of Fano resonance in single-molecule junctions using an electrochemically gated scanning tunneling microscope break junction (EC-STM-BJ) technique. The system studied is a para-carbazole molecule. The key experimental finding is that the deprotonated anion form of the molecule (Para-N-e) exhibits a distinct Fano lineshape in its conductance-gate voltage curve, characterized by a sharp transition from resonance (peak) to antiresonance (dip). This system also shows asymmetric I-V characteristics and negative differential resistance (NDR) at specific gate potentials. In contrast, the neutral, pristine molecule (Para-N-H) shows a simple, monotonic conductance trend. The primary finding from DFT-NEGF calculations is that this Fano resonance is caused by the quantum interference between a localized Highest Occupied Molecular Orbital (HOMO), which acts as a discrete state induced by the negative charge on the nitrogen atom, and the delocalized Lowest Unoccupied Molecular Orbital (LUMO), which acts as a continuous state.

# 2\. Computational Objectives

The primary computational objective is to theoretically validate the experimental observation that Fano resonance appears in the anionic para-carbazole (Para-N-e) but not in its neutral counterpart (Para-N-H). The calculation aims to compute and compare the zero-bias transmission spectra $T(E)$ for both the neutral and anionic charge states. The expected result is to show a sharp Fano resonance (a characteristic peak-and-dip lineshape) in the $T(E)$ of Para-N-e, originating from the interference between a localized (discrete) HOMO and a delocalized (continuous) LUMO, and to confirm the absence of this feature in the $T(E)$ of Para-N-H.

# 3\. Involved Systems

## System 1: Para-N-e

  - Core Molecule:
	  - abbreviation: Para-N-e
      - full\_chemical_name: para-carbazole anion
      - core\_smiles: CSc1ccc(-c2ccc3c(c2)[n-]c2cc(-c4ccc(SC)cc4)ccc23)cc1
  - Anchors:
      - anchor\_groups: ['Methylthio\_SCH3'] 
  - Electrodes:
      - electrode\_material: Au
      - electrode\_surface: N/A
  - Interface:
      - interface\_geometry\_text: The molecule is connected to gold electrodes via its two terminal sulfur atoms, likely forming thiolate (S-Au) bonds. The central carbazole unit is deprotonated, carrying a negative charge on the nitrogen atom.
  - Variation\_notes: "Anionic (deprotonated) state. Expected to show Fano resonance."

## System 2: Para-N-H

  - Core Molecule:
	  - abbreviation: Para-N-H
      - full\_chemical_name: para-carbazole neutral
      - core\_smiles: CSc1ccc(-c2ccc3c(c2)[nH]c2cc(-c4ccc(SC)cc4)ccc23)cc1
  - Variation\_notes: "Neutral (pristine) state. Control system, expected to show no Fano resonance."

# 4\. Applicability Assessment

**Applicable.**

The core computational objective is to compare the zero-bias transmission spectra $T(E)$ of the molecule in two different charge states (neutral vs. anion) to identify the Fano resonance. The QDHC guide explicitly lists "Fano resonances" and "substituent/structural effects" (which includes charge state changes) as L1-level problems. While the paper also discusses finite-bias (NDR) and thermoelectric (Seebeck) effects, which are out-of-scope for L1 or MST in general, the *origin* of the Fano resonance itself is an intrinsic, molecule-dominated (L1) phenomenon. MST can reproduce the qualitative difference in the $T(E)$ lineshapes between the two systems.

# 5\. Hierarchical Analysis

**Level: L1**

According to the QDHC criteria, this problem maps to the **L1 level**. The central question is how transport is governed by the molecule's *intrinsic electronic structure*, which is altered by its *charge state*. The Fano resonance is explicitly shown to arise from the interference between a localized discrete orbital (HOMO) and a delocalized continuous orbital (LUMO) within the molecule itself (Figure 1). This is a classic example of "Fano resonances" and "Effects of molecular... charge state on transport," both of which are L1-applicable problems. The specific geometry of the electrode interface (L2) or precise alignment with the electrode Fermi level (L3) are not required to explain the *existence* of the Fano lineshape, which is the core computational objective.

# 6\. Input Preparation

This task will use the `L1_XTB` module. The GFN-xTB method is required over EHT because it can properly handle non-neutral (charged) systems and is more reliable for capturing the electronic structure differences (orbital localization) induced by the negative charge.

1.  **Structure Files**:

      - `Para-N-H.xyz`: Structure file for the neutral para-carbazole molecule.
      - `Para-N-e.xyz`: Structure file for the anionic para-carbazole molecule. (by removing the hydrogen atom attached to the central nitrogen atom in the Para-N-H.xyz molecule.).

2.  **Anchor Atom Indices**:

      - The user must visually inspect the `.xyz` file to find the atom indices for the two terminal Sulfur (S) atoms. Let these be `[L_idx]` and `[R_idx]`.

3.  **Key Parameters (`L1_XTB`)**:

      - `--method` (`-m`): `1` (GFN1-xTB, default) or `2` (GFN2-xTB).
      - `--coupling` (`-C`): `0.2`.
      - `--Erange`: `2` (To scan from $E_F - 2$ eV to $E_F + 2$ eV).
      - `--Enum`: `1000` (A high number of points is needed to resolve the sharp Fano dip).

# 7\. Computational Workflow

## Goal:

Compute and compare the zero-bias transmission spectra $T(E)$ for the neutral (Para-N-H) and anionic (Para-N-e) systems.

## Step 1. Create directories

Create two separate directories for the calculations and place the structure files inside:

```
/Para-N-H/Para-N-H.xyz
/Para-N-e/Para-N-e.xyz
```

## Step 2. Run Calculation

Run the `L1_XTB` module in each directory, setting the appropriate charge. You must replace `[L_idx]` and `[R_idx]` with the correct sulfur atom indices.

**1. Calculate Neutral (Para-N-H):**

```bash
cd Para-N-H/
# Replace [L_idx] and [R_idx] with the correct sulfur atom indices
L1_XTB -f Para-N-H.xyz -L [L_idx] -R [R_idx] -C 0.2 --Erange 2 --Enum 1000
cd ..
```

**2. Calculate Anion (Para-N-e):**

```bash
cd Para-N-e/
# Replace [L_idx] and [R_idx] with the correct sulfur atom indices
L1_XTB -f Para-N-e.xyz -L [L_idx] -R [R_idx] -C 0.2 --Erange 2 --Enum 1000 
cd ..
```

## Step 3. Post-processing and Analysis

1.  Collect the two `Transmission.txt` files generated in each directory (`Para-N-H/Transmission.txt` and `Para-N-e/Transmission.txt`).
2.  Use a plotting tool to plot both transmission spectra on a single graph. The y-axis should be logarithmic to clearly visualize the resonance and anti-resonance.
3.  Compare the two plots. The `Para-N-e` spectrum should exhibit a sharp Fano resonance (a peak followed by a deep dip) near the Fermi level, which should be absent in the smoother `Para-N-H` spectrum.