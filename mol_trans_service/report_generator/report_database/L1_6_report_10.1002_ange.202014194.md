# 0\. Metadata

  - Title: Single-Molecule Conductance of 1,4-Azaborine Derivatives as Models of BN-doped PAHs
  - DOI: (Omit this part)

# 1\. Literature Summary

This is an experiment + computation study. The authors measure the single-molecule conductance of three acene-like derivatives using the STM-BJ technique: an all-carbon anthracene (CCA), its 1,4-azaborine (BN-doped) analog (BNA), and a longer 1,4-azaborine pentacene (BNP). All molecules use thiomethyl (SMe) linkers. Experimentally, they find that the conductance of the BN-doped BNA is comparable to, but slightly lower than, the all-carbon CCA. The longer BNP molecule shows a similarly low conductance. The study is supported by NEGF-DFT transport calculations (using a DFT+$\Sigma$ correction), which reproduce this conductance trend (CCA \> BNA \> BNP). The calculations attribute the small conductance decrease to a combination of reduced aromaticity and conformational changes (dihedral angles) induced by the BN-substitution, demonstrating that transport occurs via non-resonant tunneling.

# 2\. Computational Objectives

The primary computational objective is to theoretically validate the experimental conductance trend: $G_{CCA} > G_{BNA} > G_{BNP}$. This is achieved by computing the zero-bias transmission spectra $T(E)$ for all three molecules. The calculation aims to demonstrate that the transmission at the Fermi level, $T(E_F)$, follows this order, and to understand the physical origin of the conductance modulation, which the paper links to intrinsic molecular properties like aromaticity and conformation rather than a change in the transport mechanism (all are non-resonant).

# 3\. Involved Systems

## System 1: CCA

  - Core Molecule:
      - abbreviation: CCA
      - full\_chemical\_name: all-carbon anthracene derivative (with (4-(methylthio)phenyl) linkers)
      - core\_smiles: CSc1ccc(-c2c3ccccc3c(-c3ccc(SC)cc3)c3ccccc23)cc1
  - Anchors:
      - anchor\_groups: ['Methylthio\_SCH3']
  - Electrodes:
      - electrode\_material: Au
      - electrode\_surface: (111)
  - Interface:
      - interface\_geometry\_text: The molecule is fully extended between two Au(111) electrodes, connected via its terminal sulfur (SMe) groups. The calculation model simulates an asymmetric STM-BJ setup (tip and surface).
  - Variation\_notes: "All-carbon, linearly-conjugated reference molecule."

## System 2: BNA

  - Core Molecule:
      - abbreviation: BNA
      - full\_chemical\_name: 1,4-azaborine anthracene derivative (with (4-(methylthio)phenyl) linkers)
      - core\_smiles: CSc1ccc(B2c3ccccc3N(c3ccc(SC)cc3)c3ccccc32)cc1
  - Variation\_notes: "BN-doped (1,4-azaborine) analog of CCA."

## System 3: BNP

  - Core Molecule:
      - abbreviation: BNP
      - full\_chemical\_name: 1,4-azaborine pentacene derivative (with (4-(methylthio)phenyl) linkers)
      - core\_smiles: CSc1ccc(B2c3cc4ccccc4cc3N(c3ccc(SC)cc3)c3cc4ccccc4cc32)cc1
  - Variation\_notes: "Longer, BN-doped (1,4-azaborine) acene."

# 4\. Applicability Assessment

**Applicable.**

The core computational objective is to compare the zero-bias transmission $T(E_F)$ of three molecular analogs to explain a conductance trend. This is a classic "substituent/structural effects" problem. Although the paper uses DFT+$\Sigma$ for better quantitative alignment, it explicitly states that the *qualitative trend* (the core objective) is reproduced even without this correction. Therefore, the mechanism is not dependent on precise level alignment (L3) or out-of-scope $\Sigma$ corrections. MST can capture the qualitative differences in $T(E_F)$ arising from the intrinsic electronic structures of the three molecules.

# 5\. Hierarchical Analysis

**Level: L1**

According to the QDHC criteria, this problem maps to the **L1 level**. The central question is how transport, which occurs via non-resonant tunneling, is governed by the molecule's *intrinsic electronic structure*. The differences in conductance are explained by changes in the molecule's properties (aromaticity, conformation) induced by heteroatom *substituents* (BN-doping) and backbone *length* (anthracene vs. pentacene). This falls directly under the L1-applicable problem: "Effects of molecular... substituents... on transport." The problem does not require specific interface geometries (L2) or finite-bias/level-alignment (L3) to explain the *existence* of the conductance trend, which is the core mechanism.

# 6\. Input Preparation

This task will use the `L1_XTB` module. The GFN-xTB method is required over EHT to accurately model the electronic structure, charge distribution, and conformational properties (dihedral angles) of systems containing heteroatoms (B, N).

1.  **Structure Files**:

      - `CCA.xyz`: Structure file for the CCA molecule.
      - `BNA.xyz`: Structure file for the BNA molecule.
      - `BNP.xyz`: Structure file for the BNP molecule.

2.  **Anchor Atom Indices**:

      - The user must visually inspect each `.xyz` file to find the atom indices for the two terminal Sulfur (S) atoms. Let these be `[L_idx]` and `[R_idx]`.

3.  **Key Parameters (`L1_XTB`)**:

      - **Method (`-m`)**: `1` (GFN1-xTB, default).
      - **Coupling (`-C`)**: `1` (Default value).
      - **Energy Range (`--Erange`)**: `3` (To scan from $E_F - 3$ eV to $E_F + 3$ eV, sufficient to show the HOMO-LUMO gap as seen in the paper's Fig. 5).
      - **Energy Points (`--Enum`)**: `1000` (For a high-resolution spectrum).
      - **Charge (`--charge`)**: `0.0` (All systems are neutral).

# 7\. Computational Workflow

## Goal:

Compute and compare the zero-bias transmission spectra $T(E)$ for the CCA, BNA, and BNP systems.

## Step 1. Create directories

Create three separate directories, one for each molecule, and place the corresponding `.xyz` file inside:

```
/CCA/CCA.xyz
/BNA/BNA.xyz
/BNP/BNP.xyz
```

## Step 2. Transport calculation

For each system, navigate into its directory and run the `L1_XTB` module. You must replace `[L_idx]` and `[R_idx]` with the correct sulfur atom indices for that specific molecule.

**For CCA:**

```bash
cd CCA/
# Replace [L_idx] and [R_idx] with the correct sulfur atom indices
L1_XTB -f CCA.xyz -L [L_idx] -R [R_idx] -C 1 --Erange 3 --Enum 1000
cd ..
```

**For BNA:**

```bash
cd BNA/
# Replace [L_idx] and [R_idx] with the correct sulfur atom indices
L1_XTB -f BNA.xyz -L [L_idx] -R [R_idx] -C 1 --Erange 3 --Enum 1000
cd ..
```

**For BNP:**

```bash
cd BNP/
# Replace [L_idx] and [R_idx] with the correct sulfur atom indices
L1_XTB -f BNP.xyz -L [L_idx] -R [R_idx] -C 1 --Erange 3 --Enum 1000
cd ..
```

## Step 3. Post-processing and Analysis

1.  Collect all three `Transmission.txt` files generated in each directory.
2.  Use a plotting tool (e.g., Python/Matplotlib) to plot all three transmission spectra on a single graph. The y-axis should be logarithmic.
3.  Compare the transmission values at the Fermi level ($E=0$). The ordering of these values should qualitatively match the experimentally observed conductance trend: $T_{CCA} > T_{BNA} > T_{BNP}$.