# 0\. Metadata

  - Title: Modulating Quantum Interference Between Destructive and Constructive States in Double N-Substituted Single Molecule Junctions
  - DOI: (Omit this part)

# 1\. Literature Summary

This is an experiment + computation study. The authors investigate how double nitrogen (N) substitution within a meta-phenylene ethylene oligomer (m-OPE) backbone can modulate its charge transport properties, specifically by tuning quantum interference (QI). The systems studied include the m-OPE (destructive QI) and p-OPE (constructive QI) reference molecules, along with three double N-substituted m-OPE analogs: 2,6-2N, 3,6-2N, and 2,4-2N. Using the STM-BJ technique, they find that the conductance can be tuned by over an order of magnitude. Notably, 2,6-2N exhibits even *lower* conductance than m-OPE (enhanced destructive QI), while 2,4-2N shows high conductance approaching that of p-OPE (a switch to constructive QI). The NEGF-DFT transport calculations confirm these findings, showing that the transmission spectra $T(E)$ for m-OPE and 2,6-2N possess a sharp anti-resonance (dip) near the Fermi level, characteristic of DQI, while this feature is absent in the high-transmission spectra of p-OPE and 2,4-2N.

# 2\. Computational Objectives

The primary computational objective is to theoretically validate the experimentally observed conductance trend: $2,6-2N < m-OPE < 3,6-2N < 2,4-2N < p-OPE$. This is achieved by computing the zero-bias transmission spectra $T(E)$ for all five molecules. The calculation aims to demonstrate that this conductance order is a direct result of modulating quantum interference, expecting to show a deep DQI anti-resonance (dip) in the $T(E)$ of m-OPE and 2,6-2N, an alleviated or absent dip for 3,6-2N, and a high, flat (constructive) transmission curve for 2,4-2N and p-OPE.

# 3\. Involved Systems

## System 1: m-OPE

  - Core Molecule:
      - abbreviation: m-OPE
      - full\_chemical\_name: meta-phenylene ethylene oligomer (with acetyl-protected thiol groups)
      - core\_smiles: Sc1ccc(C#Cc2cccc(C#Cc3ccc(S)cc3)c2)cc1
  - Anchors:
      - anchor\_groups: ['Thiol\_SH']
  - Electrodes:
      - electrode\_material: Au
      - electrode\_surface: (111)
  - Interface:
      - interface\_geometry\_text: Thiolate (S-Au) bond to Au electrodes. The paper's theory section specifies a "trimer cluster shaped Au electrodes" with the sulfur atom at the "top" site for the S-S junction configuration.
  - Variation\_notes: "meta-linked, destructive QI reference"

## System 2: p-OPE

  - Core Molecule:
      - abbreviation: p-OPE
      - full\_chemical\_name: para-phenylene ethylene oligomer (with acetyl-protected thiol groups)
      - core\_smiles: Sc1ccc(C#Cc2ccc(C#Cc3ccc(S)cc3)cc2)cc1
  - Variation\_notes: "para-linked, constructive QI reference"

## System 3: 2,6-2N

  - Core Molecule:
      - abbreviation: 2,6-2N
      - full\_chemical\_name: m-OPE analog with N-substitution at 2 and 6 positions
      - core\_smiles: Sc1ccc(C#Cc2ccnc(C#Cc3ccc(S)cc3)n2)cc1
  - Variation\_notes: "Double N-substitution, enhanced DQI"

## System 4: 3,6-2N

  - Core Molecule:
      - abbreviation: 3,6-2N
      - full\_chemical\_name: m-OPE analog with N-substitution at 3 and 6 positions
      - core\_smiles: Sc1ccc(C#Cc2cncc(C#Cc3ccc(S)cc3)n2)cc1
  - Variation\_notes: "Double N-substitution, alleviated DQI"

## System 5: 2,4-2N

  - Core Molecule:
      - abbreviation: 2,4-2N
      - full\_chemical\_name: m-OPE analog with N-substitution at 2 and 4 positions
      - core\_smiles: NSc1ccc(C#Cc2cc(C#Cc3ccc(S)cc3)ncn2)cc1
  - Variation\_notes: "Double N-substitution, switched to constructive QI"

# 4\. Applicability Assessment

**Applicable.**

The core computational objective is to compare the zero-bias transmission spectra $T(E)$ of several molecular isomers to understand how heteroatom substitution (a structural effect) modulates quantum interference (DQI). This is a classic coherent transport problem well-suited for the QDHC framework. The paper's own theoretical analysis relies on standard NEGF-DFT to identify the anti-resonance features, which is a qualitative lineshape analysis that does not depend on out-of-scope effects like precise level alignment (DFT+$\Sigma$) or inelastic transport. MST can reproduce the key qualitative difference—the presence or absence of the DQI anti-resonance—which is sufficient to explain the mechanism.

# 5\. Hierarchical Analysis

**Level: L1**

According to the QDHC criteria, this problem maps to the **L1 level**. The central question is how transport is governed by the molecule's *intrinsic electronic structure*, which is modified by the *substituent* (N atoms) positions. The conductance differences are explained entirely by the resulting changes in molecular orbital symmetry and the "magic ratio", which dictates the quantum interference state (DQI vs. CQI). This falls directly under the L1-applicable problems: "Quantum Interference effects (DQI), e.g., comparing para- vs. meta-linkages" and "Effects of molecular... substituents... on transport". The problem does not require specific interface geometries (L2) or finite-bias/level-alignment (L3) to explain the *existence* of the anti-resonance, which is the core mechanism.

# 6\. Input Preparation

This task will use the `L1_XTB` module. The GFN-xTB method is required over EHT because it can more accurately handle the changes in charge distribution and orbital structure induced by the heteroatom (N) substitutions, which is the physical origin of the QI modulation.

1.  **Structure Files**:

      - `m-OPE.xyz`: Structure file for the m-OPE molecule.
      - `p-OPE.xyz`: Structure file for the p-OPE molecule.
      - `2,6-2N.xyz`: Structure file for the 2,6-2N molecule.
      - `3,6-2N.xyz`: Structure file for the 3,6-2N molecule.
      - `2,4-2N.xyz`: Structure file for the 2,4-2N molecule.

2.  **Anchor Atom Indices**:

      - The user must visually inspect each `.xyz` file to find the atom indices for the two terminal Sulfur (S) atoms. Let these be `[L_idx]` and `[R_idx]`.

3.  **Key Parameters (`L1_XTB`)**:

      - **Method (`-m`)**: `1` (for GFN1-xTB, default).
      - **Coupling (`-C`)**: `1` (Default value).
      - **Energy Range (`--Erange`)**: `2` (To scan from $E_F - 2$ eV to $E_F + 2$ eV, sufficient to cover the HOMO-LUMO gap shown in the paper's Fig. 4).
      - **Energy Points (`--Enum`)**: `1000` (For a high-resolution spectrum to resolve the sharp DQI dips).
      - **Charge (`--charge`)**: `0.0` (All systems are neutral).

# 7\. Computational Workflow

## Goal:

Compute and compare the zero-bias transmission spectra $T(E)$ for p-OPE, m-OPE, 2,6-2N, 3,6-2N, and 2,4-2N.

## Step 1. Create directories

Create five separate directories, one for each molecule, and place the corresponding `.xyz` file inside:

```
/m-OPE/m-OPE.xyz
/p-OPE/p-OPE.xyz
/2,6-2N/2,6-2N.xyz
/3,6-2N/3,6-2N.xyz
/2,4-2N/2,4-2N.xyz
```

## Step 2. Transport calculation

For each system, navigate into its directory and run the `L1_XTB` module. You must replace `[L_idx]` and `[R_idx]` with the correct sulfur atom indices for that specific molecule.

**For m-OPE:**

```bash
cd m-OPE/
L1_XTB -f m-OPE.xyz -L [L_idx] -R [R_idx] -C 1 --Erange 2 --Enum 1000
cd ..
```

**For p-OPE:**

```bash
cd p-OPE/
L1_XTB -f p-OPE.xyz -L [L_idx] -R [R_idx] -C 1 --Erange 2 --Enum 1000
cd ..
```

**For 2,6-2N:**

```bash
cd 2,6-2N/
L1_XTB -f 2,6-2N.xyz -L [L_idx] -R [R_idx] -C 1 --Erange 2 --Enum 1000
cd ..
```

**For 3,6-2N:**

```bash
cd 3,6-2N/
L1_XTB -f 3,6-2N.xyz -L [L_idx] -R [R_idx] -C 1 --Erange 2 --Enum 1000
cd ..
```

**For 2,4-2N:**

```bash
cd 2,4-2N/
L1_XTB -f 2,4-2N.xyz -L [L_idx] -R [R_idx] -C 1 --Erange 2 --Enum 1000
cd ..
```

## Step 3. Post-processing and Analysis

1.  Collect all five `Transmission.txt` files generated in each directory.
2.  Use a plotting tool (e.g., Python/Matplotlib) to plot all five transmission spectra on a single graph. The y-axis **must be logarithmic** to clearly visualize the anti-resonance dips.
3.  Compare the plots. The $T(E)$ for `m-OPE` and `2,6-2N` should show a prominent anti-resonance (dip) near the Fermi level ($E=0$). The $T(E)$ for `p-OPE` and `2,4-2N` should be high and relatively flat, lacking this dip. The $T(E)$ for `3,6-2N` should be intermediate.
4.  Check the transmission value at the Fermi level ($T(E=0)$). The ordering of these values should qualitatively match the experimentally observed conductance trend: $T_{2,6-2N} < T_{m-OPE} < T_{3,6-2N} < T_{2,4-2N} < T_{p-OPE}$.