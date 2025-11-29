# 0\. Metadata

  - Title: Single-molecule diodes with high rectification ratios through environmental control
  - DOI: (Omit this part)

# 1\. Literature Summary

This is an 'experiment + computation' study investigating a novel mechanism for achieving high rectification in single-molecule junctions. The authors use an STM-BJ setup with symmetric Au electrodes and symmetric molecules (e.g., TDO oligomers). The key finding is that high rectification (R \> 200) is induced by breaking the junction symmetry *environmentally*: an insulated tip ($\sim1~\mu m^{2}$ area) and a large-area substrate ($> 1~cm^{2}$) in a polar, ion-containing solvent (Propylene Carbonate) create an asymmetric electric double layer. This asymmetry in the electrostatic environment causes the molecular energy levels to shift asymmetrically under an applied bias (a bias-dependent Stark shift), leading to rectification. The paper supports this model by showing that LUMO-conducting (4,4'-bipyridine, TDO) and HOMO-conducting (4-4"-diamino-p-terphenyl) molecules rectify in opposite directions, as predicted. The computational part (DFT+$\Sigma$) is used to validate the model's assumptions by identifying the dominant transport channels (HOMO/LUMO) and their zero-bias alignment.

# 2\. Computational Objectives

The primary rectification mechanism—an asymmetric potential drop from an environmental electric double layer—is out-of-scope for standard MST workflows.

Therefore, the computational objective is redefined to reproduce the paper's *prerequisite* theoretical finding: the identification of the dominant transport channel (HOMO vs. LUMO) for the different molecular backbones, which the paper uses to explain the *direction* of rectification. The goal is to compute the zero-bias transmission spectra $T(E)$ for 4,4'-bipyridine (molecule **1**) and 4-4"-diamino-p-terphenyl (molecule **2**) and align them to the electrode Fermi level ($E_F$). The expected result is to show that molecule **1** is LUMO-conducting (LUMO-derived resonance is closest to $E_F$) and molecule **2** is HOMO-conducting (HOMO-derived resonance is closest to $E_F$).

# 3\. Involved Systems

## System 1: 4,4'-bipyridine

  - Core Molecule:
      - abbreviation: 1
      - full\_chemical\_name: 4,4'-bipyridine
      - core\_smiles: N/A
  - Anchors:
      - anchor\_groups: ['Pyridine\_N']
  - Electrodes:
      - electrode\_material: Au
      - electrode\_surface: (111)
  - Interface:
      - interface\_geometry\_text: Pyridine-N binds to an undercoordinated Au site. The paper's DFT uses Au(111) layers; this is modeled using an Au adatom on the Au(111) surface.
  - Variation\_notes: "LUMO-conducting system."

## System 2: 4-4"-diamino-p-terphenyl

  - Core Molecule:
      - abbreviation: 2
      - full\_chemical\_name: 4-4"-diamino-p-terphenyl
      - core\_smiles: N/A
  - Anchors:
      - anchor\_groups: ['Amine\_NH2']
  - Electrodes:
      - electrode\_material: Au
      - electrode\_surface: (111)
  - Interface:
      - interface\_geometry\_text: Amine-N binds to an undercoordinated Au site, modeled using an Au adatom on the Au(111) surface.
  - Variation\_notes: "HOMO-conducting system."

# 4\. Applicability Assessment

**Applicable.**

The original paper's primary phenomenon (rectification from an asymmetric environmental double layer) and its computational method (DFT+$\Sigma$) are both out-of-scope per the QDHC guide.

However, the *redefined computational objective* is to reproduce the paper's zero-bias analysis, which identifies the dominant transport channel (HOMO vs. LUMO) for different molecules. This is a question of **molecular level alignment with the electrode Fermi level**, which is precisely the problem the QDHC L3 scheme is designed to address. MST L3 uses DFTB+ and pre-calculated Surface Green's Functions (SGF) to achieve a proper, qualitative alignment of the molecular orbitals relative to the electrode $E_F$. This is sufficient to reproduce the key qualitative finding of whether the HOMO or LUMO is the closest transport channel.

# 5\. Hierarchical Analysis

**Level: L3**

The problem maps to L3. The core question is "Is transport governed primarily by the HOMO or the LUMO?" This is fundamentally a question of *where* the respective frontier orbitals lie relative to the gold $E_F$. The paper's entire model for rectification direction relies on this distinction. The QDHC guide explicitly states that L3 is required for problems governed by "molecular level alignment with the electrode Fermi level" and is used to "explicitly identify the conducting channel relative to $E_F$." L1 or L2 cannot provide this proper alignment relative to the bulk electrode $E_F$.

# 6\. Input Preparation

Based on the L3 workflow, the user must prepare two full junction structure files based on MST templates. The adatom interface is a common model for both pyridine and amine linkers and will be used here.

1.  **User-Created Junction Files (`.xyz`)**:
      - Create `junction_adatom_m1.xyz`: Modify an L3 adatom template from `[MST_root]/share/device/` (e.g., `junction_example_adatom_...xyz`) by replacing the placeholder molecule with molecule **1** (4,4'-bipyridine).
      - Create `junction_adatom_m2.xyz`: Modify a corresponding L3 adatom template (e.g., `junction_example_adatom_amine.xyz`) by replacing the placeholder molecule with molecule **2** (4-4"-diamino-p-terphenyl).
2.  **Conversion Script**:
      - The `xyz2POSCAR.py` script (from `[MST_root]/share/`) is required for conversion.
3.  **Directory Structure**:
      - Create two separate directories: `m1_adatom/` and `m2_adatom/`.
      - Place `junction_adatom_m1.xyz` in the first directory and `junction_adatom_m2.xyz` in the second.

# 7\. Computational Workflow

## Goal:

Compute and compare the zero-bias $T(E)$ spectra for the pyridine-linked (Molecule 1) and amine-linked (Molecule 2) junctions, aligned to the electrode $E_F$.

## Step 1. Create directories and Prepare Inputs

Create the directory structure and place the corresponding user-created junction `.xyz` files inside:

```
/m1_adatom/junction_adatom_m1.xyz
/m2_adatom/junction_adatom_m2.xyz
```

## Step 2. Convert to POSCAR

Run the `xyz2POSCAR.py` conversion script in *each* of the two directories.

1.  **For the `m1_adatom` system:**

    ```bash
    cd m1_adatom
    # Copy xyz2POSCAR.py from [MST_root]/share/ into this directory
    # Edit xyz2POSCAR.py: set xyz_filename = 'junction_adatom_m1.xyz'
    python xyz2POSCAR.py
    cd ..
    ```

      - This generates `POSCAR` and `EM_atom.txt` in the `m1_adatom` directory.

2.  **For the `m2_adatom` system:**

    ```bash
    cd m2_adatom
    # Copy and edit xyz2POSCAR.py: set xyz_filename = 'junction_adatom_m2.xyz'
    python xyz2POSCAR.py
    cd ..
    ```

      - This generates `POSCAR` and `EM_atom.txt` in the `m2_adatom` directory.

## Step 3. Run L3 Transport Calculation

Run the interactive `L3_Trans` module in *each* of the two directories.

1.  **For the `m1_adatom` system:**

    ```bash
    cd m1_adatom
    L3_Trans
    ```

      - Follow the interactive prompts:
          - `Enter POSCAR file name(...)`: `POSCAR`
          - `Specify the energy range (...)`: `3` (This scans $E_F \pm 3$ eV, a reasonable range)
          - `Specify the energy interval (...)`: `0.01`

    <!-- end list -->

    ```bash
    cd ..
    ```

2.  **Repeat this process** for the `m2_adatom` directory, ensuring the *exact same* energy range and interval are used for a valid comparison.

## Step 4. Post-processing and Analysis

The workflow will generate `Transmission.txt` and `Transmission.png` in both directories. In these files, the Fermi level is aligned to 0 eV.

1.  Use a plotting tool to load data from `m1_adatom/Transmission.txt` and `m2_adatom/Transmission.txt`. Plot them on the same graph (y-axis in log10 scale).
2.  Analyze the plots:
      - Verify that for Molecule 1 (pyridine-linked), the dominant transmission peak (originating from the LUMO) is located at an energy $E > 0$ (i.e., above the Fermi level).
      - Verify that for Molecule 2 (amine-linked), the dominant transmission peak (originating from the HOMO) is located at an energy $E < 0$ (i.e., below the Fermi level).
      - This analysis will confirm the computationally determined dominant transport channel for each linker type, reproducing the paper's theoretical premise.