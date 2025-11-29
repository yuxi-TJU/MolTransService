# 0\. Metadata

  - Title: Single-Molecule Sensing of Environmental pH—an STM Break Junction and NEGF-DFT Approach
  - DOI: (Omit this part)

# 1\. Literature Summary

This is an experiment + computation study. The authors demonstrate a single-molecule pH sensor using two dye molecules, Pararosaniline (PA) and Malachite Green (MG), in an STM break junction (STM-BJ) setup. They find that the molecules can be reversibly switched between a high-conductance "ON" state at acidic pH (5.5) and a low-conductance "OFF" state at basic pH (13.6), exhibiting a high on/off ratio of approximately 100:1. This switching is caused by a pH-induced reversible structural transformation: the low-pH form is conjugated (sp²-hybridized central carbon), while the high-pH form has its conjugation broken by the addition of an OH group to the central carbon (sp³ hybridization). NEGF-DFT calculations confirm this mechanism, showing that the conjugated "ON" state has high transmission near the Fermi level (LUMO-mediated), whereas the non-conjugated "OFF" state has a much larger HOMO-LUMO gap and the LUMO is shifted to a high energy, resulting in significantly lower transmission.

# 2\. Computational Objectives

The primary computational objective is to theoretically validate the experimentally observed high-contrast (≈100:1) conductance switching. The calculation aims to compute the zero-bias transmission spectra $T(E)$ for both PA and MG in their two distinct structural forms: the conjugated (low pH, "ON" state) and the non-conjugated (high pH, "OFF" state). The expected result is to show that the transmission near the Fermi level for the conjugated forms is several orders of magnitude higher than for the non-conjugated forms, thereby explaining the observed switching mechanism.

# 3\. Involved Systems

## System 1: PA (conjugated)

  - Core Molecule:
      - abbreviation: PA (pH 5.5)
      - full\_chemical\_name: Pararosaniline (conjugated cation form)
      - core\_smiles: N/A
  - Anchors:
      - anchor\_groups: ['Amine\_NH2']
  - Electrodes:
      - electrode\_material: Au
      - electrode\_surface: N/A (Calculations in paper use explicit Au clusters)
  - Interface:
      - interface\_geometry\_text: Amine ($NH_2$) groups at both ends of the molecule bind to the gold electrodes.
  - Variation\_notes: "Conjugated (sp²) 'ON' state. Molecule is a cation (charge +1)."

## System 2: PA (non-conjugated)

  - Core Molecule:
      - abbreviation: PA (pH 13.6)
      - full\_chemical\_name: Pararosaniline (non-conjugated neutral form)
      - core\_smiles: N/A
  - Variation\_notes: "Non-conjugated (sp³) 'OFF' state. An OH group is bonded to the central carbon. Molecule is neutral."

## System 3: MG (conjugated)

  - Core Molecule:
      - abbreviation: MG (pH 5.5)
      - full\_chemical\_name: Malachite Green (conjugated cation form)
      - core\_smiles: N/A
  - Anchors:
      - anchor\_groups: ['Dimethylamine\_N(CH3)2']
  - Electrodes:
      - electrode\_material: Au
      - electrode\_surface: N/A (Calculations in paper use explicit Au clusters)
  - Interface:
      - interface\_geometry\_text: Dimethylamine ($N(CH_3)_2$) groups at both ends of the molecule bind to the gold electrodes.
  - Variation\_notes: "Conjugated (sp²) 'ON' state. Molecule is a cation (charge +1)."

## System 4: MG (non-conjugated)

  - Core Molecule:
      - abbreviation: MG (pH 13.6)
      - full\_chemical\_name: Malachite Green (non-conjugated neutral form)
      - core\_smiles: CN(C)C1=CC=C(C=C1)C(C2=CC=CC=C2)(C3=CC=C(C=C3)N(C)C)O[H]
  - Variation\_notes: "Non-conjugated (sp³) 'OFF' state. An OH group is bonded to the central carbon. Molecule is neutral."

# 4\. Applicability Assessment

**Applicable.**

The core computational objective is to compare the zero-bias transmission spectra $T(E)$ of four different molecular systems (two molecules, each in two structural forms). The conductance switch is driven by a fundamental change in the molecule's intrinsic electronic structure (breaking of $\pi$-conjugation and a massive change in the HOMO-LUMO gap) induced by a structural change (sp² to sp³). This falls squarely within the "Effects of molecular conformation/structural effects... on transport" category. While the original paper uses NEGF-DFT with explicit clusters (which suggests L2/L3 physics) to get level alignment, the *mechanism* itself (the large gap opening) is an intrinsic molecular property that the L1 scheme is designed to capture. MST can reproduce the qualitative difference in $T(E)$ and the resulting on/off ratio.

# 5\. Hierarchical Analysis

**Level: L1**

According to the QDHC criteria, this problem maps to the **L1 level**. The central question is how transport is governed by the molecule's *intrinsic electronic structure* and how that structure is fundamentally altered by a pH-induced structural transformation. The paper's own analysis of the isolated molecules (Figure 1E) shows that the HOMO-LUMO gap nearly doubles for the non-conjugated form. This intrinsic property is the direct cause of the conductance switch. This is a classic example of "Effects of molecular... structural effects... on transport," which is an L1-applicable problem. The specific details of the interface (L2) or precise level alignment with the electrode $E_F$ (L3) are not necessary to explain the *existence* of the massive conductance drop, which is rooted in the molecule's broken conjugation.

# 6\. Input Preparation

This task will use the `L1_XTB` module. The GFN-xTB method is required over EHT because it can more accurately handle the significant changes in electronic structure, hybridization (sp² vs. sp³), and, crucially, the different charge states of the molecules.

1.  **Structure Files**:
      - `PA_conj.xyz`: Structure file for the conjugated Pararosaniline (pH 5.5, cation).
      - `PA_nonconj.xyz`: Structure file for the non-conjugated Pararosaniline (pH 13.6, neutral).
      - `MG_conj.xyz`: Structure file for the conjugated Malachite Green (pH 5.5, cation).
      - `MG_nonconj.xyz`: Structure file for the non-conjugated Malachite Green (pH 13.6, neutral).
2.  **Anchor Atom Indices**:
      - The user must visually inspect each `.xyz` file to find the atom indices for the two terminal Nitrogen (N) atoms that serve as the anchors. Let these be `[L_N_idx]` and `[R_N_idx]`.
3.  **Key Parameters (`L1_XTB`)**:
      - `--method` (`-m`): `1` (for GFN1-xTB).
      - `--coupling` (`-C`): `1` (Default value, to be applied consistently across all systems).
      - `--Erange`: `3` (To scan from $E_F - 3$ eV to $E_F + 3$ eV, which is wide enough to see the large gap of the "OFF" states).
      - `--Enum`: `800` (Default).
      - `--charge`: This is critical.
          - `1.0` for `PA_conj.xyz` and `MG_conj.xyz` (cationic "ON" states).
          - `0.0` for `PA_nonconj.xyz` and `MG_nonconj.xyz` (neutral "OFF" states).

# 7\. Computational Workflow

## Goal:

Compute and compare the zero-bias transmission spectra $T(E)$ for the conjugated (pH 5.5, +1 charge) and non-conjugated (pH 13.6, neutral) forms of PA and MG.

## Step 1. Create directories

Create four separate directories, one for each system, and place the corresponding `.xyz` file inside:

```
/PA_conj/PA_conj.xyz
/PA_nonconj/PA_nonconj.xyz
/MG_conj/MG_conj.xyz
/MG_nonconj/MG_nonconj.xyz
```

## Step 2. Run Calculation

For each system, navigate into its directory and run the `L1_XTB` module with the correct parameters. You must replace `[L_N_idx]` and `[R_N_idx]` with the correct nitrogen anchor atom indices for that specific molecule.

**1. Calculate PA (Conjugated, "ON" state):**

```bash
cd PA_conj/
# Replace [L_N_idx] and [R_N_idx] with the correct nitrogen atom indices
L1_XTB -f PA_conj.xyz -L [L_N_idx] -R [R_N_idx] -C 1 --Erange 3 --Enum 800 --charge 1.0
cd ..
```

**2. Calculate PA (Non-Conjugated, "OFF" state):**

```bash
cd PA_nonconj/
# Replace [L_N_idx] and [R_N_idx] with the correct nitrogen atom indices
L1_XTB -f PA_nonconj.xyz -L [L_N_idx] -R [R_N_idx] -C 1 --Erange 3 --Enum 800 --charge 0.0
cd ..
```

**3. Calculate MG (Conjugated, "ON" state):**

```bash
cd MG_conj/
# Replace [L_N_idx] and [R_N_idx] with the correct nitrogen atom indices
L1_XTB -f MG_conj.xyz -L [L_N_idx] -R [R_N_idx] -C 1 --Erange 3 --Enum 800 --charge 1.0
cd ..
```

**4. Calculate MG (Non-Conjugated, "OFF" state):**

```bash
cd MG_nonconj/
# Replace [L_N_idx] and [R_N_idx] with the correct nitrogen atom indices
L1_XTB -f MG_nonconj.xyz -L [L_N_idx] -R [R_N_idx] -C 1 --Erange 3 --Enum 800 --charge 0.0
cd ..
```

## Step 3. Post-processing and Analysis

1.  Collect all four `Transmission.txt` files generated in each directory.
2.  Use a plotting tool to plot the transmission spectra. The y-axis **must be logarithmic** to visualize the large on/off ratio.
3.  Create two comparison plots: one for PA (`PA_conj` vs. `PA_nonconj`) and one for MG (`MG_conj` vs. `MG_nonconj`).
4.  Observe the transmission value at the "Fermi energy" ($E=0$, the mid-gap). Verify that the transmission for the `_conj` ("ON") systems is several orders of magnitude higher than for the `_nonconj` ("OFF") systems, confirming the switching behavior.