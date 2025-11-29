# 0\. Metadata

  - Title: Tuning Rectification in Single-Molecular Diodes
  - DOI: (Omit this part)

# 1\. Literature Summary

This is an 'experiment + computation' study. The authors use a scanning tunneling microscope-based break-junction (STM-BJ) technique to measure the I-V characteristics of single-molecule diodes. The key molecular design is a symmetric stilbene backbone with asymmetric linkers: a methylsulfide group at one end and a covalent gold-carbon (Au-C) bond at the other. Experimentally, this asymmetric linkage results in significant rectification (diode-like behavior) at low bias. The paper's non-equilibrium transport calculations (DFT-NEGF) explain this finding by identifying a "gateway" state, originating from the Au-C bond, that is pinned close to the Fermi level. The calculations show that this gateway state's energy shifts drastically with applied bias, while intrinsic molecular orbitals do not, leading to an asymmetric transmission $T(E,V)$ and the observed rectification.

# 2\. Computational Objectives

The primary computational objective is to theoretically reproduce and explain the mechanism of rectification observed in the asymmetric Au-C/S-Me stilbene junction. The goal is to compute the full non-equilibrium, finite-bias I-V characteristics for this system. The expected result is a strongly asymmetric I-V curve, and the underlying transmission spectra ($T(E,V)$) should show a "gateway" state (near $E_F$) that shifts significantly with the applied bias, thereby blocking current in one direction and allowing it in the other.

# 3\. Involved Systems

## System 1: Molecule 1 (Asymmetric)

  - Core Molecule:
      - abbreviation: 1
      - full\_chemical\_name: N/A (Based on 4-methylsulfide, 4'-Au-C stilbene)
      - core\_smiles: CCc1ccc(C=Cc2ccc(SC)cc2)cc1
  - Anchors:
      - anchor\_groups: ['Methylsulfide\_SMe', 'Alkyl\_C']
  - Electrodes:
      - electrode\_material: Au
      - electrode\_surface: N/A
  - Interface:
      - interface\_geometry\_text: Highly asymmetric junction. One side is a methylsulfide-gold bond. The other is a direct covalent gold-carbon bond. The paper's computation models this using Au trimer tips.
  - Variation\_notes: "The primary system used to demonstrate the rectification mechanism."

# 4\. Applicability Assessment

**Applicable.**

The core computational objective is to calculate the non-equilibrium I-V curve and rectification ratio, which is a problem of finite-bias transport. The paper's explanation relies on the asymmetric shifting of energy levels (the gateway state) under an applied bias. This is precisely the type of problem the QDHC L3 scheme and its `L3_EEF` (Uniform External Electric Field) module are designed to simulate. MST can be used to reproduce the qualitative rectification behavior and its underlying mechanism.

# 5\. Hierarchical Analysis

**Level: L3**

The problem maps to L3. The core question is "How does the I-V curve behave under finite bias, and why does it rectify?" This is fundamentally a non-equilibrium transport problem. The QDHC guide explicitly states that L3 is required for problems governed by "applied finite bias" and lists "I–V or dI/dV characteristics" and "rectification ratios" as the key analytical evidence. The paper's central computational evidence (Figure 2b) is a plot of bias-dependent transmission $T(E,V)$ and the resulting I-V curve (inset), which is the exact output of the `L3_EEF` workflow.

# 6\. Input Preparation

Based on the L3 workflow, a full junction structure must be manually created. The paper's computation used "trimer tips" to model the contacts.

1.  **MST Template**: The `[MST_root]/share/device/junction_trimer_...xyz` template will be used for both sides.
2.  **User-Created Junction File (`.xyz`)**:
      - Create `junction_trimer_m1.xyz`: Modify the trimer template by replacing the placeholder molecule with Molecule 1 (stilbene). One end should be terminated for a covalent C-Au bond to the trimer, and the other end terminated with the methylsulfide (S-Me) group linked to the other trimer.
3.  **Conversion Script**: The `xyz2POSCAR.py` script (from `[MST_root]/share/`) is required.
4.  **Helper Script**: The `current_parallel.py` script (from `[MST_root]/share/`) is required to run the `L3_EEF` module.
5.  **EM Length**: The length of the extended molecule (L\_EM) along the transport (z) direction must be measured from the `junction_trimer_m1.xyz` file (in Ångstroms). This value is a required input for the `current_parallel.py` script.
6.  **Directory Structure**:
      - Create a directory: `m1_trimer/`.
      - Place `junction_trimer_m1.xyz` inside this directory.

# 7\. Computational Workflow

## Goal:

Compute the finite-bias I-V curve for the asymmetric Molecule 1 junction to reproduce the rectification behavior.

## Step 1. Create directory and Prepare Inputs

Create the directory structure and place the user-created junction file inside.

```
/m1_trimer/junction_trimer_m1.xyz
```

Copy `xyz2POSCAR.py` and `current_parallel.py` from `[MST_root]/share/` into this directory.

## Step 2. Convert to POSCAR

Run the `xyz2POSCAR.py` conversion script in the `m1_trimer/` directory.

```bash
cd m1_trimer
# Edit xyz2POSCAR.py: set xyz_filename = 'junction_trimer_m1.xyz'
python xyz2POSCAR.py
```

  - This generates `POSCAR` and `EM_atom.txt`.

## Step 3. Run L3 Finite-Bias Calculation

Run the `current_parallel.py` script in the `m1_trimer/` directory.

1.  **Measure Length**: Manually measure the length of the extended molecule (L\_EM) along the z-axis from the `junction_trimer_m1.xyz` file.
2.  **Edit `current_parallel.py`**:
      - `poscar_file`: `"POSCAR"`
      - `Length`: Set this to the measured length from Step 1 (e.g., `25.123`).
      - `input_energy_range`: `3` (To scan $E_F \pm 3$ eV, covering the relevant orbital and gateway states).
      - `input_energy_interval`: `0.0025`
      - `electric_field_range`: `np.arange(-0.0008, 0.0009, 0.0001)` (This scans 16 field points from -0.0008 to +0.0008 a.u., which the script will convert to voltage).
      - `max_workers`: Set based on available system RAM and CPU cores (e.g., `2`).
3.  **Run the script**:
    ```bash
    python current_parallel.py
    ```
      - The script automatically runs `L3_EEF` for all bias points, creating subdirectories for each.
      - When finished, it generates `combined_transmission.txt` and the final I-V data in `voltage_current.txt`.

## Step 4. Post-processing and Analysis

1.  Collect the `voltage_current.txt` file from the `m1_trimer/` directory.
2.  Use a plotting tool to plot the I-V data.
3.  Analyze the plot:
      - Verify that the I-V curve is asymmetric (i.e., $I(V) \neq -I(-V)$), confirming the rectification predicted in the paper.