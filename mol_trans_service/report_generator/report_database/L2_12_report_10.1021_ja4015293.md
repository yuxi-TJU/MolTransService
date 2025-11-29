# 0\. Metadata

 - Title:  Single-Molecule Conductance of Functionalized Oligoynes: Length Dependence and Junction Evolution
 - DOI: (Omit this part)  

# 1\. Literature Summary

This is an 'experiment + computation' study. It presents a comprehensive investigation into the length dependence ($n=1, 2, 4$ triple bonds) and anchor group dependence (PY, $NH_2$, CN, SH, and BT) of oligoyne molecular wires. Using STM-BJ and MCBJ techniques, the authors find that the dihydrobenzo[b]thiophene (BT) anchor group is superior, providing both 100% junction formation probability and the highest conductance values. The DFT-based transport calculations explore the junction evolution during stretching, showing that the "sliding" of anchor groups across the electrode surfaces leads to oscillations in conductance. The calculations also identify the dominant transport channels (HOMO or LUMO) for each anchor group by empirically correcting the alignment of the Fermi level.

# 2\. Computational Objectives

The paper's theoretical calculations have two main goals. The first is to quantitatively reproduce the experimental conductance-versus-length trends for all five anchor groups, which requires a complex (and out-of-scope) correction of the electrode Fermi level.

The second, more fundamental goal is to computationally validate the "junction evolution" hypothesis: that the observed conductance features (e.g., high-G and low-G states) and conductance oscillations are caused by changes in the local contact geometry as the junction is stretched. The calculation aims to specifically compute the transmission for different pulling geometries, such as a compressed "SIDE" configuration and a stretched "atop" configuration. The expected result is to show that conductance varies significantly with these changes in binding geometry, explaining the features observed in the experimental conductance traces.

# 3\. Involved Systems

(The computational analysis explores the stretching of all five molecular families. We select the BT4 molecule as a representative case, as it is explicitly shown in Figures 7, 8, and 9.)

## System 1: BT4 (Compressed / SIDE-binding)

 - Core Molecule:  
      - abbreviation: BT4
      - full\_chemical\_name: Dihydrobenzo[b]thiophene-terminated tetrayne
      - core\_smiles: C(C#CC#Cc1ccc2c(c1)CCS2)#CC#Cc1ccc2c(c1)CSC2
 - Anchors:  
      - anchor\_groups: ['Dihydrobenzothiophene_S']
 - Electrodes:  
      - electrode\_material: Au
      - electrode\_surface: 111 (modeled as pyramids)
 - Interface:  
      - interface\_geometry\_text: BT anchor binds to the Au pyramid surface in a "SIDE" configuration (aromatic ring facing the pyramid). This corresponds to a compressed, high-conductance junction geometry (e.g., BT-II or BT-III in Figure 7).
 - Variation\_notes: Represents a high-conductance geometry found during the "sliding" and stretching process.

## System 2: BT4 (Stretched / Atop-binding)

 - Core Molecule:  
      - abbreviation: BT4
      - full\_chemical\_name: Dihydrobenzo[b]thiophene-terminated tetrayne
      - core\_smiles: C(C#CC#Cc1ccc2c(c1)CCS2)#CC#Cc1ccc2c(c1)CSC2
 - Anchors:  
      - anchor\_groups: ['Dihydrobenzothiophene_S']
 - Electrodes:  
      - electrode\_material: Au
      - electrode\_surface: 111 (modeled as pyramids)
 - Interface:  
      - interface\_geometry\_text: BT anchor binds directly to the apex Au atom of the pyramid in an "atop" configuration. This corresponds to a fully extended, lower-conductance junction geometry (e.g., BT-V in Figure 7).
 - Variation\_notes: Represents a lower-conductance geometry found just before junction rupture.

# 4\. Applicability Assessment

**Applicable.**

The paper's full computational goal—quantitatively comparing the conductance of five different anchor groups—relies on precise energy level alignment, which the paper achieves via an empirical $E_F$ correction (analogous to DFT+$\Sigma$). This quantitative alignment task is listed as "Out-of-Scope" in the QDHC guide.

However, a central *component* of the paper's computational findings is the "junction evolution," i.e., how conductance oscillates as the anchor groups "slide" across the electrode pyramids (e.g., Figure 9B). This problem, which relates conductance to *interface geometry*, is a classic L2 problem. MST's L2 scheme is sufficient to reproduce the essential physical trend: the variation in transmission as the junction is stretched and the binding motif changes from "SIDE" to "atop".

# 5\. Hierarchical Analysis

**Level: L2**

The problem of junction evolution is explicitly governed by the "local geometry and electronic coupling at the molecule-electrode interface." The paper's core computational analysis (Figures 7 and 9B) links changes in conductance directly to the "sliding" of the anchor group and the resulting binding configuration (e.g., SIDE-binding vs. atop-binding). The paper's own DFT setup for this analysis, which uses a molecule attached to "two (111) directed pyramids of 35 gold atoms," is conceptually identical to the "Extended Molecule + Electrode Clusters" model of the QDHC L2 scheme. This problem does not depend on the molecule's intrinsic properties alone (L1) and can be qualitatively understood without the full, corrected level alignment of L3.

# 6\. Input Preparation

Based on the L2 workflow, the user must manually prepare "Extended Molecule" (EM) `.xyz` files. The paper explicitly mentions "pyramids" modeling the tip and electrode, so the `4au-em.xyz` template (pyramid configuration) from `[MST_root]/share/em/` must be used.

1.  **`em_side.xyz`**:
      - Create this file by modifying the `4au-em.xyz` template.
      - Replace the placeholder molecule with the BT4 molecule.
      - Adjust the geometry to represent the compressed "SIDE" configuration (similar to BT-II or BT-III in Figure 7), where the BT anchor ring is parallel to the pyramid face.
2.  **`em_atop.xyz`**:
      - Create this file using the *same* `4au-em.xyz` template.
      - Replace the placeholder molecule with the BT4 molecule.
      - Adjust the geometry to represent the stretched "atop" configuration (similar to BT-V in Figure 7), where the anchor binds to the single apex Au atom.
3.  **Constraint**: For both files, the Au atoms of the pyramid template must remain a rigid, unified block, and their original atom order from the template file must be strictly maintained.

# 7\. Computational Workflow

## Goal:

Compute and compare the zero-bias T(E) spectra for the "SIDE" (compressed) and "atop" (stretched) BT4 geometries to validate that conductance changes significantly with the binding configuration.

## Step 1. Create directories

Create two separate directories for the systems being compared and place the corresponding EM files inside:

```
/side_geom/em_side.xyz
/atop_geom/em_atop.xyz
```

## Step 2. Build "EM + Cluster" Systems (L2\_Align)

Run the `L2_Align` module in each directory to combine the EM file with the supplied cluster template.

1.  **For the "SIDE" state:**

    ```bash
    cd side_geom
    L2_Align
    cd ..
    ```

      - At the prompt, enter the EM file name: `em_side.xyz`
      - This generates the `aligned.xyz` file in the `side_geom` directory.

2.  **For the "atop" state:**

    ```bash
    cd atop_geom
    L2_Align
    cd ..
    ```

      - At the prompt, enter the EM file name: `em_atop.xyz`
      - This generates the `aligned.xyz` file in the `atop_geom` directory.

## Step 3. Run Transport Calculations (L2\_Trans)

Run the interactive `L2_Trans` module in each directory to calculate the transmission.

1.  **For the "SIDE" state:**

    ```bash
    cd side_geom
    L2_Trans
    ```

      - Follow the interactive prompts:
          - `Enter XYZ file name (...)`: `aligned.xyz`
          - `Enter calculation method (...)`: `1` (for GFN1-xTB)
          - `Specify the cluster atom number (25 or 28)`: `25` (for the pyramid template)
          - `Specify the energy range (...)`: `2` (to scan $E_F \pm 2$ eV)
          - `Specify the energy interval (...)`: `0.01`

2.  **For the "atop" state:**

    ```bash
    cd ../atop_geom
    L2_Trans
    ```

      - Enter the *exact same* parameters as for the `side_geom` calculation to ensure a valid comparison.

## Step 4. Post-processing and Analysis

The workflow will generate `Transmission.txt` and `Transmission.png` in both the `side_geom` and `atop_geom` directories.

1.  Compare the `Transmission.png` plots from both directories.
2.  Use a plotting tool (e.g., Python/Matplotlib) to load the data from both `Transmission.txt` files and plot them on the same graph for comparison (y-axis in log10 scale).
3.  Analyze the transmission values near the Fermi level (E\_F, which is defined as the cluster HOMO energy and printed to the screen).
4.  Verify that the "SIDE" geometry results in a different (likely higher) transmission near E\_F than the "atop" geometry, confirming the paper's finding that conductance oscillates with binding configuration.