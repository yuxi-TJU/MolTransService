# 0\. Metadata

  - Title:  Non-chemisorbed gold-sulfur binding prevails in self-assembled monolayers
  - DOI: (Omit this part)  

# 1\. Literature Summary

This is an 'experiment + computation' study. It investigates the fundamental nature of the gold-sulfur bond in self-assembled monolayers (SAMs) formed from dithiol precursors. Using STM-BJ measurements, the paper finds that junctions measured in a SAM environment exhibit a significantly lower conductance than junctions of the same molecule measured in a solution environment. This primary finding, supported by DFT-NEGF transport calculations, leads to the conclusion that the "SAM" state corresponds to a physisorbed (Au-S(H)R) contact where the thiol hydrogen is retained, resulting in weak coupling. In contrast, the "solution" state corresponds to a chemisorbed (Au-SR) contact where the hydrogen is lost, forming a strong covalent bond and leading to higher conductance.

# 2\. Computational Objectives

The primary goal of the paper's theoretical transport calculation is to computationally validate the hypothesis that the observed conductance difference between "SAM" and "solution" measurements is due to a change in bonding from physisorbed (H-retained) to chemisorbed (H-lost). The calculation aims to compare the transmission functions of three systems: 1) a chemisorbed Au-SR junction, 2) a physisorbed Au-S(H)R junction, and 3) a physisorbed Au-S(Me)R (thioether) junction. The expected result is to show that the chemisorbed system has a much higher transmission near the Fermi level than the two physisorbed systems, and that the two physisorbed systems have very similar transmission spectra.

# 3\. Involved Systems

## System 1: C12 Alkane (Chemisorbed)

  - Core Molecule:  
      - abbreviation: Au-SR
      - full\_chemical\_name: Dodecane (bound as thiolate)
      - core\_smiles: [S]CCCCCCCCCCCC[S]
  - Anchors:  
      - anchor\_groups: ['Thiolate\_S-']
  - Electrodes:  
      - electrode\_material: Au
      - electrode\_surface: N/A (Calculations use "gold triad" clusters)
  - Interface:  
      - interface\_geometry\_text: Thiolate (S) forms a direct covalent bond with the apex Au atom of a "gold triad" (trimer) cluster.
  - Variation\_notes: Represents the high-conductance "solution" measurement state (H-lost).

## System 2: C12 Alkane (Physisorbed, SH)

  - Core Molecule:  
      - abbreviation: Au-S(H)R
      - full\_chemical\_name: 1,12-dodecanedithiol
      - core\_smiles: SCCCCCCCCCCCCS
  - Anchors:  
      - anchor\_groups: ['Thiol\_SH']
  - Electrodes:  
      - electrode\_material: Au
      - electrode\_surface: N/A (Calculations use "gold triad" clusters)
  - Interface:  
      - interface\_geometry\_text: Intact thiol group (SH) is physisorbed (weakly coupled) to the apex Au atom of a "gold triad" (trimer) cluster.
  - Variation\_notes: Represents the low-conductance "SAM" measurement state (H-retained).

## System 3: C12 Alkane (Physisorbed, SMe)

  - Core Molecule:  
      - abbreviation: Au-S(Me)R
      - full\_chemical\_name: 1,12-bis(methylthio)dodecane
      - core\_smiles: CSCCCCCCCCCCCCSC
  - Anchors:  
      - anchor\_groups: ['Thioether\_SMe']
  - Electrodes:  
      - electrode\_material: Au
      - electrode\_surface: N/A (Calculations use "gold triad" clusters)
  - Interface:  
      - interface\_geometry\_text: Intact thioether group (SMe) is physisorbed (weakly coupled) to the apex Au atom of a "gold triad" (trimer) cluster.
  - Variation\_notes: Represents the low-conductance control system.

# 4\. Applicability Assessment

**Applicable.**

The paper's core computational objective is to compare the *relative transmission magnitude* resulting from three different "anchoring chemistries" (Au-SR vs. Au-S(H)R vs. Au-S(Me)R). This is a question of interface-dominated transport. The problem is explicitly about the difference in coupling strength originating from the local bonding motif. This fundamental physical trend can be qualitatively captured by the QDHC L2 scheme, even though the original paper used a DFT-based method (TranSIESTA).

# 5\. Hierarchical Analysis

**Level: L2**

The paper's central computational question is why conductance changes based on the bonding at the Au-S interface. The molecule's intrinsic structure (the C12 backbone) is identical in all cases (ruling out L1). The problem is not about absolute level alignment or finite-bias effects (ruling out L3). Instead, the problem is explicitly governed by the "local geometry and electronic coupling at the molecule-electrode interface." The key analytical evidence sought is the change in the T(E) spectrum as a direct result of "anchoring chemistry" (chemisorbed vs. physisorbed). This perfectly aligns with the QDHC Guide's criteria for L2. The paper's computational model, which uses a "gold triad junction structure," is conceptually identical to the "Extended molecule + electrode clusters" model (specifically, the trimer template) of the MST L2 scheme.

# 6\. Input Preparation

Based on the L2 workflow, the user must manually prepare three "Extended Molecule" (EM) `.xyz` files. The paper explicitly mentions a "gold triad," so the `3au-em.xyz` template (trimer configuration) from `[MST_root]/share/em/` should be used.

1.  **`em_chemisorbed.xyz`**:
      - Create this file by modifying the `3au-em.xyz` template.
      - Replace the placeholder molecule with the C12 backbone.
      - Connect the backbone to the apex Au atoms on each side via a sulfur atom (thiolate, H removed), forming a covalent Au-S bond.
2.  **`em_physis_SH.xyz`**:
      - Create this file using the *same* `3au-em.xyz` template.
      - Replace the placeholder molecule with the C12 backbone, *including* the full -SH groups.
      - Position the intact -SH groups near the apex Au atoms to represent a weak, physisorbed interaction.
3.  **`em_physis_SMe.xyz`**:
      - Create this file using the *same* `3au-em.xyz` template.
      - Replace the placeholder molecule with the C12 backbone, *including* the full -SMe groups.
      - Position the intact -SMe groups near the apex Au atoms to represent a weak, physisorbed interaction.
4.  **Constraint**: For all three files, the Au atoms of the trimer template must remain a rigid block, and their original atom order from the template file must be strictly maintained.

# 7\. Computational Workflow

## Goal:

Compute and compare the zero-bias T(E) spectra for the chemisorbed (Au-SR), physisorbed (Au-S(H)R), and physisorbed (Au-S(Me)R) anchoring geometries.

## Step 1. Create directories

Create three separate directories for the systems being compared and place the corresponding EM files inside:

```
/chemisorbed/em_chemisorbed.xyz
/physis_SH/em_physis_SH.xyz
/physis_SMe/em_physis_SMe.xyz
```

## Step 2. Build "EM + Cluster" Systems (L2\_Align)

Run the `L2_Align` module in each directory to combine the EM file with the supplied cluster template.

1.  **For the `chemisorbed` system:**

    ```bash
    cd chemisorbed
    L2_Align
    cd ..
    ```

      - At the prompt, enter the EM file name: `em_chemisorbed.xyz`
      - This generates `aligned.xyz` in the `chemisorbed` directory.

2.  **For the `physis_SH` system:**

    ```bash
    cd physis_SH
    L2_Align
    cd ..
    ```

      - At the prompt, enter the EM file name: `em_physis_SH.xyz`
      - This generates `aligned.xyz` in the `physis_SH` directory.

3.  **For the `physis_SMe` system:**

    ```bash
    cd physis_SMe
    L2_Align
    cd ..
    ```

      - At the prompt, enter the EM file name: `em_physis_SMe.xyz`
      - This generates `aligned.xyz` in the `physis_SMe` directory.

## Step 3. Run Transport Calculations (L2\_Trans)

Run the interactive `L2_Trans` module in each directory to calculate the transmission.

1.  **For the `chemisorbed` system:**

    ```bash
    cd chemisorbed
    L2_Trans
    ```

      - Follow the interactive prompts:
          - `Enter XYZ file name (...)`: `aligned.xyz`
          - `Enter calculation method (...)`: `1` (for GFN1-xTB)
          - `Specify the cluster atom number (25 or 28)`: `25` (for the trimer template)
          - `Specify the energy range (...)`: `4` (to match the paper's plot range of $E_F \pm 4$ eV)
          - `Specify the energy interval (...)`: `0.01`

2.  **For the `physis_SH` and `physis_SMe` systems:**

    ```bash
    cd ../physis_SH
    L2_Trans
    # ...
    cd ../physis_SMe
    L2_Trans
    ```

      - Repeat the process in the other two directories, entering the *exact same* computational parameters to ensure a valid comparison.

## Step 4. Post-processing and Analysis

1.  The workflow will generate `Transmission.txt` and `Transmission.png` in all three directories.
2.  Use a plotting tool (e.g., Python/Matplotlib) to load the data from all three `Transmission.txt` files and plot them on the same graph with the y-axis in log10 scale.
3.  Analyze the transmission spectra near the Fermi level (E\_F, which is defined as the cluster HOMO energy and printed to the screen).
4.  Verify that:
      - The transmission for the `chemisorbed` system is significantly *higher* than for the two physisorbed systems.
      - The transmission spectra for `physis_SH` and `physis_SMe` are very similar to each other.