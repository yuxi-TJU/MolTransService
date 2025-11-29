# 0\. Metadata

  - Title: Conformation-Controlled Electron Transport in Single-Molecule Junctions Containing Oligo(phenylene ethynylene) Derivatives
  - DOI: (Omit this part)

# 1\. Literature Summary

This is an experiment + computation study. The authors investigate how the intramolecular conformation (dihedral angle) of oligo(phenylene ethynylene) (OPE) derivatives affects their single-molecule conductance. Using an STM-based break-junction (STM-BJ) technique, they study a series of five OPE molecules (OPE 1 to OPE 5) where the dihedral angle between two $\pi$-conjugated subunits is systematically controlled (from $\approx 0^\circ$ to $\approx 89^\circ$) by adding steric-hindering methyl groups. The key experimental finding is that the molecular conductance is strongly dependent on this conformation, decreasing systematically from OPE 1 to OPE 5 and showing a clear linear relationship with $\cos^2\theta$. Temperature-independent measurements suggest a coherent tunneling mechanism. These results are supported by NEGF-DFT calculations, which confirm the $\cos^2\theta$ dependence of conductance and attribute the mechanism to the torsion angle controlling the $\pi$-coupling and orbital delocalization across the molecule.

# 2\. Computational Objectives

The primary computational objective is to theoretically validate the experimental observation that the conductance of OPE molecular junctions is controlled by their intramolecular dihedral angle. The calculation aims to compute the zero-bias conductance (or transmission at $E_F$) for all five molecules (OPE 1-5) and to demonstrate that the conductance trend decreases as the dihedral angle ($\theta$) increases. The expected result is to reproduce the linear dependence of conductance on $\cos^2\theta$, confirming that the transport mechanism is governed by conformation-controlled $\pi$-conjugation.

# 3\. Involved Systems

## System 1: OPE 1

  - Core Molecule:
      - abbreviation: OPE 1
      - full\_chemical\_name: Oligo(phenylene ethynylene) derivative (planar)
      - core\_smiles: Sc1ccc(C#Cc2ccc3c(c2)Cc2cc(C#Cc4ccc(S)cc4)ccc2-3)cc1
  - Anchors:
      - anchor\_groups: ['Thiol\_SH']
  - Electrodes:
      - electrode\_material: Au
      - electrode\_surface: (111)
  - Interface:
      - interface\_geometry\_text: Thiolate (S-Au) bond to an Au(111) surface, with the sulfur atom preferring a hollow site.
  - Variation\_notes: "Planar reference molecule (dihedral angle $\approx 0^\circ$). Expected high conductance."

## System 2: OPE 2

  - Core Molecule:
      - abbreviation: OPE 2
      - full\_chemical\_name: OPE derivative (twisted)
      - core\_smiles: Sc1ccc(C#Cc2ccc(-c3ccc(C#Cc4ccc(S)cc4)cc3)cc2)cc1
  - Variation\_notes: "Twisted (dihedral angle $\approx 34^\circ$)."

## System 3: OPE 3

  - Core Molecule:
      - abbreviation: OPE 3
      - full\_chemical\_name: OPE derivative (twisted)
      - core\_smiles: Cc1cc(C#Cc2ccc(S)cc2)ccc1-c1ccc(C#Cc2ccc(S)cc2)cc1
  - Variation\_notes: "Twisted (dihedral angle $\approx 52^\circ$)."

## System 4: OPE 4

  - Core Molecule:
      - abbreviation: OPE 4
      - full\_chemical\_name: OPE derivative (twisted)
      - core\_smiles: Cc1cc(C#Cc2ccc(S)cc2)ccc1-c1ccc(C#Cc2ccc(S)cc2)cc1C
  - Variation\_notes: "Twisted (dihedral angle $\approx 79^\circ$)."

## System 5: OPE 5

  - Core Molecule:
      - abbreviation: OPE 5
      - full\_chemical\_name: OPE derivative (highly twisted)
      - core\_smiles: Cc1cc(C#Cc2ccc(S)cc2)cc(C)c1-c1c(C)cc(C#Cc2ccc(S)cc2)cc1C
  - Variation\_notes: "Highly twisted (dihedral angle $\approx 89^\circ$). Expected low conductance."

# 4\. Applicability Assessment

**Applicable.**

The core computational objective is to analyze the effect of molecular conformation (dihedral angle) on zero-bias conductance. This is a classic coherent transport problem that falls directly within the scope of the QDHC framework. According to the QDHC guide, "correlations with conformation" is a key indicator for L1, molecule-dominated transport. While the paper also presents finite-bias I-V curves (an L3-level feature), the fundamental mechanism and the $\cos^2\theta$ trend can be captured by the L1 scheme, which is the lowest level that addresses the core scientific question.

# 5\. Hierarchical Analysis

**Level: L1**

According to the QDHC criteria, this problem maps to the **L1 level**. The central question is whether transport is "governed primarily by the molecule’s intrinsic electronic structure". The paper's key finding is that the conductance is directly controlled by the intramolecular conformation (dihedral angle), which dictates the degree of $\pi$-conjugation. This falls perfectly under the L1 "Key analytical evidence": "conductance differences between isomers" (or conformers) and "correlations with conformation". The problem does not require specific interface geometries (L2) or finite-bias/level-alignment (L3) to explain the fundamental $\cos^2\theta$ conductance trend.

# 6\. Input Preparation

This task will use the `L1_EHT` module. The `L1_EHT` module is explicitly noted as suitable for "simple $\pi$-conjugated systems" and "scenarios requiring scans over many conformations," making it ideal for this problem.

1.  **Structure Files**:

      - `OPE-1.xyz`: Structure file for the planar OPE 1 molecule.
      - `OPE-2.xyz`: Structure file for the twisted OPE 2 molecule.
      - `OPE-3.xyz`: Structure file for the twisted OPE 3 molecule.
      - `OPE-4.xyz`: Structure file for the twisted OPE 4 molecule.
      - `OPE-5.xyz`: Structure file for the twisted OPE 5 molecule.

2.  **Anchor Atom Indices**:

      - The user must visually inspect each `.xyz` file to find the atom indices for the two terminal Sulfur (S) atoms. Let these be `[L_idx]` and `[R_idx]`.

3.  **Directory Structure**:

      - Create five separate directories, one for each molecule: `OPE-1/`, `OPE-2/`, `OPE-3/`, `OPE-4/`, `OPE-5/`.
      - Place the corresponding `.xyz` file inside its directory.

4.  **Key Parameters (`L1_EHT`)**:

      - `-C`, `--coupling`: `0.1` (Default value, suitable for qualitative comparison).
      - `--Erange`: `-15 -6` (Default).
      - `--Enum`: `900` (Default).

# 7\. Computational Workflow

## Goal:

Compute and compare the zero-bias transmission at the "Fermi level" (mid-gap) for the five OPE-1 to OPE-5 molecules.

## Step 1. Create directories

Create the directory structure and place the corresponding `.xyz` files as described in section 6:

```
/OPE-1/OPE-1.xyz
/OPE-2/OPE-2.xyz
/OPE-3/OPE-3.xyz
/OPE-4/OPE-4.xyz
/OPE-5/OPE-5.xyz
```

## Step 2. Run Calculation

Run the `L1_EHT` module in each of the five directories. You must replace `[L_idx]` and `[R_idx]` with the correct sulfur atom indices for that specific molecule.

**1. Calculate OPE-1:**

```bash
cd OPE-1/
# Replace [L_idx] and [R_idx] with the correct sulfur atom indices
L1_EHT -f OPE-1.xyz -L [L_idx] -R [R_idx] -C 0.1
cd ..
```

**2. Calculate OPE-2:**

```bash
cd OPE-2/
# Replace [L_idx] and [R_idx] with the correct sulfur atom indices
L1_EHT -f OPE-2.xyz -L [L_idx] -R [R_idx] -C 0.1
cd ..
```

**3. Calculate OPE-3:**

```bash
cd OPE-3/
# Replace [L_idx] and [R_idx] with the correct sulfur atom indices
L1_EHT -f OPE-3.xyz -L [L_idx] -R [R_idx] -C 0.1
cd ..
```

**4. Calculate OPE-4:**

```bash
cd OPE-4/
# Replace [L_idx] and [R_idx] with the correct sulfur atom indices
L1_EHT -f OPE-4.xyz -L [L_idx] -R [R_idx] -C 0.1
cd ..
```

**5. Calculate OPE-5:**

```bash
cd OPE-5/
# Replace [L_idx] and [R_idx] with the correct sulfur atom indices
L1_EHT -f OPE-5.xyz -L [L_idx] -R [R_idx] -C 0.1
cd ..
```

## Step 3. Post-processing and Analysis

1.  For each of the five runs, inspect the screen/log output to find the calculated HOMO and LUMO energies. Calculate the "Fermi energy" for each system as the midpoint ($E_F = (E_{HOMO} + E_{LUMO}) / 2$).
2.  Collect all five `Transmission.txt` files generated in each directory.
3.  For each system, extract the transmission value $T(E)$ from its `Transmission.txt` file at its calculated $E_F$. This value is the calculated zero-bias conductance.
4.  Create a plot of the calculated conductance (y-axis) against the known $\cos^2\theta$ values for OPE 1-5 (x-axis).
5.  Verify that the resulting plot shows a linear trend, confirming that the calculated conductance decreases systematically from OPE-1 to OPE-5.