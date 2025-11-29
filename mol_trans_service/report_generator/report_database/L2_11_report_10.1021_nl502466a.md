# 0\. Metadata

 - Title:  Hapticity-Dependent Charge Transport through Carbodithioate-Terminated [5,15-Bis(phenylethynyl)porphinato]zinc(II) Complexes in Metal-Molecule-Metal Junctions
 - DOI: (Omit this part)  

# 1\. Literature Summary

This is an 'experiment + computation' study. It investigates the charge transport properties of a porphyrin-based molecule anchored to gold electrodes via carbodithioate (`-CS2-`) linkers, comparing it to a thiolate (`-S-`) anchored analogue. Using the STM break junction method, the paper finds that the carbodithioate-anchored junction has a conductance an order of magnitude higher than the thiolate one. More importantly, it reveals three distinct conductance states (N, M, S) for the carbodithioate junction. The primary finding, supported by NEGF-DFT calculations, is that these three states are not due to different molecules but rather to different "hapticities" (bonding configurations) of the *same* linker: bidentate/bidentate (N, high-G), bidentate/monodentate (M, mid-G), and monodentate/monodentate (S, low-G).

# 2\. Computational Objectives

The primary goal of the paper's theoretical transport calculation is to computationally validate the hypothesis that the three observed conductance states (N, M, and S) are caused by different hapticities of the carbodithioate linker. The calculation aims to compute and compare the transmission functions for the bidentate/bidentate, bidentate/monodentate, and monodentate/monodentate binding geometries. The expected result is to show that the transmission at the Fermi level ($T(E_F)$) and the broadening of the transmission resonances both increase with the number of S-Au bonds, following the trend N \> M \> S, thereby explaining the experimentally observed conductance steps.

# 3\. Involved Systems

## System 1: `S2C-PZn-CS2` (N State)

 - Core Molecule:  
      - abbreviation: `S2C-PZn-CS2` (N)
      - full\_chemical\_name: [5,15-bis(4'-(dithiocarboxylate)phenylethynyl)-10,20-diarylporphinato]zinc(II)
      - core\_smiles: N/A
 - Anchors:  
      - anchor\_groups: ['Carbodithioate\_CS2']
 - Electrodes:  
      - electrode\_material: Au
      - electrode\_surface: N/A (Calculations use pyramidal clusters)
 - Interface:  
      - interface\_geometry\_text: Carbodithioate (`-CS2-`) forms a **bidentate** bond with the apex atoms of a pyramidal gold cluster on both sides of the junction.
 - Variation\_notes: Represents the "Normal" (N) high-conductance state (bidentate/bidentate).

## System 2: `S2C-PZn-CS2` (M State)

 - Core Molecule:  
      - abbreviation: `S2C-PZn-CS2` (M)
      - full\_chemical\_name: [5,15-bis(4'-(dithiocarboxylate)phenylethynyl)-10,20-diarylporphinato]zinc(II)
      - core\_smiles: N/A
 - Anchors:  
      - anchor\_groups: ['Carbodithioate\_CS2']
 - Electrodes:  
      - electrode\_material: Au
      - electrode\_surface: N/A (Calculations use pyramidal clusters)
 - Interface:  
      - interface\_geometry\_text: Carbodithioate (`-CS2-`) forms a **bidentate** bond on one side and a **monodentate** bond on the other side with the pyramidal gold clusters.
 - Variation\_notes: Represents the "Medium" (M) intermediate-conductance state (bidentate/monodentate).

## System 3: `S2C-PZn-CS2` (S State)

 - Core Molecule:  
      - abbreviation: `S2C-PZn-CS2` (S)
      - full\_chemical\_name: [5,15-bis(4'-(dithiocarboxylate)phenylethynyl)-10,20-diarylporphinato]zinc(II)
      - core\_smiles: N/A
 - Anchors:  
      - anchor\_groups: ['Carbodithioate\_CS2']
 - Electrodes:  
      - electrode\_material: Au
      - electrode\_surface: N/A (Calculations use pyramidal clusters)
 - Interface:  
      - interface\_geometry\_text: Carbodithioate (`-CS2-`) forms a **monodentate** bond with the apex Au atom of a pyramidal gold cluster on both sides.
 - Variation\_notes: Represents the "Small" (S) low-conductance state (monodentate/monodentate). This geometry is analogous to the thiolate-anchored system.

# 4\. Applicability Assessment

**Applicable.**

The paper's core computational objective is to demonstrate that conductance is modulated by the "hapticity" (i.e., monodentate vs. bidentate binding) of the anchoring group. This is a question of how interface-dominated coupling strength changes with local bonding geometry. The paper's own analysis confirms this by linking higher conductance to broader transmission peaks. While the original paper used a full-slab NEGF-DFT model (an L3-like setup), the essential physical trend—the difference in coupling strength originating from local bonding motifs—can be qualitatively captured by the QDHC L2 scheme.

# 5\. Hierarchical Analysis

**Level: L2**

The paper's central computational task is to explain why conductance changes based on the anchoring group's bonding configuration (hapticity). This is not a problem of the molecule's intrinsic structure (L1) or of finite-bias/level alignment (L3). Instead, the problem is explicitly governed by the "local geometry and electronic coupling at the molecule-electrode interface." The key analytical evidence sought is the change in the T(E) spectrum (specifically, resonance broadening and $T(E_F)$) as a direct result of "anchoring chemistry" (monodentate vs. bidentate). This perfectly aligns with the QDHC Guide's criteria for L2. The conceptual model (Fig. 3) uses a pyramid-like tip, which is conceptually identical to the "Extended molecule + electrode clusters" model of the MST L2 scheme.

# 6\. Input Preparation

Based on the L2 workflow, the user must manually prepare "Extended Molecule" (EM) `.xyz` files. The paper's conceptual model (Fig. 3) involves an undercoordinated tip atom, so the `4au-em.xyz` (pyramid) template from `[MST_root]/share/em/` is appropriate.

1.  **`em_N_state.xyz`**:
      - Create this file by modifying the `4au-em.xyz` template.
      - Replace the placeholder molecule with the `S2C-PZn-CS2` core.
      - Connect the molecule to the Au pyramids via **bidentate** bonds on *both* sides (e.g., both S atoms of the `-CS2-` group bind to Au atoms in the pyramid).
2.  **`em_M_state.xyz`**:
      - Create this file using the *same* `4au-em.xyz` template.
      - Connect the molecule with a **bidentate** bond on one side and a **monodentate** bond on the other (e.g., only one S atom of the `-CS2-` group binds to the apex Au).
3.  **`em_S_state.xyz`**:
      - Create this file using the *same* `4au-em.xyz` template.
      - Connect the molecule to the apex Au atoms via **monodentate** bonds on *both* sides.
4.  **Constraint**: For all three files, the Au atoms of the pyramid template must remain a rigid block, and their original atom order from the template file must be strictly maintained.

# 7\. Computational Workflow

## Goal:

Compute and compare the zero-bias T(E) spectra for the N (bidentate/bidentate), M (bidentate/monodentate), and S (monodentate/monodentate) anchoring geometries.

## Step 1. Create directories

Create three separate directories for the systems being compared and place the corresponding EM files inside:

```
/N_state/em_N_state.xyz
/M_state/em_M_state.xyz
/S_state/em_S_state.xyz
```

## Step 2. Build "EM + Cluster" Systems (L2\_Align)

Run the `L2_Align` module in each directory to combine the EM file with the supplied cluster template.

1.  **For the N system:**

    ```bash
    cd N_state
    L2_Align
    cd ..
    ```

      - At the prompt, enter the EM file name: `em_N_state.xyz`
      - This generates `aligned.xyz` in the `N_state` directory.

2.  **For the M system:**

    ```bash
    cd M_state
    L2_Align
    cd ..
    ```

      - At the prompt, enter the EM file name: `em_M_state.xyz`
      - This generates `aligned.xyz` in the `M_state` directory.

3.  **For the S system:**

    ```bash
    cd S_state
    L2_Align
    cd ..
    ```

      - At the prompt, enter the EM file name: `em_S_state.xyz`
      - This generates `aligned.xyz` in the `S_state` directory.

## Step 3. Run Transport Calculations (L2\_Trans)

Run the interactive `L2_Trans` module in each directory to calculate the transmission.

1.  **For the N system:**

    ```bash
    cd N_state
    L2_Trans
    ```

      - Follow the interactive prompts:
          - `Enter XYZ file name (...)`: `aligned.xyz`
          - `Enter calculation method (...)`: `1` (for GFN1-xTB)
          - `Specify the cluster atom number (25 or 28)`: `25` (for the pyramid template)
          - `Specify the energy range (...)`: `3` (to scan $E_F \pm 3$ eV)
          - `Specify the energy interval (...)`: `0.01`

2.  **For the M and S systems:**

      - Repeat the process in the `M_state` and `S_state` directories:

    <!-- end list -->

    ```bash
    cd ../M_state
    L2_Trans
    cd ../S_state
    L2_Trans
    ```

      - Enter the *exact same* parameters for all three calculations to ensure a valid comparison.

## Step 4. Post-processing and Analysis

The workflow will generate `Transmission.txt` and `Transmission.png` in all three directories (`/N_state`, `/M_state`, `/S_state`).

1.  Use a plotting tool (e.g., Python/Matplotlib) to load the data from all three `Transmission.txt` files and plot them on the same graph, with the y-axis in log10 scale.
2.  Analyze the transmission values near the Fermi level (E\_F, which is defined as the cluster HOMO energy and printed to the screen).
3.  Verify that the transmission at $E_F$ follows the trend: `N_state` \> `M_state` \> `S_state`.
4.  Visually inspect the plots to confirm that the transmission resonances near $E_F$ are broadest for the `N_state` (strongest coupling) and narrowest for the `S_state` (weakest coupling), confirming the paper's computational findings.