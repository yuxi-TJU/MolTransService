# 0\. Metadata

  - Title: $\sigma$-dominated charge transport in sub-nanometer molecular junctions
  - DOI: (Omit this part)

# 1\. Literature Summary

This is an experiment + computation study. The authors investigate the possibility of $\sigma$-dominated transport in $\pi$-conjugated molecules at the sub-nanometer scale using the STM-BJ technique. They primarily study para- (p-PA) and meta- (m-PA) connected picolinic acid. The key experimental finding is that the conductance of the *meta*-isomer (m-PA) is \~35 times *higher* than the *para*-isomer (p-PA). This result is a direct reversal of the standard trend for $\pi$-systems, where *meta*-linkages exhibit destructive quantum interference (DQI) and thus much lower conductance than *para*-linkages. DFT-NEGF calculations corroborate this finding, revealing that the transport is dominated by the molecule's $\sigma$-system, not its $\pi$-system. In this $\sigma$-pathway, the *meta*-connection is inherently more conductive. The study also explores longer analogs (PAA) and systems with different anchors (MBA) to show the transition back towards $\pi$-dominated transport.

# 2\. Computational Objectives

The primary computational objective is to theoretically validate the counter-intuitive experimental observation that $G_{m-PA} \gg G_{p-PA}$. The calculation aims to compute and compare the zero-bias transmission spectra $T(E)$ for the *meta* and *para* isomers of three molecular series (PA, PAA, and MBA). The expected result is to show that for the PA series, the transmission of m-PA is significantly higher than p-PA near the Fermi level, which is a hallmark of $\sigma$-dominated transport, in direct contrast to the $\pi$-only DQI effect.

# 3\. Involved Systems

## System 1: m-PA

  - Core Molecule:
      - abbreviation: m-PA
      - full\_chemical\_name: meta-connected picolinic acid
      - core\_smiles: O=C(O)c1cccnc1
  - Anchors:
      - anchor\_groups: ['Pyridine\_N', 'Carboxylic acid\_COOH']
  - Electrodes:
      - electrode\_material: Au
      - electrode\_surface: N/A
  - Interface:
      - interface\_geometry\_text: The molecule bridges two gold electrodes. One anchor is the nitrogen atom of the pyridine ring, and the other anchor is the carbonyl oxygen atom of the carboxylic acid group.
  - Variation\_notes: "meta-linked picolinic acid. Expected to show anomalously high conductance."

## System 2: p-PA

  - Core Molecule:
      - abbreviation: p-PA
      - full\_chemical\_name: para-connected picolinic acid
      - core\_smiles: O=C(O)c1ccncc1
  - Variation\_notes: "para-linked picolinic acid. Control system, expected to show low conductance."

## System 3: m-PAA

  - Core Molecule:
      - abbreviation: m-PAA
      - full\_chemical\_name: meta-connected pyridyl-cinnamic acid
      - core\_smiles: O=C(O)C=Cc1cccnc1
  - Variation\_notes: "meta-linked, longer $\pi$-system."

## System 4: p-PAA

  - Core Molecule:
      - abbreviation: p-PAA
      - full\_chemical\_name: para-connected pyridyl-cinnamic acid
      - core\_smiles: O=C(O)C=Cc1ccncc1
  - Variation\_notes: "para-linked, longer $\pi$-system."

## System 5: m-MBA

  - Core Molecule:
      - abbreviation: m-MBA
      - full\_chemical\_name: meta-methylthio-terminated benzoic acid
      - core\_smiles: CSc1cccc(C(=O)O)c1
  - Anchors:
      - anchor\_groups: ['Methylthio\_S', 'Carboxylic acid\_COOH']
  - Electrodes:
      - electrode\_material: Au
      - electrode\_surface: N/A
  - Interface:
      - interface\_geometry\_text: The molecule bridges two gold electrodes. One anchor is the sulfur atom of the methylthiol group, and the other anchor is the carbonyl oxygen atom of the carboxylic acid group.
  - Variation\_notes: "meta-linked, benzene core, S and COOH anchors."

## System 6: p-MBA

  - Core Molecule:
      - abbreviation: p-MBA
      - full\_chemical\_name: para-methylthio-terminated benzoic acid
      - core\_smiles: CSc1ccc(C(=O)O)cc1
  - Anchors:
      - anchor\_groups: ['Methylthio\_S', 'Carboxylic acid\_COOH']
  - Variation\_notes: "para-linked, benzene core, S and COOH anchors."

# 4\. Applicability Assessment

**Applicable.**

The core computational objective is to compare the zero-bias transmission spectra $T(E)$ of several molecular isomers to explain a conductance trend. This is a classic coherent transport problem. The central finding (reversal of the DQI rule) is explained by the *type* of orbital ($\sigma$ vs. $\pi$) contributing to transport, which is an intrinsic electronic structure property. This falls directly under L1-level problems. MST's L1-XTB module is well-suited to distinguish between $\sigma$ and $\pi$ orbital contributions, which an EHT-based (Hückel-like) model would fail to do.

# 5\. Hierarchical Analysis

**Level: L1**

According to the QDHC criteria, this problem maps to the **L1 level**. The central question is how transport is governed by the molecule's *intrinsic electronic structure*, which is modified by the *substituent* (isomer) linkage. The paper's core finding is that the transport is dominated by $\sigma$-orbitals, and the comparison between *meta* and *para* isomers is the key evidence. This falls directly under the L1-applicable problems: "Quantum Interference effects (DQI), e.g., comparing para- vs. meta-linkages" (even though it's a subversion of this rule) and "Effects of molecular... substituents... on transport". The problem does not require specific interface geometries (L2) or finite-bias/level-alignment (L3) to explain the *existence* of the $\sigma$-pathway and its resulting conductance trend.

# 6\. Input Preparation

This task will use the `L1_XTB` module. The GFN-xTB method is required over EHT because it treats all valence electrons and can correctly capture the electronic structure of both $\sigma$- and $\pi$-systems, which is essential to reproduce the paper's main finding. EHT, being a $\pi$-only-like model, would incorrectly predict DQI for m-PA.

1.  **Structure Files**:

      - `m-PA.xyz`: Structure file for the meta-picolinic acid.
      - `p-PA.xyz`: Structure file for the para-picolinic acid.
      - `m-PAA.xyz`: Structure file for the meta-pyridyl-cinnamic acid.
      - `p-PAA.xyz`: Structure file for the para-pyridyl-cinnamic acid.
      - `m-MBA.xyz`: Structure file for the meta-methylthio-benzoic acid.
      - `p-MBA.xyz`: Structure file for the para-methylthio-benzoic acid.

2.  **Anchor Atom Indices**:

      - The user must visually inspect each `.xyz` file to find the atom indices for the two terminal anchoring atoms.
      - **For PA and PAA series**: The anchors are the **Pyridine N** atom and the **Carbonyl O** atom. Let these be `[N_idx]` and `[O_idx]`.
      - **For MBA series**: The anchors are the **Sulfur S** atom (from S-CH3) and the **Carbonyl O** atom. Let these be `[S_idx]` and `[O_idx]`.

3.  **Key Parameters (`L1_XTB`)**:

      - `--method` (`-m`): `1` (for GFN1-xTB, default).
      - `--coupling` (`-C`): `1` (Default value).
      - `--Erange`: `2` (To scan from $E_F - 2$ eV to $E_F + 2$ eV, sufficient to cover the relevant orbital resonances).
      - `--Enum`: `1000` (For a high-resolution spectrum).
      - `--charge`: `0.0` (All systems are neutral).

# 7\. Computational Workflow

## Goal:

Compute and compare the zero-bias transmission spectra $T(E)$ for the *meta* and *para* isomers of the PA, PAA, and MBA series.

## Step 1. Create directories

Create six separate directories, one for each molecule, and place the corresponding `.xyz` file inside:

```
/m-PA/m-PA.xyz
/p-PA/p-PA.xyz
/m-PAA/m-PAA.xyz
/p-PAA/p-PAA.xyz
/m-MBA/m-MBA.xyz
/p-MBA/p-MBA.xyz
```

## Step 2. Run Calculation

For each system, navigate into its directory and run the `L1_XTB` module. You must replace the bracketed indices with the correct anchor atom indices for that specific molecule.

**PA Series (N and O anchors):**

```bash
cd m-PA/
L1_XTB -f m-PA.xyz -L [N_idx] -R [O_idx] -C 1 --Erange 2 --Enum 1000
cd ..
cd p-PA/
L1_XTB -f p-PA.xyz -L [N_idx] -R [O_idx] -C 1 --Erange 2 --Enum 1000
cd ..
```

**PAA Series (N and O anchors):**

```bash
cd m-PAA/
L1_XTB -f m-PAA.xyz -L [N_idx] -R [O_idx] -C 1 --Erange 2 --Enum 1000
cd ..
cd p-PAA/
L1_XTB -f p-PAA.xyz -L [N_idx] -R [O_idx] -C 1 --Erange 2 --Enum 1000
cd ..
```

**MBA Series (S and O anchors):**

```bash
cd m-MBA/
L1_XTB -f m-MBA.xyz -L [S_idx] -R [O_idx] -C 1 --Erange 2 --Enum 1000
cd ..
cd p-MBA/
L1_XTB -f p-MBA.xyz -L [S_idx] -R [O_idx] -C 1 --Erange 2 --Enum 1000
cd ..
```

## Step 3. Post-processing and Analysis

1.  Collect all six `Transmission.txt` files generated in each directory.
2.  Use a plotting tool to plot the transmission spectra, grouped by series (PA, PAA, MBA). The y-axis should be logarithmic to clearly visualize the differences.
3.  Compare the transmission value at the Fermi level ($E=0$) for each pair.
4.  Check the transmission order. The expected result is:
      - $T_{m-PA} > T_{p-PA}$
      - $T_{m-PAA} > T_{p-PAA}$ (but with a smaller ratio than PA)
      - $T_{p-MBA} > T_{m-MBA}$ (reverting to the $\pi$-DQI trend)