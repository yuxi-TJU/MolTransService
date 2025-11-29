# 0\. Metadata

  - Title:  Enhanced $\pi-\pi$ Stacking between Dipole-Bearing Single Molecules Revealed by Conductance Measurement
  - DOI: (Omit this part)

# 1\. Literature Summary

This is an 'experiment + computation' study. It investigates the influence of intrinsic molecular dipoles on $\pi-\pi$ stacking interactions by comparing polar, azulene-based molecules (AZ1) with their nonpolar, naphthalene-based isomers (NA1) using the STM-BJ technique. The study identifies two conductance states: a high-conductance (HC) state attributed to single-molecule (monomer) junctions and a low-conductance (LC) state attributed to $\pi$-stacked dimer junctions. The primary experimental finding is that the polar AZ1 dimers (LC state) exhibit significantly higher electrical conductance and greater mechanical stability than the nonpolar NA1 dimers. This enhancement is attributed to the favorable electrostatic interaction of the dipoles in an antiparallel stacking configuration. DFT-NEGF calculations support these findings, confirming that the polar AZ1 dimer has a stronger binding energy and a smaller HOMO-LUMO gap, leading to higher charge transport efficiency.

# 2\. Computational Objectives

The primary goal of the paper's theoretical transport calculation is to computationally validate the experimental observation that the $\pi$-stacked dimer of the polar azulene (AZ1) molecule has a higher conductance than the $\pi$-stacked dimer of the nonpolar naphthalene (NA1) molecule. The calculation aims to compute and compare the zero-bias transmission functions for these two dimer systems. The expected result is to show that the transmission spectrum for the AZ1 dimer is significantly higher near the Fermi level than that of the NA1 dimer, thereby explaining the experimentally measured conductance enhancement.

# 3\. Involved Systems

## System 1: AZ1 Dimer ($\pi$-stacked)

  - Core Molecule:  
      - abbreviation: AZ1 Dimer
      - full\_chemical\_name: $\pi$-stacked dimer of 1-([1,1'-biphenyl]-4-yl)-4-(methylthio)azulene
      - core\_smiles: CSc1ccc(-c2ccc3cccc-3cc2)cc1
  - Anchors:  
      - anchor\_groups: ['Methylthio\_SMe']
  - Electrodes:  
      - electrode\_material: Au
      - electrode\_surface: N/A (Calculations use pyramidal clusters)
  - Interface:  
      - interface\_geometry\_text: The sulfur atom of the methylthio (-SMe) group on each monomer binds to the apex Au atom of a pyramidal gold cluster. The two monomers are arranged in an antiparallel, $\pi$-stacked configuration.
  - Variation\_notes: Represents the polar, high-conductance LC state.

## System 2: NA1 Dimer ($\pi$-stacked)

  - Core Molecule:  
      - abbreviation: NA1 Dimer
      - full\_chemical\_name: $\pi$-stacked dimer of 2-([1,1'-biphenyl]-4-yl)-6-(methylthio)naphthalene
      - core\_smiles: CSc1ccc(-c2ccc3ccccc3c2)cc1
  - Variation\_notes: Represents the nonpolar, low-conductance LC reference state. The two monomers are arranged in a $\pi$-stacked configuration.

# 4\. Applicability Assessment

**Applicable.**

The paper's core computational objective is to compare the *relative* zero-bias conductance of two distinct $\pi$-stacked dimer systems (AZ1 vs. NA1) that are coupled to explicit electrode clusters. The paper's own computational model (using "pyramidal Au electrodes" and DFT-NEGF) is conceptually identical to the "Extended Molecule + Electrode Clusters" model of the MST L2 scheme. While MST uses GFN-xTB, it is sufficient to capture the qualitative trend—the difference in transmission magnitude due to the different electronic structures of the polar vs. nonpolar dimers—which is the central theoretical question.

# 5\. Hierarchical Analysis

**Level: L2**

The problem requires comparing the transport properties of two different supramolecular systems (the $\pi$-stacked dimers). The paper's computational method explicitly models the junction using "pyramidal Au electrodes," not a simple constant coupling (L1) or a full periodic slab (L3). This setup perfectly aligns with the "Extended molecule + Electrode clusters" system defined by the QDHC Guide for L2. The core question is how the different electronic structures of the dimers (one polar, one nonpolar) and their coupling to the clusters affect the transmission spectrum. This is a problem governed by the local geometry and electronic coupling at the interface, making L2 the appropriate level.

# 6\. Input Preparation

Based on the L2 workflow, the user must manually prepare "Extended Molecule" (EM) `.xyz` files. The paper explicitly mentions "pyramidal Au electrodes," so the `4au-em.xyz` template (pyramid configuration) from `[MST_root]/share/em/` should be used.

1.  **`em_AZ1_dimer.xyz`**:
      - Create this file by modifying the `4au-em.xyz` template.
      - Replace the placeholder molecule with the $\pi$-stacked AZ1 dimer.
      - The geometry should be set to the optimized antiparallel, fully stacked configuration (as shown in Figure 5b, top).
      - Connect the sulfur atom of the -SMe group from each monomer to the apex Au atom of one of the pyramid templates.
2.  **`em_NA1_dimer.xyz`**:
      - Create this file using the *same* `4au-em.xyz` template.
      - Replace the placeholder molecule with the $\pi$-stacked NA1 dimer.
      - Set the geometry to the optimized stacked configuration (as shown in Figure 5b, bottom).
      - Connect the sulfur atom of the -SMe group from each monomer to the apex Au atom of one of the pyramid templates.
3.  **Constraint**: For both files, the Au atoms of the pyramid template must remain a rigid block, and their original atom order from the template file must be strictly maintained.

# 7\. Computational Workflow

## Goal:

Compute and compare the zero-bias T(E) spectra for the "AZ1 Dimer" (polar) and "NA1 Dimer" (nonpolar) junction geometries to validate the experimentally observed conductance enhancement.

## Step 1. Create directories

Create two separate directories matching the em systems and place the corresponding xyz files:

```
/AZ1_dimer/em_AZ1_dimer.xyz
/NA1_dimer/em_NA1_dimer.xyz
```

## Step 2. Build "EM + Cluster" Systems (L2\_Align)

Run the `L2_Align` module in each directory to generate the full system file.

1.  **For the AZ1 Dimer state:**

<!-- end list -->

```bash
cd AZ1_dimer
L2_Align
cd ..
```

  - At the prompt, enter the EM file name: `em_AZ1_dimer.xyz`
  - This will generate the `aligned.xyz` file in the `AZ1_dimer` directory.

<!-- end list -->

2.  **For the NA1 Dimer state:**

<!-- end list -->

```bash
cd NA1_dimer
L2_Align
cd ..
```

  - At the prompt, enter the EM file name: `em_NA1_dimer.xyz`
  - This will generate the `aligned.xyz` file in the `NA1_dimer` directory.

## Step 3. Run Transport Calculations (L2\_Trans)

Run the interactive `L2_Trans` module in each directory to calculate the transmission.

1.  **For the AZ1 Dimer state:**

<!-- end list -->

```bash
cd AZ1_dimer
L2_Trans
```

  - Follow the interactive prompts:
      - `Enter XYZ file name (...)`: `aligned.xyz`
      - `Enter calculation method (...)`: `1` (for GFN1-xTB)
      - `Specify the cluster atom number (25 or 28)`: `25` (for the pyramid template)
      - `Specify the energy range (...)`: `2` (to match the paper's plot range of $E_F \pm 2$ eV)
      - `Specify the energy interval (...)`: `0.01`

<!-- end list -->

2.  **For the NA1 Dimer state:**

<!-- end list -->

```bash
cd ../NA1_dimer
L2_Trans
```

  - Enter the *exact same* parameters as for the `AZ1_dimer` calculation to ensure a valid comparison.

## Step 4. Post-processing and Analysis

The workflow will generate `Transmission.txt` and `Transmission.png` in both the `AZ1_dimer` and `NA1_dimer` directories.

1.  Compare the `Transmission.png` plots from both directories.
2.  Use a plotting tool (e.g., Python/Matplotlib) to load the data from both `Transmission.txt` files and plot them on the same graph for comparison, with the y-axis in log10 scale.
3.  Analyze the transmission values near the Fermi level (E\_F, which is defined as the cluster HOMO energy and printed to the screen).
4.  Verify that the "AZ1 Dimer" geometry results in a significantly higher transmission near E\_F than the "NA1 Dimer" geometry, confirming the paper's findings (Figure 5d).