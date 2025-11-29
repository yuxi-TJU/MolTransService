# 0\. Metadata

  - Title: Resonant charge transport in conjugated molecular wires beyond 10 nm range
  - DOI: (Omit this part)

# 1\. Literature Summary

This is an 'experiment + computation' study on long-range charge transport in single molecular wires. The authors use a scanning tunneling microscope (STM) to repeatedly lift and measure the conductance of single poly-porphyrin (bp-ppo) wires on a Au(111) surface, testing lengths from 1.3 nm up to 13 nm. The key experimental finding is that for wires longer than 6 nm, the conductance becomes nearly length-independent (attenuation $\beta < 0.001 \AA^{-1}$), which is a hallmark of coherent resonant transport. The paper's computations (DFT+NEGF using ATK) support this finding, revealing that the high, length-independent conductance is mediated by a delocalized Lowest Unoccupied Molecular Orbital (LUMO) acting as the resonant transport channel. The computations also successfully model the observed conductance peak shifts as a function of wire length and applied bias.

# 2\. Computational Objectives

The primary computational objective is to support and explain the experimental findings of length-dependent resonant transport. The goal is to compute the non-equilibrium transport properties (specifically, the bias-dependent transmission or differential conductance) for oligomers of increasing length. The expected result is to show that:

1.  Transport is dominated by a LUMO-based resonance.
2.  The conductance peaks associated with this resonance shift to more negative bias voltages as the molecular wire length increases, corroborating the experimental $dI/dV$ measurements (Fig. 4f) and LDC maps (Fig. 4d, e).

# 3\. Involved Systems

The paper's computational models focus on simulating the "strong contact" case, which the SI notes is modeled using an Au-S bond. The simulations in Fig. 4f and S6 compare double and triple TPP units.

## System 1: Double-unit bp-ppo

  - Core Molecule:
      - abbreviation: bp-ppo (2-unit)
      - full\_chemical\_name: N/A
      - core\_smiles: N/A
  - Anchors:
      - anchor\_groups: ['Thiolate\_S-']
  - Electrodes:
      - electrode\_material: Au
      - electrode\_surface: (111)
  - Interface:
      - interface\_geometry\_text: Thiolate-S (modeling the experimental 'strong contact') binds to Au(111) electrodes. The simulation models (e.g., Fig S6a) show the molecule bridging two flat Au electrodes.
  - Variation\_notes: "Double TPP unit (n=2) wire, corresponding to the black trace in Fig. 4f."

## System 2: Triple-unit bp-ppo

  - Core Molecule:
      - abbreviation: bp-ppo (3-unit)
      - full\_chemical\_name: N/A
      - core\_smiles: N/A
  - (Anchors, Electrodes, and Interface are the same as System 1)
  - Variation\_notes: "Triple TPP unit (n=3) wire, corresponding to the red trace in Fig. 4f."

# 4\. Applicability Assessment

**Applicable.**

The original paper uses DFT+NEGF (with LDA/GGA functionals) to compute finite-bias $dI/dV$ and $T(E,V)$ spectra. The core objective—calculating non-equilibrium transport to see how resonance peaks shift with bias and length—is precisely the intended use case for the MST L3 scheme. The QDHC guide identifies "I–V or dI/dV characteristics" and "applied finite bias" as L3 problems. While MST L3 uses DFTB+ (a different electronic structure method), it employs the same NEGF formalism and simulates finite bias with a Uniform External Electric Field (EEF), making it suitable for reproducing the qualitative trends (i.e., the *direction* of the peak shift) reported in the paper's computations. The paper also finds the metal center (Fe) is not critical for long-range transport, so modeling the free-base porphyrin is appropriate.

# 5\. Hierarchical Analysis

**Level: L3**

The core computational evidence in the paper consists of finite-bias differential conductance ($dI/dV$) spectra (Fig. 4f) and bias-dependent transmission maps ($T(E,V)$) (Fig. 3b, S6b). The computational objective is to explain how the LUMO resonance shifts as a function of *both* molecular length and *applied bias*. This is fundamentally a non-equilibrium transport problem. The QDHC guide explicitly states that L3 is required for "I–V or dI/dV characteristics" and problems governed by "applied finite bias". L1 and L2 modules are designed for zero-bias calculations and cannot reproduce these key results.

# 6\. Input Preparation

Based on the L3 workflow, full junction structures must be manually created for the two systems.

1.  **MST Template**: The "strong contact" is modeled as Thiolate-S on Au(111). We will use the trimer template: `[MST_root]/share/device/junction_trimer_...xyz`.
2.  **User-Created Junction Files (`.xyz`)**:
      - Create `junction_trimer_bppo_2unit.xyz`: Replace the placeholder molecule in the trimer template with the 2-unit bp-ppo molecule.
      - Create `junction_trimer_bppo_3unit.xyz`: Replace the placeholder with the 3-unit bp-ppo molecule.
3.  **Conversion Script**: The `xyz2POSCAR.py` script (from `[MST_root]/share/`) is required.
4.  **Helper Script**: The `current_parallel.py` script (from `[MST_root]/share/`) is required to run the `L3_EEF` module.
5.  **EM Lengths**: The length of the extended molecule ($L_{EM}$) along the transport (z) direction must be measured from each of the two `.xyz` files (e.g., `L_2unit`, `L_3unit`) in Ångstroms. This is a required input for `current_parallel.py`.
6.  **Directory Structure**:
      - Create two directories: `n2/`, `n3/`.
      - Place each corresponding `junction_trimer_...xyz` file into its directory.

# 7\. Computational Workflow

## Goal:

Compute and compare the finite-bias transmission spectra $T(E,V)$ for the 2-unit and 3-unit bp-ppo wires.

## Step 1. Create directories and Prepare Inputs

Create the directory structure and place the corresponding user-created junction `.xyz` files inside:

```
/n2/junction_trimer_bppo_2unit.xyz
/n3/junction_trimer_bppo_3unit.xyz
```

Copy `xyz2POSCAR.py` and `current_parallel.py` from `[MST_root]/share/` into *each* of the two directories.

## Step 2. Convert to POSCAR

Run the `xyz2POSCAR.py` conversion script in *each* of the two directories.

1.  **For the `n2` system:**
    ```bash
    cd n2
    # Edit xyz2POSCAR.py: set xyz_filename = 'junction_trimer_bppo_2unit.xyz'
    python xyz2POSCAR.py
    cd ..
    ```
2.  **For the `n3` system:**
    ```bash
    cd n3
    # Edit xyz2POSCAR.py: set xyz_filename = 'junction_trimer_bppo_3unit.xyz'
    python xyz2POSCAR.py
    cd ..
    ```
    *This generates `POSCAR` and `EM_atom.txt` in each directory.*

## Step 3. Run L3 Finite-Bias Calculation

Run the `current_parallel.py` script in *each* of the two directories to compute the $T(E,V)$ maps.

**In each directory (`n2/`, `n3/`)**:

1.  **Edit `current_parallel.py`**:

      - `poscar_file`: `"POSCAR"`
      - `Length`: Set this to the specific measured length for the system in that directory (e.g., `L_2unit` or `L_3unit`).
      - `input_energy_range`: `3` (The paper's spectra span several eV, e.g., -2.0V to 2.0V, so $E_F \pm 3$ eV provides a safe window).
      - `input_energy_interval`: `0.01`
      - `electric_field_range`: `np.arange(-0.0008, 0.0009, 0.0001)` (This scans a range of positive and negative fields to map the bias-dependent behavior).
      - `max_workers`: Set based on available system RAM (e.g., `2`).

2.  **Run the script**:

    ```bash
    python current_parallel.py
    ```

    *The script automatically runs `L3_EEF` for all bias points and generates `combined_transmission.txt` (the $T(E,V)$ map) and `voltage_current.txt`.*

## Step 4. Post-processing and Analysis

1.  Collect the `combined_transmission.txt` file from both the `n2/` and `n3/` directories.
2.  Use a plotting tool to visualize these files as 2D color maps (plotting Transmission vs. Energy and Voltage), similar to Fig. S6b in the paper.
3.  Analyze the plots:
      - Identify the LUMO resonance (the band of high transmission).
      - Compare the two plots to verify that the LUMO resonance for the `n3` (3-unit) system shifts to a more negative bias compared to the `n2` (2-unit) system, reproducing the key computational trend shown in Fig. 4f and Fig. S6b.