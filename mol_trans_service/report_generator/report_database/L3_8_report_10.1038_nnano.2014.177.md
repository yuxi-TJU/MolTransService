# 0\. Metadata

  - Title: Large negative differential conductance in single-molecule break junctions
  - DOI: (Omit this part)

# 1\. Literature Summary

This is an 'experiment + computation' study. The authors use a mechanically controllable break junction (MCBJ) to measure the transport properties of single-molecule junctions. The study focuses on two molecules: AH, which has a non-conjugated 9,10-dihydroanthracene core, and AC, a fully conjugated control molecule with an anthracene core. The key experimental finding is that the AH molecule exhibits pronounced Negative Differential Conductance (NDC) at low bias, while the fully conjugated AC molecule does not. The paper's theoretical model and DFT+NEGF computations attribute this NDC to the intrinsic structure of AH, which acts as a two-site system (the two conjugated arms). At zero bias, these sites are in resonance, allowing high current. An applied finite bias shifts the sites off-resonance, suppressing transport and causing the current to decrease.

# 2\. Computational Objectives

The primary computational objective is to reproduce the key theoretical finding of the paper: the emergence of Negative Differential Conductance (NDC) in the AH molecule due to its two-site nature, and the absence of NDC in the fully conjugated AC control molecule. The goal is to compute the full non-equilibrium I-V characteristics for both systems. The expected result is an I-V curve for AH that shows a current peak at low bias followed by a sharp decrease, and a monotonic I-V curve for AC.

# 3\. Involved Systems

## System 1: AH

  - Core Molecule:
      - abbreviation: AH
      - full\_chemical\_name: thiolated arylethynylene with a 9,10-dihydroanthracene core
      - core\_smiles: Sc1ccc(C#Cc2ccc3c(c2)Cc2ccc(C#Cc4ccc(S)cc4)cc2C3)cc1
  - Anchors:
      - anchor\_groups: ['Thiolate\_S-']
  - Electrodes:
      - electrode\_material: Au
      - electrode\_surface: (111)
  - Interface:
      - interface\_geometry\_text: Thiolate-S binds to an Au(111) surface. The paper's MCBJ setup implies binding to an undercoordinated Au site, which is modeled using an Au trimer template.
  - Variation\_notes: "Non-conjugated core, expected to show NDC."

## System 2: AC

  - Core Molecule:
      - abbreviation: AC
      - full\_chemical\_name: thiolated arylethynylene with an anthracene core
      - core\_smiles: Sc1ccc(C#Cc2ccc3cc4cc(C#Cc5ccc(S)cc5)ccc4cc3c2)cc1
  - (Anchors, Electrodes, and Interface are the same as System 1)
  - Variation\_notes: "Fully conjugated core, control molecule, expected to show no NDC."

# 4\. Applicability Assessment

**Applicable.**

The core computational objective is to calculate the finite-bias I-V characteristics for two different molecules to observe Negative Differential Conductance (NDC). This is a non-equilibrium transport problem directly dependent on the applied bias. The MST L3 scheme, specifically using the `L3_EEF` module, is designed to simulate the effect of an applied bias (as a Uniform External Electric Field) and compute the resulting I-V curve. This is precisely the capability needed to reproduce the paper's central theoretical finding.

# 5\. Hierarchical Analysis

**Level: L3**

The problem maps to L3. The key phenomenon, NDC, is by definition a finite-bias effect where the current *decreases* as voltage *increases*. The core question is "How does the I-V curve behave under an applied finite bias?" The QDHC guide explicitly identifies "I–V or dI/dV characteristics" as key analytical evidence requiring the L3 level. L1 and L2 are zero-bias (or near-equilibrium) approximations and cannot capture this non-equilibrium phenomenon.

# 6\. Input Preparation

Based on the L3 workflow for finite-bias, two full junction structures must be manually created from MST templates.

1.  **MST Template**: The thiolate anchor suggests using an Au trimer or pyramid interface. We will use the `[MST_root]/share/device/junction_trimer_...xyz` template.
2.  **User-Created Junction Files (`.xyz`)**:
      - Create `junction_trimer_AH.xyz`: Replace the placeholder molecule in the trimer template with the AH molecule.
      - Create `junction_trimer_AC.xyz`: Replace the placeholder with the AC molecule.
3.  **Conversion Script**: The `xyz2POSCAR.py` script (from `[MST_root]/share/`) is required.
4.  **Helper Script**: The `current_parallel.py` script (from `[MST_root]/share/`) is required to run the `L3_EEF` module for the I-V curve.
5.  **EM Lengths**: The length of the extended molecule (L\_EM) along the transport (z) direction must be measured from both `.xyz` files (e.g., `L_AH`, `L_AC`) in Ångstroms. This value is a required input for the `current_parallel.py` script.
6.  **Directory Structure**:
      - Create two directories: `AH/` and `AC/`.
      - Place each corresponding `junction_trimer_...xyz` file into its directory.

# 7\. Computational Workflow

## Goal:

Compute and compare the finite-bias I-V curves for the AH (non-conjugated) and AC (conjugated) systems to check for Negative Differential Conductance (NDC).

## Step 1. Create directories and Prepare Inputs

Create the directory structure and place the corresponding user-created junction `.xyz` files inside:

```
/AH/junction_trimer_AH.xyz
/AC/junction_trimer_AC.xyz
```

Also copy `xyz2POSCAR.py` and `current_parallel.py` into each of the two directories.

## Step 2. Convert to POSCAR

Run the `xyz2POSCAR.py` conversion script in *each* of the two directories.

1.  **For the `AH` system:**
    ```bash
    cd AH
    # Edit xyz2POSCAR.py: set xyz_filename = 'junction_trimer_AH.xyz'
    python xyz2POSCAR.py
    cd ..
    ```
2.  **For the `AC` system:**
    ```bash
    cd AC
    # Edit xyz2POSCAR.py: set xyz_filename = 'junction_trimer_AC.xyz'
    python xyz2POSCAR.py
    cd ..
    ```
      * This generates `POSCAR` and `EM_atom.txt` in each directory.

## Step 3. Run L3 Finite-Bias Calculation

Run the `current_parallel.py` script in *each* of the two directories.

**In each directory (`AH/`, `AC/`)**:

1.  **Edit `current_parallel.py`**:

      - `poscar_file`: `"POSCAR"`
      - `Length`: Set this to the specific measured length for the system in that directory (e.g., `L_AH` or `L_AC`).
      - `input_energy_range`: `2` (Scans $E_F \pm 2$ eV).
      - `input_energy_interval`: `0.0025`
      - `electric_field_range`: `np.arange(-0.0008, 0.0009, 0.0001)` (This scans 16 field points; the script will convert this to a voltage range).
      - `max_workers`: Set based on available system RAM and CPU cores (e.g., `2`).

2.  **Run the script**:

    ```bash
    python current_parallel.py
    ```

      - This script automatically runs `L3_EEF` for all bias points and generates the final I-V data in `voltage_current.txt`.

## Step 4. Post-processing and Analysis

1.  Collect the `voltage_current.txt` file from each of the two directories (`AH/` and `AC/`).
2.  Use a plotting tool to plot the I-V data from both files on the same graph.
3.  Analyze the plot:
      - Verify that the I-V curve for `AH` shows a peak in current at a low bias, followed by a region where current *decreases* as voltage increases (NDC).
      - Verify that the I-V curve for `AC` is monotonic and does not show any NDC.