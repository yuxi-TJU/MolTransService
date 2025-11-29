# 0\. Metadata

  - Title: Electric Field-Induced Assembly in Single-Stacking Terphenyl Junctions
  - DOI: (Omit this part)

# 1\. Literature Summary

This is an experiment + computation study. The authors use the scanning tunneling microscope break junction (STM-BJ) technique to investigate charge transport through terphenyl (S1) junctions. They find that the junctions exhibit two conductance states: a high-conductance (H) state corresponding to a single, through-bond molecule, and a low-conductance (L) state corresponding to a $\pi$-stacked dimer. The key experimental finding is that increasing the applied bias voltage (and thus the electric field) increases the probability of forming the low-conductance "Stacking" junction. Combined density functional theory (DFT) calculations explain this by showing that the electric field planarizes the molecule (reduces the dihedral angle between phenyl rings) and significantly increases the binding energy of the $\pi$-stacked dimer, making its formation more favorable. Zero-bias transmission calculations confirm that the single-molecule conformations ("Original" and "Twist") are high-conductance, while the "Stacking" dimer is low-conductance.

# 2\. Computational Objectives

The primary computational transport objective is to theoretically validate the assignment of the experimentally observed high- and low-conductance states. The calculation aims to compute and compare the zero-bias transmission spectra $T(E)$ for three distinct, static conformations:

1.  "Original": The relaxed single-molecule monomer with its natural dihedral angle (\~35°).
2.  "Twist": The field-planarized single-molecule monomer with a reduced dihedral angle (\~24°).
3.  "Stacking": The field-stabilized $\pi$-stacked dimer.

The expected result is to show that the "Original" and "Twist" monomer systems have high transmission near the Fermi level (corresponding to the H state), while the "Stacking" dimer system has significantly suppressed transmission (corresponding to the L state).

# 3\. Involved Systems

## System 1: Original (S1 Monomer)

  - Core Molecule:
      - abbreviation: S1 (Original)
      - full\_chemical\_name: 4,4''-bis(methylthio)-1,1':4',1''-terphenyl
      - core\_smiles: CSc1ccc(-c2ccc(-c3ccc(SC)cc3)cc2)cc1
  - Anchors:
      - anchor\_groups: ['Thioether\_SMe']
  - Electrodes:
      - electrode\_material: Au
      - electrode\_surface: N/A
  - Interface:
      - interface\_geometry\_text: A single molecule bridges two gold electrodes via terminal methylthio groups. Transport is through-bond.
  - Variation\_notes: "High-conductance reference system. Represents the relaxed monomer conformation at zero field, with a \~35° dihedral angle."

## System 2: Twist (S1 Monomer)

  - Core Molecule:
      - abbreviation: S1 (Twist)
      - full\_chemical\_name: 4,4''-bis(methylthio)-1,1':4',1''-terphenyl
      - core\_smiles: N/A
  - Variation\_notes: "High-conductance system. Represents the field-planarized monomer conformation, with a reduced \~24° dihedral angle."

## System 3: Stacking (S1 Dimer)

  - Core Molecule:
      - abbreviation: S1 (Stacking)
      - full\_chemical\_name: $\pi$-stacked dimer of 4,4''-bis(methylthio)-1,1':4',1''-terphenyl
      - core\_smiles: N/A
  - Anchors:
      - anchor\_groups: ['Thioether\_SMe']
  - Electrodes:
      - electrode\_material: Au
      - electrode\_surface: N/A
  - Interface:
      - interface\_geometry\_text: A dimer of two S1 molecules forms a $\pi$-stacked junction. Each molecule is anchored to one electrode via its terminal methylthio group. Transport is through-space.
  - Variation\_notes: "Low-conductance system. Represents the field-induced stacked dimer configuration."

# 4\. Applicability Assessment

**Applicable.**

The paper's core transport objective is to compare the zero-bias transmission spectra of three different molecular conformations ("Original", "Twist", and "Stacking"). This is a classic "conformation-dependent transport" problem. Although the *reason* for these conformational differences is an external electric field (a finite-bias effect, potentially L3), the *transport calculation itself* (Fig 3d) is a simple zero-bias $T(E)$ comparison between static structures. This is a problem dominated by the intrinsic electronic structure of the molecule and its assembly (monomer vs. dimer) and is therefore well-suited for the L1 level. MST can reproduce the qualitative $T(E)$ differences between the high-conductance monomers and the low-conductance dimer.

# 5\. Hierarchical Analysis

**Level: L1**

According to the QDHC guide, this problem maps to the **L1 level**. The central computational question is how transport is governed by the molecule's *intrinsic electronic structure*, which is altered by its *conformation* (dihedral angle) and *assembly* (monomer vs. dimer). This falls directly under the L1 criterion: "Effects of molecular conformation... on transport". The calculation aims to correlate these distinct structures with high or low conductance, which is an L1-level insight. The problem does not require explicit interface geometry (L2) or finite-bias/level-alignment simulation (L3) to achieve its core objective.

# 6\. Input Preparation

This task will use the `L1_XTB` module, as GFN-xTB is better suited than EHT for capturing the electronic structure differences from ring torsion (conjugation) and the through-space interactions in the $\pi$-stacked dimer.

1.  **Structure Files**:

      - `Original.xyz`: Molecular structure file for the S1 monomer with a \~35° dihedral angle.
      - `Twist.xyz`: Molecular structure file for the S1 monomer with a \~24° dihedral angle.
      - `Stacking.xyz`: Molecular structure file for the $\pi$-stacked S1 dimer.

2.  **Anchor Atom Indices**:

      - The user must visually inspect each of the three `.xyz` files to find the atom indices for the two terminal Sulfur (S) atoms that serve as the left and right anchors. Let these be `[L_idx]` and `[R_idx]` for each file.

3.  **Key Parameters (`L1_XTB`)**:

      - **Method (`-m`)**: `1` (for GFN1-xTB, default).
      - **Coupling (`-C`)**: `1` (A reasonable default value).
      - **Energy Range (`--Erange`)**: `3` (To scan from $E_F - 3$ eV to $E_F + 3$ eV, capturing the main frontier orbitals).
      - **Energy Points (`--Enum`)**: `1000` (For a high-resolution spectrum).

# 7\. Computational Workflow

## Goal:

Compute and compare the zero-bias transmission spectra $T(E)$ for the "Original" (monomer), "Twist" (monomer), and "Stacking" (dimer) S1 conformations.

## Step 1. Create directories

Create three separate directories and place the corresponding structure files inside:

```
/Original/Original.xyz
/Twist/Twist.xyz
/Stacking/Stacking.xyz
```

## Step 2. Transport calculation

For each system, navigate into its directory and run the `L1_XTB` module. You must replace `[L_idx]` and `[R_idx]` with the correct sulfur atom indices identified for *that specific file*.

**For Original:**

```bash
cd Original/
L1_XTB -f Original.xyz -L [L_idx] -R [R_idx] -C 1 --Erange 3 --Enum 1000
cd ..
```

**For Twist:**

```bash
cd Twist/
L1_XTB -f Twist.xyz -L [L_idx] -R [R_idx] -C 1 --Erange 3 --Enum 1000
cd ..
```

**For Stacking:**

```bash
cd Stacking/
L1_XTB -f Stacking.xyz -L [L_idx] -R [R_idx] -C 1 --Erange 3 --Enum 1000
cd ..
```

## Step 3. Post-processing and Analysis

1.  Collect the three `Transmission.txt` files (one from each directory).
2.  Use a plotting tool (e.g., Python/Matplotlib) to plot all three transmission spectra on a single graph. Use a logarithmic scale for the y-axis to match the paper's presentation (Fig 3d).
3.  Compare the plots. The spectra for "Original" and "Twist" should show high transmission values near the Fermi energy (which L1\_XTB defines as the mid-gap). The spectrum for "Stacking" should show significantly lower transmission, confirming the experimental assignment of the H and L states.