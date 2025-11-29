# 0\. Metadata

 - Title:  Not So Innocent After All: Interfacial Chemistry Determines Charge-Transport Efficiency in Single-Molecule Junctions
 - DOI: (Omit this part)

# 1\. Literature Summary

This is an 'experiment + computation' study. It investigates the charge transport properties of two pairs of molecules: dithienophosphole oxides (1T, 1P) and their bithiophene counterparts (2T, 2P), using two different anchor groups: electron-rich 4-thioanisole (T-series) and electron-deficient 4-pyridyl (P-series). Using the STMBJ technique, the authors find a surprising *inversion* of the conductance trend based on the anchor. For the thioanisole anchors, the phosphole (1T) is *more* conductive than the bithiophene (2T). For the pyridyl anchors, the trend reverses, and the phosphole (1P) is *less* conductive than the bithiophene (2P). DFT-NEGF calculations confirm this trend, attributing the behavior to the interplay between the backbone's electron-accepting nature and the anchor's charge-buffering capacity, which directly modulates the molecule-electrode interface coupling.

# 2\. Computational Objectives

The primary goal of the paper's theoretical transport calculation is to computationally validate the experimentally observed *inversion* of the conductance trend. The calculation aims to compare the transmission functions and conductance histograms for all four molecules (1T, 2T, 1P, 2P). The expected result is to computationally reproduce the experimental finding: $G_{1T} > G_{2T}$ and $G_{1P} < G_{2P}$. This is intended to demonstrate that the conductance is not governed by the molecular backbone alone, but by the anchor group's chemical nature, which alters the electronic transparency of the molecule-electrode interface.

# 3\. Involved Systems

## System 1: 1T

 - Core Molecule:  
      - abbreviation: 1T
      - full\_chemical\_name: 2,6-bis(4-(methylthio)phenyl)dithieno[3,2-b:2',3'-d]phosphole oxide
      - core\_smiles: CSc1ccc(-c2cc3c(s2)-c2sc(-c4ccc(SC)cc4)cc2P3(=O)c2ccccc2)cc1
 - Anchors:  
      - anchor\_groups: ['Thioanisole\_SMe']
 - Electrodes:  
      - electrode\_material: Au
      - electrode\_surface: N/A (STMBJ nanogap)
 - Interface:  
      - interface\_geometry\_text: Thioanisole-S atom couples to an undercoordinated Au atom (e.g., adatom, trimer, or pyramid motif) on the Au surface.
 - Variation\_notes: Phosphole core with electron-rich thioanisole anchors.

## System 2: 2T

 - Core Molecule:  
      - abbreviation: 2T
      - full\_chemical\_name: 5,5'-bis(4-(methylthio)phenyl)-2,2'-bithiophene
      - core\_smiles: CSc1ccc(-c2ccc(-c3ccc(-c4ccc(SC)cc4)s3)s2)cc1
 - Variation\_notes: Bithiophene core with electron-rich thioanisole anchors.

## System 3: 1P

 - Core Molecule:  
      - abbreviation: 1P
      - full\_chemical\_name: 2,6-bis(pyridin-4-yl)dithieno[3,2-b:2',3'-d]phosphole oxide
      - core\_smiles: O=P1(c2ccccc2)c2cc(-c3ccncc3)sc2-c2sc(-c3ccncc3)cc21
 - Anchors:  
      - anchor\_groups: ['Pyridine\_N']
 - Electrodes:  
      - electrode\_material: Au
      - electrode\_surface: N/A (STMBJ nanogap)
 - Interface:  
      - interface\_geometry\_text: Pyridine-N atom couples to an undercoordinated Au atom (e.g., adatom, trimer, or pyramid motif) on the Au surface.
 - Variation\_notes: Phosphole core with electron-deficient pyridyl anchors.

## System 4: 2P

 - Core Molecule:  
      - abbreviation: 2P
      - full\_chemical\_name: 5,5'-bis(pyridin-4-yl)-2,2'-bithiophene
      - core\_smiles:c1cc(-c2ccc(-c3ccc(-c4ccncc4)s3)s2)ccn1
 - Variation\_notes: Bithiophene core with electron-deficient pyridyl anchors.

# 4\. Applicability Assessment

**Applicable.**

The paper's core computational objective is to explain a change in *relative* conductance trends ($G_{1T} > G_{2T}$ vs. $G_{1P} < G_{2P}$) by analyzing how different anchor groups ("anchoring chemistry") interact with different molecular backbones to modulate the "molecule-electrode interface" transparency and coupling. This is a problem of interface-dominated transport. While the original paper used DFT (SIESTA) and scanned multiple contact geometries, the fundamental physical trend—the difference in coupling strength originating from the combined backbone-anchor motif—can be qualitatively captured by the QDHC L2 scheme using GFN-xTB.

# 5\. Hierarchical Analysis

**Level: L2**

The paper explicitly argues that a simple L1 model (segmenting the molecule) is insufficient, as the intrinsic electronic structure of the isolated molecules (Fig 2e) cannot explain the observed trend inversion. The problem is also not a pure L3-level alignment issue, as the paper's conclusion rests on changes in "Au-N coordination" and interface transparency, not on the absolute alignment of orbitals with $E_F$.

The problem is fundamentally governed by the "local geometry and electronic coupling at the molecule-electrode interface," where the "anchoring chemistry" (Thioanisole vs. Pyridyl) interacts with the backbone electronics to alter the coupling strength. This perfectly aligns with the QDHC Guide's criteria for L2. The MST L2 scheme, using "Extended Molecule + Electrode Clusters" (e.g., pyramid templates), is designed to model exactly these interface-dependent coupling effects.

# 6\. Input Preparation

Based on the L2 workflow, the user must manually prepare a *series* of "Extended Molecule" (EM) `.xyz` files using a template from `[MST_root]/share/em/`. The `4au-em.xyz` (pyramid) template is a suitable choice for modeling the STMBJ tip.

1.  **`em_1T.xyz`**: Modify the `4au-em.xyz` template. Replace the placeholder with the 1T molecule, binding the apex Au atoms to the S atoms of the thioanisole groups.
2.  **`em_2T.xyz`**: Modify the `4au-em.xyz` template. Replace the placeholder with the 2T molecule, binding the apex Au atoms to the S atoms of the thioanisole groups.
3.  **`em_1P.xyz`**: Modify the `4au-em.xyz` template. Replace the placeholder with the 1P molecule, binding the apex Au atoms to the N atoms of the pyridyl groups.
4.  **`em_2P.xyz`**: Modify the `4au-em.xyz` template. Replace the placeholder with the 2P molecule, binding the apex Au atoms to the N atoms of the pyridyl groups.
5.  **Constraint**: For all files, the Au atoms of the pyramid template must remain a rigid, unified block, and their original atom order from the template file must be strictly maintained.

# 7\. Computational Workflow

## Goal:

Compute and compare the zero-bias T(E) spectra for the 1T, 2T, 1P, and 2P systems to validate the conductance trend inversion.

## Step 1. Create directories

Create four separate directories for the systems being compared and place the corresponding EM files inside:

```
/1T/em_1T.xyz
/2T/em_2T.xyz
/1P/em_1P.xyz
/2P/em_2P.xyz
```

## Step 2. Build "EM + Cluster" Systems (L2\_Align)

Run the `L2_Align` module in *each* of the four directories to combine the EM file with the supplied cluster template.

1.  **For the 1T system:**

    ```bash
    cd 1T
    L2_Align
    cd ..
    ```

      - At the prompt, enter the EM file name: `em_1T.xyz`
      - This generates the `aligned.xyz` file in the `1T` directory.

2.  **Repeat this process** for the `2T`, `1P`, and `2P` directories.

## Step 3. Run Transport Calculations (L2\_Trans)

Run the interactive `L2_Trans` module in *each* directory to calculate the transmission.

1.  **For the 1T system:**

    ```bash
    cd 1T
    L2_Trans
    ```

      - Follow the interactive prompts:
          - `Enter XYZ file name (...)`: `aligned.xyz`
          - `Enter calculation method (...)`: `1` (for GFN1-xTB)
          - `Specify the cluster atom number (25 or 28)`: `25` (for the pyramid template)
          - `Specify the energy range (...)`: `3` (to scan $E_F \pm 3$ eV)
          - `Specify the energy interval (...)`: `0.01`

2.  **Repeat this process** for all other directories (`2T`, `1P`, `2P`), ensuring the *exact same* computational parameters are used for a valid comparison.

## Step 4. Post-processing and Analysis

1.  The workflow will generate `Transmission.txt` and `Transmission.png` in each of the four directories.
2.  Use a plotting tool to load the data from `1T/Transmission.txt` and `2T/Transmission.txt` and plot them on a single graph (with y-axis in log10 scale).
3.  Use a plotting tool to load the data from `1P/Transmission.txt` and `2P/Transmission.txt` and plot them on a second graph (with y-axis in log10 scale).
4.  Visually compare the transmission values near the Fermi level (E\_F, which is the cluster HOMO energy printed to the screen) for both pairs to confirm the trend inversion: $T(E_F)$ for 1T should be higher than 2T, and $T(E_F)$ for 1P should be lower than 2P.