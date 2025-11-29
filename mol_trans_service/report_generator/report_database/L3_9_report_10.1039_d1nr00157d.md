# 0\. Metadata

  - Title: Electrostatic gating of single-molecule junctions based on the STM-BJ technique
  - DOI: (Omit this part)

# 1\. Literature Summary

This is an 'experiment + computation' study. The authors use a modified scanning tunneling microscope break-junction (STM-BJ) technique with a back-gated substrate to measure how an electrostatic gate voltage ($V_g$) tunes the conductance of single-molecule junctions. The study focuses on three biphenyl-based molecules with different anchors: thiomethyl (M1), pyridine (M2), and cyano (M3). The key experimental finding is that the conductance of HOMO-dominated molecules (M1) *decreases* with increasing (more positive) $V_g$, while the conductance of LUMO-dominated molecules (M2, M3) shows the opposite trend. The paper's DFT calculations provide zero-bias transmission spectra to support this, computationally identifying M1 as a HOMO-conductor and M2/M3 as LUMO-conductors, which explains their opposing responses to the gate-induced orbital shift.

# 2\. Computational Objectives

The primary computational objective is to reproduce the paper's theoretical validation for its experimental findings: the determination of the dominant transport channel (HOMO vs. LUMO) for the three different molecular junctions at zero bias. The goal is to compute the zero-bias transmission spectra $T(E)$ for M1, M2, and M3, aligning them to the electrode Fermi level ($E_F$). The expected result is to show that for M1, the HOMO-derived resonance is the closest transport channel to $E_F$ (from below), while for M2 and M3, the LUMO-derived resonance is the closest channel (from above). This alignment explains *why* they respond differently to the electrostatic gate.

# 3\. Involved Systems

## System 1: M1 (Thiomethyl-Biphenyl)

  - Core Molecule:
      - abbreviation: M1
      - full\_chemical\_name: N/A
      - core\_smiles: CSc1ccc(-c2ccc(-c3ccc(SC)cc3)cc2)cc1
  - Anchors:
      - anchor\_groups: ['Methylthio\_SCH3']
  - Electrodes:
      - electrode\_material: Au
      - electrode\_surface: (111)
  - Interface:
      - interface\_geometry\_text: S atom in methylthio binds to an Au trimer on the Au(111) surface.
  - Variation\_notes: "HOMO-conducting system."

## System 2: M2 (Pyridine-Biphenyl)

  - Core Molecule:
      - abbreviation: M2
      - full\_chemical\_name: N/A (4,4'-bipyridine)
      - core\_smiles: c1cc(-c2ccc(-c3ccncc3)cc2)ccn1
  - Anchors:
      - anchor\_groups: ['Pyridine\_N']
  - Electrodes:
      - electrode\_material: Au
      - electrode\_surface: (111)
  - Interface:
      - interface\_geometry\_text: Pyridine-N binds to an Au adatom on the Au(111) surface.
  - Variation\_notes: "LUMO-conducting system."

## System 3: M3 (Cyano-Biphenyl)

  - Core Molecule:
      - abbreviation: M3
      - full\_chemical\_name: N/A
      - core\_smiles: N#Cc1ccc(-c2ccc(-c3ccc(C#N)cc3)cc2)cc1
  - Anchors:
      - anchor\_groups: ['Cyano\_CN']
  - Electrodes:
      - electrode\_material: Au
      - electrode\_surface: (111)
  - Interface:
      - interface\_geometry\_text: Cyano-N binds to an Au adatom on the Au(111) surface.
  - Variation\_notes: "LUMO-conducting system."

# 4\. Applicability Assessment

**Applicable.**

The main experimental phenomenon (electrostatic gating in a three-terminal device) is out-of-scope for the QDHC framework. However, the *core computational objective* is to reproduce the paper's supporting DFT calculations (Fig 4d), which are standard two-terminal, zero-bias transmission spectra used to identify the dominant transport channel (HOMO vs. LUMO). This is fundamentally a question of **molecular level alignment with the electrode Fermi level**, which is precisely the problem the QDHC L3 scheme is designed to address. MST L3 can compute the $T(E)$ spectra relative to $E_F$ to reproduce this key qualitative finding.

# 5\. Hierarchical Analysis

**Level: L3**

The core question is "Is transport through M1, M2, and M3 junctions governed by the HOMO or the LUMO?" This is fundamentally a problem of molecular level alignment. The key analytical evidence in the paper (Figure 4d) is a set of $T(E)$ spectra plotted relative to $E-E_F^{DFT}=0$. The QDHC guide explicitly states that L3 is required for problems governed by level alignment and lists "T(E) spectra referenced to the electrode Fermi level (E−E\_F=0) that explicitly identify the conducting channel" as the key evidence. L1 or L2 cannot provide this proper alignment relative to the bulk electrode $E_F$.

# 6\. Input Preparation

Based on the L3 workflow and the paper's computational models (Fig 4a-c), three full junction structures must be manually created from different MST templates.

1.  **MST Templates**:
      - For M1: `[MST_root]/share/device/junction_trimer_...xyz` (to match Fig 4a).
      - For M2 & M3: `[MST_root]/share/device/junction_adatom_...xyz` (to match Fig 4b, 4c).
2.  **User-Created Junction Files (`.xyz`)**:
      - Create `junction_trimer_m1.xyz`: Replace the placeholder molecule in the trimer template with the M1 molecule.
      - Create `junction_adatom_m2.xyz`: Replace the placeholder molecule in the adatom template with the M2 molecule.
      - Create `junction_adatom_m3.xyz`: Replace the placeholder molecule in the adatom template with the M3 molecule.
3.  **Conversion Script**: The `xyz2POSCAR.py` script (from `[MST_root]/share/`) is required.
4.  **Directory Structure**:
      - Create three directories: `m1_trimer/`, `m2_adatom/`, `m3_adatom/`.
      - Place each corresponding `junction_...xyz` file into its respective directory.

# 7\. Computational Workflow

## Goal:

Compute and compare the zero-bias $T(E)$ spectra for the M1, M2, and M3 systems, aligned to the electrode $E_F$.

## Step 1. Create directories and Prepare Inputs

Create the directory structure and place the corresponding user-created junction `.xyz` files inside:

```
/m1_trimer/junction_trimer_m1.xyz
/m2_adatom/junction_adatom_m2.xyz
/m3_adatom/junction_adatom_m3.xyz
```

## Step 2. Convert to POSCAR

Run the `xyz2POSCAR.py` conversion script in *each* of the three directories.

1.  **For the `m1_trimer` system:**
    ```bash
    cd m1_trimer
    # Copy xyz2POSCAR.py from [MST_root]/share/ into this directory
    # Edit xyz2POSCAR.py: set xyz_filename = 'junction_trimer_m1.xyz'
    python xyz2POSCAR.py
    cd ..
    ```
2.  **For the `m2_adatom` system:**
    ```bash
    cd m2_adatom
    # Copy and edit xyz2POSCAR.py: set xyz_filename = 'junction_adatom_m2.xyz'
    python xyz2POSCAR.py
    cd ..
    ```
3.  **For the `m3_adatom` system:**
    ```bash
    cd m3_adatom
    # Copy and edit xyz2POSCAR.py: set xyz_filename = 'junction_adatom_m3.xyz'
    python xyz2POSCAR.py
    cd ..
    ```
      - This generates `POSCAR` and `EM_atom.txt` in each of the three directories.

## Step 3. Run L3 Transport Calculation

Run the interactive `L3_Trans` module in *each* of the three directories.

1.  **For the `m1_trimer` system:**
    ```bash
    cd m1_trimer
    L3_Trans
    ```
      - Follow the interactive prompts:
          - `Enter POSCAR file name(...)`: `POSCAR`
          - `Specify the energy range (...)`: `3` (This scans $E_F \pm 3$ eV, matching the paper's Fig 4d range)
          - `Specify the energy interval (...)`: `0.01`
    <!-- end list -->
    ```bash
    cd ..
    ```
2.  **Repeat this exact process** for the `m2_adatom/` directory.
3.  **Repeat this exact process** for the `m3_adatom/` directory, ensuring the *exact same* energy range and interval are used.

## Step 4. Post-processing and Analysis

The workflow will generate `Transmission.txt` in all three directories, with the Fermi level aligned to 0 eV.

1.  Collect the `Transmission.txt` file from all three directories (`m1_trimer/`, `m2_adatom/`, `m3_adatom/`).
2.  Use a plotting tool to plot the transmission data (y-axis in log10 scale) from all three files on the same graph.
3.  Analyze the plot:
      - Verify that for M1, the dominant transmission peak (originating from the HOMO) is located at an energy $E < 0$ (i.e., below the Fermi level).
      - Verify that for M2 and M3, the dominant transmission peak (originating from the LUMO) is located at an energy $E > 0$ (i.e., above the Fermi level).
      - This analysis will confirm the computationally determined dominant transport channel for each molecule.