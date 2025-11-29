# 0\. Metadata

  - Title: Exploring Electronic Characteristics of Acceptor-Donor-Acceptor-Type Molecules by Single-Molecule Charge Transport
  - DOI: (Omit this part)

# 1\. Literature Summary

This is an experiment + computation study. The authors use STM-BJ measurements and theoretical calculations to investigate the charge transport properties of a specially designed Acceptor-Donor-Acceptor (A-D-A) molecule compared to a Donor-only (D) control molecule. The key experimental finding is that the A-D-A molecule exhibits a higher conductance than the shorter D molecule, which is contrary to typical length-dependent transport. The theoretical calculations (DFT-NEGF) explain this "nonclassical" observation by showing that the acceptor units on the A-D-A molecule introduce additional, well-conjugated molecular orbitals (specifically a new LUMO) that act as efficient transport channels near the Fermi level, which are absent in the D-only molecule. A secondary experiment uses protonation to break an internal S...O noncovalent lock, exposing -S anchors on the donor core. This allows measurement of transport through the donor part, and calculations confirm the assignment of different transport pathways.

# 2\. Computational Objectives

The primary computational objective is to theoretically explain the "nonclassical" experimental result: why the longer A-D-A molecule (anchored via -CN groups) has a higher zero-bias conductance than the shorter D control molecule (anchored via -S groups). The calculation must compute and compare the zero-bias transmission spectra $T(E)$ for both systems. The expected result is to show that the $T(E)$ for A-D-A is higher near the Fermi level than for D, and to demonstrate that this is caused by new transport channels (molecular orbitals) introduced by the A-units. A secondary objective is to compare the calculated $T(E)$ of the protonated A-D-A-2 molecule through its -S anchors versus its -CN anchors to validate the experimental assignment of high and low conductance states.

# 3\. Involved Systems

## System 1: A-D-A

  - Core Molecule:
      - abbreviation: A-D-A (or A-D-A-2CN)
      - full\_chemical\_name: A-D-A-type F2Cl molecule
      - core\_smiles: N#CC(C#N)=C1C(=Cc2cc3c(s2)-c2cc4c(cc2C3)-c2cc3c(cc2C4)-c2sc(C=C4C(=O)c5cc(Cl)c(Cl)cc5C4=C(C#N)C#N)cc2C3)C(=O)c2cc(Cl)c(Cl)cc21
  - Anchors:
      - anchor\_groups: ['Cyano\_CN']
  - Electrodes:
      - electrode\_material: Au
      - electrode\_surface: N/A
  - Interface:
      - interface\_geometry\_text: A single molecule bridges two gold electrodes. The primary transport pathway is through the two terminal -CN groups located on the acceptor units.
  - Variation\_notes: "Main A-D-A system. The molecule also contains -S groups that are initially blocked by an S...O noncovalent lock."

## System 2: D

  - Core Molecule:
      - abbreviation: D (or D-2S)
      - full\_chemical\_name: Thiophene-fused fluorene donor molecule
      - core\_smiles: c1cc2c(s1)-c1cc3c(cc1C2)-c1cc2c(cc1C3)-c1sccc1C2
  - Anchors:
      - anchor\_groups: ['Thiophene Sulfur\_S']
  - Electrodes:
      - electrode\_material: Au
      - electrode\_surface: N/A
  - Interface:
      - interface\_geometry\_text: A single molecule bridges two gold electrodes via its two terminal -S (Thiophene) groups.
  - Variation\_notes: "Control system, consists of only the donor unit."

## System 3: A-D-A-2

  - Core Molecule:
      - abbreviation: A-D-A-2
      - full\_chemical\_name: Protonated A-D-A molecule (reverse conformation)
      - core\_smiles: N/A
  - Anchors:
      - anchor\_groups: ['Cyano\_CN'] or ['Thiophene Sulfur\_S']
  - Electrodes:
      - electrode\_material: Au
      - electrode\_surface: N/A
  - Interface:
      - interface\_geometry\_text: A single molecule bridges two gold electrodes. In this protonated conformer, the S...O lock is broken, allowing calculations to compare transport through the -S anchors (on the donor core) vs. the -CN anchors (on the acceptors).
  - Variation\_notes: "Protonated conformation of System 1. Carries a +1 charge."

# 4\. Applicability Assessment

**Applicable.**

The core computational objective is to compare the transmission spectra $T(E)$ of different molecules (A-D-A vs. D) and different anchoring configurations (S-anchored vs. CN-anchored) to understand how the molecular structure (i.e., the addition of A-units) creates new transport channels. This is a problem of intrinsic molecular electronic structure. While the original paper uses a full DFT-NEGF method, the fundamental mechanism (presence vs. absence of new molecular orbitals) can be qualitatively and correctly reproduced by the L1 scheme.

# 5\. Hierarchical Analysis

**Level: L1**

According to the QDHC criteria, this problem maps to the **L1 level**. The central question is how transport is "governed primarily by the molecule’s intrinsic electronic structure." The paper's core finding is that the A-D-A molecule's higher conductance is due to new molecular orbitals created by the acceptor "substituents." This is a classic L1-level problem, falling under "Effects of molecular conformation, substituents... on transport" and "correlations with... orbital character." The analysis does not depend on the specific details of the interface geometry (L2) or precise level alignment/finite bias (L3) to establish the *mechanism* of why new transport channels appear.

# 6\. Input Preparation

This task will use the `L1_XTB` module. The GFN-xTB method is more accurate than EHT and is better suited for these large, complex A-D-A molecules, especially for handling the protonated (charged) state of System 3.

1.  **Structure Files**:

      - `A-D-A.xyz`: Structure file for the neutral A-D-A molecule (System 1).
      - `D.xyz`: Structure file for the neutral D control molecule (System 2).
      - `A-D-A-2.xyz`: Structure file for the protonated A-D-A-2 molecule (System 3).

2.  **Anchor Atom Indices**:

      - **For `A-D-A.xyz`**: The user must find the atom indices for the two terminal **Cyanide (CN)** anchors. Let these be `[L_CN_idx]` and `[R_CN_idx]`.
      - **For `D.xyz`**: The user must find the atom indices for the two terminal **Sulfur (S)** anchors. Let these be `[L_S_idx]` and `[R_S_idx]`.
      - **For `A-D-A-2.xyz`**: The user must find two sets of indices:
          - The two terminal **Sulfur (S)** anchors: `[L_S2_idx]` and `[R_S2_idx]`.
          - The two terminal **Cyanide (CN)** anchors: `[L_CN2_idx]` and `[R_CN2_idx]`.

3.  **Directory Structure**:

      - Create four separate directories for the four calculations:
          - `A-D-A_CN/` (containing `A-D-A.xyz`)
          - `D_S/` (containing `D.xyz`)
          - `A-D-A-2_S/` (containing `A-D-A-2.xyz`)
          - `A-D-A-2_CN/` (containing `A-D-A-2.xyz`)

4.  **Key Parameters (`L1_XTB`)**:

      - `-m`, `--method`: `1` (GFN1-xTB).
      - `-C`, `--coupling`: `1` (A reasonable default value).
      - `--Erange`: `2` (To scan $\pm 2$ eV around $E_F$).
      - `--Enum`: `1000` (For high resolution).
      - `--charge`:
          - `0.0` for `A-D-A_CN` and `D_S`.
          - `1.0` for `A-D-A-2_S` and `A-D-A-2_CN` (to account for the added proton).

# 7\. Computational Workflow

## Goal:

Compute and compare the zero-bias transmission spectra $T(E)$ for:

1.  The A-D-A molecule (via -CN anchors) versus the D control (via -S anchors).
2.  The protonated A-D-A-2 molecule via its -S anchors versus its -CN anchors.

## Step 1. Create directories

Create the directory structure and place the corresponding `.xyz` files as described in section 6:

```
/A-D-A_CN/A-D-A.xyz
/D_S/D.xyz
/A-D-A-2_S/A-D-A-2.xyz
/A-D-A-2_CN/A-D-A-2.xyz
```

## Step 2. Run Calculation

Run four separate `L1_XTB` calculations.

**1. Calculate A-D-A (CN-anchored):**

```bash
cd A-D-A_CN/
# Replace [L_CN_idx] and [R_CN_idx] with the correct Cyanide anchor indices
L1_XTB -f A-D-A.xyz -L [L_CN_idx] -R [R_CN_idx] -C 1 --Erange 2 --Enum 1000
cd ..
```

**2. Calculate D (S-anchored):**

```bash
cd D_S/
# Replace [L_S_idx] and [R_S_idx] with the correct Sulfur anchor indices
L1_XTB -f D.xyz -L [L_S_idx] -R [R_S_idx] -C 1 --Erange 2 --Enum 1000
cd ..
```

**3. Calculate A-D-A-2 (S-anchored, protonated):**

```bash
cd A-D-A-2_S/
# Replace [L_S2_idx] and [R_S2_idx] with the correct Sulfur anchor indices
L1_XTB -f A-D-A-2.xyz -L [L_S2_idx] -R [R_S2_idx] -C 1 --Erange 2 --Enum 1000 --charge 1.0
cd ..
```

**4. Calculate A-D-A-2 (CN-anchored, protonated):**

```bash
cd A-D-A-2_CN/
# Replace [L_CN2_idx] and [R_CN2_idx] with the correct Cyanide anchor indices
L1_XTB -f A-D-A-2.xyz -L [L_CN2_idx] -R [R_CN2_idx] -C 1 --Erange 2 --Enum 1000 --charge 1.0
cd ..
```

## Step 3. Post-processing and Analysis

1.  Collect the four `Transmission.txt` files from each directory.
2.  **Plot 1 (Main Objective):** Use a plotting tool to overlay the spectra from `A-D-A_CN/Transmission.txt` and `D_S/Transmission.txt`. Use a logarithmic y-axis. Compare the transmission values near the $E_F$ (mid-gap) to confirm if A-D-A has a higher transmission than D.
3.  **Plot 2 (Secondary Objective):** Overlay the spectra from `A-D-A-2_S/Transmission.txt` and `A-D-A-2_CN/Transmission.txt`. Use a logarithmic y-axis. Compare the transmission values to confirm if the S-anchored pathway is more conductive.