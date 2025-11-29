# 0\. Metadata

  - Title: A gate-tunable single-molecule diode
  - DOI: (Omit this part)

# 1\. Literature Summary

This is an 'experiment + computation' study. The authors use a gateable mechanically controllable break junction (gMCBJ) technique to measure transport through a single, asymmetrically designed molecule (DPE-2F) anchored between gold electrodes via thiol groups. The molecule consists of two conjugated sites weakly coupled through a non-conjugated ethane bridge; asymmetry is introduced by electron-withdrawing fluorine atoms on one site. The key experimental finding is that the molecule functions as a rectifier (diode) with high rectification ratios (up to 600), and this rectification can be tuned by the applied gate voltage. The rectification mechanism is a two-site resonant tunneling model: the sites are misaligned at zero bias (low current), align at a specific positive bias (high current peak), and move further apart at negative bias (low current). DFT+NEGF calculations of the two-terminal $I-V$ characteristics support this model, reproducing the strong rectification peak.

# 2\. Computational Objectives

The primary computational objective is to reproduce the fundamental rectification behavior demonstrated in the paper's DFT+NEGF calculations (Fig. 1c). This requires computing the full non-equilibrium $I-V$ characteristics for the asymmetric DPE-2F molecule and a symmetric DPE control molecule (also mentioned in the paper). The expected result is a highly asymmetric, rectifying $I-V$ curve for DPE-2F (showing a distinct current peak at one bias polarity) and a symmetric, non-rectifying $I-V$ curve for the DPE control, thereby validating the model that molecular asymmetry is responsible for the rectification.

# 3\. Involved Systems

## System 1: DPE-2F (Asymmetric)

  - Core Molecule:
      - abbreviation: DPE-2F
      - full\_chemical\_name: N/A
      - core\_smiles: Fc1cc(C#Cc2ccc(S)cc2)cc(F)c1CCc1ccc(C#Cc2ccc(S)cc2)cc1
  - Anchors:
      - anchor\_groups: ['Thiol\_SH']
  - Electrodes:
      - electrode\_material: Au
      - electrode\_surface: (111)
  - Interface:
      - interface\_geometry\_text: Thiol-SH anchors to Au electrodes, formed via MCBJ. This is modeled as a Thiolate-S binding to an Au(111) trimer (hollow) site in a two-terminal junction.
  - Variation\_notes: "Asymmetric molecule with fluorine substituents, expected to show rectification."

## System 2: DPE (Symmetric)

  - Core Molecule:
      - abbreviation: DPE
      - full\_chemical\_name: N/A
      - core\_smiles: Sc1ccc(C#Cc2ccc(CCc3ccc(C#Cc4ccc(S)cc4)cc3)cc2)cc1
  - (Anchors, Electrodes, and Interface are the same as System 1)
  - Variation\_notes: "Symmetric control molecule (no fluorine). Expected to be non-rectifying."

# 4\. Applicability Assessment

**Applicable.**

While the paper's key *experimental* finding involves a three-terminal gate, its core *computational* evidence (Fig. 1c) is a standard two-terminal DFT+NEGF calculation demonstrating rectification. This rectification, which arises from the asymmetric molecule's response to the *bias* field (not a gate field), is precisely the phenomenon the MST L3-EEF workflow is designed to simulate. The gate-tunability aspect is out-of-scope, but the fundamental bias-driven rectification is applicable.

# 5\. Hierarchical Analysis

**Level: L3**

The core question is "How does the molecule's asymmetric structure lead to an asymmetric $I-V$ curve (rectification) under finite bias?" This is a non-equilibrium transport problem. The QDHC guide explicitly identifies "I–V or dI/dV characteristics" and "rectification ratios" as key analytical evidence requiring the L3 level. The L3-EEF module is the only one in the QDHC framework that can simulate the effect of an applied finite bias to compute a full $I-V$ curve.

# 6\. Input Preparation

Based on the L3 workflow, two full junction structures must be manually created from MST templates. The thiol anchors are best modeled using the trimer template.

1.  **MST Template**: The `[MST_root]/share/device/junction_trimer_...xyz` template will be used.
2.  **User-Created Junction Files (`.xyz`)**:
      - Create `junction_trimer_dpe2f.xyz`: Replace the placeholder molecule in the trimer template with the asymmetric DPE-2F molecule.
      - Create `junction_trimer_dpe.xyz`: Replace the placeholder with the symmetric DPE molecule.
3.  **Conversion Script**: The `xyz2POSCAR.py` script (from `[MST_root]/share/`) is required.
4.  **Helper Script**: The `current_parallel.py` script (from `[MST_root]/share/`) is required to run the `L3_EEF` module.
5.  **EM Lengths**: The length of the extended molecule (L\_EM) along the transport (z) direction must be measured from each of the two `.xyz` files (e.g., `L_dpe2f`, `L_dpe`) in Ångstroms. This is a required input for the `current_parallel.py` script.
6.  **Directory Structure**:
      - Create two directories: `dpe2f/`, `dpe/`.
      - Place each corresponding `junction_trimer_...xyz` file into its directory.

# 7\. Computational Workflow

## Goal:

Compute and compare the finite-bias $I-V$ curves for the asymmetric (DPE-2F) and symmetric (DPE) systems to reproduce the rectification effect.

## Step 1. Create directories and Prepare Inputs

Create the directory structure and place the corresponding user-created junction `.xyz` files inside:

```
/dpe2f/junction_trimer_dpe2f.xyz
/dpe/junction_trimer_dpe.xyz
```

Copy `xyz2POSCAR.py` and `current_parallel.py` into each of the two directories.

## Step 2. Convert to POSCAR

Run the `xyz2POSCAR.py` conversion script in *each* of the two directories.

1.  **For the `dpe2f` system:**
    ```bash
    cd dpe2f
    # Edit xyz2POSCAR.py: set xyz_filename = 'junction_trimer_dpe2f.xyz'
    python xyz2POSCAR.py
    cd ..
    ```
2.  **For the `dpe` system:**
    ```bash
    cd dpe
    # Edit xyz2POSCAR.py: set xyz_filename = 'junction_trimer_dpe.xyz'
    python xyz2POSCAR.py
    cd ..
    ```
      - This generates `POSCAR` and `EM_atom.txt` in each directory.

## Step 3. Run L3 Finite-Bias Calculation

Run the `current_parallel.py` script in *each* of the two directories.

**In each directory (`dpe2f/`, `dpe/`)**:

1.  **Edit `current_parallel.py`**:

      - `poscar_file`: `"POSCAR"`
      - `Length`: Set this to the specific measured length for the system in that directory (e.g., `L_dpe2f` or `L_dpe`).
      - `input_energy_range`: `2` (Scans $E_F \pm 2$ eV).
      - `input_energy_interval`: `0.0025`
      - `electric_field_range`: `np.arange(-0.0008, 0.0009, 0.0001)` (Scans 16 field points from -0.0008 to +0.0008 a.u. to cover positive and negative bias).
      - `max_workers`: Set based on available system RAM (e.g., `2`).

2.  **Run the script**:

    ```bash
    python current_parallel.py
    ```

      - The script automatically runs `L3_EEF` for all bias points.
      - When finished, it generates `voltage_current.txt` containing the final $I-V$ data.

## Step 4. Post-processing and Analysis

1.  Collect the `voltage_current.txt` file from each of the two directories (`dpe2f/`, `dpe/`).
2.  Use a plotting tool to plot the $I-V$ data from both files on the same graph.
3.  Analyze the plot:
      - Verify that the `dpe` (symmetric) curve is symmetric around 0V.
      - Verify that the `dpe2f` (asymmetric) curve is highly asymmetric, showing significant current at one bias polarity and low current at the other, confirming rectification.