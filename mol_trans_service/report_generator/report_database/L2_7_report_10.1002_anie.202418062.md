# 0\. Metadata

 - Title:  Single-Molecule Mechanoresistivity by Intermetallic Bonding
 - DOI: (Omit this part)  

# 1\. Literature Summary

This is an 'experiment + computation' study. It investigates the mechanoresistive properties of organometallic molecular wires incorporating a $Pt(II)$ cation (e.g., L1PtCl and L2PtP). Using the STM-BJ technique, the authors find that these molecules exhibit two distinct conductance states (high-G and low-G). Mechanical compression and elongation of the junction can reversibly switch the device between these states, resulting in a large conductance modulation of up to three orders of magnitude. The primary finding, supported by DFT-NEGF calculations, is that this switching is caused by a change in the contact interface. The low-G state corresponds to a "relaxed" junction anchored via its terminal S-Au or N-Au groups, while the high-G state results from a "compressed" geometry where one electrode forms a direct, highly conductive intermetallic Pt-Au bond.

# 2\. Computational Objectives

The primary goal of the paper's theoretical transport calculation is to computationally validate the hypothesis that the observed high-G/low-G switching is caused by a mechanical-induced change in the molecule-electrode binding geometry. The calculation aims to compare the transmission function for a $Pt(II)$ complex in two distinct configurations: (1) a "relaxed" geometry where the molecule is anchored to the Au electrodes via its terminal S-Au (or N-Au) groups on both sides, and (2) a "compressed" geometry where one electrode binds to a terminal anchor and the other binds directly to the central $Pt(II)$ atom. The expected result is to show that the "compressed" (Pt-Au) geometry has a significantly higher transmission near the Fermi level, corresponding to the experimental high-G state.

# 3\. Involved Systems

## System 1: L1PtCl (Relaxed / Low-G State)

 - Core Molecule:  
      - abbreviation: L1PtCl
      - full\_chemical\_name: (Cyclometalated Pt(II) complex of 1,3-bis(5-(methylthio)pyridin-2-yl)-5-(tert-butyl)benzene with a chloride ligand)
      - core\_smiles: N/A
 - Anchors:  
      - anchor\_groups: ['Thioether\_SMe']
 - Electrodes:  
      - electrode\_material: Au
      - electrode\_surface: N/A (Calculations use Au clusters/pyramids)
 - Interface:  
      - interface\_geometry\_text: Thioether (S) group on both ends coordinates to an apex Au atom of the electrode clusters.
 - Variation\_notes: Represents the "relaxed" or "low-G" state (d=1.5 nm). The transport path is S...S.

## System 2: L1PtCl (Compressed / High-G State)

 - Core Molecule:  
      - abbreviation: L1PtCl
      - full\_chemical\_name: (Cyclometalated Pt(II) complex of 1,3-bis(5-(methylthio)pyridin-2-yl)-5-(tert-butyl)benzene with a chloride ligand)
      - core\_smiles: N/A
 - Anchors:  
      - anchor\_groups: ['Thioether\_SMe', 'Organometallic\_Pt']
 - Electrodes:  
      - electrode\_material: Au
      - electrode\_surface: N/A (Calculations use Au clusters/pyramids)
 - Interface:  
      - interface\_geometry\_text: One thioether (S) group coordinates to an apex Au atom. The central $Pt(II)$ atom forms a direct intermetallic bond with the other apex Au atom.
 - Variation\_notes: Represents the "compressed" or "high-G" state (d=1.0 nm). The transport path is S...Pt.

# 4\. Applicability Assessment

**Applicable.**

The paper's core computational goal is to compare the relative transmission of two distinct contact geometries (S-Au...Au-S vs. S-Au...Au-Pt). This is a problem of interface-dominated transport. While the QDHC guide notes that GFN-xTB (used in MST) may have reduced reliability for heavy transition-metal complexes like Pt(II) compared to the paper's DFT method, the GFN-xTB method does include parameters for Pt. Therefore, it is sufficient to capture the *qualitative trend*—the significant conductance increase caused by the formation of the direct Pt-Au intermetallic bond—which is the central question.

# 5\. Hierarchical Analysis

**Level: L2**

The paper's central claim is that the mechanoresistivity is "attributed to distinct contact geometries" and is triggered by "mechanical compression of the single-molecule device." The core computational question is to quantify how conductance changes with this "interfacial" rearrangement (S-S binding vs. S-Pt binding). This is not a problem of the isolated molecule's intrinsic properties (L1) or precise level alignment with $E_F$ (L3). It is a clear case of transport governed by the "local geometry and electronic coupling at the molecule-electrode interface." The QDHC Guide lists "conductance or T(E) changes with... anchoring chemistry" as key L2 evidence. The paper's own computational model (Fig. 4b), which compares two different cluster-molecule-cluster geometries, is conceptually identical to the "Extended Molecule + Electrode Clusters" model of the MST L2 scheme.

# 6\. Input Preparation

Based on the L2 workflow and the paper's computational model (Fig. 4b, which uses Au clusters), the user must manually prepare "Extended Molecule" (EM) `.xyz` files using a template like `4au-em.xyz` (pyramid) from `[MST_root]/share/em/`.

1.  **`em_relaxed.xyz`**:
      - Create this file by modifying the `4au-em.xyz` template.
      - Replace the placeholder molecule with the L1PtCl molecule.
      - Adjust the geometry to represent the "relaxed" (low-G) state: The thioether (S) atoms on both ends should be bound to the apex Au atoms of the two pyramids, corresponding to the "relaxed" structure in Fig. 4b.
2.  **`em_compressed.xyz`**:
      - Create this file using the *same* `4au-em.xyz` template.
      - Replace the placeholder with the L1PtCl molecule.
      - Adjust the geometry to represent the "compressed" (high-G) state: One thioether (S) atom binds to one apex Au atom. The central $Pt(II)$ atom binds *directly* to the other apex Au atom, as shown in the "compressed" structure in Fig. 4b.
3.  **Constraint**: For both files, the Au atoms of the pyramid template must remain a rigid, unified block, and their original atom order from the template file must be strictly maintained.

# 7\. Computational Workflow

## Goal:

Compute and compare the zero-bias T(E) spectra for the "relaxed" (S-S) and "compressed" (S-Pt) junction geometries to validate the switching mechanism.

## Step 1. Create directories

Create two separate directories for the systems being compared and place the corresponding EM files inside:

```
/relaxed/em_relaxed.xyz
/compressed/em_compressed.xyz
```

## Step 2. Build "EM + Cluster" Systems (L2\_Align)

Run the `L2_Align` module in each directory to generate the full system file.

1.  **For the relaxed state:**

<!-- end list -->

```bash
cd relaxed
L2_Align
cd ..
```

  - At the prompt, enter the EM file name: `em_relaxed.xyz`
  - This will generate the `aligned.xyz` file in the `relaxed` directory.

<!-- end list -->

2.  **For the compressed state:**

<!-- end list -->

```bash
cd compressed
L2_Align
cd ..
```

  - At the prompt, enter the EM file name: `em_compressed.xyz`
  - This will generate the `aligned.xyz` file in the `compressed` directory.

## Step 3. Run Transport Calculations (L2\_Trans)

Run the interactive `L2_Trans` module in each directory to calculate the transmission.

1.  **For the relaxed state:**

<!-- end list -->

```bash
cd relaxed
L2_Trans
```

  - Follow the interactive prompts:
      - `Enter XYZ file name (...)`: `aligned.xyz`
      - `Enter calculation method (...)`: `1` (for GFN1-xTB)
      - `Specify the cluster atom number (25 or 28)`: `25` (for the pyramid template)
      - `Specify the energy range (...)`: `3` (to match the paper's plot range of $E_F \pm 3$ eV)
      - `Specify the energy interval (...)`: `0.01`

<!-- end list -->

2.  **For the compressed state:**

<!-- end list -->

```bash
cd ../compressed
L2_Trans
```

  - Enter the *exact same* parameters as for the `relaxed` calculation to ensure a valid comparison.

## Step 4. Post-processing and Analysis

The workflow will generate `Transmission.txt` and `Transmission.png` in both the `relaxed` and `compressed` directories.

1.  Use a plotting tool to load the data from both `Transmission.txt` files and plot them on a single graph (with the y-axis in log10 scale).
2.  Analyze the transmission values near the Fermi level (E\_F, which is defined as the cluster HOMO energy and printed to the screen).
3.  Verify that the "compressed" (S-Pt) geometry results in a significantly higher transmission near E\_F than the "relaxed" (S-S) geometry, confirming the paper's computational findings (Fig. 4c).