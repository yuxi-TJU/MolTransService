# 0\. Metadata

  - Title: Redox-Addressable Single-Molecule Junctions Incorporating a Persistent Organic Radical
  - DOI: (Omit this part)

# 1\. Literature Summary

This is an 'experiment + computation' study investigating the transport properties of a persistent organic radical. The authors compare a 6-oxo-verdazyl radical (molecule **1**) with its closed-shell, non-radical precursor (molecule **2**) using STM-BJ and electrochemical (EC) STM-BJ techniques. The key experimental findings are: (1) The open-shell radical **1** is significantly more conductive (by almost one order of magnitude) than the closed-shell molecule **2**. (2) Molecule **1** exhibits strong non-linear I-V behavior and rectification (RR≈5 at ±2V), whereas **2** shows linear, non-rectifying I-V curves. (3) The computations (DFT+NEGF) explain these findings by showing that for molecule **1**, SOMO/SUMO resonances lie very close to the electrode Fermi level ($E_F$), leading to high zero-bias conductance. Furthermore, these resonances shift asymmetrically under an applied bias, explaining the rectification. For molecule **2**, $E_F$ lies in the middle of a large HOMO-LUMO gap, resulting in low conductance and symmetric I-V behavior.

# 2\. Computational Objectives

The primary computational objective is to reproduce the key non-equilibrium transport findings: the rectification and non-linear I-V characteristics of the open-shell radical (**1**) and the contrasting linear, symmetric I-V behavior of the closed-shell precursor (**2**). The goal is to compute the full I-V curves for both systems. The expected result is to show a strongly asymmetric, rectifying I-V curve for molecule **1** and a symmetric, non-rectifying (Ohmic) I-V curve for molecule **2**, thereby validating the model's ability to capture the bias-dependent shifting of the transport resonances.

# 3\. Involved Systems

## System 1: Molecule 1 (Radical)

  - Core Molecule:
      - abbreviation: 1
      - full\_chemical\_name: 6-oxo-verdazyl derivative
      - core\_smiles: CSc1ccc(N2N=C(c3ccccc3)[N-]N(c3ccc(SC)cc3)C2=O)cc1
  - Anchors:
      - anchor\_groups: ['Methylthio_SCH3']
  - Electrodes:
      - electrode\_material: Au
      - electrode\_surface: (111)
  - Interface:
      - interface\_geometry\_text: Methylthio (thioanisole) S-atom coordinates to an Au adatom on the Au(111) surface, representing an STM-BJ point contact.
  - Variation\_notes: "Open-shell persistent radical system."

## System 2: Molecule 2 (Closed-shell)

  - Core Molecule:
      - abbreviation: 2
      - full\_chemical\_name: Closed-shell tetrazin-3-one precursor
      - core\_smiles: CSc1ccc(N2NC(c3ccccc3)NN(c3ccc(SC)cc3)C2=O)cc1
  - (Anchors, Electrodes, and Interface are the same as System 1)
  - Variation\_notes: "Closed-shell, non-radical precursor for comparison."

# 4\. Applicability Assessment

**Applicable.**

The core computational objective is to calculate and compare the finite-bias I-V characteristics and rectification ratios for two different molecules. This is a non-equilibrium transport problem. The QDHC L3 scheme, specifically using the `L3_EEF` module, is designed to address this exact type of problem by simulating the effect of an applied bias as a Uniform External Electric Field (EEF). While the original paper used a DFT+NEGF (Gollum) approach, the MST L3 workflow (DFTB+ + EEF) is designed to capture the same qualitative physics: the asymmetric electrostatic potential drop across the molecule that causes the energy levels to shift, leading to rectification. The open-shell nature of molecule **1** can be handled by the underlying DFTB+ electronic structure engine.

# 5\. Hierarchical Analysis

**Level: L3**

The problem maps to L3. The core question is "How does the I-V curve and rectification ratio evolve under an applied finite bias?" This is fundamentally a non-equilibrium, bias-dependent problem. The QDHC guide (Section 3.3) explicitly identifies L3 as the correct tier for problems "governed primarily by... the applied finite bias." The key analytical evidence mentioned in the guide, "I–V or dI/dV characteristics" and "rectification ratios," perfectly matches the paper's computational objective (Fig 4). L1 and L2 are zero-bias methods and cannot be used to calculate an I-V curve.

# 6\. Input Preparation

Based on the L3 workflow, two full junction structures must be manually created from MST templates. The methylthio anchor (a neutral S-atom linker) is best modeled by the adatom interface, similar to the amine-adatom example.

1.  **MST Template**: The `[MST_root]/share/device/junction_example_adatom_amine.xyz` template (or a similar adatom template) will be used.
2.  **User-Created Junction Files (`.xyz`)**:
      - Create `junction_adatom_m1.xyz`: Replace the placeholder molecule in the adatom template with the open-shell radical molecule **1**.
      - Create `junction_adatom_m2.xyz`: Replace the placeholder molecule with the closed-shell precursor molecule **2**.
3.  **Conversion Script**: The `xyz2POSCAR.py` script (from `[MST_root]/share/`) is required.
4.  **Helper Script**: The `current_parallel.py` script (from `[MST_root]/share/`) is required to run the `L3_EEF` module.
5.  **EM Lengths**: The user must manually measure the length of the extended molecule (L\_EM) along the transport (z) direction (in Ångstroms) from both `junction_adatom_m1.xyz` (call it `L_m1`) and `junction_adatom_m2.xyz` (call it `L_m2`).
6.  **Directory Structure**:
      - Create two directories: `m1/`, `m2/`.
      - Place `junction_adatom_m1.xyz` in `m1/` and `junction_adatom_m2.xyz` in `m2/`.

# 7\. Computational Workflow

## Goal:

Compute and compare the finite-bias I-V curves for the open-shell (1) and closed-shell (2) systems to reproduce the rectification phenomenon.

## Step 1. Create directories and Prepare Inputs

Create the directory structure and place the corresponding user-created junction `.xyz` files inside:

```
/m1/junction_adatom_m1.xyz
/m2/junction_adatom_m2.xyz
```

Copy `xyz2POSCAR.py` and `current_parallel.py` from `[MST_root]/share/` into *each* of the two directories (`m1/` and `m2/`).

## Step 2. Convert to POSCAR

Run the `xyz2POSCAR.py` conversion script in *each* of the two directories.

1.  **For the `m1` system:**
    ```bash
    cd m1
    # Edit xyz2POSCAR.py: set xyz_filename = 'junction_adatom_m1.xyz'
    python xyz2POSCAR.py
    cd ..
    ```
2.  **For the `m2` system:**
    ```bash
    cd m2
    # Edit xyz2POSCAR.py: set xyz_filename = 'junction_adatom_m2.xyz'
    python xyz2POSCAR.py
    cd ..
    ```
      * This generates `POSCAR` and `EM_atom.txt` in each directory.

## Step 3. Run L3 Finite-Bias Calculation

Run the `current_parallel.py` script in *each* of the two directories to execute the `L3_EEF` calculations.

**In each directory (`m1/`, `m2/`)**:

1.  **Edit `current_parallel.py`**:

      - `poscar_file`: `"POSCAR"`
      - `Length`: Set this to the specific measured length for the system in that directory (`L_m1` or `L_m2`).
      - `input_energy_range`: `2` (To scan $E_F \pm 2$ eV).
      - `input_energy_interval`: `0.0025` (A fine grid is needed for integrating the I-V curve).
      - `electric_field_range`: `np.arange(-0.0008, 0.0009, 0.0001)` (This scans 16 field points from -0.0008 to +0.0008 a.u. to cover both positive and negative bias, matching the paper's need for a ±2V-range scan).
      - `max_workers`: Set based on available system RAM and CPU cores (e.g., `2`).

2.  **Run the script**:

    ```bash
    python current_parallel.py
    ```

      - The script will automatically run `L3_EEF` for all specified bias points.
      - When finished, it generates `combined_transmission.txt` and the final I-V data in `voltage_current.txt`.

## Step 4. Post-processing and Analysis

1.  Collect the `voltage_current.txt` file from both directories (`m1/` and `m2/`).
2.  Use a plotting tool to plot the I-V data from both files on the same graph (Current vs. Voltage, linear scale).
3.  Analyze the plot:
      - Verify that the `m1` (radical) curve is asymmetric, showing higher current at positive bias than negative bias (rectification).
      - Verify that the `m2` (closed-shell) curve is symmetric and linear around 0V (non-rectifying).