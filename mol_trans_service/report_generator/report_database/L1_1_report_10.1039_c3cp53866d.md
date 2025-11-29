# 0\. Metadata

 - Title: Cross-conjugation and quantum interference: a general correlation?
 - DOI: 10.1039/c3cp53866d

# 1\. Literature Summary

This is an experiment + computation study. The authors examine, from both experimental and theoretical perspectives, how π-conjugation motifs govern charge transport in molecular wires, with a particular focus on destructive quantum interference (DQI) in cross-conjugated systems. They compare conductance across three length-matched OPE trimers—AC (linear conjugation), AQ (cross-conjugation), and AH (broken conjugation)—measured on multiple platforms (CP-AFM, STM-BJ, MCBJ, EGaIn). On the theory side they compute the zero-bias transmission T(E) using NEGF-DFT(+Σ) to assess the contribution of quantum interference. The key result is that AQ exhibits a clear DQI feature in T(E) near the Fermi level (absent for AC/AH), which is consistent with the experimental conductance ordering where AQ is the least conductive, establishing the causal chain cross-conjugation → DQI → low conductance.

# 2\. Computational Objectives

The computation targets a theoretical demonstration of destructive quantum interference (DQI) in AQ near Fermi level and uses it to rationalize why the conductance of AQ is lower than AC and AH. To that end, one needs to compute and compare the zero-bias transmission spectra T(E) for AC/AQ/AH, resolve the AQ antiresonance near Fermi level, and reproduce the qualitative conductance ordering. This minimal reproduction does not require finite-bias I–V modeling and does not rely on strict level-alignment corrections; the paper’s DFT+Σ step improves quantitative agreement with experiment but is not necessary to establish the mechanism “cross-conjugation induces DQI, which suppresses conductance.”

# 3\. Involved Systems

## System 1: AQ

 - Core Molecule:
    - abbreviation: AQ
	- full\_chemical\_name: 2,6-Bis[(4-acetylthiophenyl)ethynyl]-9,10-anthraquinone
    - core\_smiles: O=C1c2ccc(C#Cc3ccc(S)cc3)cc2C(=O)c2ccc(C#Cc3ccc(S)cc3)cc21
 - Anchors:
    - anchor_groups: ['Thiol_SH']
 - Electrodes:
    - electrode\_material: Au 
    - electrode\_surface: N/A
 - Interface:
    - interface\_geometry\_text: The molecules have two thiol terminals to connect to gold electrodes, presumably forming thiolate (S-Au) bonds.
 - Variation\_notes: "Cross-conjugated" core

## System 2: AC
 - Core Molecule:
	- abbreviation: AC
    - full\_chemical\_name: Anthracene-based wire with two thiolate termini
    - core\_smiles: Sc1ccc(C#Cc2ccc3cc4cc(C#Cc5ccc(S)cc5)ccc4cc3c2)cc1
 - Variation\_notes: "Linearly conjugated" core. Has the same length, anchors, and electrodes as System 1.

## System 3: AH
 - Core Molecule:
	- abbreviation: AH
    - full\_chemical\_name: 2,6-Bis[(4-acetylthiophenyl)ethynyl]-9,10-dihydroanthracene
    - core\_smiles: Sc1ccc(C#Cc2ccc3c(c2)Cc2ccc(C#Cc4ccc(S)cc4)cc2C3)cc1
 - Variation\_notes: "Broken conjugation" core. Has the same length, anchors, and electrodes as System 1.

# 4\. Applicability Assessment

**Applicable.**

The computational objective is only to compare the transmission spectra of different systems at zero bias; although the original paper employs DFT+Σ for quantitative alignment, the determination of the “trend and mechanism” does not rely on this step, and the problem can be reproduced with MST.

# 5\. Hierarchical Analysis

**Level: L1**

According to the QDHC hierarchical criteria, the core conclusion of this study is that the zero-bias transmission lineshape differences are determined by quantum interference induced by intramolecular cross-conjugation (i.e., by the molecule itself), without involving interface effects or non-equilibrium influences; therefore it maps to the **L1 level** (molecule-only + WBL constant coupling). Considering that the investigated system (the AQ system containing an anthraquinone unit) is not a simple conjugated system, the electronic-structure calculation should therefore employ the GFN-xTB method, which accounts for more key interactions.

# 6\. Input Preparation

This task will use the `L1_XTB` module, as the GFN-xTB method is more accurate than EHT and better suited for capturing the complex electronic structures and charge distributions (e.g., the push-pull character of AQ) discussed in the paper.

1. **Structure Files**:
 - `AQ.xyz`: Molecular structure file for the full AQ wire (core + linkers + thiol anchors).
 - `AC.xyz`: Molecular structure file for the full AC wire.
 - `AH.xyz`: Molecular structure file for the full AH wire.

2. **Anchor Atom Indices**:
 - The user must visually inspect each `.xyz` file (e.g., in VESTA or Multiwfn) to find the atom indices for the two Sulfur (S) atoms that serve as the left and right anchors. Let these be `[L_idx]` and `[R_idx]`.
 
3. **Key Parameters**:

 - **Method (`-m`)**: `1` (for GFN1-xTB, default).
 - **Coupling (`-C`)**: `1` (A reasonable starting value for S-Au coupling, as per the `L1_XTB` example).
 - **Energy Range (`--Erange`)**: `2` (To scan from $E_F - 2$ eV to $E_F + 2$ eV).
 - **Energy Points (`--Enum`)**: `1000` (For a high-resolution spectrum).

# 7\. Computational Workflow

## Goal：Compute and compare the zero-bias transmission spectra of AC/AQ/AH

## Step 1. Create directories
Create three separate directories matching the molecular systems and place the corresponding xyz files:

```
/AC/AC.xyz
/AQ/AQ.xyz
/AH/AH.xyz
```

## Step 2. Transport calculation
For each system, navigate into its directory and run the `L1_XTB` module. You must replace `[L_idx]` and `[R_idx]` with the correct sulfur atom indices identified in the preparation step.

**For AC:**

```bash
cd AC/
L1_XTB -f AC.xyz -L [L_idx] -R [R_idx] -C 1 --Erange 2 --Enum 1000
cd ..
```

**For AQ:**

```bash
cd AQ/
L1_XTB -f AQ.xyz -L [L_idx] -R [R_idx] -C 1 --Erange 2 --Enum 1000
cd ..
```

**For AH:**

```bash
cd AH/
L1_XTB -f AH.xyz -L [L_idx] -R [R_idx] -C 1 --Erange 2 --Enum 1000
cd ..
```

## Step 3. Post-processing and Analysis

Each calculation will generate a `Transmission.txt` and `Transmission.png` file in its respective directory.

1.  Collect the three `Transmission.txt` files (e.g., `AC/Transmission.txt`, `AQ/Transmission.txt`, `AH/Transmission.txt`).
2.  Use a plotting tool (e.g., Python/Matplotlib) to plot all three transmission spectra on a single graph with a logarithmic y-axis.
3.  Compare the plots. The T(E) for AQ should show a prominent anti-resonance (dip) between the HOMO and LUMO peaks, while the spectra for AC and AH should not. This dip explains the experimentally observed low conductance. 
