# 0\. Metadata

  - Title:  Electronically Transparent Au-N Bonds for Molecular Junctions
  - DOI: (Omit this part)

# 1\. Literature Summary

This is an 'experiment + computation' study. It investigates the charge transport properties of oligophenylenediamine (P2-P6) single-molecule junctions using the scanning tunneling microscope-break junction (STM-BJ) technique in an ionic environment. The primary finding is that these molecules exhibit three discrete conductance states: a "Low-G" state, a "High-G" state (\~20x higher), and an "Ultra-high-G" state (\~400x higher). The Low-G state corresponds to the expected dative Au-N ($-NH_2$) bond. The higher-conducting states are accessed by applying a high positive (oxidizing) bias, which is proposed to trigger an in-situ electrochemical conversion of the dative bond to a new, covalently-anchored $Au-N(H)R$ contact. Density functional theory (DFT) calculations support this hypothesis, showing that this new contact dramatically increases the electronic coupling to the electrodes.

# 2\. Computational Objectives

The primary goal of the paper's theoretical transport calculation is to computationally validate the hypothesis that the observed discrete conductance switching (Low-G, High-G, Ultra-high-G) is caused by a chemical change in the anchoring group at the molecule-electrode interface. The calculation aims to compare the zero-bias transmission functions for three distinct junction models:

1.  **Low-G:** Dative $Au-NH_2$ contacts on both sides.
2.  **High-G:** One dative $Au-NH_2$ contact and one converted $Au-N(H)R$ contact.
3.  **Ultra-high-G:** Two converted $Au-N(H)R$ contacts.
    The expected result is to show that the converted contacts lead to significantly higher transmission near the Fermi level, with conductance ratios (High-G/Low-G and Ultra-high-G/Low-G) that match the experimental findings.

# 3\. Involved Systems

## System 1: P4 (Low-G State)

  - Core Molecule:  
      - abbreviation: P4
      - full\_chemical\_name: p-Quaterphenylene-4,4''-diamine
      - core\_smiles: Nc1ccc(-c2ccc(-c3ccc(-c4ccc(N)cc4)cc3)cc2)cc1
  - Anchors:  
      - anchor\_groups: ['Amine\_NH2']
  - Electrodes:  
      - electrode\_material: Au
      - electrode\_surface: N/A (Calculations use cluster models)
  - Interface:  
      - interface\_geometry\_text: Dative (donor-acceptor) bond between the $N~sp^3$-like lone pair of the primary aromatic amine ($-NH_2$) and an undercoordinated Au atom.
  - Variation\_notes: Represents the "Low-G" state. Modeled with two dative $Au-NH_2$ contacts.

## System 2: P4 (High-G State)

  - Core Molecule:  
      - abbreviation: P4
      - full\_chemical\_name: p-Quaterphenylene-4,4''-diamine
      - core\_smiles: N/A
  - Variation\_notes: Represents the "High-G" state. Modeled with one dative $Au-NH_2$ contact and one converted $Au-N(H)R$ contact (formed by removing one H from an amine).

## System 3: P4 (Ultra-high-G State)

  - Core Molecule:  
      - abbreviation: P4
      - full\_chemical\_name: p-Quaterphenylene-4,4''-diamine
      - core\_smiles: N/A
  - Variation\_notes: Represents the "Ultra-high-G" state. Modeled with two converted $Au-N(H)R$ contacts.

# 4\. Applicability Assessment

**Applicable.**

The paper's core computational objective is to compare the *relative coupling strength* and resulting transmission changes caused by different "anchoring chemistries" ($Au-NH_2$ vs. $Au-N(H)R$). This is a question of interface-dominated transport. While the original paper used DFT+$\Sigma$ (a self-energy correction) for precise level alignment, the fundamental physical trend—the difference in electronic coupling originating from local bonding motifs—can be qualitatively captured by the QDHC L2 scheme.

# 5\. Hierarchical Analysis

**Level: L2**

The paper's central claim is that the discrete conductance states are caused by a chemical change in the "anchoring chemistry" at the interface. The molecular backbone itself (P4) is identical in all three states. Therefore, the problem is not dominated by intrinsic molecular properties (L1). The switching is a discrete chemical event, not a bias-induced resonance shift, making the finite-bias or precise level-alignment features of L3 unnecessary for the core question. The problem is explicitly governed by the "local geometry and electronic coupling at the molecule-electrode interface" and the change in "anchoring chemistry," which perfectly aligns with the QDHC Guide's criteria for L2. The MST L2 scheme, using "Extended Molecule + Electrode Clusters," is designed to model exactly these interface effects.

# 6\. Input Preparation

Based on the L2 workflow, the user must manually prepare three "Extended Molecule" (EM) `.xyz` files. The `4au-em.xyz` (pyramid) template from `[MST_root]/share/em/` is a suitable model for the undercoordinated Au contact site.

1.  **`em_low_G.xyz`**:
      - Create this file by modifying the `4au-em.xyz` template.
      - Replace the placeholder molecule with the P4 backbone.
      - Connect both ends to the apex Au atoms via a standard dative $Au-NH_2$ bond geometry.
2.  **`em_high_G.xyz`**:
      - Create this file using the *same* `4au-em.xyz` template.
      - Connect one end via the dative $Au-NH_2$ bond.
      - Connect the *other* end via the converted $Au-N(H)R$ bond (i.e., remove one H atom from the $NH_2$ group and adjust the $Au-N$ bond to be shorter/covalent, as suggested by the paper).
3.  **`em_ultra_high_G.xyz`**:
      - Create this file using the *same* `4au-em.xyz` template.
      - Connect *both* ends via the converted $Au-N(H)R$ bond geometry.
4.  **Constraint**: For all three files, the Au atoms of the pyramid template must remain a rigid block, and their original atom order from the template file must be strictly maintained.

# 7\. Computational Workflow

## Goal:

Compute and compare the zero-bias T(E) spectra for the "Low-G" ($NH_2/NH_2$), "High-G" ($NH_2/NHR$), and "Ultra-high-G" ($NHR/NHR$) junction geometries to validate the switching mechanism.

## Step 1. Create directories

Create three separate directories for the systems being compared and place the corresponding EM files inside:

```
/low_G/em_low_G.xyz
/high_G/em_high_G.xyz
/ultra_high_G/em_ultra_high_G.xyz
```

## Step 2. Build "EM + Cluster" Systems (L2\_Align)

Run the `L2_Align` module in *each* directory to combine the EM file with the supplied cluster template.

1.  **For the Low-G state:**

    ```bash
    cd low_G
    L2_Align
    cd ..
    ```

      - At the prompt, enter the EM file name: `em_low_G.xyz`
      - This generates `aligned.xyz` in the `low_G` directory.

2.  **For the High-G state:**

    ```bash
    cd high_G
    L2_Align
    cd ..
    ```

      - At the prompt, enter the EM file name: `em_high_G.xyz`
      - This generates `aligned.xyz` in the `high_G` directory.

3.  **For the Ultra-high-G state:**

    ```bash
    cd ultra_high_G
    L2_Align
    cd ..
    ```

      - At the prompt, enter the EM file name: `em_ultra_high_G.xyz`
      - This generates `aligned.xyz` in the `ultra_high_G` directory.

## Step 3. Run Transport Calculations (L2\_Trans)

Run the interactive `L2_Trans` module in *each* directory to calculate the transmission.

1.  **For the Low-G state:**

    ```bash
    cd low_G
    L2_Trans
    ```

      - Follow the interactive prompts:
          - `Enter XYZ file name (...)`: `aligned.xyz`
          - `Enter calculation method (...)`: `1` (for GFN1-xTB)
          - `Specify the cluster atom number (25 or 28)`: `25` (for the pyramid template)
          - `Specify the energy range (...)`: `2.0` (to scan $E_F \pm 2$ eV, capturing the main resonances shown in Fig 3b)
          - `Specify the energy interval (...)`: `0.01`

2.  **For the High-G and Ultra-high-G states:**

      - Repeat the process in their respective directories:

    <!-- end list -->

    ```bash
    cd ../high_G
    L2_Trans

    cd ../ultra_high_G
    L2_Trans
    ```

      - Enter the *exact same* parameters at the prompts for all three calculations to ensure a valid comparison.

## Step 4. Post-processing and Analysis

The workflow will generate `Transmission.txt` and `Transmission.png` in all three directories.

1.  Use a plotting tool to load the data from all three `Transmission.txt` files (`low_G/`, `high_G/`, `ultra_high_G/`).
2.  Plot all three T(E) spectra on the same graph, with the y-axis in log10 scale.
3.  Analyze the transmission values near the Fermi level (E\_F, which is defined as the cluster HOMO energy and printed to the screen).
4.  Verify that the transmission follows the trend $T(\text{low_G}) \ll T(\text{high_G}) < T(\text{ultra_high_G})$, confirming the paper's computational findings.