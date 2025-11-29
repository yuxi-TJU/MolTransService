# 0\. Metadata

  - Title: Molecular Rectification Enhancement Based On Conformational and Chemical Modifications
  - DOI: (Omit this part)

# 1\. Literature Summary

This is a 'pure computation' study investigating the design principles for intrinsic molecular rectifiers. The authors perform a systematic DFT-NEGF computational study on the effect of conformational changes (torsion angles) and chemical modifications (substituents) on the transport properties of D-B-A (donor-bridge-acceptor) molecules at low bias. The systems are based on 1,4-bis(phenylethynyl)benzene (BPEB) and para-terphenyl, functionalized with electron-donating ($-NH_2$) and electron-withdrawing ($-NO_2$) groups. The primary finding is that significant rectification at low bias ($\le 0.3$ V) is not achieved by torsion or asymmetric substitution alone, but requires a *combination* of both. An optimal D-B-A setup with torsion angles of $\sim 60^{\circ}$ localizes the HOMO on one end of the molecule, causing its alignment relative to the Fermi level to shift asymmetrically under an applied bias, which in turn produces high rectification ratios (RR up to 20.08 at 0.3 V).

# 2\. Computational Objectives

The primary computational objective is to calculate the non-equilibrium current-voltage (I-V) characteristics and rectification ratios (RR) for a series of molecules. The goal is to demonstrate how the combination of asymmetric D-B-A substitution and conformational twisting (torsion) enhances rectification. The expected result is to show that systems with *only* torsion or *only* D-A groups have symmetric I-V curves (RR $\approx$ 1), while systems with *both* features (e.g., D-B-A para-terphenyl with $\sim 60^{\circ}$ torsion) exhibit highly asymmetric I-V curves and large RR values at low bias.

# 3\. Involved Systems

## System 1: Unsubstituted para-terphenyl

  - Core Molecule:
      - abbreviation: Unsubstituted tailored system (Fig 5a)
      - full\_chemical\_name: para-terphenyl
      - core\_smiles: N/A
  - Anchors:
      - anchor\_groups: ['Thiolate\_S-']
  - Electrodes:
      - electrode\_material: Au
      - electrode\_surface: (111)
  - Interface:
      - interface\_geometry\_text: Thiolate-S binds to Au(111) electrodes. The paper uses Au(111) nanowires. This is modeled in MST using a standard thiolate-Au junction template (e.g., trimer).
  - Variation\_notes: "Baseline (unsubstituted) tailored system. The minimum-energy geometry is non-planar with torsion angles of \~40°."

## System 2: Substituted para-terphenyl (D-B-A)

  - Core Molecule:
      - abbreviation: Substituted tailored system (Fig 5b)
      - full\_chemical\_name: para-terphenyl substituted with amino (donor) and nitro (acceptor) groups.
      - core\_smiles: N/A
  - (Anchors, Electrodes, and Interface are the same as System 1)
  - Variation\_notes: "D-B-A tailored system. The minimum-energy geometry is non-planar with optimized torsion angles close to 60° (e.g., -63°, 65°)."

# 4\. Applicability Assessment

**Applicable.**

The core computational objective is to calculate finite-bias I-V characteristics and rectification ratios. This is a primary, intended application of the QDHC L3 scheme. While the original paper used a full DFT-NEGF method (TranSIESTA), the MST L3 scheme (using DFTB+ and a Uniform External Electric Field via the `L3_EEF` module) is designed to capture the same fundamental physics: the asymmetric response of the molecular orbitals and transmission spectrum to an applied bias, which is the mechanism for rectification.

# 5\. Hierarchical Analysis

**Level: L3**

The problem maps directly to L3. The core question is "How does transport, and specifically rectification, evolve under an applied finite bias?" This is explicitly covered by the L3 Core Question: "Is transport governed primarily by molecular level alignment with the electrode Fermi level or by the applied finite bias?" The key analytical evidence in the paper (Figures 2-5, 7) consists of "I–V... characteristics" and "discussion of rectification ratios," which are the exact indicators listed in the QDHC guide for requiring an L3 analysis. The mechanism itself—an asymmetric shift of the $T(E)$ spectrum under bias (Figure 4c,d)—is a non-equilibrium phenomenon that only L3 can model.

# 6\. Input Preparation

Based on the L3 workflow for finite-bias, two full junction structures must be manually created from MST templates and converted.

1.  **MST Template**: The thiolate-S anchor on Au(111) suggests using a standard MST junction template, such as `[MST_root]/share/device/junction_trimer_...xyz`.
2.  **User-Created Junction Files (`.xyz`)**:
      - Create `junction_trimer_terphenyl_unsub.xyz`: Replace the placeholder molecule in the trimer template with the unsubstituted para-terphenyl molecule.
      - Create `junction_trimer_terphenyl_DBA.xyz`: Replace the placeholder with the D-B-A substituted para-terphenyl molecule.
3.  **Conversion Script**: The `xyz2POSCAR.py` script (from `[MST_root]/share/`) is required.
4.  **Helper Script**: The `current_parallel.py` script (from `[MST_root]/share/`) is required to run the `L3_EEF` module for the I-V curve.
5.  **EM Lengths**: The length of the extended molecule (L\_EM) along the transport (z) direction must be manually measured (in Ångstroms) from each of the two `.xyz` files (e.g., `L_unsub`, `L_DBA`). This value is a required input for the `current_parallel.py` script.
6.  **Directory Structure**:
      - Create two directories: `unsubstituted/` and `substituted_DBA/`.
      - Place each corresponding `junction_trimer_...xyz` file into its directory.

# 7\. Computational Workflow

## Goal:

Compute and compare the finite-bias I-V curves for the unsubstituted (System 1) and D-B-A substituted (System 2) para-terphenyl junctions to reproduce the bias-induced rectification.

## Step 1. Create directories and Prepare Inputs

Create the directory structure and place the corresponding user-created junction `.xyz` files inside:

```
/unsubstituted/junction_trimer_terphenyl_unsub.xyz
/substituted_DBA/junction_trimer_terphenyl_DBA.xyz
```

Also copy `xyz2POSCAR.py` and `current_parallel.py` into each of the two directories.

## Step 2. Convert to POSCAR

Run the `xyz2POSCAR.py` conversion script in *each* of the two directories.

1.  **For the `unsubstituted` system:**
    ```bash
    cd unsubstituted
    # Edit xyz2POSCAR.py: set xyz_filename = 'junction_trimer_terphenyl_unsub.xyz'
    python xyz2POSCAR.py
    cd ..
    ```
2.  **For the `substituted_DBA` system:**
    ```bash
    cd substituted_DBA
    # Edit xyz2POSCAR.py: set xyz_filename = 'junction_trimer_terphenyl_DBA.xyz'
    python xyz2POSCAR.py
    cd ..
    ```
      - This generates `POSCAR` and `EM_atom.txt` in each directory.

## Step 3. Run L3 Finite-Bias Calculation

Run the `current_parallel.py` script in *each* of the two directories.

**In each directory (`unsubstituted/`, `substituted_DBA/`)**:

1.  **Edit `current_parallel.py`**:

      - `poscar_file`: `"POSCAR"`
      - `Length`: Set this to the specific measured length for the system in that directory (e.g., `L_unsub` or `L_DBA`).
      - `input_energy_range`: `2` (Scans $E_F \pm 2$ eV)
      - `input_energy_interval`: `0.0025` (A dense grid is needed for integration)
      - `electric_field_range`: `np.arange(-0.0003, 0.00031, 0.00005)` (This scans 12 points from -0.0003 to +0.0003 a.u., corresponding to the low bias range of $\approx \pm 0.3$ V needed by the paper, depending on the exact EM length).
      - `max_workers`: Set based on available system RAM and CPU cores (e.g., `2`).

2.  **Run the script**:

    ```bash
    python current_parallel.py
    ```

      - The script automatically runs `L3_EEF` for all bias points.
      - When finished, it generates `combined_transmission.txt` and the final I-V data in `voltage_current.txt`.

## Step 4. Post-processing and Analysis

1.  Collect the `voltage_current.txt` file from each of the two directories (`unsubstituted/` and `substituted_DBA/`).
2.  Use a plotting tool to plot the I-V data from both files on the same graph.
3.  Analyze the plot:
      - Verify that the `unsubstituted` curve is symmetric (or nearly symmetric) around 0V.
      - Verify that the `substituted_DBA` curve is highly asymmetric (rectifying).
      - Calculate the rectification ratio $RR = |I(V) / I(-V)|$ at the voltage corresponding to $\pm 0.3$ V to confirm the rectification enhancement.