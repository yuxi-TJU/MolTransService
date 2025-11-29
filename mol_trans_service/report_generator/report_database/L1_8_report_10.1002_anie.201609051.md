# 0\. Metadata

  - Title: Gating of Quantum Interference in Molecular Junctions by Heteroatom Substitution
  - DOI: (Omit this part)

# 1\. Literature Summary

This is an experiment + computation study. The authors investigate how heteroatom (Nitrogen) substitution in a meta-phenylene ethylene-type oligomer (m-OPE) core affects destructive quantum interference (DQI). The systems studied are the "parent" m-OPE (DQI reference) and p-OPE (constructive QI reference), along with their N-substituted "daughter" molecules (M1, M2, M3, and P). Using the Mechanically Controllable Break Junction (MCBJ) technique, they find that N-substitution can alleviate DQI and increase conductance (M2, M3) or have no effect (M1), depending on the substitution position. In contrast, the high conductance of p-OPE is unaffected by N-substitution (molecule P). Transport calculations confirm these experimental trends and rationalize them based on changes to the core transmission function and quantum interference patterns.

# 2\. Computational Objectives

The primary computational objective is to theoretically validate the experimentally observed conductance trend: $M2 > M3 > M1 \approx m-OPE$, and $p-OPE \approx P$. This is achieved by computing the zero-bias transmission spectra $T(E)$ (or "core transmission functions") for all six molecules (m-OPE, p-OPE, M1, M2, M3, P). The calculation aims to demonstrate that this conductance order is a direct result of modulating quantum interference, expecting to show a deep DQI anti-resonance (dip) in the $T(E)$ of m-OPE and M1, an alleviated or absent dip for M2 and M3, and a high, flat (constructive) transmission curve for p-OPE and P.

# 3\. Involved Systems

## System 1: m-OPE

  - Core Molecule:
      - abbreviation: m-OPE
      - full\_chemical\_name: meta-phenylene ethylene-type oligomer (with S-acetyl anchors)
      - core\_smiles: Sc1ccc(C#Cc2cccc(C#Cc3ccc(S)cc3)c2)cc1
  - Anchors:
      - anchor\_groups: ['Thiol\_SH']
  - Electrodes:
      - electrode\_material: Au
      - electrode\_surface: N/A
  - Interface:
      - interface\_geometry\_text: Thiolate (S-Au) covalent bonds to Au electrodes in an MCBJ setup.
  - Variation\_notes: "meta-linked, destructive QI reference (parent)"

## System 2: p-OPE

  - Core Molecule:
      - abbreviation: p-OPE
      - full\_chemical\_name: para-phenylene ethylene-type oligomer (with S-acetyl anchors)
      - core\_smiles: Sc1ccc(C#Cc2ccc(C#Cc3ccc(S)cc3)cc2)cc1
  - Variation\_notes: "para-linked, constructive QI reference (parent)"

## System 3: M1

  - Core Molecule:
      - abbreviation: M1
      - full\_chemical\_name: N-substituted m-OPE analog
      - core\_smiles: Sc1ccc(C#Cc2cncc(C#Cc3ccc(S)cc3)c2)cc1
  - Variation\_notes: "N-substituted daughter of m-OPE. N is meta to both linkers."

## System 4: M2

  - Core Molecule:
      - abbreviation: M2
      - full\_chemical\_name: N-substituted m-OPE analog
      - core\_smiles: Sc1ccc(C#Cc2ccnc(C#Cc3ccc(S)cc3)c2)cc1
  - Variation\_notes: "N-substituted daughter of m-OPE. N is ortho to one linker, para to the other."

## System 5: M3

  - Core Molecule:
      - abbreviation: M3
      - full\_chemical\_name: N-substituted m-OPE analog
      - core\_smiles: Sc1ccc(C#Cc2cccc(C#Cc3ccc(S)cc3)n2)cc1
  - Variation\_notes: "N-substituted daughter of m-OPE. N is ortho to both linkers."

## System 6: P

  - Core Molecule:
      - abbreviation: P
      - full\_chemical\_name: N-substituted p-OPE analog
      - core\_smiles: Sc1ccc(C#Cc2ccc(C#Cc3ccc(S)cc3)nc2)cc1
  - Variation\_notes: "N-substituted daughter of p-OPE."

# 4\. Applicability Assessment

Applicable. The core computational objective is to compare the zero-bias transmission spectra $T(E)$ of several molecular isomers to understand how heteroatom substitution (a structural effect) modulates quantum interference (DQI). This is a classic coherent transport problem well-suited for the QDHC framework. The paper's own theoretical analysis relies on identifying anti-resonance features (DQI) in the transmission function, which is a qualitative lineshape analysis. MST can reproduce the key qualitative difference—the presence or absence of the DQI anti-resonance—which is sufficient to explain the mechanism.

# 5\. Hierarchical Analysis

**Level: L1**

According to the QDHC criteria, this problem maps to the **L1 level**. The central question is how transport is governed by the molecule's *intrinsic electronic structure*, which is modified by the *substituent* (N atoms) positions. The conductance differences are explained by the resulting changes in the quantum interference pattern (the presence, absence, or shift of a DQI anti-resonance), as shown in the paper's Figure 3. This falls directly under the L1-applicable problems: "molecularly induced quantum interference" and "substituent/structural effects". The problem does not require specific interface geometries (L2) or finite-bias/level-alignment (L3) to explain the *existence* of the anti-resonance, which is the core mechanism.

# 6\. Input Preparation

This task will use the `L1_XTB` module. The GFN-xTB method is required over EHT because it can more accurately handle the changes in charge distribution and orbital structure induced by the heteroatom (N) substitutions, which is the physical origin of the QI modulation.

1.  **Structure Files**:

      - `m-OPE.xyz`: Structure file for the m-OPE molecule.
      - `p-OPE.xyz`: Structure file for the p-OPE molecule.
      - `M1.xyz`: Structure file for the M1 molecule.
      - `M2.xyz`: Structure file for the M2 molecule.
      - `M3.xyz`: Structure file for the M3 molecule.
      - `P.xyz`: Structure file for the P molecule.

2.  **Anchor Atom Indices**:

      - The user must visually inspect each `.xyz` file to find the atom indices for the two terminal Sulfur (S) atoms. Let these be `[L_idx]` and `[R_idx]`.

3.  **Key Parameters (`L1_XTB`)**:

      - `--method` (`-m`): `1` (GFN1-xTB, default).
      - `--coupling` (`-C`): `1` (Default value).
      - `--Erange`: `2` (To scan from $E_F - 2$ eV to $E_F + 2$ eV).
      - `--Enum`: `1000` (For a high-resolution spectrum to resolve the DQI dips).
      - `--charge`: `0.0` (All systems are neutral).

# 7\. Computational Workflow

## Goal:

Compute and compare the zero-bias transmission spectra $T(E)$ for m-OPE, p-OPE, M1, M2, M3, and P.

## Step 1. Create directories

Create six separate directories, one for each molecule, and place the corresponding `.xyz` file inside:

```
/m-OPE/m-OPE.xyz
/p-OPE/p-OPE.xyz
/M1/M1.xyz
/M2/M2.xyz
/M3/M3.xyz
/P/P.xyz
```

## Step 2. Run Calculation

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

**For M1:**

```bash
cd M1/
L1_XTB -f M1.xyz -L [L_idx] -R [R_idx] -C 1 --Erange 2 --Enum 1000
cd ..
```

**For M2:**

```bash
cd M2/
L1_XTB -f M2.xyz -L [L_idx] -R [R_idx] -C 1 --Erange 2 --Enum 1000
cd ..
```

**For M3:**

```bash
cd M3/
L1_XTB -f M3.xyz -L [L_idx] -R [R_idx] -C 1 --Erange 2 --Enum 1000
cd ..
```

**For P:**

```bash
cd P/
L1_XTB -f P.xyz -L [L_idx] -R [R_idx] -C 1 --Erange 2 --Enum 1000
cd ..
```

## Step 3. Post-processing and Analysis

1.  Collect all six `Transmission.txt` files generated in each directory.
2.  Use a plotting tool to plot all six transmission spectra on a single graph. The y-axis **must be logarithmic** to clearly visualize the anti-resonance dips.
3.  Compare the plots. The $T(E)$ for `m-OPE` and `M1` should show a prominent anti-resonance (dip) near the Fermi level ($E=0$). The $T(E)$ for `p-OPE` and `P` should be high and relatively flat. The $T(E)$ for `M2` and `M3` should show an alleviated or absent dip.
4.  Check the transmission value at the Fermi level ($T(E=0)$). The ordering of these values should qualitatively match the experimentally observed conductance trend: $T_{M2} > T_{M3} > T_{M1} \approx T_{m-OPE}$.