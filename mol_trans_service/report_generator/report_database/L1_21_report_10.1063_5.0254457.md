# 0\. Metadata

  - Title: Fano interference in single-molecule transistors
  - DOI: (Omit this part)

# 1\. Literature Summary

This is an 'experiment + computation' study investigating gate-controllable Fano interference in single-molecule transistors (SMTs). The authors fabricate three-terminal devices using molecules (DPSBF and DPFO) designed to have two interfering transport paths: a 'quasi-continuous state' along the molecular backbone and a 'discrete state' on a side group. The key experimental finding, obtained from 2D differential conductance maps ($G$ vs. $V_{sd}$ and $V_g$), is the observation of non-centrosymmetrical Fano patterns, which show a characteristic asymmetric peak and dip. The paper's first-principles (NEGF-DFT) calculations corroborate this by simulating the zero-bias transmission spectrum, which shows a characteristic asymmetric Fano lineshape resulting from the interference between the backbone (LUMO) and side-group (LUMO+2) orbitals.

# 2\. Computational Objectives

The primary computational objective is to theoretically reproduce the origin of the experimentally observed Fano interference. The goal is to compute the zero-bias transmission spectrum $T(E)$ for the DPSBF molecule. The expected result is to show that the spectrum exhibits a characteristic asymmetric Fano lineshape, which arises from the quantum interference between a broad, 'quasi-continuous' transport channel (associated with the backbone LUMO) and a 'discrete' channel (associated with the side-group LUMO+2). This calculation aims to validate the proposed two-pathway interference mechanism.

# 3\. Involved Systems

## System 1: DPSBF

  - Core Molecule:
      - abbreviation: DPSBF
      - full\_chemical\_name: 2,7-di(4-pyridyl)-9,9-spirobifluorene
      - core\_smiles: c1ccc2c(c1)-c1ccccc1C21c2cc(-c3ccncc3)ccc2-c2ccc(-c3ccncc3)cc21
  - Anchors:
      - anchor\_groups: ['Pyridine\_N']
  - Electrodes:
      - electrode\_material: Au
      - electrode\_surface: (111)
  - Interface:
      - interface\_geometry\_text: Pyridine-N binds to an Au adatom on the Au(111) surface (based on the paper's computational model in Fig. 4b).
  - Variation\_notes: "Main molecule (Devices 1 & 2). Has a biphenyl side group, which provides the discrete state."

## System 2: DPFO

  - Core Molecule:
      - abbreviation: DPFO
      - full\_chemical\_name: 2,7-di(pyridin-4-yl)-fluoren-9-one
      - core\_smiles: O=C1c2cc(-c3ccncc3)ccc2-c2ccc(-c3ccncc3)cc21
  - (Anchors, Electrodes, and Interface are the same as System 1)
  - Variation\_notes: "Secondary molecule (Device 3). Has a small oxygen side group, which provides a different discrete state."

# 4\. Applicability Assessment

**Applicable.**

The paper investigates a three-terminal gated device (SMT), which is out-of-scope for the two-terminal MST framework. However, the core *computational objective* is to reproduce the characteristic Fano lineshape in the *zero-bias* transmission spectrum ($T(E)$). This phenomenon is driven by the molecule's intrinsic electronic structure (interference between backbone and side-group orbitals) and is explicitly listed as an L1-level problem in the QDHC guide. MST L1 can compute the $T(E)$ spectrum, which is sufficient to identify the Fano resonance. The gating aspect ($G-V_g$ curve) is considered a post-processing step (rigid shift of the $T(E)$) and not part of the core transport calculation itself.

# 5\. Hierarchical Analysis

**Level: L1**

The core question is "Is transport governed primarily by the molecule’s intrinsic electronic structure?" The paper's key finding is a Fano resonance, which arises from quantum interference between two *molecular* pathways (backbone vs. side group). The QDHC guide explicitly identifies "Fano resonances" and "molecularly induced quantum interference" as L1 problems. The analysis relies on identifying the *shape* of the transmission spectrum (an asymmetric peak/dip), not its absolute alignment with $E_F$ (L3) or its dependence on specific contact geometries (L2). The paper's own computational analysis begins with the bare molecule's orbitals (Fig. 4a) to identify the interfering states, confirming this is a molecule-dominated problem.

# 6\. Input Preparation

Based on the L1 workflow, the user must prepare the molecular structure files and identify the anchor atoms. The `L1_XTB` module is appropriate given the use of DFT in the original paper.

1.  **Structure Files**: User-created `.xyz` files for the two molecules:
      - `dpsbf.xyz`
      - `dpfo.xyz`
2.  **Anchor Atom Indices**: The user must visualize each `.xyz` file to identify the atom indices of the two nitrogen anchors (one for the left electrode, one for the right) for both molecules.
3.  **Directory Structure**:
      - Create two directories: `dpsbf/` and `dpfo/`.
      - Place each `.xyz` file into its corresponding directory.

# 7\. Computational Workflow

## Goal:

Compute and compare the zero-bias $T(E)$ spectra for the DPSBF and DPFO molecules to identify the Fano resonance lineshapes.

## Step 1. Create directories and Prepare Inputs

Create the directory structure and place the corresponding user-created molecule `.xyz` files inside:

```
/dpsbf/dpsbf.xyz
/dpfo/dpfo.xyz
```

The user must determine the left and right anchor Nitrogen atom indices (e.g., `[N_left_idx]`, `[N_right_idx]`) for each file beforehand.

## Step 2. Run L1 Transport Calculation

Run the `L1_XTB` module in *each* of the two directories. A high number of energy points (`--Enum`) is recommended to resolve the sharp Fano feature.

1.  **For the `dpsbf` system:**
    ```bash
    cd dpsbf
    # Replace [N_left_idx] and [N_right_idx] with the correct indices
    L1_XTB -f dpsbf.xyz -L [N_left_idx] -R [N_right_idx] -m 2 --Erange 3 --Enum 1500
    cd ..
    ```
2.  **For the `dpfo` system:**
    ```bash
    cd dpfo
    # Replace [N_left_idx] and [N_right_idx] with the correct indices
    L1_XTB -f dpfo.xyz -L [N_left_idx] -R [N_right_idx] -m 2 --Erange 3 --Enum 1500
    cd ..
    ```
      - **Note**: We use `-m 2` for GFN2-xTB (closer to DFT) and `--Erange 3` to scan $E_F \pm 3$ eV, matching the paper's plot (Fig 4c).

## Step 3. Post-processing and Analysis

The workflow will generate `Transmission.txt` and `Transmission.png` in each directory.

1.  Collect the `Transmission.txt` file from both directories (`dpsbf/` and `dpfo/`).
2.  Use a plotting tool to plot the transmission data (y-axis in linear or log10 scale) from both files.
3.  Analyze the plots: Inspect the $T(E)$ spectra for the characteristic asymmetric Fano lineshapes (a sharp peak combined with a sharp dip) near the molecular frontier orbitals, as shown in the paper's Fig 4c.