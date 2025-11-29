# 0\. Metadata

  - Title:  Hemilabile ligands as mechanosensitive electrode contacts for molecular electronics
  - DOI: (Omit this part)

# 1\. Literature Summary

This is an 'experiment + computation' study. It investigates the design of mechanosensitive single-molecule junctions using wires terminated with (methylthio)thiophene, a hemilabile ligand. Using a modified STM-BJ technique with mechanical modulation, the authors found that junctions with hemilabile contacts (compounds 1, 2, 4) show a large, reversible conductance modulation of up to two orders of magnitude upon compression and stretching. In contrast, a control molecule (compound 3) with a non-hemilabile (methylthio)benzene contact shows very little conductance change. DFT-NEGF calculations confirm that the mechanism for the hemilabile molecules involves a mechanically-induced, reversible transition from a stretched, monodentate contact (low conductance) to a compressed, bidentate contact where the thienyl sulfur also interacts with the electrode, increasing the coupling ($\Gamma$) and thus the conductance. This bidentate interaction is absent in the control molecule 3, whose conductance is therefore "almost independent of the electrode separation".

# 2\. Computational Objectives

The primary goal of the paper's theoretical transport calculation is to computationally validate the hypothesis that the observed mechanosensitivity originates from the hemilabile (methylthio)thiophene contact, and not from the non-hemilabile (methylthio)benzene control. [cite\_start]The calculation aims to compare the transmission function $T(E)$ as a function of electrode separation for both a hemilabile molecule (compound 4) and the non-hemilabile control (compound 3) [cite: 236-240]. The expected result is to show that for the hemilabile molecule 4, compressing the junction (e.g., from geometry 4-IV to 4-I) causes a significant broadening of transport resonances and an increase in the mid-gap $T(E)$. Conversely, for the control molecule 3, the transmission resonances and mid-gap $T(E)$ should remain "almost independent of the electrode separation" under similar compression (e.g., from 3-IV to 3-I). This comparison directly explains the experimentally observed "sensitivity boost".

# 3\. Involved Systems

## System 1: Compound 3 (Non-hemilabile, Geometry 3-I)

  - Core Molecule:  
      - abbreviation: 3-I
      - full\_chemical\_name: 4,4'-bis(methylthio)-1,1'-biphenyl
      - core\_smiles: CSc1ccc(-c2ccc(SC)cc2)cc1
  - Anchors:  
      - anchor\_groups: ['Thioether\_SMe']
  - Electrodes:  
      - electrode\_material: Au
      - electrode\_surface: N/A (Calculations use Au tip clusters, per Fig. 5)
  - Interface:  
      - interface\_geometry\_text: The methyl thioether (SMe) sulfur forms a monodentate bond with the apex Au atom of an electrode tip.
  - Variation\_notes: Non-hemilabile control. This is the most compressed geometry for molecule 3.

## System 2: Compound 3 (Non-hemilabile, Geometry 3-II)

  - Core Molecule:  
      - abbreviation: 3-II
      - full\_chemical\_name: 4,4'-bis(methylthio)-1,1'-biphenyl
      - core\_smiles: CSc1ccc(-c2ccc(SC)cc2)cc1
  - Variation\_notes: Non-hemilabile control. Intermediate stretched geometry.

## System 3: Compound 3 (Non-hemilabile, Geometry 3-III)

  - Core Molecule:  
      - abbreviation: 3-III
      - full\_chemical\_name: 4,4'-bis(methylthio)-1,1'-biphenyl
      - core\_smiles: CSc1ccc(-c2ccc(SC)cc2)cc1
  - Variation\_notes: Non-hemilabile control. More stretched geometry.

## System 4: Compound 3 (Non-hemilabile, Geometry 3-IV)

  - Core Molecule:  
      - abbreviation: 3-IV
      - full\_chemical\_name: 4,4'-bis(methylthio)-1,1'-biphenyl
      - core\_smiles: CSc1ccc(-c2ccc(SC)cc2)cc1
  - Variation\_notes: Non-hemilabile control. This is the most stretched geometry for molecule 3.

## System 5: Compound 4 (Hemilabile, Geometry 4-I)

  - Core Molecule:  
      - abbreviation: 4-I
      - full\_chemical\_name: (5'-(methylthio)-[2,2':5',2''-terthiophen]-5-yl)(methyl)sulfane
      - core\_smiles: CSc1ccc(-c2ccc(-c3ccc(SC)s3)s2)s1
  - Anchors:  
      - anchor\_groups: ['Thioether\_SMe', 'Thiophene\_S']
  - Electrodes:  
      - electrode\_material: Au
      - electrode\_surface: N/A (Calculations use Au tip clusters, per Fig. 5)
  - Interface:  
      - interface\_geometry\_text: The junction is compressed, forcing a bidentate configuration. Each electrode is connected to the molecule through two anchoring sites. The primary methyl thioether (SMe) sulfur binds to the apex Au, and the hemilabile thienyl sulfur forms a secondary, weaker interaction with the Au electrode.
  - Variation\_notes: Hemilabile system. This is the most compressed (bidentate) geometry for molecule 4.

## System 6: Compound 4 (Hemilabile, Geometry 4-II)

  - Core Molecule:  
      - abbreviation: 4-II
      - full\_chemical\_name: (5'-(methylthio)-[2,2':5',2''-terthiophen]-5-yl)(methyl)sulfane
      - core\_smiles: CSc1ccc(-c2ccc(-c3ccc(SC)s3)s2)s1
  - Anchors:  
      - anchor\_groups: ['Thioether\_SMe', 'Thiophene\_S']
  - Variation\_notes: Each electrode is connected to the molecule through two anchoring sites. Hemilabile system. Intermediate geometry, transitioning from bidentate to monodentate.

## System 7: Compound 4 (Hemilabile, Geometry 4-III)

  - Core Molecule:  
      - abbreviation: 4-III
      - full\_chemical\_name: (5'-(methylthio)-[2,2':5',2''-terthiophen]-5-yl)(methyl)sulfane
      - core\_smiles: CSc1ccc(-c2ccc(-c3ccc(SC)s3)s2)s1
  - Anchors:  
      - anchor\_groups: ['Thiophene\_S']
  - Variation\_notes: Each electrode is connected to the molecule only via the S at the SMe position. Hemilabile system. Stretched geometry, likely monodentate.

## System 8: Compound 4 (Hemilabile, Geometry 4-IV)

  - Core Molecule:  
      - abbreviation: 4-IV
      - full\_chemical\_name: (5'-(methylthio)-[2,2':5',2''-terthiophen]-5-yl)(methyl)sulfane
      - core\_smiles: CSc1ccc(-c2ccc(-c3ccc(SC)s3)s2)s1
  - Anchors:  
      - anchor\_groups: ['Thiophene\_S']
  - Variation\_notes: Each electrode is connected to the molecule only via the S at the SMe position. Hemilabile system. This is the most stretched (monodentate) geometry for molecule 4.

# 4\. Applicability Assessment

**Applicable.**

The paper's core computational objective is to compare the *relative coupling strength* (i.e., transmission resonance broadening, $\Gamma$) induced by two different contact types (hemilabile vs. non-hemilabile) as a function of mechanical compression/stretching. This is a problem of interface-dominated transport. While the original paper used DFT-NEGF, the fundamental physical trend—the difference in mechanosensitivity originating from local bonding motifs—can be qualitatively captured by the QDHC L2 scheme.

# 5\. Hierarchical Analysis

**Level: L2**

The paper's central computational question is *why* one contact (hemilabile) responds to geometry changes (compression) while another (non-hemilabile) does not. This is not a problem of the molecule's intrinsic structure (L1) or of precise level alignment with $E_F$ (L3). Instead, the problem is explicitly governed by the "local geometry and electronic coupling at the molecule-electrode interface". The key analytical evidence sought is the change in the $T(E)$ spectrum (specifically, resonance broadening) as a direct result of the contact coordination, which differs between the two molecules. This perfectly aligns with the QDHC Guide's criteria for L2. The paper's computational model (Fig. 5a, 5b), which uses explicit Au clusters, is conceptually identical to the "Extended Molecule + Electrode Clusters" model of the MST L2 scheme.

# 6\. Input Preparation

Based on the L2 workflow, the user must manually prepare 8 "Extended Molecule" (EM) `.xyz` files. These files should be based on the paper's Figure 5 geometries. The `4au-em.xyz` (pyramid) template from `[MST_root]/share/em/` is a suitable choice for modeling the Au tip.

1.  **`em_3_I.xyz`**: Based on `4au-em.xyz`, replace placeholder with molecule 3, matching geometry 3-I.
2.  **`em_3_II.xyz`**: Based on `4au-em.xyz`, replace placeholder with molecule 3, matching geometry 3-II.
3.  **`em_3_III.xyz`**: Based on `4au-em.xyz`, replace placeholder with molecule 3, matching geometry 3-III.
4.  **`em_3_IV.xyz`**: Based on `4au-em.xyz`, replace placeholder with molecule 3, matching geometry 3-IV.
5.  **`em_4_I.xyz`**: Based on `4au-em.xyz`, replace placeholder with molecule 4, matching geometry 4-I (bidentate).
6.  **`em_4_II.xyz`**: Based on `4au-em.xyz`, replace placeholder with molecule 4, matching geometry 4-II.
7.  **`em_4_III.xyz`**: Based on `4au-em.xyz`, replace placeholder with molecule 4, matching geometry 4-III.
8.  **`em_4_IV.xyz`**: Based on `4au-em.xyz`, replace placeholder with molecule 4, matching geometry 4-IV (monodentate).

**Constraint**: For all 8 files, the Au atoms of the pyramid template must remain a rigid block, and their original atom order from the template file must be strictly maintained.

# 7\. Computational Workflow

## Goal:

Compute and compare the zero-bias $T(E)$ spectra for all 8 geometries (3-I, 3-II, 3-III, 3-IV, 4-I, 4-II, 4-III, 4-IV) to reproduce the trends in Figure 5c and 5d.

## Step 1. Create directories

Create eight separate directories, one for each geometry, and place the corresponding EM file inside:

```
/mol_3_I/em_3_I.xyz
/mol_3_II/em_3_II.xyz
/mol_3_III/em_3_III.xyz
/mol_3_IV/em_3_IV.xyz
/mol_4_I/em_4_I.xyz
/mol_4_II/em_4_II.xyz
/mol_4_III/em_4_III.xyz
/mol_4_IV/em_4_IV.xyz
```

## Step 2. Build "EM + Cluster" Systems (L2\_Align)

Run the `L2_Align` module in *each* of the eight directories.

1.  **Example for mol\_3\_I:**

    ```bash
    cd mol_3_I
    L2_Align
    cd ..
    ```

      - At the prompt, enter the EM file name: `em_3_I.xyz`
      - This generates `aligned.xyz` in the `mol_3_I` directory.

2.  **Repeat this exact process** for all other 7 directories (`mol_3_II` through `mol_4_IV`), using their respective EM file names.

## Step 3. Run Transport Calculations (L2\_Trans)

Run the interactive `L2_Trans` module in *each* of the eight directories.

1.  **Example for mol\_3\_I:**

    ```bash
    cd mol_3_I
    L2_Trans
    ```

      - Follow the interactive prompts:
          - `Enter XYZ file name (...)`: `aligned.xyz`
          - `Enter calculation method (...)`: `1` (for GFN1-xTB)
          - `Specify the cluster atom number (25 or 28)`: `25` (for the pyramid template)
          - `Specify the energy range (...)`: `3` (to scan $E_F \pm 3$ eV, matching Fig. 5)
          - `Specify the energy interval (...)`: `0.01`

2.  **Repeat this exact process** for the other 7 directories, ensuring the *exact same* computational parameters are used for a valid comparison.

## Step 4. Post-processing and Analysis

The workflow will generate a `Transmission.txt` file in each of the 8 directories.

1.  **Analyze Non-hemilabile Molecule (3):**

      - Use a plotting tool to load the 4 files: `mol_3_I/Transmission.txt`, `mol_3_II/Transmission.txt`, `mol_3_III/Transmission.txt`, and `mol_3_IV/Transmission.txt`.
      - Plot all 4 spectra on the same graph (with y-axis in log10 scale).
      - Verify that all 4 transmission curves are very similar, showing little change with geometry, to reproduce the trend in Fig. 5d.

2.  **Analyze Hemilabile Molecule (4):**

      - Use a plotting tool to load the 4 files: `mol_4_I/Transmission.txt`, `mol_4_II/Transmission.txt`, `mol_4_III/Transmission.txt`, and `mol_4_IV/Transmission.txt`.
      - Plot all 4 spectra on the same graph (with y-axis in log10 scale).
      - Verify that the transmission curves show significant changes: the compressed geometries (e.g., 4-I) should have broader resonances and a much higher mid-gap transmission than the stretched geometries (e.g., 4-IV), reproducing the trend in Fig. 5c.