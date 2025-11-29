# 0\. Metadata

  - Title: Understanding Role of Parallel Pathways via In Situ Switching of Quantum Interference in Molecular Tunneling Junctions
  - DOI: (Omit this part)

# 1\. Literature Summary

This is an experiment + computation study. The authors investigate how charge transport in molecular junctions can be modulated by switching one of two parallel intramolecular pathways. The study focuses on a series of molecules (BT, BPh, FH, and FO) where transport is influenced by quantum interference (QI). The key system, FO (Fluorenone), contains parallel linear- and cross-conjugated pathways, with the latter inducing destructive quantum interference (DQI) and low conductance. Using STM-BJ and EGaIn measurements, the authors show that protonating FO to FOH (forming a trivalent carbocation) effectively "switches off" the DQI by altering the bond topology of the cross-conjugated path. This switch results in a significant conductance increase. DFT-NEGF transport calculations support this finding, showing a characteristic DQI anti-resonance in the transmission spectrum of FO which is absent in the spectrum of FOH, leading to higher transmission at the Fermi level for FOH.

# 2\. Computational Objectives

The primary computational objective is to theoretically validate the experimentally observed conductance trends ($BT > FOH > FH > BPh > FO$) by calculating the zero-bias transmission spectra $T(E)$ for all five molecules. The calculation aims to demonstrate that these conductance differences, particularly the low conductance of FO and the subsequent increase for FOH, are a direct result of modulating destructive quantum interference (DQI). The expected result is to find a DQI-induced anti-resonance (dip) in the $T(E)$ of FO, which is absent in the other molecules, and to show that this dip disappears upon protonation to FOH.

# 3\. Involved Systems

## System 1: BT

  - Core Molecule:
      - abbreviation: BT
      - full\_chemical\_name: Bithiophene (core)
      - core\_smiles: Sc1ccc(C#Cc2ccc(-c3ccc(C#Cc4ccc(S)cc4)s3)s2)cc1
  - Anchors:
      - anchor\_groups: ['Thiol\_SH']
  - Electrodes:
      - electrode\_material: Au
      - electrode\_surface: N/A
  - Interface:
      - interface\_geometry\_text: Thiol anchoring groups forming covalent bonds to Au electrodes. The computational model in the paper uses a full junction with semi-infinite periodic bulk electrodes.
  - Variation\_notes: "Linearly-conjugated reference system."

## System 2: BPh

  - Core Molecule:
      - abbreviation: BPh
      - full\_chemical\_name: Biphenyl (core)
      - core\_smiles: Sc1ccc(C#Cc2ccc(-c3ccc(C#Cc4ccc(S)cc4)cc3)cc2)cc1
  - Variation\_notes: "Linearly-conjugated reference, subject to twisting in single-molecule junctions."

## System 3: FH

  - Core Molecule:
      - abbreviation: FH
      - full\_chemical\_name: Fluorene (core)
      - core\_smiles: Sc1ccc(C#Cc2ccc3c(c2)Cc2cc(C#Cc4ccc(S)cc4)ccc2-3)cc1
  - Variation\_notes: "Contains parallel linear- and non-conjugated pathways."

## System 4: FO

  - Core Molecule:
      - abbreviation: FO
      - full\_chemical\_name: Fluorenone (core)
      - core\_smiles: O=C1c2cc(C#Cc3ccc(S)cc3)ccc2-c2ccc(C#Cc3ccc(S)cc3)cc21
  - Variation\_notes: "Contains parallel linear- and cross-conjugated pathways, expected to show DQI."

## System 5: FOH

  - Core Molecule:
      - abbreviation: FOH
      - full\_chemical\_name: Protonated Fluorenone (forms a trivalent carbocation)
      - core\_smiles: [OH+]=C1c2cc(C#Cc3ccc(S)cc3)ccc2-c2ccc(C#Cc3ccc(S)cc3)cc21
  - Variation\_notes: "Protonated (cationic) form of FO, expected to have DQI suppressed."

# 4\. Applicability Assessment

**Applicable.**

The core computational objective is to compare the zero-bias transmission spectra $T(E)$ of several molecular isomers and one charged species (FOH) to understand how bond topology and substituents modulate destructive quantum interference (DQI). This is a classic coherent transport problem well-suited for the QDHC framework. The QDHC guide explicitly lists "Quantum Interference effects (DQI)" and "Effects of molecular... substituents" as L1-level problems. While the original paper used a full NEGF-DFT calculation (an L3-level method) to get an aligned $T(E)$ spectrum, the fundamental *mechanism* (the existence or absence of the DQI anti-resonance) is an intrinsic property of the molecule's electronic structure and can be captured by the L1 scheme.

# 5\. Hierarchical Analysis

**Level: L1**

According to the QDHC criteria, this problem maps to the **L1 level**. The central question is how transport is governed by the molecule's *intrinsic electronic structure*, which is modified by the bond topology (e.g., cross-conjugation in FO) and substituents (protonation of FO to FOH). The conductance differences are explained by the presence or absence of a DQI anti-resonance in the $T(E)$ spectrum, which falls directly under the L1-applicable problem: "Quantum Interference effects (DQI), e.g., comparing para- vs. meta-linkages". The comparison between FO and FOH is analogous to a substituent effect, also listed under L1. The problem does not require specific interface geometries (L2) or finite-bias (L3) to explain the *existence* of the anti-resonance, which is the core mechanism.

# 6\. Input Preparation

This task will use the `L1_XTB` module. The GFN-xTB method is required over EHT because it can more accurately handle the complex electronic structures and, crucially, the non-neutral (charged) state of the FOH cation.

1.  **Structure Files**:

      - `BT.xyz`: Structure file for the BT molecule.
      - `BPh.xyz`: Structure file for the BPh molecule.
      - `FH.xyz`: Structure file for the FH molecule.
      - `FO.xyz`: Structure file for the FO molecule.
      - `FOH.xyz`: Structure file for the FOH molecule (protonated FO, which is a cation).

2.  **Anchor Atom Indices**:

      - The user must visually inspect each `.xyz` file to find the atom indices for the two terminal Sulfur (S) atoms. Let these be `[L_idx]` and `[R_idx]`.

3.  **Key Parameters (`L1_XTB`)**:

      - **Method (`-m`)**: `1` (GFN1-xTB, default).
      - **Coupling (`-C`)**: `1` (Default value).
      - **Energy Range (`--Erange`)**: `2.0` (To scan from $E_F - 2$ eV to $E_F + 2$ eV, matching the paper's approximate range).
      - **Energy Points (`--Enum`)**: `1000` (For a high-resolution spectrum to resolve sharp DQI dips).
      - **Charge (`--charge`)**:
          - `0.0` for BT, BPh, FH, and FO.
          - `1.0` for FOH (as it is a protonated cation).

# 7\. Computational Workflow

## Goal:

Compute and compare the zero-bias transmission spectra $T(E)$ for BT, BPh, FH, FO, and FOH.

## Step 1. Create directories

Create five separate directories, one for each molecule, and place the corresponding `.xyz` file inside:

```
/BT/BT.xyz
/BPh/BPh.xyz
/FH/FH.xyz
/FO/FO.xyz
/FOH/FOH.xyz
```

## Step 2. Run Calculation

For each system, navigate into its directory and run the `L1_XTB` module. You must replace `[L_idx]` and `[R_idx]` with the correct sulfur atom indices for that specific molecule.

**For BT, BPh, FH, FO (Neutral):**
(Repeat for each of the four neutral molecules)

```bash
# Example for FO:
cd FO/
L1_XTB -f FO.xyz -L [L_idx] -R [R_idx] -C 1 --Erange 2.0 --Enum 1000 --charge 0.0
cd ..
```

**For FOH (Cation):**

```bash
cd FOH/
L1_XTB -f FOH.xyz -L [L_idx] -R [R_idx] -C 1 --Erange 2.0 --Enum 1000 --charge 1.0
cd ..
```

## Step 3. Post-processing and Analysis

1.  Collect all five `Transmission.txt` files generated in each directory.
2.  Use a plotting tool (e.g., Python/Matplotlib) to plot all five transmission spectra on a single graph. The y-axis **must be logarithmic** to clearly visualize the anti-resonance dips.
3.  Compare the plots. The $T(E)$ for `FO` should show a prominent anti-resonance (dip) near the Fermi level ($E=0$), which should be absent in the `FOH` spectrum.
4.  Check the transmission value at the Fermi level ($T(E=0)$). The ordering of these values should be compared to qualitatively match the experimentally observed conductance trend: $T_{BT} > T_{FOH} > T_{FH} > T_{BPh} > T_{FO}$.