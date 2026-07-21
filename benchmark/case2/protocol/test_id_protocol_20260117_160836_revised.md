# 0. Metadata
 - Protocol status: Revised with as-executed L2 settings

# 1. Query Summary
The user has experimentally observed that alkynyl-terminated oligophenylenes (OPAn, n=2-4) have lower conductance than analogous methylene-terminated oligophenylenes (OPMn, n=2-4) when forming C-Au bonds. They hypothesize that this difference originates from the distinct interfacial hybridization of the sp and sp3 carbon contacts. The workflow should calculate and compare the zero-bias transmission spectra and conductance-decay trends of all six systems at L2, estimate the theoretical attenuation factor (β) independently for the OPA and OPM series, and perform a detailed L3 interfacial orbital analysis for representative OPA3 and OPM3 junctions.

# 2. Computational Objectives
1.  Calculate the zero-bias transmission spectra, T(E), for OPA2, OPA3, OPA4, OPM2, OPM3, and OPM4 using the same L2 settings.
2.  Extract the transmission at the common L2 reference energy for all six systems.
3.  Determine the theoretical attenuation factors β for both the OPA and OPM series from `ln[T(E_ref)]` versus the number of phenyl rings, n.
4.  Compare the transmission magnitudes and line shapes of the two series to establish the contact-dependent conductance trend associated with sp and sp3 carbon-gold bonding.
5.  Perform an interfacial orbital analysis for representative OPA3 and OPM3 junctions.
6.  Identify and visualize the molecular and electrode states contributing to the selected transport features near the electrode Fermi level.

# 3. Involved Systems

## System 1: OPA2
 - Core Molecule:  
	- abbreviation: OPA2
	- full_chemical_name: 4,4'-diethynyl-1,1'-biphenyl
	- core_smiles: 
 - Anchors:  
	- anchor_groups: ['Alkynyl_C']
 - Electrodes:  
	- electrode_material: Au
	- electrode_surface: N/A (cluster model)
 - Interface:  
	- interface_geometry_text: Direct covalent C(sp)-Au σ-bond to an Au pyramid.
 - Variation_notes: Baseline for length-dependence study (n=2) with sp-hybridized anchors.

## System 2: OPA3
 - Core Molecule:  
	- abbreviation: OPA3
	- full_chemical_name: 4,4''-diethynyl-1,1':4',1''-terphenyl
	- core_smiles: 
 - Variation_notes: Member of homologous series (n=3) with sp-hybridized anchors.

## System 3: OPA4
 - Core Molecule:  
	- abbreviation: OPA4
	- full_chemical_name: 4,4'''-diethynyl-1,1':4',1'':4'',1'''-quaterphenyl
	- core_smiles: 
 - Variation_notes: Member of homologous series (n=4) with sp-hybridized anchors.

## System 4: OPM2
 - Core Molecule:  
	- abbreviation: OPM2
	- full_chemical_name: 4,4'-dimethyl-1,1'-biphenyl
	- core_smiles: 
 - Anchors:  
	- anchor_groups: ['Methylene_C']
 - Electrodes:  
	- electrode_material: Au
	- electrode_surface: N/A (cluster model)
 - Interface:  
	- interface_geometry_text: Direct covalent C(sp3)-Au σ-bond to an Au pyramid.
 - Variation_notes: n=2 member of the methylene-contacted OPM series.

## System 5: OPM3
 - Core Molecule:  
	- abbreviation: OPM3
	- full_chemical_name: 4,4''-dimethyl-1,1':4',1''-terphenyl
	- core_smiles: 
 - Anchors:  
	- anchor_groups: ['Methylene_C']
 - Electrodes:  
	- electrode_material: Au
	- electrode_surface: N/A (cluster model)
 - Interface:  
	- interface_geometry_text: Direct covalent C(sp3)-Au σ-bond to an Au pyramid.
 - Variation_notes: n=3 member of the methylene-contacted OPM series.

## System 6: OPM4
 - Core Molecule:  
	- abbreviation: OPM4
	- full_chemical_name: 4,4'''-dimethyl-1,1':4',1'':4'',1'''-quaterphenyl
	- core_smiles: 
 - Anchors:  
	- anchor_groups: ['Methylene_C']
 - Electrodes:  
	- electrode_material: Au
	- electrode_surface: N/A (cluster model)
 - Interface:  
	- interface_geometry_text: Direct covalent C(sp3)-Au σ-bond to an Au pyramid.
 - Variation_notes: n=4 member of the methylene-contacted OPM series.

# 4. Applicability Assessment
**Applicable.**

The query focuses on coherent, single-molecule transport through gold electrodes and is within the scope of the QDHC framework. Explicit finite Au clusters are required for the six-system contact-dependent comparison at L2, while electrode-referenced interfacial orbital diagnosis requires selective escalation of OPA3 and OPM3 to L3.

# 5. Hierarchical Analysis

 - L1 Assessment
   - **Applicable?** YES. L1 could describe molecule-length attenuation within an individual homologous series.
   - **Escalation needed?** YES. L1 does not explicitly represent the different carbon-gold contacts and therefore cannot adequately test the contact-hybridization origin of the conductance gap.

 - L2 Assessment
   - **Applicable?** YES. L2 explicitly models the interface with electrode clusters, allowing it to capture how different anchoring chemistries and hybridization affect transmission.
   - **Escalation needed?** YES for electrode-referenced orbital diagnosis. The common finite-cluster HOMO reference is sufficient for relative L2 trends but not for definitive analysis of states referenced to the bulk-electrode Fermi level.

 - L3 Assessment
   - **Applicable?** YES. L3 provides the electrode-referenced energy scale and MPSH/eigenchannel tools required for the representative OPA3/OPM3 interfacial diagnosis.
   - **Scope warning:** None. The query asks for qualitative identification of contributing orbitals relative to E_F, not quantitative absolute level alignment.

 - Final Recommendation
   - **Staged Path: L2 (trend verification) → L3 (full analysis).**
   - Use L2 for the common six-system transmission calculations, matched-length OPA/OPM comparisons, and separate attenuation fits for the two series.
   - Selectively escalate OPA3 and OPM3 to L3 for electrode-referenced MPSH and eigenchannel analysis.

# 6. Input Preparation

## L2 Input Preparation
The L2 workflow requires six "Extended Molecule" (EM) `.xyz` files containing the target molecule between two Au pyramid contacts.

1.  **EM Files**:
    Prepare the following six EM structures while retaining the Au pyramid blocks and the atom ordering required by `L2_Align`:
    -   `em_opa2.xyz`
    -   `em_opa3.xyz`
    -   `em_opa4.xyz`
    -   `em_opm2_xtbopt.xyz`
    -   `em_opm3_xtbopt.xyz`
    -   `em_opm4_xtbopt.xyz`

2.  **Directory Structure**:
    All paths are relative to `benchmark/case2/`:
    ```text
    extended_molecules/
      opa2/em_opa2.xyz
      opa3/em_opa3.xyz
      opa4/em_opa4.xyz
      opm2/em_opm2_xtbopt.xyz
      opm3/em_opm3_xtbopt.xyz
      opm4/em_opm4_xtbopt.xyz
    ```

    The Au pyramid blocks must be treated as rigid units, and their original atom ordering must be preserved.

## L3 Input Preparation
The L3 workflow requires the manual creation of full junction structures. A pyramid interface model is suitable for modeling the direct C-Au bond.

1.  **MST Templates**: Use the `junction_example_pyramid_amine.xyz` template from `[MST_root]/share/device/` as a starting point.
2.  **User-Created Junction Files (`.xyz`)**:
    -   `junction_pyramid_opa3.xyz`: Modify the pyramid template by replacing the placeholder molecule with the OPA3 molecule, forming a C-Au bond at each end.
    -   `junction_pyramid_opm3.xyz`: Create a reference junction by replacing the placeholder with the OPM3 molecule, forming a C(sp3)-Au bond at each end.
3.  **Conversion Script**: The `xyz2POSCAR.py` script, located in `[MST_root]/share/`, is required for file conversion.
4.  **Directory Structure**: Create separate `opa3/` and `opm3/` directories and place the corresponding user-created junction `.xyz` file inside each directory.

# 7a. L2 Computational Workflow

## Goal:
Compute T(E) for OPA2-4 and OPM2-4 using one common L2 setup, determine β independently for the OPA and OPM series, and compare the contact-dependent transmission of matched-length sp and sp3 systems.

## Step 1. Create directories
Set up the six directories (`opa2/`, `opa3/`, `opa4/`, `opm2/`, `opm3/`, and `opm4/`) under `extended_molecules/` and place the corresponding EM files inside each directory, as described in Section 6.

## Step 2. Build "EM + Cluster" Systems
Run the `L2_Align` module in each of the six directories to generate the full system file (`aligned.xyz`).

**1. For OPA2:**
```bash
cd extended_molecules/opa2
L2_Align 
# At the prompt, enter: em_opa2.xyz
cd ../..
```
**2. For the other five systems:**
Repeat the process in the respective directories, providing the correct EM filename at the prompt.
```bash
cd extended_molecules/opa3; L2_Align; cd ../.. # Enter em_opa3.xyz
cd extended_molecules/opa4; L2_Align; cd ../.. # Enter em_opa4.xyz
cd extended_molecules/opm2; L2_Align; cd ../.. # Enter em_opm2_xtbopt.xyz
cd extended_molecules/opm3; L2_Align; cd ../.. # Enter em_opm3_xtbopt.xyz
cd extended_molecules/opm4; L2_Align; cd ../.. # Enter em_opm4_xtbopt.xyz
```

## Step 3. Run Transport Calculations
Run the interactive `L2_Trans` module in each of the six directories. Use the same parameters for all calculations to ensure a valid comparison.

**Example for OPA2:**
```bash
cd extended_molecules/opa2
L2_Trans
```
Follow the interactive prompts, entering the following values:
-   `Enter XYZ file name (...)`: `aligned.xyz`
-   `Enter calculation method (...)`: `1` (for GFN1-xTB)
-   `Specify the cluster atom number (25 or 28)`: `28`
-   `Specify the energy range (...)`: `4.0`
-   `Specify the energy interval (...)`: `0.01`

Repeat this exact `L2_Trans` procedure in the `opa3`, `opa4`, `opm2`, `opm3`, and `opm4` directories. This setup produces 801 points over `E_ref ± 4.0 eV` with a spacing of `0.01 eV`. The common cluster-HOMO reference energy in the completed calculations was `E_ref = -11.14726 eV`.

## Step 4. L2 Post-processing and Analysis
This workflow will generate `Transmission.txt` and `Transmission.png` in each of the six directories.

1.  **Extract Conductance Values**: For all six calculations, use the finite-cluster HOMO reference printed by L2 and extract `T(E_ref)` from the corresponding `Transmission.txt` file. Treat `G/G0 = T(E_ref)` as the common L2 conductance proxy; do not describe this finite-cluster reference as a bulk-electrode Fermi level.

2.  **Calculate Attenuation Factor (β)**:
    -   For OPA2, OPA3, and OPA4, fit `ln[T(E_ref)]` against `n = 2, 3, 4`.
    -   For OPM2, OPM3, and OPM4, perform a separate fit of `ln[T(E_ref)]` against `n = 2, 3, 4`.
    -   Use `ln[T(E_ref)] = a + b n` and report `β = -b` in units of inverse phenyl repeat units.

3.  **Compare Interface Coupling**:
    -   Plot all six T(E) spectra on a common absolute-energy axis with a logarithmic transmission axis.
    -   Compare the matched-length pairs OPA2/OPM2, OPA3/OPM3, and OPA4/OPM4.
    -   Analyze the relative transmission magnitudes and spectral broadening consistently across the two series.

4.  **Generate Compact Outputs**:
    -   Six-system spectra: `outputs/data/l2_transmission_spectra.csv`.
    -   Reference-energy transmissions: `outputs/data/l2_conductance_summary.csv`.
    -   OPA and OPM attenuation fits: `outputs/data/l2_attenuation_fits.csv`.
    -   Six-system spectrum plot: `outputs/figures/l2_transmission_spectra.png`.
    -   Length-attenuation plot: `outputs/figures/lnG_vs_n.png`.

5.  **Validation Targets from the Completed Workflow**:
    -   `β_OPA ≈ 0.76` per phenyl repeat unit.
    -   `β_OPM ≈ 1.75` per phenyl repeat unit.
    -   At each matched value of n, the OPM system has a larger `T(E_ref)` than the corresponding OPA system.

# 7b. L3 Computational Workflow

## Goal:
Compute the zero-bias T(E) spectra for the OPA3 and OPM3 systems to perform a detailed eigenchannel analysis on the dominant transport features near E_F for OPA3 and OPM3.

## Step 1. Create directories and Prepare Inputs
Set up the project with a directory for each system and place the corresponding `.xyz` file inside.

```
/opa3/junction_pyramid_opa3.xyz
/opm3/junction_pyramid_opm3.xyz
```

## Step 2. Convert to POSCAR format
In each of the two directories, run the `xyz2POSCAR.py` script to generate the `POSCAR` file required by the L3 modules.

1.  **For the `opa3` system:**
    ```bash
    cd opa3
    # Copy xyz2POSCAR.py from [MST_root]/share/ into this directory
    # Edit xyz2POSCAR.py: set xyz_filename = 'junction_pyramid_opa3.xyz'
    python xyz2POSCAR.py
    cd ..
    ```
2.  **Repeat this process** for the `opm3` directory, editing the `xyz_filename` variable in the script accordingly. This will generate `POSCAR` and `EM_atom.txt` in each directory.

## Step 3. Run Zero-Bias Transport Calculation
Run the interactive `L3_Trans` module in each of the two directories to compute the transmission spectra.

1.  **For the `opa3` system:**
    ```bash
    cd opa3
    L3_Trans
    ```
    - Follow the interactive prompts:
        - `Enter POSCAR file name(...)`: `POSCAR`
        - `Specify the energy range (...)`: `2.5` (to scan E_F ± 2.5 eV)
        - `Specify the energy interval (...)`: `0.01`
    ```bash
    cd ..
    ```
2.  **Repeat this exact process** for the `opm3` directory, using the same energy range and interval for both calculations.

## Step 4. Post-processing and Analysis
This workflow generates the necessary files for interfacial orbital analysis.

**Interfacial Orbital Analysis (for OPA3 and OPM3)**:
    -   Focus on the `opa3/` and `opm3/` directories.
    -   **Identify Peak Energy**: Examine the `Transmission.txt` (or `.png`) file in each directory to find the energy of the dominant transmission peak closest to E_F=0. Let's call this `E_peak`.
    -   **Generate MPSH Orbitals**: In each directory, run the `L3_MPSH` module. This will create an `MPSH.molden` file for visualizing the basis orbitals of the extended molecule.
        ```bash
        cd opa3
        L3_MPSH
        cd ../opm3
        L3_MPSH
        cd ..
        ```
    -   **Analyze Eigenchannel Composition**: In each directory, run the interactive `L3_EC` module. When prompted, enter the `E_peak` value you identified.
        ```bash
        cd opa3
        L3_EC
        # At the prompt, enter the E_peak value for OPA3
        cd ../opm3
        L3_EC
        # At the prompt, enter the E_peak value for OPM3
        cd ..
        ```
    -   **Interpret Results**: The `L3_EC` module will print the MPSH orbitals that contribute most to the transport at `E_peak`. It will also generate `.molden` files (e.g., `EigenChannel_abs_...molden`) for visualizing the spatial distribution of this transport channel. By comparing the contributing MPSH orbitals (visualized from `MPSH.molden`) with the eigenchannel visualization, you can determine the specific molecular and gold orbitals (e.g., Au-s vs Au-d) involved in the coupling, thus verifying the hypothesis. Repeat for both OPA3 and OPM3 to contrast the sp and sp3 interfaces.
