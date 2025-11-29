# 0\. Metadata

  - Title: Transport Modulation Through Electronegativity Gating in Multiple Nitrogenous Circuits
  - DOI: (Omit this part)

# 1\. Literature Summary

This is an experiment + computation study. The authors investigate how tuning the electronegativity of nitrogen atoms affects charge transport in single-molecule junctions. They designed and synthesized two series of molecules: one with a single nitrogenous conductive channel (Sg) and one with dual channels (Db). The electronegativity of the nitrogen atoms was modulated by either replacing a methyl group with hydrogen (Me vs. H) or by protonating the nitrogen with acid (e.g., Sg-Me -\> Sg-Me+). Using the STM-BJ technique, they found that conductance is suppressed as the nitrogen's electronegativity becomes more negative (i.e., upon H-substitution or protonation). This suppression effect is significantly more pronounced in the dual-channel (Db) series than in the single-channel (Sg) series. Theoretical calculations, including NEGF-DFT and frontier molecular orbital (FMO) analysis, confirm this trend, attributing the conductance suppression to the increased localization of the frontier orbitals caused by the change in electronegativity.

# 2\. Computational Objectives

The primary computational objective is to theoretically validate the experimentally observed conductance trends for both the Sg and Db series. This involves demonstrating that conductance decreases as the nitrogen atom's electronegativity is reduced (chemically modulated from Me to H, and from neutral to protonated cation). The calculation aims to compute and compare the zero-bias transmission spectra $T(E)$ for all eight molecules (Sg-Me, Sg-Me+, Sg-H, Sg-H+, Db-Me, Db-Me+, Db-H, Db-H+). The expected result is to show that the transmission at the Fermi level, $T(E_F)$, follows the experimentally observed order, and to confirm that the conductance suppression is more significant in the Db series than in the Sg series.

# 3\. Involved Systems

(All systems share the same Anchors, Electrodes, and Interface)

## System 1: Sg-Me

  - Core Molecule:
      - abbreviation: Sg-Me
      - full\_chemical\_name: Single-channel compound, methyl-substituted
      - core\_smiles: N/A
  - Anchors:
      - anchor\_groups: ['Methylthio\_SCH3']
  - Electrodes:
      - electrode\_material: Au
      - electrode\_surface: N/A
  - Interface:
      - interface\_geometry\_text: Molecule anchored via terminal methylthio (SMe) groups to Au electrodes in an STM-BJ configuration.
  - Variation\_notes: "Single-channel, neutral, methyl-substituted."

## System 2: Sg-Me+

  - Core Molecule:
      - abbreviation: Sg-Me+
      - full\_chemical\_name: Single-channel compound, methyl-substituted, protonated
      - core\_smiles: N/A
  - Variation\_notes: "Single-channel, protonated cation (+1 charge), methyl-substituted."

## System 3: Sg-H

  - Core Molecule:
      - abbreviation: Sg-H
      - full\_chemical\_name: Single-channel compound, hydrogen-substituted
      - core\_smiles: N/A
  - Variation\_notes: "Single-channel, neutral, hydrogen-substituted."

## System 4: Sg-H+

  - Core Molecule:
      - abbreviation: Sg-H+
      - full\_chemical\_name: Single-channel compound, hydrogen-substituted, protonated
      - core\_smiles: N/A
  - Variation\_notes: "Single-channel, protonated cation (+1 charge), hydrogen-substituted."

## System 5: Db-Me

  - Core Molecule:
      - abbreviation: Db-Me
      - full\_chemical\_name: Dual-channel compound, methyl-substituted
      - core\_smiles: N/A
  - Variation\_notes: "Dual-channel, neutral, methyl-substituted."

## System 6: Db-Me+

  - Core Molecule:
      - abbreviation: Db-Me+
      - full\_chemical\_name: Dual-channel compound, methyl-substituted, protonated
      - core\_smiles: N/A
  - Variation\_notes: "Dual-channel, protonated cation (+1 charge), methyl-substituted."

## System 7: Db-H

  - Core Molecule:
      - abbreviation: Db-H
      - full\_chemical\_name: Dual-channel compound, hydrogen-substituted
      - core\_smiles: N/A
  - Variation\_notes: "Dual-channel, neutral, hydrogen-substituted."

## System 8: Db-H+

  - Core Molecule:
      - abbreviation: Db-H+
      - full\_chemical\_name: Dual-channel compound, hydrogen-substituted, protonated
      - core\_smiles: N/A
  - Variation\_notes: "Dual-channel, protonated cation (+1 charge), hydrogen-substituted."

# 4\. Applicability Assessment

**Applicable.**

The core computational objective is to compare the zero-bias transmission spectra $T(E)$ of several molecules with different substituents (Me vs. H) and in different charge states (neutral vs. protonated cation). This is a classic coherent transport problem. The paper's own theoretical explanation (Fig 4) relies heavily on the analysis of frontier orbitals of the *isolated molecules* and how their localization changes, which is an intrinsic molecular property. This falls directly within the scope of the QDHC framework. The NEGF-DFT calculations in the paper (Fig 5) are used to confirm the relative trend of $T(E_F)$, which can be qualitatively reproduced by the L1 scheme.

# 5\. Hierarchical Analysis

**Level: L1**

According to the QDHC criteria, this problem maps to the **L1 level**. The central question is how transport is governed by the molecule's *intrinsic electronic structure*, which is being modified by *substituents* (Me vs. H) and *charge state* (protonation). This falls directly under the L1-applicable problems: "Effects of molecular... substituents, or charge state on transport" (QDHC Guide, Sec 3.1; MST Manual, L1 Overview). The paper's primary explanation is based on the localization of isolated-molecule frontier orbitals, a property inherent to the molecule. The goal is to compare the relative transmission values at $E_F$ for the eight systems, which does not require the explicit interface modeling of L2 or the precise level alignment of L3.

# 6\. Input Preparation

This task will use the `L1_XTB` module. The GFN-xTB method is required over EHT because it can properly handle non-neutral (charged) systems and is more reliable for capturing the electronic structure differences induced by the different substituents and charge states.

1.  **Structure Files**:

      - `Sg-Me.xyz`: Structure file for the neutral Sg-Me molecule.
      - `Sg-Me+.xyz`: Structure file for the protonated Sg-Me+ molecule.
      - `Sg-H.xyz`: Structure file for the neutral Sg-H molecule.
      - `Sg-H+.xyz`: Structure file for the protonated Sg-H+ molecule.
      - `Db-Me.xyz`: Structure file for the neutral Db-Me molecule.
      - `Db-Me+.xyz`: Structure file for the protonated Db-Me+ molecule.
      - `Db-H.xyz`: Structure file for the neutral Db-H molecule.
      - `Db-H+.xyz`: Structure file for the protonated Db-H+ molecule.

2.  **Anchor Atom Indices**:

      - The user must visually inspect each `.xyz` file to find the atom indices for the two terminal Sulfur (S) atoms (from the -SMe groups). Let these be `[L_idx]` and `[R_idx]`.

3.  **Key Parameters (`L1_XTB`)**:

      - **Method (`-m`)**: `1` (GFN1-xTB, default) or `2` (GFN2-xTB).
      - **Coupling (`-C`)**: `1` (Default value).
      - **Energy Range (`--Erange`)**: `3` (To scan from $E_F - 3$ eV to $E_F + 3$ eV, covering the main frontier orbitals shown in the paper's Fig. 5).
      - **Energy Points (`--Enum`)**: `1000` (For a high-resolution spectrum).
      - **Charge (`--charge`)**: This is the most critical parameter.
          * `0.0` for Sg-Me, Sg-H, Db-Me, Db-H.
          * `1.0` for Sg-Me+, Sg-H+, Db-Me+, Db-H+.

# 7\. Computational Workflow

## Goal:

Compute and compare the zero-bias transmission spectra $T(E)$ for all eight molecules (Sg-Me, Sg-Me+, Sg-H, Sg-H+, Db-Me, Db-Me+, Db-H, and Db-H+).

## Step 1. Create directories

Create eight separate directories, one for each molecule, and place the corresponding `.xyz` file inside:

```
/Sg-Me/Sg-Me.xyz
/Sg-Me+/Sg-Me+.xyz
/Sg-H/Sg-H.xyz
/Sg-H+/Sg-H+.xyz
/Db-Me/Db-Me.xyz
/Db-Me+/Db-Me+.xyz
/Db-H/Db-H.xyz
/Db-H+/Db-H+.xyz
```

## Step 2. Run Calculation

For each system, navigate into its directory and run the `L1_XTB` module. You must replace `[L_idx]` and `[R_idx]` with the correct sulfur atom indices for that specific molecule. **Crucially, set the `--charge` parameter correctly for neutral (0.0) and protonated (1.0) systems.**

**For Sg-Me (Neutral):**

```bash
cd Sg-Me/
L1_XTB -f Sg-Me.xyz -L [L_idx] -R [R_idx] -C 1 --Erange 3 --Enum 1000 --charge 0.0
cd ..
```

**For Sg-Me+ (Cation):**

```bash
cd Sg-Me+/
L1_XTB -f Sg-Me+.xyz -L [L_idx] -R [R_idx] -C 1 --Erange 3 --Enum 1000 --charge 1.0
cd ..
```

**For Sg-H (Neutral):**

```bash
cd Sg-H/
L1_XTB -f Sg-H.xyz -L [L_idx] -R [R_idx] -C 1 --Erange 3 --Enum 1000 --charge 0.0
cd ..
```

**For Sg-H+ (Cation):**

```bash
cd Sg-H+/
L1_XTB -f Sg-H+.xyz -L [L_idx] -R [R_idx] -C 1 --Erange 3 --Enum 1000 --charge 1.0
cd ..
```

**For Db-Me (Neutral):**

```bash
cd Db-Me/
L1_XTB -f Db-Me.xyz -L [L_idx] -R [R_idx] -C 1 --Erange 3 --Enum 1000 --charge 0.0
cd ..
```

**For Db-Me+ (Cation):**

```bash
cd Db-Me+/
L1_XTB -f Db-Me+.xyz -L [L_idx] -R [R_idx] -C 1 --Erange 3 --Enum 1000 --charge 1.0
cd ..
```

**For Db-H (Neutral):**

```bash
cd Db-H/
L1_XTB -f Db-H.xyz -L [L_idx] -R [R_idx] -C 1 --Erange 3 --Enum 1000 --charge 0.0
cd ..
```

**For Db-H+ (Cation):**

```bash
cd Db-H+/
L1_XTB -f Db-H+.xyz -L [L_idx] -R [R_idx] -C 1 --Erange 3 --Enum 1000 --charge 1.0
cd ..
```

## Step 3. Post-processing and Analysis

1.  Collect all eight `Transmission.txt` files generated in each directory.
2.  Use a plotting tool (e.g., Python/Matplotlib) to plot all eight transmission spectra. It is recommended to create two separate plots: one for the Sg series (Sg-Me, Sg-Me+, Sg-H, Sg-H+) and one for the Db series (Db-Me, Db-Me+, Db-H, Db-H+). The y-axis **must be logarithmic** to visualize the full spectrum, similar to Figure 5 in the paper.
3.  Extract the transmission value at the calculated Fermi level ($E=0$ in the output `Transmission.txt` files) for all eight systems.
4.  Compare these $T(E=0)$ values. The ordering of these values should qualitatively match the experimentally observed conductance trend, with protonated and H-substituted species showing lower transmission than their neutral, Me-substituted counterparts.
5.  Confirm that the *magnitude* of the conductance drop (suppression) is larger for the Db series than for the Sg series.