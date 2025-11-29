# 0\. Metadata

  - Title: Zero-Bias Anti-Ohmic Behaviour in Diradicaloid Molecular Wires
  - DOI: (Omit this part)

# 1\. Literature Summary

This is an 'experiment + computation' study investigating charge transport in a series of diradicaloid molecular wires (R1, R2, R3) of increasing length. Using the STMBJ technique, the authors measure single-molecule conductance and I-V characteristics. The key experimental finding is a strong "anti-ohmic" behavior: conductance *increases* as the molecular length increases (R1 \< R2 \< R3). This results in a negative conductance attenuation factor ($\beta$) that is observed not only at zero-bias but across the entire measured bias window (up to $\pm1.3$ V). The paper's computations (DFT + NEGF) explain this phenomenon, showing that as the molecules get longer, their diradical character increases, which causes a rapid narrowing of the HOMO-LUMO gap. This shrinking energy gap leads to higher transmission, overcoming the typical exponential decay with length.

# 2\. Computational Objectives

The primary computational objective is to theoretically explain the key experimental finding: the "anti-ohmic" behavior where conductance increases with molecular length. The goal is to compute the zero-bias transmission spectra, $T(E)$, for the three systems (R1, R2, R3) and align them with the electrode Fermi level ($E_F$). The expected result is to demonstrate that as the molecular length increases, the HOMO-LUMO gap rapidly narrows. This electronic structure change is expected to cause the transmission at or near the Fermi level to increase, showing a trend of $T(E_F)_{R1} < T(E_F)_{R2} < T(E_F)_{R3}$, which explains the negative conductance attenuation ($\beta$).

# 3\. Involved Systems

## System 1: R1

  - Core Molecule:
      - abbreviation: R1
      - full\_chemical\_name: N/A
      - core\_smiles: CSc1cc(C)c(C2=c3cc4c(cc3-c3ccccc32)=C(c2c(C)cc(SC)cc2C)c2ccccc2-4)c(C)c1
  - Anchors:
      - anchor\_groups: ['Thioether_SMe']
  - Electrodes:
      - electrode\_material: Au
      - electrode\_surface: (111)
  - Interface:
      - interface\_geometry\_text: Thioether-S (from 3,5-dimethylthioanisolyl anchor) binds to an undercoordinated Au site, modeled as an adatom on the Au(111) surface (see Fig 4a).
  - Variation\_notes: "Shortest molecule (indenofluorene core), weakest diradicaloid character (y=0.13)."

## System 2: R2

  - Core Molecule:
      - abbreviation: R2
      - full\_chemical\_name: N/A
      - core\_smiles: CSc1cc(C)c(C2=c3cc4cc5c(cc4cc3-c3ccccc32)=C(c2c(C)cc(SC)cc2C)c2ccccc2-5)c(C)c1
  - (Anchors, Electrodes, and Interface are the same as System 1)
  - Variation\_notes: "Intermediate length molecule (fluorenofluorene core), medium diradicaloid character (y=0.33)."

## System 3: R3

  - Core Molecule:
      - abbreviation: R3
      - full\_chemical\_name: N/A
      - core\_smiles: CSc1cc(C)c(C2=c3cc4cc5cc6c(cc5cc4cc3-c3ccccc32)=C(c2c(C)cc(SC)cc2C)c2ccccc2-6)c(C)c1
  - (Anchors, Electrodes, and Interface are the same as System 1)
  - Variation\_notes: "Longest molecule (bis(indeno)anthracene core), strongest diradicaloid character (y=0.49)."

# 4\. Applicability Assessment

**Applicable.**

The core computational objective is to determine the zero-bias transmission, $T(E)$, as a function of molecular length and diradical character. This is a problem of molecular level alignment relative to the electrode Fermi level. The paper's experimental findings also include finite-bias I-V curves, but their own computational analysis (Fig 4) focuses on zero-bias $T(E)$ to explain the fundamental anti-ohmic trend. This zero-bias level alignment problem is precisely what the QDHC L3 scheme is designed to address. While the original paper uses DFT (SIESTA), MST L3 (using DFTB+) is sufficient to capture the key qualitative trend: the narrowing of the HOMO-LUMO gap and the resulting increase in transmission at $E_F$ as the acene core is lengthened. The problem does not involve spintronics (it assumes a singlet ground state) or incoherent transport.

# 5\. Hierarchical Analysis

**Level: L3**

The core question is "How does the alignment of the frontier molecular orbitals (HOMO and LUMO) with the electrode Fermi level ($E_F$) change as the molecular backbone is lengthened?" The paper's central theoretical argument is that the HOMO-LUMO gap narrows, causing a change in transmission *relative* to $E_F$. This is a classic molecular level alignment problem. The key analytical evidence in the paper (Figure 4b, c) is the transmission spectrum $T(E)$ plotted relative to $E_F=0$. The QDHC guide explicitly states that L3 is required for problems governed by level alignment and for analyzing "T(E) spectra referenced to the electrode Fermi level (E−E\_F=0)". L1 and L2 cannot provide this proper alignment to the bulk electrode's $E_F$.

# 6\. Input Preparation

Based on the L3 workflow, three full junction structures must be manually created from MST templates. The interface geometry (Thioether-S binding to an apical Au atom, shown in Fig 4a) is best represented by the L3 adatom template.

1.  **MST Template**: The `[MST_root]/share/device/junction_example_adatom_...xyz` template will be used as the base.
2.  **User-Created Junction Files (`.xyz`)**:
      - Create `junction_adatom_r1.xyz`: Replace the placeholder molecule in the adatom template with the R1 molecule.
      - Create `junction_adatom_r2.xyz`: Replace the placeholder molecule with the R2 molecule.
      - Create `junction_adatom_r3.xyz`: Replace the placeholder molecule with the R3 molecule.
3.  **Conversion Script**: The `xyz2POSCAR.py` script (from `[MST_root]/share/`) is required.
4.  **Directory Structure**:
      - Create three directories: `r1/`, `r2/`, `r3/`.
      - Place each corresponding `junction_adatom_...xyz` file into its respective directory.

# 7\. Computational Workflow

## Goal:

Compute and compare the zero-bias $T(E)$ spectra for the R1, R2, and R3 systems to validate the trend of increasing transmission with molecular length.

## Step 1. Create directories and Prepare Inputs

Create the directory structure and place the corresponding user-created junction `.xyz` files inside:

```
/r1/junction_adatom_r1.xyz
/r2/junction_adatom_r2.xyz
/r3/junction_adatom_r3.xyz
```

## Step 2. Convert to POSCAR

Run the `xyz2POSCAR.py` conversion script in *each* of the three directories.

1.  **For the `r1` system:**
    ```bash
    cd r1
    # Copy xyz2POSCAR.py from [MST_root]/share/ into this directory
    # Edit xyz2POSCAR.py: set xyz_filename = 'junction_adatom_r1.xyz'
    python xyz2POSCAR.py
    cd ..
    ```
2.  **For the `r2` system:**
    ```bash
    cd r2
    # Copy and edit xyz2POSCAR.py: set xyz_filename = 'junction_adatom_r2.xyz'
    python xyz2POSCAR.py
    cd ..
    ```
3.  **For the `r3` system:**
    ```bash
    cd r3
    # Copy and edit xyz2POSCAR.py: set xyz_filename = 'junction_adatom_r3.xyz'
    python xyz2POSCAR.py
    cd ..
    ```
      * This generates `POSCAR` and `EM_atom.txt` in each of the three directories.

## Step 3. Run L3 Transport Calculation

Run the interactive `L3_Trans` module in *each* of the three directories.

1.  **For the `r1` system:**
    ```bash
    cd r1
    L3_Trans
    ```
      - Follow the interactive prompts:
          - `Enter POSCAR file name(...)`: `POSCAR`
          - `Specify the energy range (...)`: `2.0` (Scans $E_F \pm 2.0$ eV, covering the paper's -1.5 to 0.5 eV range)
          - `Specify the energy interval (...)`: `0.01`
    <!-- end list -->
    ```bash
    cd ..
    ```
2.  **Repeat this exact process** for the `r2/` directory.
3.  **Repeat this exact process** for the `r3/` directory, ensuring the *exact same* energy range and interval are used for a valid comparison.

## Step 4. Post-processing and Analysis

The workflow will generate `Transmission.txt` in all three directories, with the Fermi level aligned to 0 eV.

1.  Collect the `Transmission.txt` file from all three directories (`r1/`, `r2/`, `r3/`).
2.  Use a plotting tool to plot the transmission data (y-axis in log10 scale) from all three files on the same graph.
3.  Analyze the plot:
      - Verify that the HOMO-LUMO gap (distance between the main resonance below $E_F=0$ and the main resonance above $E_F=0$) decreases in the order R1 \> R2 \> R3.
      - Verify that the transmission value *at* or *near* $E_F=0$ follows the trend: R1 \< R2 \< R3.