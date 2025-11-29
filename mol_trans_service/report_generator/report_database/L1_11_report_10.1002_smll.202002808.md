# 0\. Metadata

  - Title: Nonadditive Transport in Multi-Channel Single-Molecule Circuits
  - DOI: (Omit this part)

# 1\. Literature Summary

This is an experiment + computation study. The authors investigate how quantum interference (QI) affects conductance in multi-channel molecular circuits, specifically challenging the classical additivity of Kirchhoff's laws. The systems are based on a diphenylacetylene backbone, using amino (H2N) and pyridine (N) anchors in various meta (M) and para (P) configurations. The study compares two-terminal molecules (P-P, M-P, P-M, M-M) with three-terminal, multi-channel molecules (MP-P and MP-M) where two input anchors are connected to one electrode. Using the MCBJ technique, they find that combining a constructive (P-P) and a destructive (M-P) channel in the MP-P molecule results in nonadditive transport: the total conductance is *significantly lower* than the sum of its parts. Conversely, combining two destructive channels (P-M and M-M) in the MP-M molecule *does* result in additive conductance, closely matching the sum. DFT-NEGF calculations of the transmission spectra successfully reproduce and explain these additive and nonadditive trends as a result of inter-pathway quantum interference.

# 2\. Computational Objectives

The primary computational objective is to theoretically validate the experimentally observed additivity and nonadditivity in multi-channel transport. This is achieved by computing and comparing the zero-bias transmission spectra $T(E)$ for all six molecules. The calculation aims to demonstrate:

1.  **Nonadditivity (Destructive):** The transmission at the Fermi level for the MP-P system is *not* the sum of $T_{P-P}$ and $T_{M-P}$, but is suppressed, confirming inter-channel destructive interference.
2.  **Additivity:** The transmission at the Fermi level for the MP-M system *is* approximately the sum of $T_{P-M}$ and $T_{M-M}$, confirming that two destructive channels combine additively.

# 3\. Involved Systems

## System 1: P-P

  - Core Molecule:
      - abbreviation: P-P
      - full\_chemical\_name: para,para-dipyridyl diphenylacetylene
      - core\_smiles: C(#Cc1ccncc1)c1ccncc1
  - Anchors:
      - anchor\_groups: ['Pyridine\_N']
  - Electrodes:
      - electrode\_material: Au
      - electrode\_surface: N/A (MCBJ)
  - Interface:
      - interface\_geometry\_text: Pyridine-N atoms serve as anchors to the Au electrodes at both para-positions.
  - Variation\_notes: "Two-terminal reference, para-para linkage (Constructive QI)"

## System 2: M-P

  - Core Molecule:
      - abbreviation: M-P
      - full\_chemical\_name: meta-amino, para-pyridine diphenylacetylene
      - core\_smiles: Nc1cccc(C#Cc2ccncc2)c1
  - Variation\_notes: "Two-terminal reference, meta-para linkage (Destructive QI)"

## System 3: P-M

  - Core Molecule:
      - abbreviation: P-M
      - full\_chemical\_name: para,meta-pyridine diphenylacetylene
      - core\_smiles: C(#Cc1cccnc1)c1ccncc1
  - Variation\_notes: "Two-terminal reference, para-meta linkage (Destructive QI)"

## System 4: M-M

  - Core Molecule:
      - abbreviation: M-M
      - full\_chemical\_name: meta-amino, meta-pyridine diphenylacetylene
      - core\_smiles: Nc1cccc(C#Cc2cccnc2)c1
  - Variation\_notes: "Two-terminal reference, meta-meta linkage (Destructive QI)"

## System 5: MP-P

  - Core Molecule:
      - abbreviation: MP-P
      - full\_chemical\_name: para,para-pyridine, meta-amino diphenylacetylene
      - core\_smiles: Nc1cc(C#Cc2ccncc2)ccn1
  - Variation\_notes: "Three-terminal, multi-channel system. Combines P-P and M-P channels. Expected to show nonadditive destructive interference."

## System 6: MP-M

  - Core Molecule:
      - abbreviation: MP-M
      - full\_chemical\_name: para,meta-pyridine, meta-amino diphenylacetylene
      - core\_smiles: Nc1cc(C#Cc2cccnc2)ccn1
  - Variation\_notes: "Three-terminal, multi-channel system. Combines P-M and M-M channels. Expected to show additive transport."

# 4\. Applicability Assessment

**Applicable.**

The core computational objective is to compare the zero-bias transmission spectra $T(E)$ of several molecular isomers and multi-terminal configurations to understand how quantum interference (DQI vs. CQI) from different substituent positions combines. This is a classic coherent transport problem. The QDHC guide explicitly lists "Quantum Interference effects (DQI), e.g., comparing para- vs. meta-linkages" and "Effects of molecular... substituents... on transport" as L1-applicable problems. While the original paper used full DFT-NEGF (ATK), MST can reproduce the key qualitative differences in the $T(E)$ spectra and the resulting additive/nonadditive conductance trends, which is sufficient to explain the mechanism.

# 5\. Hierarchical Analysis

**Level: L1**

According to the QDHC criteria, this problem maps to the **L1 level**. The central question is how transport is governed by the molecule's *intrinsic electronic structure*, which is modified by the *substituent positions* (meta vs. para) and the *combination of pathways* (two-terminal vs. three-terminal). The observed nonadditivity is explained entirely by the interference between different transport pathways defined by the molecular orbitals. This falls directly under the L1-applicable problems: "Quantum Interference effects (DQI), e.g., comparing para- vs. meta-linkages" and "Effects of molecular... substituents... on transport". The problem does not require specific interface geometries (L2) or finite-bias/level-alignment (L3) to explain the core mechanism of pathway interference.

# 6\. Input Preparation

This task will use the `L1_XTB` module. The GFN-xTB method is required over EHT because it can more accurately handle the changes in charge distribution and orbital structure induced by the different heteroatom (N) anchor types (amino vs. pyridine) and their linkage positions, which is the physical origin of the QI effects.

1.  **Structure Files**:

      - `P-P.xyz`: Structure file for the P-P molecule.
      - `M-P.xyz`: Structure file for the M-P molecule.
      - `P-M.xyz`: Structure file for the P-M molecule.
      - `M-M.xyz`: Structure file for the M-M molecule.
      - `MP-P.xyz`: Structure file for the MP-P molecule.
      - `MP-M.xyz`: Structure file for the MP-M molecule.

2.  **Anchor Atom Indices**:

      - The user must visually inspect each `.xyz` file to find the atom indices for the anchoring Nitrogen (N) atoms.
	  - **For P-P, P-M**: Find the two N index of the pyridine ring (`[L_idx_pyri_N]`) and (`[R_idx_pyri_N]`).
	  - **For M-P, M-M**: Find the N index of the amino group (`[L_idx_amino_N]`) and the N index of the pyridine ring (`[R_idx_pyri_N]`).
      - **For MP-P, MP-M**: Find the indices for the two N atoms on the left (`[L_idx_pyri_N]`, `[L_idx_amino_N]`) and the N index on the right (`[R_idx_pyri_N]`).

3.  **Key Parameters (`L1_XTB`)**:

      - **Method (`-m`)**: `1` (for GFN1-xTB, default).
      - **Coupling (`-C`)**: `1` (Default value).
      - **Energy Range (`--Erange`)**: `2` (To scan from $E_F - 2$ eV to $E_F + 2$ eV, matching the paper's Fig. 3 range).
      - **Energy Points (`--Enum`)**: `1000` (For a high-resolution spectrum).
      - **Charge (`--charge`)**: `0.0` (All systems are neutral).

# 7\. Computational Workflow

## Goal:

Compute and compare the zero-bias transmission spectra $T(E)$ for all six systems (P-P, M-P, MP-P, P-M, M-M, MP-M) to analyze their additive/nonadditive transport properties.

## Step 1. Create directories

Create six separate directories, one for each molecule, and place the corresponding `.xyz` file inside:

```
/P-P/P-P.xyz
/M-P/M-P.xyz
/P-M/P-M.xyz
/M-M/M-M.xyz
/MP-P/MP-P.xyz
/MP-M/MP-M.xyz
```

## Step 2. Transport calculation

For each system, navigate into its directory and run the `L1_XTB` module. You must replace the bracketed `[idx]` placeholders with the correct nitrogen atom indices for that specific molecule.

**For P-P:**

```bash
cd P-P/
L1_XTB -f P-P.xyz -L [L_idx_pyri_N] -R [R_idx_pyri_N] -C 1 --Erange 2 --Enum 1000
cd ..
```

**For M-P:**

```bash
cd M-P/
L1_XTB -f M-P.xyz -L [L_idx_amino_N] -R [R_idx_pyri_N] -C 1 --Erange 2 --Enum 1000
cd ..
```

**For P-M:**

```bash
cd P-M/
L1_XTB -f P-M.xyz -L [L_idx_pyri_N] -R [R_idx_pyri_N] -C 1 --Erange 2 --Enum 1000
cd ..
```

**For M-M:**

```bash
cd M-M/
L1_XTB -f M-M.xyz -L [L_idx_amino_N] -R [R_idx_pyri_N] -C 1 --Erange 2 --Enum 1000
cd ..
```

**For MP-P (Multi-channel input):**

```bash
cd MP-P/
L1_XTB -f MP-P.xyz -L [L_idx_pyri_N] [L_idx_amino_N] -R [R_idx_pyri_N] -C 1 --Erange 2 --Enum 1000
cd ..
```

**For MP-M (Multi-channel input):**

```bash
cd MP-M/
L1_XTB -f MP-M.xyz -L [L_idx_pyri_N] [L_idx_amino_N] -R [R_idx_pyri_N] -C 1 --Erange 2 --Enum 1000
cd ..
```

## Step 3. Post-processing and Analysis

1.  Collect all six `Transmission.txt` files generated in each directory.
2.  Use a plotting tool (e.g., Python/Matplotlib) to create two separate plots, mimicking Figure 3 from the paper. The y-axis **must be logarithmic**.
3.  **Plot 1 (Constructive + Destructive):** Plot the transmission spectra for `P-P`, `M-P`, and `MP-P` on a single graph.
4.  **Plot 2 (Destructive + Destructive):** Plot the transmission spectra for `P-M`, `M-M`, and `MP-M` on a single graph.
5.  Extract the transmission value at the Fermi level ($T(E=0)$) for all six systems.
6.  **Analyze Plot 1:** Check for nonadditivity. Verify that $T_{MP-P}(E=0)$ is significantly *less* than $T_{P-P}(E=0) + T_{M-P}(E=0)$.
7.  **Analyze Plot 2:** Check for additivity. Verify that $T_{MP-M}(E=0)$ is *approximately equal* to $T_{P-M}(E=0) + T_{M-M}(E=0)$.