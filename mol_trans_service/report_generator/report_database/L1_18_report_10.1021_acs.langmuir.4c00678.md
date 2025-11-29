# 0\. Metadata

  - Title: Effects of Connectivity Isomerization on Electron Transport Through Thiophene Heterocyclic Molecular Junction
  - DOI: (Omit this part)

# 1\. Literature Summary

This is an experiment + computation study. The authors investigate how the "connectivity isomerization" (i.e., different substitution positions) of a central thiophene (TP) ring affects single-molecule conductance. The systems studied are four isomers (2,3-TP-BT, 2,4-TP-BT, 2,5-TP-BT, and 3,4-TP-BT) where a TP core is connected to two dihydrobenzo[b]thiophene (BT) anchoring groups via ethynyl spacers. Using the STM-BJ technique, they find a \~12-fold change in conductance, with the order: 2,4-TP-BT \< 3,4-TP-BT \< 2,3-TP-BT \< 2,5-TP-BT. DFT-NEGF transport calculations are used to explain this trend. The key finding is that the 2,5-TP-BT isomer (para-like) has high conductance due to high electron delocalization, while the 2,4-TP-BT isomer has the lowest conductance due to strong destructive quantum interference (DQI) near the Fermi level.

# 2\. Computational Objectives

The primary computational objective is to theoretically validate the experimentally observed conductance trend: $2,4-TP-BT < 3,4-TP-BT < 2,3-TP-BT < 2,5-TP-BT$. This is achieved by computing the zero-bias transmission spectra $T(E)$ for all four isomers. The calculation aims to demonstrate that this conductance order is a direct result of modulating quantum interference, expecting to show a deep DQI anti-resonance (dip) in the $T(E)$ of 2,4-TP-BT (explaining its low conductance) and a high, constructive-like transmission for 2,5-TP-BT.

# 3\. Involved Systems

## System 1: 2,5-TP-BT

  - Core Molecule:
      - abbreviation: 2,5-TP-BT
      - full\_chemical\_name: 2,5-bis((2,3-dihydrobenzo[b]thiophen-5-yl)ethynyl)thiophene
      - core\_smiles: C(#Cc1ccc(C#Cc2ccc3c(c2)CCS3)s1)c1ccc2c(c1)CCS2
  - Anchors:
      - anchor\_groups: ['Benzothiophene\_S']
  - Electrodes:
      - electrode\_material: Au
      - electrode\_surface: (111)
  - Interface:
      - interface\_geometry\_text: The S-atom of the terminal dihydrobenzo[b]thiophene (BT) group bonds to Au electrodes.
  - Variation\_notes: "para-like 2,5-substitution. Constructive QI reference, highest conductance."

## System 2: 2,4-TP-BT

  - Core Molecule:
      - abbreviation: 2,4-TP-BT
      - full\_chemical\_name: 2,4-bis((2,3-dihydrobenzo[b]thiophen-5-yl)ethynyl)thiophene
      - core\_smiles: C(#Cc1ccc2c(c1)CCS2)c1csc(C#Cc2ccc3c(c2)CCS3)c1
  - Variation\_notes: "meta-like 2,4-substitution. Strong Destructive QI (DQI), lowest conductance."

## System 3: 2,3-TP-BT

  - Core Molecule:
      - abbreviation: 2,3-TP-BT
      - full\_chemical\_name: 2,3-bis((2,3-dihydrobenzo[b]thiophen-5-yl)ethynyl)thiophene
      - core\_smiles: C(#Cc1cscc1C#Cc1ccc2c(c1)CCS2)c1ccc2c(c1)CCS2
  - Variation\_notes: "Asymmetric 2,3-substitution. Intermediate conductance."

## System 4: 3,4-TP-BT

  - Core Molecule:
      - abbreviation: 3,4-TP-BT
      - full\_chemical\_name: 3,4-bis((2,3-dihydrobenzo[b]thiophen-5-yl)ethynyl)thiophene
      - core\_smiles: C(#Cc1ccsc1C#Cc1ccc2c(c1)CCS2)c1ccc2c(c1)CCS2
  - Variation\_notes: "Symmetric 3,4-substitution. Intermediate conductance, second lowest."

# 4\. Applicability Assessment

**Applicable.**

The core computational objective is to compare the zero-bias transmission spectra $T(E)$ of several molecular isomers to understand how "connectivity isomerization" (a structural/substituent effect) modulates quantum interference (DQI). This is a classic coherent transport problem. The QDHC guide explicitly lists "Quantum Interference effects (DQI), e.g., comparing para- vs. meta-linkages" and "Effects of molecular... substituents... on transport" as L1-level problems. While the paper mentions a Fermi level shift to reconcile quantitative values (an L3-level concept), the *fundamental mechanism* (the existence of the DQI anti-resonance in 2,4-TP-BT vs. its absence in 2,5-TP-BT) is an intrinsic property of the molecule's electronic structure. MST at the L1 level can reproduce this key qualitative difference in the $T(E)$ lineshapes.

# 5\. Hierarchical Analysis

**Level: L1**

According to the QDHC criteria, this problem maps to the **L1 level**. The central question is how transport is governed by the molecule's *intrinsic electronic structure*, which is modified by the *substituent* positions (connectivity). The large conductance differences are explained entirely by the resulting changes in molecular orbital symmetry and the quantum interference state (DQI vs. CQI). This falls directly under the L1-applicable problems: "Quantum Interference effects (DQI)" and "Effects of molecular... substituents... on transport". The problem does not require specific interface geometries (L2) or precise level alignment (L3) to explain the *existence* and *location* of the anti-resonance relative to the molecular orbitals, which is the core mechanism.

# 6\. Input Preparation

This task will use the `L1_XTB` module. The GFN-xTB method is required over EHT because it can more accurately handle the changes in charge distribution and orbital structure induced by the heteroatom (S) and the different connectivity patterns, which is the physical origin of the QI modulation.

1.  **Structure Files**:

      - `2,5-TP-BT.xyz`: Structure file for the 2,5-isomer.
      - `2,4-TP-BT.xyz`: Structure file for the 2,4-isomer.
      - `2,3-TP-BT.xyz`: Structure file for the 2,3-isomer.
      - `3,4-TP-BT.xyz`: Structure file for the 3,4-isomer.

2.  **Anchor Atom Indices**:

      - The user must visually inspect each `.xyz` file to find the atom indices for the two terminal Sulfur (S) atoms (one on each BT anchor group). Let these be `[L_idx]` and `[R_idx]`.

3.  **Key Parameters (`L1_XTB`)**:

      - **Method (`-m`)**: `1` (for GFN1-xTB, default).
      - **Coupling (`-C`)**: `1` (Default value).
      - **Energy Range (`--Erange`)**: `2` (To scan from $E_F - 2$ eV to $E_F + 2$ eV, matching the paper's Figure 4b).
      - **Energy Points (`--Enum`)**: `1000` (For a high-resolution spectrum to resolve the sharp DQI dip).
      - **Charge (`--charge`)**: `0.0` (All systems are neutral).

# 7\. Computational Workflow

## Goal:

Compute and compare the zero-bias transmission spectra $T(E)$ for the 2,5-TP-BT, 2,4-TP-BT, 2,3-TP-BT, and 3,4-TP-BT isomers.

## Step 1. Create directories

Create four separate directories, one for each molecule, and place the corresponding `.xyz` file inside:

```
/2,5-TP-BT/2,5-TP-BT.xyz
/2,4-TP-BT/2,4-TP-BT.xyz
/2,3-TP-BT/2,3-TP-BT.xyz
/3,4-TP-BT/3,4-TP-BT.xyz
```

## Step 2. Run Calculation

For each system, navigate into its directory and run the `L1_XTB` module. You must replace `[L_idx]` and `[R_idx]` with the correct sulfur atom indices for that specific molecule.

**For 2,5-TP-BT:**

```bash
cd 2,5-TP-BT/
L1_XTB -f 2,5-TP-BT.xyz -L [L_idx] -R [R_idx] -C 1 --Erange 2 --Enum 1000
cd ..
```

**For 2,4-TP-BT:**

```bash
cd 2,4-TP-BT/
L1_XTB -f 2,4-TP-BT.xyz -L [L_idx] -R [R_idx] -C 1 --Erange 2 --Enum 1000
cd ..
```

**For 2,3-TP-BT:**

```bash
cd 2,3-TP-BT/
L1_XTB -f 2,3-TP-BT.xyz -L [L_idx] -R [R_idx] -C 1 --Erange 2 --Enum 1000
cd ..
```

**For 3,4-TP-BT:**

```bash
cd 3,4-TP-BT/
L1_XTB -f 3,4-TP-BT.xyz -L [L_idx] -R [R_idx] -C 1 --Erange 2 --Enum 1000
cd ..
```

## Step 3. Post-processing and Analysis

1.  Collect all four `Transmission.txt` files generated in each directory.
2.  Use a plotting tool to plot all four transmission spectra on a single graph. The y-axis **must be logarithmic** to clearly visualize the anti-resonance dips.
3.  Compare the plots. The $T(E)$ for `2,4-TP-BT` should show a prominent anti-resonance (dip) near the Fermi level ($E=0$). The $T(E)$ for `2,5-TP-BT` should be high and relatively flat, lacking this dip. The $T(E)$ for `2,3-TP-BT` and `3,4-TP-BT` should be intermediate.
4.  Check the transmission value at the Fermi level ($T(E=0)$). The ordering of these values should qualitatively match the experimentally observed conductance trend: $T_{2,4-TP-BT} < T_{3,4-TP-BT} < T_{2,3-TP-BT} < T_{2,5-TP-BT}$.