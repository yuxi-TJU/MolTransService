# 0\. Metadata

  - Title:  C-Au Covalently Bonded Molecular Junctions Using Nonprotected Alkynyl Anchoring Groups
  - DOI: (Omit this part)

# 1\. Literature Summary

This is an 'experiment + computation' study. It investigates the charge transport properties of a family of oligo(phenyl ethynylene) (OPAn) molecules that form direct C-Au covalent bonds via unprotected alkynyl (sp-hybridized carbon) anchoring groups. Using the MCBJ technique, the paper finds that these `sp`-anchored junctions have a significantly lower conductance than similar oligophenylene molecules anchored via `sp3`-hybridized carbon atoms. The primary finding, supported by DFT-NEGF calculations, is that this conductance difference is due to the nature of the orbital coupling at the interface. The `sp`-hybridized carbon couples weakly, primarily to the Au `5d` orbitals, while the `sp3`-hybridized carbon couples strongly to the Au `6s` orbital, leading to a much broader transmission resonance and higher conductance.

# 2\. Computational Objectives

The primary goal of the paper's theoretical transport calculation is to computationally validate the hypothesis that the observed conductance difference between `sp`- and `sp3`-anchored molecules is due to a difference in molecule-electrode coupling strength. The calculation aims to specifically compare the transmission functions of an OP3 molecule connected to gold electrodes via an `sp` carbon versus an `sp3` carbon. The expected result is to show that the `sp3`-anchored system exhibits a much broader transmission resonance near the Fermi level, indicating stronger coupling and explaining its higher conductance.

# 3\. Involved Systems

## System 1: OP3 (sp-hybridized anchor)

  - Core Molecule:  
      - abbreviation: OP3 (sp)
      - full\_chemical\_name: Oligo(phenyl ethynylene) (n=3)
      - core\_smiles: C#Cc1ccc(-c2ccc(-c3ccc(C#C)cc3)cc2)cc1
  - Anchors:  
      - anchor\_groups: ['Alkynyl_C']
  - Electrodes:  
      - electrode\_material: Au
      - electrode\_surface: N/A (Calculations use pyramidal clusters)
  - Interface:  
      - interface\_geometry\_text: `sp`-hybridized **alkynyl carbon** forms a direct covalent bond with the apex Au atom of a pyramidal gold cluster.
  - Variation\_notes: Represents the low-conductance system studied experimentally in the paper.

## System 2: OP3 (sp3-hybridized anchor)

  - Core Molecule:  
      - abbreviation: OP3 (sp3)
      - full\_chemical\_name: Oligophenylene (n=3)
      - core\_smiles: Cc1ccc(-c2ccc(-c3ccc(C)cc3)cc2)cc1
  - Anchors:  
      - anchor\_groups: ['Methylene_CH2']
  - Electrodes:  
      - electrode\_material: Au
      - electrode\_surface: N/A (Calculations use pyramidal clusters)
  - Interface:  
      - interface\_geometry\_text: `sp3`-hybridized **methylene (CH2) carbon** forms a direct covalent bond with the apex Au atom of a pyramidal gold cluster.
  - Variation\_notes: Represents the high-conductance comparison system (based on literature, e.g., SnMe-OPn) used in the computational analysis.

# 4\. Applicability Assessment

**Applicable.**

The paper's core computational objective is to compare the *relative coupling strength* (i.e., transmission resonance broadening) induced by two different anchoring chemistries (`sp` vs. `sp3`). This is a question of interface-dominated transport. While the original paper used DFT+$\Sigma$ for precise energy level alignment (a method listed as Out-of-Scope for *quantitative* alignment in the QDHC guide), the fundamental physical trend—the difference in coupling strength originating from local bonding motifs—can be qualitatively captured by the QDHC L2 scheme.

# 5\. Hierarchical Analysis

**Level: L2**

The paper's central computational task is to explain why conductance changes based on the anchoring atom's hybridization. This is not a problem of the molecule's intrinsic structure (L1) or of finite-bias/level alignment (L3). Instead, the problem is explicitly governed by the "local geometry and electronic coupling at the molecule-electrode interface." The key analytical evidence sought is the change in the T(E) spectrum (specifically, resonance broadening) as a direct result of "anchoring chemistry" (sp vs. sp3). This perfectly aligns with the QDHC Guide's criteria for L2. The paper's computational model, which connects the molecule to "two pyramidal gold electrodes consisting of 30 atoms each," is conceptually identical to the "Extended molecule + electrode clusters" model of the MST L2 scheme.

# 6\. Input Preparation

Based on the L2 workflow, the user must manually prepare "Extended Molecule" (EM) `.xyz` files. The paper explicitly mentions "pyramidal gold electrodes," so the `4au-em.xyz` template (pyramid configuration) from `[MST_root]/share/em/` should be used.

1.  **`em_sp.xyz`**:
      - Create this file by modifying the `4au-em.xyz` template.
      - Replace the placeholder molecule with the OP3 backbone.
      - Connect the backbone to the apex Au atoms on each side via an `sp`-hybridized carbon (e.g., from an alkynyl group).
2.  **`em_sp3.xyz`**:
      - Create this file using the *same* `4au-em.xyz` template.
      - Replace the placeholder molecule with the OP3 backbone.
      - Connect the backbone to the apex Au atoms on each side via an `sp3`-hybridized carbon (e.g., a methylene -CH2- group).
3.  **Constraint**: For both files, the Au atoms of the pyramid template must remain a rigid block, and their original atom order from the template file must be strictly maintained.

# 7\. Computational Workflow

## Goal:

Compute and compare the zero-bias T(E) spectra for the `sp` and `sp3` anchoring geometries to validate that the `sp3` system has a broader transmission resonance.

## Step 1. Create directories

Create two separate directories for the systems being compared and place the corresponding EM files inside:

```
/sp/em_sp.xyz
/sp3/em_sp3.xyz
```

## Step 2. Build "EM + Cluster" Systems (L2\_Align)

Run the `L2_Align` module in each directory to combine the EM file with the supplied cluster template.

1.  **For the `sp` system:**

```bash
cd sp
L2_Align
cd ..
```

  - At the prompt, enter the EM file name: `em_sp.xyz`
  - This generates the `aligned.xyz` file in the `sp` directory.

2.  **For the `sp3` system:**

```bash
cd sp3
L2_Align
cd ..
```

  - At the prompt, enter the EM file name: `em_sp3.xyz`
  - This generates the `aligned.xyz` file in the `sp3` directory.

## Step 3. Run Transport Calculations (L2\_Trans)

Run the interactive `L2_Trans` module in each directory to calculate the transmission.

1.  **For the `sp` system:**

```bash
cd sp
L2_Trans
```

  - Follow the interactive prompts:
      - `Enter XYZ file name (...)`: `aligned.xyz`
      - `Enter calculation method (...)`: `1` (for GFN1-xTB)
      - `Specify the cluster atom number (25 or 28)`: `25` (for the pyramid template)
      - `Specify the energy range (...)`: `3` (to scan $E_F \pm 3$ eV)
      - `Specify the energy interval (...)`: `0.01`

2.  **For the `sp3` system:**

```bash
cd ../sp3
L2_Trans
```

  - Enter the *exact same* parameters as for the `sp` calculation to ensure a valid comparison.

## Step 4. Post-processing and Analysis

The workflow will generate `Transmission.txt` and `Transmission.png` in both the `/sp` and `/sp3` directories.

1.  Compare the `Transmission.png` plots from both directories.
2.  Use a plotting tool (e.g., Python/Matplotlib) to load the data from both `Transmission.txt` files and plot them on the same graph for comparison, with y-axis in log10 scale.
3.  Analyze the transmission resonances near the Fermi level (E\_F, which is defined as the cluster HOMO energy and printed to the screen).
4.  Verify that the transmission resonance for the `sp3` is significantly broader (higher coupling) than the resonance for the `sp`, confirming the paper's computational findings.