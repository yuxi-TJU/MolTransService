# 0. Metadata
 - Title:  (Omit this part)  
 - DOI: (Omit this part)  

# 1. Query Summary
The user requests a computational protocol to investigate the relationship between molecular conformation and rectification properties in an asymmetric Au-S-dipyrimidinyl-diphenyl-S-Au (DPDP-type) junction. The protocol should involve scanning three internal torsional angles (phi_A, phi_B, phi_C) to create a 3D conformational transport landscape. For each conformation, the current at a specific finite-bias pair (+/-1.72 V) must be calculated to determine the rectification ratio and direction. The goal is to identify conformational regimes with favorable current-rectification trade-offs and select representative conformations for detailed analysis of their bias-dependent transmission spectra and MPSH orbital distributions. The entire workflow should be framed as an L3 finite-bias study.

# 2. Computational Objectives
1.  Generate a series of full molecular junction structures for the DPDP molecule, systematically scanning three torsional angles (phi_A, phi_B, phi_C) from 0 to 90 degrees.
2.  For each generated conformation, perform an L3 finite-bias calculation to compute the current at an electric field corresponding to approximately +/-1.72 V.
3.  From the calculated currents, determine the rectification ratio (RR = |I(+V)/I(-V)|) and rectification direction for each conformation.
4.  Construct a 3D landscape mapping the calculated current and rectification ratio to the torsional angles (phi_A, phi_B, phi_C).
5.  Analyze the landscape to identify conformational regimes that preserve forward rectification, switch to reverse rectification, or offer an improved current-rectification trade-off.
6.  Select representative conformations from these regimes for further in-depth analysis, including comparison of their full bias-dependent transmission spectra and visualization of their MPSH orbital distributions.

# 3. Involved Systems

## System 1: DPDP-type Molecule
 - Core Molecule:  
	- abbreviation: DPDP
	- full_chemical_name: N/A (Asymmetric dipyrimidinyl-diphenyl)
	- core_smiles: 
 - Anchors:  
	- anchor_groups: ['Thiol_SH']
 - Electrodes:  
	- electrode_material: Au
	- electrode_surface: 111
 - Interface:  
	- interface_geometry_text: Thiolate-S binds to Au(111) electrodes. The validated junction structure serves as the template, likely involving a specific binding site like hollow, bridge, or an adatom motif.
 - Variation_notes: This is a single system whose internal conformation is varied by scanning three torsional angles (phi_A, phi_B, phi_C). Each point in the scan represents a unique geometric configuration.

# 4. Applicability Assessment
**Applicable.**

The query's core requirements—calculating finite-bias I-V characteristics, determining rectification ratios, and analyzing bias-dependent transmission spectra—are standard two-terminal transport problems. The system involves Au electrodes and a coherent transport mechanism, which are within the scope of the QDHC framework. The problem does not require any of the "Out-of-Scope" criteria, such as precise absolute level alignment or spintronics.

# 5. Hierarchical Analysis

 - L1 Assessment
   - Applicable? NO. The query requires the calculation of finite-bias current and rectification, which are non-equilibrium properties.
   - Escalation needed? YES. L1 neglects finite-bias nonequilibrium response, which is a central requirement of the query. The analysis must be escalated to a tier that includes bias effects.

 - L2 Assessment
   - Applicable? NO. While L2 captures interface effects, it is an equilibrium (zero-bias) model.
   - Escalation needed? YES. L2 neglects the alignment to the electrode Fermi level and the non-equilibrium response under an applied bias, both of which are essential for calculating I-V curves and rectification. The analysis must be escalated to L3.

 - L3 Assessment
   - Applicable? YES. The query explicitly requests the calculation of finite-bias observables (current at +/-V, rectification ratio) and analysis of bias-dependent phenomena (bias-dependent transmission spectra). As per the QDHC guide, these are defining applications of the L3 tier, which captures "Nonequilibrium finite-bias response (I–V)".
   - Scope warning: None. The query asks for a standard L3 analysis, not for experimentally quantitative absolute level alignment.

 - Final Recommendation
   - The query explicitly frames the problem as an L3 study and requires the calculation of finite-bias properties (I-V, rectification) for a large set of conformations. This task falls squarely and exclusively within the L3 domain. A lower tier cannot provide the necessary physical observables.

 - Final Tier
<FINAL_TIER>L3</FINAL_TIER>

# 6. Input Preparation
The L3 workflow will be used. Because this is a large conformational scan, the structure preparation and transport setup should be automated.

1.  **Baseline Molecular Structure**:  
    -   Use a baseline DPDP molecular `.xyz` structure (for example, `dpdp_0_0_0.xyz`) as the starting point for the conformational scan.
    -   The three torsional coordinates are defined around three fixed internal bond axes:
        -   `phi_A`: dihedral between the two phenyl rings in the diphenyl unit
        -   `phi_B`: dihedral between the dipyrimidinyl and diphenyl units
        -   `phi_C`: dihedral between the two pyrimidinyl rings in the dipyrimidinyl unit
2.  **User-Created Conformation Files (`.xyz`)**:
    -   Generate the conformational set by scanning `phi_A`, `phi_B`, and `phi_C` over `0, 15, 30, 45, 60, 75, 90` degrees.
    -   This gives a `7 x 7 x 7 = 343` point grid.
    -   A geometry-operation script should be prepared to apply the torsional rotations and save one molecular `.xyz` file for each conformation.
    -   A convenient directory structure is:
        ```
        /scan_root/A_000/B_000/C_000/
        /scan_root/A_000/B_000/C_015/
        ...
        /scan_root/A_090/B_090/C_090/
        ```
    -   Each `C_*` directory should contain one molecular conformation file, for example `dpdp_A000_B000_C000.xyz`.
3.  **User-Created Junction Files (`.xyz`)**:
    -   For each molecular conformation, create a full Au-molecule-Au trimer junction `.xyz` file using an MST trimer device template.
    -   The junction construction should preserve the validated DPDP contact motif and use the same anchor definition consistently across the scan.
    -   In the completed scan setup, the junction assembly uses left/right anchor indices `2` and `39` in the molecular file and Au-S bond lengths of `2.386 Å` on both sides.
    -   Each conformation directory should then contain one corresponding junction file, e.g. `junction_dpdp_A000_B000_C000.xyz`.
4.  **Conversion Script**:
    -   The `xyz2POSCAR.py` script, located in `[MST_root]/share/`, is required for file conversion.
    -   This script should be run in each conformation directory after setting `xyz_filename` to the corresponding junction `.xyz` file.
5.  **Extended Molecule Length (L_EM)**:
    -   The extended-molecule length along the transport axis must be measured and recorded for the generated junctions.
    -   In practice, the measured values across this scan are nearly constant, around `22.27 Å`, and the transport calculations may use a common rounded value such as `22.2746`.
6.  **Finite-Bias Driver Parameters**:
    -   The finite-bias calculations should be configured with:
        -   `poscar_file`: `"POSCAR"`
        -   `Length`: `22.2746`
        -   `save_mat_files`: `True`
        -   `input_energy_range`: `2`
        -   `input_energy_interval`: `0.01`
        -   `electric_field_range`: `np.array([-0.0015, 0.0, 0.0015])`
    -   This field set corresponds to the three target bias points `-1.718 V`, `0 V`, and `+1.718 V`.

# 7. Computational Workflow

## Goal:
To compute the current and rectification ratio for a 3D landscape of molecular conformations, identify optimal geometries, and perform detailed analysis on representative cases.

## Step 1. Create directories and Generate Conformations
1.  Create a root project directory.
2.  Write and execute a master script (as described in Section 6) that generates the full set of conformational `.xyz` files and organizes them into a directory structure like:
    ```
    /scan_root/A_000/B_000/C_000/dpdp_A000_B000_C000.xyz
    /scan_root/A_000/B_000/C_015/dpdp_A000_B000_C015.xyz
    ...
    /scan_root/A_090/B_090/C_090/dpdp_A090_B090_C090.xyz
    ```
3.  The script should also prepare each conformation directory for the subsequent junction-building and transport setup steps.

## Step 2. Build Junctions and Convert to POSCAR
For each conformation directory, construct the corresponding trimer junction `.xyz` file, then run `xyz2POSCAR.py` to generate the `POSCAR` and `EM_atoms.txt` files needed for the L3 transport calculation.

## Step 3. Run High-Throughput Three-Point Finite-Bias Calculations
For each directory (e.g., `A_000/B_000/C_030/`):
1.  **Convert to POSCAR**: The script executes `python xyz2POSCAR.py` after setting the `xyz_filename` inside it.
2.  **Configure and Run L3_EEF**: The script edits a serial finite-bias driver with the specific parameters for that conformation:
    -   `poscar_file`: `"POSCAR"`
    -   `Length`: The pre-measured length for this specific conformation.
    -   `save_mat_files`: `True`
    -   `input_energy_range`: `2`
    -   `input_energy_interval`: `0.01`
    -   `electric_field_range`: `np.array([-0.0015, 0.0, 0.0015])`
3.  The script then executes the serial finite-bias driver. This will run the `L3_EEF` module for the negative-bias, zero-bias, and positive-bias field points, generating a `voltage_current.txt` file with three data points.

## Step 4. Post-processing and Landscape Analysis
1.  Write a final analysis script that:
    -   Traverses all `A_*/B_*/C_*` subdirectories.
    -   Reads the `voltage_current.txt` file from each one.
    -   Extracts the current values I(+) and I(-).
    -   Calculates the rectification ratio RR = |I(+)/I(-)|.
    -   Stores the results (phi_A, phi_B, phi_C, I(+), I(-), RR) in a master data file (e.g., a CSV).
2.  Use a plotting library (e.g., Matplotlib, Plotly) to visualize the 3D landscape data, for instance, by creating 2D slices of RR vs. (phi_A, phi_B) for a fixed phi_C.
3.  From these plots, identify the coordinates (phi_A, phi_B, phi_C) of representative conformations (e.g., max RR, min RR, max current with good RR).

## Step 5. Detailed Analysis of Representative Conformations
For each selected representative conformation:
1.  **Bias-dependent transmission comparison**:
    -   Use the existing three field directories:
        -   `Field_-0.0015/`
        -   `Field_0.0000/`
        -   `Field_0.0015/`
    -   Compare the corresponding `Transmission.txt` files directly to inspect the bias response associated with forward, reverse, or weak rectification.
2.  **MPSH and orbital-distribution analysis**:
    -   Use the files in `Field_0.0000/` for zero-field orbital analysis and compare with `Field_-0.0015/` and `Field_0.0015/` when field-dependent changes are of interest.
    -   If Molden-format visualization is required, run the appropriate MPSH export/analysis step in the representative field directory and inspect the resulting orbitals in Multiwfn or another visualization program.
