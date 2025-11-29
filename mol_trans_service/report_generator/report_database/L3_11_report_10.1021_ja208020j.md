# 0\. Metadata

  - Title: Highly Conducting π-Conjugated Molecular Junctions Covalently Bonded to Gold Electrodes
  - DOI: (Omit this part)

# 1\. Literature Summary

This is an 'experiment + computation' study. The authors use the scanning tunneling microscope-based break-junction (STM-BJ) technique to measure the conductance of a series of methylene-terminated oligophenyl molecules (P1-P4) that form direct Au-C covalent bonds with gold electrodes. The key experimental finding is that these junctions are highly conducting; the shortest molecule (P1, p-xylylene) shows a conductance approaching one conductance quantum (1 $G_0$). For longer molecules (P2-P4), the conductance exhibits a clear exponential decay with length, characteristic of tunneling. The paper's density functional theory (DFT)-based transport calculations support these findings by showing that P1 exhibits near-resonant transmission, with the Fermi level ($E_F$) positioned just above the main transport resonance. For the longer P2-P4 series, this resonance moves further from $E_F$, leading to a drop in transmission at $E_F$ and a transition to the tunneling regime.

# 2\. Computational Objectives

The primary computational objective is to theoretically reproduce the observed conductance trend and explain the origin of the high conductance in P1. The goal is to compute the zero-bias transmission spectrum, $T(E)$, for the four systems (P1, P2, P3, P4) and, crucially, align them with the electrode Fermi level ($E_F$). The expected result is to show that for P1, a strong transmission resonance is located very close to $E_F$ (near-resonant transport), resulting in high conductance. For the longer molecules (P2-P4), the transmission *at* the Fermi level ($T(E_F)$) should decrease systematically, explaining the exponential decay in conductance.

# 3\. Involved Systems

## System 1: P1

  - Core Molecule:
      - abbreviation: P1
      - full\_chemical\_name: 1,4-dimethylenebenzene (p-xylylene)
      - core\_smiles: Cc1ccc(C)cc1
  - Anchors:
      - anchor\_groups: ['Alkyl\_C']
  - Electrodes:
      - electrode\_material: Au
      - electrode\_surface: N/A
  - Interface:
      - interface\_geometry\_text: Direct Au-C covalent bond. The terminal methylene-C binds directly to the Au electrode. The paper's calculation notes a minimum energy configuration with a 90-degree angle between the Au-C bond and the phenyl plane.
  - Variation\_notes: "Shortest oligophenyl (n=1), p-xylylene. Near-resonant transport."

## System 2: P2

  - Core Molecule:
      - abbreviation: P2
      - full\_chemical\_name: 4,4'-dimethylenebiphenyl
      - core\_smiles: Cc1ccc(-c2ccc(C)cc2)cc1
  - (Anchors, Electrodes, and Interface are the same as System 1)
  - Variation\_notes: "Oligophenyl, n=2."

## System 3: P3

  - Core Molecule:
      - abbreviation: P3
      - full\_chemical\_name: 4,4''-dimethylene-p-terphenyl
      - core\_smiles: Cc1ccc(-c2ccc(-c3ccc(C)cc3)cc2)cc1
  - (Anchors, Electrodes, and Interface are the same as System 1)
  - Variation\_notes: "Oligophenyl, n=3."

## System 4: P4

  - Core Molecule:
      - abbreviation: P4
      - full\_chemical\_name: 4,4'''-dimethylene-p-tetraphenyl
      - core\_smiles: Cc1ccc(-c2ccc(-c3ccc(-c4ccc(C)cc4)cc3)cc2)cc1
  - (Anchors, Electrodes, and Interface are the same as System 1)
  - Variation\_notes: "Oligophenyl, n=4."

# 4\. Applicability Assessment

**Applicable.**

The core computational objective is to calculate the zero-bias transmission $T(E)$ for a series of molecules and determine their alignment relative to the electrode Fermi level ($E_F$) to explain a conductance trend. This is a standard single-molecule transport problem. It does not involve any of the out-of-scope criteria (e.g., spintronics, thermoelectric, incoherent transport, or ensemble effects). The QDHC L3 scheme is specifically designed to address such level-alignment problems by computing $T(E)$ relative to the bulk electrode $E_F$.

# 5\. Hierarchical Analysis

**Level: L3**

The problem maps directly to L3. The core question is "Is transport governed primarily by molecular level alignment with the electrode Fermi level?" The distinction between P1 (near-resonant) and P2-P4 (tunneling) is fundamentally a question of *where* the dominant molecular resonances lie relative to the gold $E_F$. The paper's primary computational evidence (Figure 4) is a $T(E)$ spectrum plotted relative to $E-E_F=0$. The QDHC guide explicitly identifies "T(E) spectra referenced to the electrode Fermi level (E−E\_F=0)" as the key analytical evidence for an L3 problem, as this is required to identify the conducting channel and its proximity to $E_F$. L1 and L2 cannot provide this proper alignment to the bulk $E_F$.

# 6\. Input Preparation

Based on the L3 workflow, four full junction structures must be manually created from MST templates. The direct Au-C bond is best represented by an undercoordinated site, such as the `adatom` template.

1.  **MST Template**: The `[MST_root]/share/device/junction_example_adatom...xyz` template will be used.
2.  **User-Created Junction Files (`.xyz`)**:
      - Create `junction_adatom_p1.xyz`: Modify the adatom template by replacing the placeholder molecule with molecule P1 (p-xylylene).
      - Create `junction_adatom_p2.xyz`: Replace the placeholder with molecule P2.
      - Create `junction_adatom_p3.xyz`: Replace the placeholder with molecule P3.
      - Create `junction_adatom_p4.xyz`: Replace the placeholder with molecule P4.
3.  **Conversion Script**: The `xyz2POSCAR.py` script (from `[MST_root]/share/`) is required.
4.  **Directory Structure**:
      - Create four directories: `p1_adatom/`, `p2_adatom/`, `p3_adatom/`, `p4_adatom/`.
      - Place each corresponding `junction_adatom_...xyz` file into its respective directory.

# 7\. Computational Workflow

## Goal:

Compute and compare the zero-bias $T(E)$ spectra for the P1, P2, P3, and P4 systems, aligned to the electrode $E_F$.

## Step 1. Create directories and Prepare Inputs

Create the directory structure and place the corresponding user-created junction `.xyz` files inside:

```
/p1_adatom/junction_adatom_p1.xyz
/p2_adatom/junction_adatom_p2.xyz
/p3_adatom/junction_adatom_p3.xyz
/p4_adatom/junction_adatom_p4.xyz
```

## Step 2. Convert to POSCAR

Run the `xyz2POSCAR.py` conversion script in *each* of the four directories.

1.  **For the `p1_adatom` system:**
    ```bash
    cd p1_adatom
    # Copy xyz2POSCAR.py from [MST_root]/share/ into this directory
    # Edit xyz2POSCAR.py: set xyz_filename = 'junction_adatom_p1.xyz'
    python xyz2POSCAR.py
    cd ..
    ```
2.  **For the `p2_adatom` system:**
    ```bash
    cd p2_adatom
    # Copy and edit xyz2POSCAR.py: set xyz_filename = 'junction_adatom_p2.xyz'
    python xyz2POSCAR.py
    cd ..
    ```
3.  **For the `p3_adatom` system:**
    ```bash
    cd p3_adatom
    # Copy and edit xyz2POSCAR.py: set xyz_filename = 'junction_adatom_p3.xyz'
    python xyz2POSCAR.py
    cd ..
    ```
4.  **For the `p4_adatom` system:**
    ```bash
    cd p4_adatom
    # Copy and edit xyz2POSCAR.py: set xyz_filename = 'junction_adatom_p4.xyz'
    python xyz2POSCAR.py
    cd ..
    ```
      - This generates `POSCAR` and `EM_atom.txt` in each of the four directories.

## Step 3. Run L3 Transport Calculation

Run the interactive `L3_Trans` module in *each* of the four directories.

1.  **For the `p1_adatom` system:**
    ```bash
    cd p1_adatom
    L3_Trans
    ```
      - Follow the interactive prompts:
          - `Enter POSCAR file name(...)`: `POSCAR`
          - `Specify the energy range (...)`: `3` (This scans $E_F \pm 3$ eV, which covers the key features shown in the paper's Fig 4)
          - `Specify the energy interval (...)`: `0.01`
    <!-- end list -->
    ```bash
    cd ..
    ```
2.  **Repeat this exact process** for the `p2_adatom/` directory.
3.  **Repeat this exact process** for the `p3_adatom/` directory.
4.  **Repeat this exact process** for the `p4_adatom/` directory, ensuring the *exact same* energy range and interval are used for a valid comparison.

## Step 4. Post-processing and Analysis

The workflow will generate `Transmission.txt` in all four directories, with the Fermi level aligned to 0 eV.

1.  Collect the `Transmission.txt` file from all four directories (`p1_adatom/`, `p2_adatom/`, `p3_adatom/`, `p4_adatom/`).
2.  Use a plotting tool to plot the transmission data (y-axis in log10 scale) from all four files on the same graph.
3.  Analyze the plot:
      - Verify that for P1, the transmission value *at* $E_F=0$ is very high (near-resonant).
      - Verify that the transmission value *at* $E_F=0$ decreases exponentially for the series: P1 \> P2 \> P3 \> P4.
      - Observe how the main transmission resonance(s) near $E_F$ for P1 evolve and move further away from $E_F=0$ for the longer P2-P4 molecules.