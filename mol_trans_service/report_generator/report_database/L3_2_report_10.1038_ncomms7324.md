# 0\. Metadata

  - Title: Controlling the direction of rectification in a molecular diode
  - DOI: (Omit this part)

# 1\. Literature Summary

This is an 'experiment + computation' study on controlling molecular rectification. The authors use Self-Assembled Monolayers (SAMs) of a series of ferrocenyl-alkanethiol molecules ($SC_{n}FcC_{13-n}$) where the position of the redox-active ferrocenyl (Fc) unit is systematically varied (by changing n from 0 to 13). The junctions are formed between a bottom $Ag^{TS}$ or $Au^{TS}$ electrode and a top EGaIn liquid metal electrode. The key experimental finding is the ability to control and reverse the direction of rectification: when the Fc unit (which hosts the HOMO) is near the bottom electrode (e.g., n=3), the diode conducts at positive bias (R\<1); when it is near the top electrode (e.g., n=13), it conducts at negative bias (R\>1); when centered (n=6), rectification is minimal. The paper's computations (DFT and MD) support this by analyzing the system's structure and electronics (e.g., HOMO position, broadening, and work functions), which provides a model for the asymmetric potential drop under bias, but the paper does not include direct I-V transport simulations.

# 2\. Computational Objectives

The primary computational objective is to reproduce the key experimental finding: the control and reversal of rectification by altering the spatial position of the active molecular unit (Fc). The goal is to compute the full non-equilibrium I-V characteristics for systems representing the symmetric (Fc-centered, e.g., n=6) and asymmetric (Fc-offset, e.g., n=3) cases. The expected result is to show symmetric I-V curves for the n=6 system and strongly asymmetric, opposing I-V curves (rectification) for the n=3 systems, thus validating the L3-EEF model's ability to capture this electrostatic phenomenon.

# 3\. Involved Systems

The original paper uses SAMs. To model this within the MST single-molecule framework, the system is adapted to a two-terminal junction where the molecule is anchored at both ends.

## System 1: $SC_6FcC_7S$ (Symmetric)

  - Core Molecule:
      - abbreviation: $SC_6FcC_7S$
      - full\_chemical\_name: N/A
      - core\_smiles: N/A
  - Anchors:
      - anchor\_groups: ['Thiolate_S-']
  - Electrodes:
      - electrode\_material: Au
      - electrode\_surface: (111)
  - Interface:
      - interface\_geometry\_text: Thiolate-S binds to an Au(111) surface, adapted as a two-terminal junction. The paper's DFT uses Au(111).
  - Variation\_notes: "Symmetric case. Ferrocene (Fc) unit is centered in the alkyl chain (n=6)."

## System 2: $SC_3FcC_{10}S$ (Asymmetric, R\<1)

  - Core Molecule:
      - abbreviation: $SC_3FcC_{10}S$
      - full\_chemical\_name: N/A
      - core\_smiles: N/A
  - Anchors: (Same as System 1)
  - Electrodes: (Same as System 1)
  - Interface: (Same as System 1)
  - Variation\_notes: "Asymmetric case. Fc unit is close to one electrode (n=3), corresponding to the experimental R\<1 case."

# 4\. Applicability Assessment

**Applicable.**

The original paper investigates a system that is technically "Out-of-Scope" per the QDHC guide on multiple counts: it involves a SAM (ensemble effect), a non-standard EGaIn electrode, and the transport mechanism is identified as incoherent sequential tunneling.

However, the *computational objective* can be adapted. The core phenomenon—rectification caused by the asymmetric spatial position of the HOMO level—is a general electrostatic effect. The MST L3 scheme is designed to model how an applied bias (simulated as a Uniform External Electric Field, EEF) creates an asymmetric potential drop across an asymmetric molecule, leading to the shifting of energy levels and, consequently, rectification. Therefore, by adapting the SAM problem into a two-terminal single-molecule problem, MST L3 can be used to simulate the fundamental physics of the I-V curve asymmetry.

# 5\. Hierarchical Analysis

**Level: L3**

The core question is "How does the I-V curve and rectification ratio change with applied bias?" This is fundamentally a non-equilibrium, finite-bias problem. The QDHC guide explicitly states that L3 is required for problems governed by level alignment or applied finite bias, and lists "I–V or dI/dV characteristics" and "rectification ratios" as the key analytical evidence. The L3 scheme, with its `L3_EEF` module, is the only tier designed to apply a finite bias and compute the resulting I-V curve.

# 6\. Input Preparation

Based on the L3 workflow, two full junction structures must be manually created from MST templates.

1.  **MST Template**: The thiol anchor suggests using an Au trimer or pyramid interface. We will follow the example and use the trimer template: `[MST_root]/share/device/junction_trimer_...xyz`.
2.  **User-Created Junction Files (`.xyz`)**:
      - Create `junction_trimer_sc3fcc10s.xyz`: Replace the placeholder molecule in the trimer template with the adapted $SC_3FcC_{10}S$ molecule.
      - Create `junction_trimer_sc6fcc7s.xyz`: Replace the placeholder with the $SC_6FcC_7S$ molecule.
3.  **Conversion Script**: The `xyz2POSCAR.py` script (from `[MST_root]/share/`) is required.
4.  **Helper Script**: The `current_parallel.py` script (from `[MST_root]/share/`) is required to run the `L3_EEF` module.
5.  **EM Lengths**: The length of the extended molecule (L\_EM) along the transport (z) direction must be measured from each of the two `.xyz` files (e.g., `L_sc3`, `L_sc6`) in Ångstroms. This value is a required input for the `current_parallel.py` script.
6.  **Directory Structure**:
      - Create two directories: `sc3/`, `sc6/`.
      - Place each corresponding `junction_trimer_...xyz` file into its directory.

# 7\. Computational Workflow

## Goal:

Compute and compare the finite-bias I-V curves for the symmetric (n=6) and asymmetric (n=3) systems to reproduce the control and reversal of rectification.

## Step 1. Create directories and Prepare Inputs

Create the directory structure and place the corresponding user-created junction `.xyz` files inside:

```
/sc3/junction_trimer_sc3fcc10s.xyz
/sc6/junction_trimer_sc6fcc7s.xyz
```

Also copy `xyz2POSCAR.py` and `current_parallel.py` into each of the two directories.

## Step 2. Convert to POSCAR

Run the `xyz2POSCAR.py` conversion script in *each* of the two directories.

1.  **For the `sc3` system:**
    ```bash
    cd sc3
    # Edit xyz2POSCAR.py: set xyz_filename = 'junction_trimer_sc3fcc10s.xyz'
    python xyz2POSCAR.py
    cd ..
    ```
2.  **For the `sc6` system:**
    ```bash
    cd sc6
    # Edit xyz2POSCAR.py: set xyz_filename = 'junction_trimer_sc6fcc7s.xyz'
    python xyz2POSCAR.py
    cd ..
    ```
      * This generates `POSCAR` and `EM_atom.txt` in each directory.

## Step 3. Run L3 Finite-Bias Calculation

Run the `current_parallel.py` script in *each* of the two directories.

**In each directory (`sc3/`, `sc6/`)**:

1.  **Edit `current_parallel.py`**:

      - `poscar_file`: `"POSCAR"`
      - `Length`: Set this to the specific measured length for the system in that directory (e.g., `L_sc3`, `L_sc6`).
      - `input_energy_range`: `2` (Scans $E_F \pm 2$ eV).
      - `input_energy_interval`: `0.0025`
      - `electric_field_range`: `np.arange(-0.0008, 0.0009, 0.0001)` (This scans 16 field points from -0.0008 to +0.0008 a.u. The script will convert this to voltage).
      - `max_workers`: Set based on available system RAM and CPU cores (e.g., `2`).

2.  **Run the script**:

    ```bash
    python current_parallel.py
    ```

      - The script automatically runs `L3_EEF` for all bias points, creating subdirectories for each.
      - When finished, it generates `combined_transmission.txt` and the final I-V data in `voltage_current.txt`.

## Step 4. Post-processing and Analysis

1.  Collect the `voltage_current.txt` file from each of the two directories (`sc3/`, `sc6/`).
2.  Use a plotting tool to plot the I-V data from all two files on the same graph.
3.  Analyze the plot:
      - Check if the `sc6` (symmetric) curve is symmetric around 0V.
      - Check if the `sc3` (asymmetric) curve is asymmetric and rectifies in one direction.
