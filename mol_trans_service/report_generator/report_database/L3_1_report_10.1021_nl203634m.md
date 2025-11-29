# 0\. Metadata

  - Title: Simultaneous Determination of Conductance and Thermopower of Single Molecule Junctions
  - DOI: (Omit this part)

# 1\. Literature Summary

This is an 'experiment + computation' study. The authors use a modified scanning tunneling microscope-based break-junction (STM-BJ) technique, which applies a temperature gradient, to measure junction properties, including conductance (G) and Seebeck coefficient (S). The primary goal is to identify the dominant transport channel (HOMO or LUMO) for two main classes of molecules: amine-Au linked molecules (e.g., 4,4'-diaminostilbene, **1**) and pyridine-Au linked molecules (e.g., 4,4'-bipyridine, **4**). Experimentally, they use the sign of the Seebeck coefficient to identify amine-linked molecules as HOMO conductors (S \> 0) and pyridine-linked molecules as LUMO conductors (S \< 0). This finding is supported by self-energy corrected density functional theory (DFT+$\Sigma$) calculations, which show that for amine-linked junctions, the HOMO-derived resonance is the closest transport channel to the Fermi level ($E_F$), while for pyridine-linked junctions, the LUMO-derived resonance is the closest.

# 2\. Computational Objectives

The primary computational objective, as redefined for this report, is to theoretically determine and validate the dominant transport channel (HOMO vs. LUMO) for the two different junction types (amine-linked vs. pyridine-linked). The calculation must compute the zero-bias transmission spectrum, $T(E)$, for both systems and, crucially, align it with the electrode Fermi level ($E_F$). The expected result is to show that for the amine-linked molecule **1**, the transmission spectrum features a HOMO-derived resonance just below $E_F$ (making it the dominant channel). In contrast, for the pyridine-linked molecule **4**, the LUMO-derived resonance should be the closest feature to $E_F$ (just above it), confirming it as the dominant channel.

# 3\. Involved Systems

## System 1: Molecule 1 (Amine-linked)

  - Core Molecule:
      - abbreviation: 1
      - full\_chemical\_name: 4,4'-diaminostilbene
      - core\_smiles: [N]c1ccc(C=Cc2ccc([N])cc2)cc1
  - Anchors:
      - anchor\_groups: ['Amine\_NH2']
  - Electrodes:
      - electrode\_material: Au
      - electrode\_surface: (111)
  - Interface:
      - interface\_geometry\_text: Amine-N binds to an undercoordinated Au site. The paper models this using either an Au adatom or an Au trimer on the Au(111) surface.
  - Variation\_notes: "HOMO-conducting system."

## System 2: Molecule 4 (Pyridine-linked)

  - Core Molecule:
      - abbreviation: 4
      - full\_chemical\_name: 4,4'-bipyridine
      - core\_smiles: c1cc(-c2ccncc2)ccn1
  - Anchors:
      - anchor\_groups: ['Pyridine\_N']
  - Electrodes:
      - electrode\_material: Au
      - electrode\_surface: (111)
  - Interface:
      - interface\_geometry\_text: Pyridine-N binds to an undercoordinated Au site. The paper models this using either an Au adatom or an Au trimer on the Au(111) surface.
  - Variation\_notes: "LUMO-conducting system."

# 4\. Applicability Assessment

**Applicable.**

While the original paper's primary metric (Seebeck coefficient) is out-of-scope for MST, the redefined objective is to identify the dominant transport channel (HOMO vs. LUMO). This is a question of **molecular level alignment with the electrode Fermi level**, which is precisely the problem the QDHC L3 scheme is designed to address. The original paper used DFT+$\Sigma$ (a self-energy correction method) to achieve quantitative alignment. The MST L3 scheme uses DFTB+ and pre-calculated Surface Green's Functions (SGF) to achieve a proper, qualitative alignment of the molecular orbitals relative to the electrode $E_F$. This is sufficient to reproduce the key qualitative finding of whether the HOMO or LUMO is the closest transport channel.

# 5\. Hierarchical Analysis

**Level: L3**

The problem maps to L3. The core question is "Is transport governed primarily by molecular level alignment with the electrode Fermi level?" The distinction between molecule **1** (HOMO-conducting) and molecule **4** (LUMO-conducting) is not an intrinsic property (L1) nor an interface-coupling-geometry property (L2), but fundamentally a question of *where* the respective frontier orbitals lie relative to the gold $E_F$. The paper's computational evidence (Figure 4) is a $T(E)$ spectrum plotted relative to $E-E_F=0$, which is the exact output of an L3 calculation. This analysis is required to "explicitly identify the conducting channel relative to $E_F$."

# 6\. Input Preparation

Based on the L3 workflow, the user must prepare two full junction structure files based on MST templates, then convert them to `POSCAR` format. The paper investigates adatom and trimer interfaces; the adatom interface is a common model and will be used here.

1.  **User-Created Junction Files (`.xyz`)**:
      - Create `junction_adatom_m1.xyz`: Modify an L3 adatom template from `[MST_root]/share/device/` (e.g., `junction_example_adatom_amine.xyz`) by replacing the placeholder molecule with molecule **1** (4,4'-diaminostilbene).
      - Create `junction_adatom_m4.xyz`: Modify a corresponding L3 adatom template by replacing the placeholder molecule with molecule **4** (4,4'-bipyridine).
2.  **Conversion Script**:
      - The `xyz2POSCAR.py` script (from `[MST_root]/share/`) is required for conversion.
3.  **Directory Structure**:
      - Create two separate directories: `m1_adatom/` and `m4_adatom/`.
      - Place `junction_adatom_m1.xyz` in the first directory and `junction_adatom_m4.xyz` in the second.

# 7\. Computational Workflow

## Goal:

Compute and compare the zero-bias $T(E)$ spectra for the amine-linked (Molecule 1) and pyridine-linked (Molecule 4) junctions, aligned to the electrode $E_F$.

## Step 1. Create directories and Prepare Inputs

Create the directory structure and place the corresponding user-created junction `.xyz` files inside:

```
/m1_adatom/junction_adatom_m1.xyz
/m4_adatom/junction_adatom_m4.xyz
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

2.  **For the `m4_adatom` system:**

    ```bash
    cd m4_adatom
    # Copy and edit xyz2POSCAR.py: set xyz_filename = 'junction_adatom_m4.xyz'
    python xyz2POSCAR.py
    cd ..
    ```

      - This generates `POSCAR` and `EM_atom.txt` in the `m4_adatom` directory.

## Step 3. Run L3 Transport Calculation

Run the interactive `L3_Trans` module in *each* of the two directories.

1.  **For the `m1_adatom` system:**

    ```bash
    cd m1_adatom
    L3_Trans
    ```

      - Follow the interactive prompts:
          - `Enter POSCAR file name(...)`: `POSCAR`
          - `Specify the energy range (...)`: `3` (This scans $E_F \pm 3$ eV, matching the paper's plot range)
          - `Specify the energy interval (...)`: `0.01`

    <!-- end list -->

    ```bash
    cd ..
    ```

2.  **Repeat this process** for the `m4_adatom` directory, ensuring the *exact same* energy range and interval are used for a valid comparison.

## Step 4. Post-processing and Analysis

The workflow will generate `Transmission.txt` and `Transmission.png` in both directories. In these files, the Fermi level is aligned to 0 eV.

1.  Use a plotting tool to load data from `m1_adatom/Transmission.txt` and `m4_adatom/Transmission.txt`. Plot them on the same graph (y-axis in log10 scale).
2.  Analyze the plots:
      - Verify that for Molecule 1 (amine-linked), the dominant transmission peak (originating from the HOMO) is located at an energy $E < 0$ (i.e., below the Fermi level).
      - Verify that for Molecule 4 (pyridine-linked), the dominant transmission peak (originating from the LUMO) is located at an energy $E > 0$ (i.e., above the Fermi level).
      - This analysis will confirm the computationally determined dominant transport channel for each linker type.