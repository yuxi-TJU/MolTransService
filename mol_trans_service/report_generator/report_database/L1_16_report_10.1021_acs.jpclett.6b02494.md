# 0\. Metadata

  - Title: Probing the Conductance of the $\sigma$-System of Bipyridine Using Destructive Interference
  - DOI: (Omit this part)

# 1\. Literature Summary

This is an experiment + computation study. The authors investigate charge transport through a family of para- and meta-linked bipyridine molecules of two different lengths. Using STM-break junction (STM-BJ) experiments and density functional theory (DFT) transport calculations, they find a counter-intuitive result: the short *meta*-linked molecule (3,3'-bipyridine) exhibits a *higher* conductance than its *para*-linked analog (4,4'-bipyridine). This trend is reversed for the extended (longer) molecules, where the para-linked system is more conductive, as expected. The paper's calculations explain this by showing that in the short meta molecule, destructive quantum interference (DQI) effectively "shuts down" the $\pi$-system pathway, allowing a more conductive $\sigma$-system pathway to dominate transport. In the longer molecules, the $\sigma$-transport decays rapidly, and the $\pi$-system's properties (CQI vs. DQI) re-establish the expected para \> meta conductance trend.

# 2\. Computational Objectives

The primary computational objective is to theoretically validate the experimentally observed conductance trends. This involves two parts:

1.  Reproducing the surprising trend for the short molecules: $Conductance(meta) > Conductance(para)$.
2.  Reproducing the expected trend for the long molecules: $Conductance(para) > Conductance(meta)$.

The calculation aims to compute the zero-bias transmission spectra $T(E)$ for all four molecules. The expected result is to show that the *total* transmission near the Fermi energy for the short meta molecule (System 2) is higher than for the short para molecule (System 1), and that this order is inverted for the long systems (System 3 vs. System 4). This validates the paper's hypothesis of a competition between $\sigma$- and $\pi$-transport pathways, where DQI in the $\pi$-system allows the $\sigma$-system to dominate in the short meta case.

# 3\. Involved Systems

## System 1: 4,4'-Bipyridine

  - Core Molecule:
      - abbreviation: 1
      - full\_chemical\_name: 4,4'-Bipyridine
      - core\_smiles: c1cc(-c2ccncc2)ccn1
  - Anchors:
      - anchor\_groups: ['Pyridine\_N']
  - Electrodes:
      - electrode\_material: Au
      - electrode\_surface: N/A
  - Interface:
      - interface\_geometry\_text: Pyridine-N lone pair forms a donor-acceptor bond to an under-coordinated Au atom on the electrode.
  - Variation\_notes: "Short para-linked molecule. Expected constructive quantum interference (CQI) in the $\pi$-system."

## System 2: 3,3'-Bipyridine

  - Core Molecule:
      - abbreviation: 2
      - full\_chemical\_name: 3,3'-Bipyridine
      - core\_smiles: c1cncc(-c2cccnc2)c1
  - Variation\_notes: "Short meta-linked molecule. Expected destructive quantum interference (DQI) in the $\pi$-system."

## System 3: Extended para-linked molecule

  - Core Molecule:
      - abbreviation: 3
      - full\_chemical\_name: N/A (Described as "extended para linked molecules")
      - core\_smiles: c1cc(-c2ccc(-c3ccncc3)cc2)ccn1
  - Variation\_notes: "Long para-linked molecule (CQI)."

## System 4: Extended meta-linked molecule

  - Core Molecule:
      - abbreviation: 4
      - full\_chemical\_name: N/A (Described as "extended meta linked molecules")
      - core\_smiles: c1cncc(-c2ccc(-c3cccnc3)cc2)c1
  - Variation\_notes: "Long meta-linked molecule (DQI)."

# 4\. Applicability Assessment

**Applicable.**

The core computational objective is to compare the zero-bias transmission spectra $T(E)$ of four molecular isomers/analogs, focusing on the effects of linkage (meta vs. para) and length. This is a classic problem involving "Quantum Interference effects (DQI)" and "substituent/structural effects," which is well-suited for the QDHC framework.

The paper's most detailed analysis (Fig. 3) uses DFT-NEGF with a specialized $\sigma/\pi$ partitioning scheme to isolate the orbital contributions. While MST cannot perform this partitioning, it *can* calculate the *total* transmission spectrum. The central goal is to see if the MST-calculated total transmission $T(E)$ successfully reproduces the final experimental trend ($T_2 > T_1$ and $T_3 > T_4$), which is the key finding.

# 5\. Hierarchical Analysis

**Level: L1**

According to the QDHC criteria, this problem maps to the **L1 level**. The central question is how transport is governed by the molecule's *intrinsic electronic structure*, which is directly manipulated by changing the linkage (meta- vs. para-) and the length. These structural changes are the root cause of the quantum interference (DQI) and the $\sigma/\pi$ competition. This falls directly under the L1-applicable problems: "Quantum Interference effects (DQI), e.g., comparing para- vs. meta-linkages" and "Effects of molecular... substituents, or charge state on transport." The problem does not fundamentally depend on specific interface geometries (L2) or finite-bias (L3) to explain the existence of DQI or the length-dependent trend.

# 6\. Input Preparation

This task will use the `L1_XTB` module. The GFN-xTB method is required over EHT because it provides a more robust all-valence-electron description, which is essential for capturing the competition between the $\sigma$-system and the $\pi$-system, as well as the N-lone pair anchoring.

1.  **Structure Files**:

      - `mol_1.xyz`: Structure file for 4,4'-Bipyridine.
      - `mol_2.xyz`: Structure file for 3,3'-Bipyridine.
      - `mol_3.xyz`: Structure file for the extended para molecule.
      - `mol_4.xyz`: Structure file for the extended meta molecule.

2.  **Anchor Atom Indices**:

      - The user must visually inspect each of the four `.xyz` files to find the atom indices for the two terminal **Nitrogen (N)** atoms that act as anchors. Let these be `[L_N_idx]` and `[R_N_idx]` for each file.

3.  **Key Parameters (`L1_XTB`)**:

      - `--method` (`-m`): `1` (GFN1-xTB, default).
      - `--coupling` (`-C`): `1` (Default value).
      - `--Erange`: `4.0` (Default, sufficient to cover the $\pm 3$ eV range in the paper's Fig. 1b).
      - `--Enum`: `1000` (For a high-resolution spectrum to resolve any sharp DQI dips).
      - `--charge`: `0.0` (All systems are neutral).

# 7\. Computational Workflow

## Goal:

Compute and compare the zero-bias transmission spectra $T(E)$ for all four molecules (1, 2, 3, and 4).

## Step 1. Create directories

Create four separate directories, one for each molecule, and place the corresponding `.xyz` file inside:

```
/mol_1/mol_1.xyz
/mol_2/mol_2.xyz
/mol_3/mol_3.xyz
/mol_4/mol_4.xyz
```

## Step 2. Run Calculation

For each system, navigate into its directory and run the `L1_XTB` module. You must replace `[L_N_idx]` and `[R_N_idx]` with the correct nitrogen atom indices for that specific molecule.

**For System 1:**

```bash
cd mol_1/
L1_XTB -f mol_1.xyz -L [L_N_idx_1] -R [R_N_idx_1] --Enum 1000
cd ..
```

**For System 2:**

```bash
cd mol_2/
L1_XTB -f mol_2.xyz -L [L_N_idx_2] -R [R_N_idx_2] --Enum 1000
cd ..
```

**For System 3:**

```bash
cd mol_3/
L1_XTB -f mol_3.xyz -L [L_N_idx_3] -R [R_N_idx_3] --Enum 1000
cd ..
```

**For System 4:**

```bash
cd mol_4/
L1_XTB -f mol_4.xyz -L [L_N_idx_4] -R [R_N_idx_4] --Enum 1000
cd ..
```

## Step 3. Post-processing and Analysis

1.  Collect all four `Transmission.txt` files generated in each directory.
2.  Use a plotting tool (e.g., Python/Matplotlib) to plot all four transmission spectra on a single graph. The y-axis **must be logarithmic** to clearly visualize the DQI anti-resonances and compare transmission magnitudes (as in the paper's Fig. 1b).
3.  Analyze the plot:
      - First, confirm the DQI feature: Check if `mol_2` and `mol_4` (meta) show a deep anti-resonance (dip) near the Fermi level ($E=0$) that is absent in `mol_1` and `mol_3` (para).
      - Second, check the paper's key finding: Compare the transmission values at the Fermi level ($T(E=0)$). Verify if $T_2 > T_1$ (for the short molecules) and $T_3 > T_4$ (for the long molecules).