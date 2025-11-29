# 0\. Metadata

  - Title: Molecular Heterojunctions of Oligo (phenylene ethynylene)s with Linear to Cruciform Framework
  - DOI: (Omit this part)

# 1\. Literature Summary

This is an 'experiment + computation' study investigating the effect of electron-donating substituents on the transport properties of oligo(phenylene ethynylene) (OPE) molecular wires. The authors use Self-Assembled Monolayers (SAMs) of three molecules (OPE3, OPE3-DTF, and OPE3-TTF) on Au substrates. Transport is measured using Conducting Probe-Atomic Force Microscopy (CP-AFM) with different metal tips (Ag, Au, Pt). The key experimental finding is that conductance follows the trend OPE3-TTF \> OPE3-DTF \> OPE3, regardless of the tip metal. This is attributed to the electron-donating DTF and TTF groups raising the HOMO energy level, bringing it closer to the electrode Fermi level. A secondary finding is that significant rectification is observed only for asymmetric junctions (e.g., Ag tip on Au substrate) due to the large work function difference. The paper's computations (DFT) focus on calculating the zero-bias transmission $T(E)$ for single-molecule Au-Molecule-Au junctions, which successfully reproduce the experimental conductance trend by showing the substituent-induced shift of the HOMO level.

# 2\. Computational Objectives

The primary computational objective is to reproduce the key theoretical finding: the modulation of zero-bias conductance by chemical substitution. The goal is to compute the zero-bias transmission spectra $T(E)$ for the three systems (OPE3, OPE3-DTF, OPE3-TTF) and align them to the electrode Fermi level ($E_F$). The expected result is to show that the HOMO-derived transport resonance shifts progressively closer to $E_F$ (from below) in the order OPE3 \< OPE3-DTF \< OPE3-TTF. This shift should result in an increase in the transmission at the Fermi level ($T(E_F)$), thereby explaining the experimentally observed conductance trend: $G_{OPE3} < G_{OPE3-DTF} < G_{OPE3-TTF}$.

# 3\. Involved Systems

## System 1: OPE3

  - Core Molecule:
      - abbreviation: OPE3
      - full\_chemical\_name: N/A
      - core\_smiles: Sc1ccc(C#Cc2ccc(C#Cc3ccc(S)cc3)cc2)cc1
  - Anchors:
      - anchor\_groups: ['Thiolate\_S-']
  - Electrodes:
      - electrode\_material: Au
      - electrode\_surface: (111)
  - Interface:
      - interface\_geometry\_text: Thiolate-S binds to an Au(111) surface. The paper's computation models this using two Au(111) slabs with the anchor at an FCC hollow site.
  - Variation\_notes: "Baseline (unsubstituted) linear OPE3 molecule."

## System 2: OPE3-DTF

  - Core Molecule:
      - abbreviation: OPE3-DTF
      - full\_chemical\_name: N/A
      - core\_smiles: CCCC(=O)OC1=C(OC(=O)CCC)SC(=Cc2cc(C#Cc3ccc(S)cc3)ccc2C#Cc2ccc(S)cc2)S1
  - (Anchors, Electrodes, and Interface are the same as System 1)
  - Variation\_notes: "Cruciform molecule with one electron-donating DTF substituent."

## System 3: OPE3-TTF

  - Core Molecule:
      - abbreviation: OPE3-TTF
      - full\_chemical\_name: N/A
      - core\_smiles: CCCC(=O)OC1=C(OC(=O)CCC)SC(=Cc2cc(C#Cc3ccc(S)cc3)c(C=C3SC(OC(=O)CCC)=C(OC(=O)CCC)S3)cc2C#Cc2ccc(S)cc2)S1
  - (Anchors, Electrodes, and Interface are the same as System 1)
  - Variation\_notes: "Cruciform molecule with two electron-donating DTF substituents (forming a TTF-like core)."

# 4\. Applicability Assessment

**Applicable.**

The original paper investigates SAMs (an ensemble effect, which is out-of-scope) and rectification due to *asymmetric electrodes* (Ag vs. Au, also out-of-scope). However, the *core computational objective* is to explain the *conductance trend* in symmetric Au-Molecule-Au junctions, which the paper's own DFT calculations model as a single-molecule problem. This objective relies on identifying the *relative* alignment of the HOMO level with the electrode $E_F$. This is a level-alignment problem, which is precisely what the QDHC L3 scheme is designed to address. MST L3 can be used to adapt the problem to a single-molecule junction and compute the $T(E)$ spectra relative to $E_F$ to reproduce the qualitative trend of the HOMO-level shift.

# 5\. Hierarchical Analysis

**Level: L3**

The core question is "How do chemical substituents (DTF, TTF) shift the molecular orbital alignment relative to the electrode Fermi level, and how does this affect zero-bias conductance?" This is fundamentally a problem of molecular level alignment. The key analytical evidence in the paper (Figure 5a) is a $T(E)$ spectrum plotted relative to $E-E_F=0$. The QDHC guide explicitly states that L3 is required for problems governed by level alignment and lists "T(E) spectra referenced to the electrode Fermi level (E−E\_F=0) that explicitly identify the conducting channel" as the key evidence. L1 or L2 cannot provide this proper alignment relative to the bulk electrode $E_F$.

# 6\. Input Preparation

Based on the L3 workflow, three full junction structures must be manually created from MST templates. The paper's computational model (thiolate on Au(111) FCC hollow site) is best represented by the MST trimer or pyramid template. We will use the trimer template, following the precedent of other thiolate-on-Au(111) examples.

1.  **MST Template**: The `[MST_root]/share/device/junction_trimer_...xyz` template will be used.
2.  **User-Created Junction Files (`.xyz`)**:
      - Create `junction_trimer_ope3.xyz`: Replace the placeholder molecule in the trimer template with the OPE3 molecule.
      - Create `junction_trimer_ope3dtf.xyz`: Replace the placeholder with the OPE3-DTF molecule.
      - Create `junction_trimer_ope3ttf.xyz`: Replace the placeholder with the OPE3-TTF molecule.
3.  **Conversion Script**: The `xyz2POSCAR.py` script (from `[MST_root]/share/`) is required.
4.  **Directory Structure**:
      - Create three directories: `ope3/`, `ope3dtf/`, `ope3ttf/`.
      - Place each corresponding `junction_trimer_...xyz` file into its respective directory.

# 7\. Computational Workflow

## Goal:

Compute and compare the zero-bias $T(E)$ spectra for the OPE3, OPE3-DTF, and OPE3-TTF systems, aligned to the electrode $E_F$.

## Step 1. Create directories and Prepare Inputs

Create the directory structure and place the corresponding user-created junction `.xyz` files inside:

```
/ope3/junction_trimer_ope3.xyz
/ope3dtf/junction_trimer_ope3dtf.xyz
/ope3ttf/junction_trimer_ope3ttf.xyz
```

## Step 2. Convert to POSCAR

Run the `xyz2POSCAR.py` conversion script in *each* of the three directories.

1.  **For the `ope3` system:**
    ```bash
    cd ope3
    # Copy xyz2POSCAR.py from [MST_root]/share/ into this directory
    # Edit xyz2POSCAR.py: set xyz_filename = 'junction_trimer_ope3.xyz'
    python xyz2POSCAR.py
    cd ..
    ```
2.  **For the `ope3dtf` system:**
    ```bash
    cd ope3dtf
    # Copy and edit xyz2POSCAR.py: set xyz_filename = 'junction_trimer_ope3dtf.xyz'
    python xyz2POSCAR.py
    cd ..
    ```
3.  **For the `ope3ttf` system:**
    ```bash
    cd ope3ttf
    # Copy and edit xyz2POSCAR.py: set xyz_filename = 'junction_trimer_ope3ttf.xyz'
    python xyz2POSCAR.py
    cd ..
    ```
      - This generates `POSCAR` and `EM_atom.txt` in each of the three directories.

## Step 3. Run L3 Transport Calculation

Run the interactive `L3_Trans` module in *each* of the three directories.

1.  **For the `ope3` system:**
    ```bash
    cd ope3
    L3_Trans
    ```
      - Follow the interactive prompts:
          - `Enter POSCAR file name(...)`: `POSCAR`
          - `Specify the energy range (...)`: `2` (This scans $E_F \pm 2$ eV, matching the paper's Fig 5a)
          - `Specify the energy interval (...)`: `0.01`
    <!-- end list -->
    ```bash
    cd ..
    ```
2.  **Repeat this exact process** for the `ope3dtf/` directory.
3.  **Repeat this exact process** for the `ope3ttf/` directory, ensuring the *exact same* energy range and interval are used.

## Step 4. Post-processing and Analysis

The workflow will generate `Transmission.txt` in all three directories, with the Fermi level aligned to 0 eV.

1.  Collect the `Transmission.txt` file from all three directories (`ope3/`, `ope3dtf/`, `ope3ttf/`).
2.  Use a plotting tool to plot the transmission data (y-axis in log10 scale) from all three files on the same graph.
3.  Analyze the plot:
      - Verify that the main transmission peak below $E_F=0$ (the HOMO resonance) shifts closer to 0 in the order: OPE3 \< OPE3-DTF \< OPE3-TTF.
      - Verify that the transmission value *at* $E_F=0$ follows the trend: OPE3 \< OPE3-DTF \< OPE3-TTF.