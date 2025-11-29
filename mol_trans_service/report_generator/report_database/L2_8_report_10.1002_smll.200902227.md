# 0\. Metadata

  - Title:  Revealing the Role of Anchoring Groups in the Electrical Conduction Through Single-Molecule Junctions
  - DOI: (Omit this part)

# 1\. Literature Summary

This is an 'experiment + computation' study. It investigates how different anchoring groups (thiol, nitro, and cyano) attached to a central tolane backbone molecule influence electronic transport in single-molecule gold junctions. Using the MCBJ technique, the authors measure current-voltage (I-V) characteristics and fit them to a single-level tunneling model to extract the effective molecular orbital position ($E_0$) and the coupling strength ($\Gamma$). The primary finding, supported by DFT-based transport calculations, is that the anchoring groups determine the junction's transport properties by controlling *both* the coupling strength and the position of the frontier molecular orbitals. The calculations show that electron-donating groups (thiol, amine) result in HOMO-dominated (hole) transport, while electron-withdrawing groups (nitro, cyano) result in LUMO-dominated (electron) transport.

# 2\. Computational Objectives

The primary goal of the paper's theoretical transport calculation is to computationally validate and provide a physical explanation for the parameters ($E_0$ and $\Gamma$) extracted from the experimental I-V fits. The calculation aims to:

1.  Compute the zero-bias transmission spectra $T(E)$ for tolane molecules with thiol (BTT), nitro (BNT), cyano (BCT), and amine (BAT) anchors.
2.  Investigate the effect of different, stable binding geometries (e.g., top vs. hollow, cis vs. trans) on the transmission.
3.  Justify the use of the single-level model by demonstrating that transport is dominated by a single frontier orbital resonance near the Fermi level.
4.  Reproduce the key physical trend: show how the *identity* of the anchoring group (donating vs. withdrawing) determines both the conducting orbital (HOMO vs. LUMO) and the strength of the electronic coupling (i.e., the width of the transmission resonance).

# 3\. Involved Systems

The theoretical study computed 7 distinct systems based on 4 molecules and their different binding geometries.

## System 1: BTT (top)

  - Core Molecule:  
      - abbreviation: BTT
      - full\_chemical\_name: 4,4'-bisthiotolane
      - core\_smiles: Sc1ccc(C#Cc2ccc(S)cc2)cc1
  - Anchors:  
      - anchor\_groups: ['Thiol\_SH']
  - Electrodes:  
      - electrode\_material: Au
      - electrode\_surface: N/A (Calculations use gold clusters)
  - Interface:  
      - interface\_geometry\_text: Thiol group binds to a single Au atom (top site) of a gold cluster.
  - Variation\_notes: Thiol-anchored, top-binding geometry. HOMO-dominated transport.

## System 2: BTT (hollow)

  - Core Molecule:  
      - abbreviation: BTT
      - full\_chemical\_name: 4,4'-bisthiotolane
      - core\_smiles: Sc1ccc(C#Cc2ccc(S)cc2)cc1
  - Interface:  
      - interface\_geometry\_text: Thiol group binds to a multi-atom (hollow site) of a gold cluster.
  - Variation\_notes: Thiol-anchored, hollow-binding geometry. Results in a narrower transmission resonance than the top site.

## System 3: BAT (top)

  - Core Molecule:  
      - abbreviation: BAT
      - full\_chemical\_name: 1,2-bisaminotolane
      - core\_smiles: Nc1ccc(C#Cc2ccc(N)cc2)cc1
  - Anchors:  
      - anchor\_groups: ['Amine\_NH2'] (inferred from name)
  - Electrodes:  
      - (Same as System 1)
  - Interface:  
      - interface\_geometry\_text: Amine group binds to a single Au atom (top site) of a gold cluster.
  - Variation\_notes: Amine-anchored, top-binding geometry. This system was calculated for completeness. HOMO-dominated transport.

## System 4: BNT (trans)

  - Core Molecule:  
      - abbreviation: BNT
      - full\_chemical\_name: 4,4'-bisnitrotolane
      - core\_smiles: O=[N+]([O-])c1ccc(C#Cc2ccc([N+](=O)[O-])cc2)cc1
  - Anchors:  
      - anchor\_groups: ['Nitro\_NO2']
  - Electrodes:  
      - (Same as System 1)
  - Interface:  
      - interface\_geometry\_text: Nitro group binds to Au cluster via its Oxygen atoms in a top binding position.
  - Variation\_notes: Nitro-anchored, trans configuration. LUMO-dominated transport.

## System 5: BNT (cis)

  - Core Molecule:  
      - abbreviation: BNT
      - full\_chemical\_name: 4,4'-bisnitrotolane
      - core\_smiles: O=[N+]([O-])c1ccc(C#Cc2ccc([N+](=O)[O-])cc2)cc1
  - Anchors:  
      - (Same as System 4)
  - Electrodes:  
      - (Same as System 1)
  - Interface:  
      - (Same as System 4)
  - Variation\_notes: Nitro-anchored, cis configuration. This bent structure brings two oxygen atoms closer to the cluster, leading to a broader resonance than the trans configuration.

## System 6: BCT (top)

  - Core Molecule:  
      - abbreviation: BCT
      - full\_chemical\_name: 4,4'-biscyanotolane
      - core\_smiles: N#Cc1ccc(C#Cc2ccc(C#N)cc2)cc1
  - Anchors:  
      - anchor\_groups: ['Cyano\_CN']
  - Electrodes:  
      - (Same as System 1)
  - Interface:  
      - interface\_geometry\_text: Cyano group binds to a single Au atom (top site) of a gold cluster.
  - Variation\_notes: Cyano-anchored, straight geometry, binding to a low-coordination Au atom. LUMO-dominated transport.

## System 7: BCT (hollow)

  - Core Molecule:  
      - abbreviation: BCT
      - full\_chemical\_name: 4,4'-biscyanotolane
      - core\_smiles: N#Cc1ccc(C#Cc2ccc(C#N)cc2)cc1
  - Anchors:  
      - (Same as System 6)
  - Electrodes:  
      - (Same as System 1)
  - Interface:  
      - (Same as System 6)
  - Variation\_notes: Cyano-anchored, bent geometry, one of the hollow bindings changed to a top one.

# 4\. Applicability Assessment

**Applicable.**

The paper's core computational objective is to compare the *relative coupling strength* (resonance broadening) and the *conducting channel* (HOMO vs. LUMO resonance position) for different anchoring chemistries and local geometries. This is a problem of interface-dominated transport. While the original paper used DFT, the fundamental physical trend—the difference in coupling ($\Gamma$) and the qualitative shift from HOMO- to LUMO-dominated transport due to anchor identity—can be captured by the QDHC L2 scheme, which is designed to model "local geometry and electronic coupling" and "anchoring chemistry."

# 5\. Hierarchical Analysis

**Level: L2**

The paper's central computational task is to explain *why* conductance and level alignment change based on the choice of anchoring group and binding site. This is not a problem of the molecule's intrinsic structure (L1) nor of finite-bias effects (L3, as the calculations are zero-bias $T(E)$). The problem is explicitly governed by the "local geometry and electronic coupling at the molecule–electrode interface." The key analytical evidence sought is the change in the $T(E)$ spectrum (resonance position and width) as a direct result of "anchoring chemistry" (thiol, amine, nitro, cyano) and "contact geometry" (top vs. hollow, cis vs. trans). This perfectly aligns with the QDHC Guide's criteria for L2. The paper's computational model, which connects the molecule to "gold clusters", is conceptually identical to the "Extended molecule + electrode clusters" model of the MST L2 scheme.

# 6\. Input Preparation

Based on the L2 workflow, the user must manually prepare 7 "Extended Molecule" (EM) `.xyz` files. The paper explores various geometries; the MST L2 templates `4au-em.xyz` (pyramid) and `3au-em.xyz` (trimer) from `[MST_root]/share/em/` can be used to model the "top" and "hollow" sites, respectively.

1.  **`em_btt_top.xyz`**: Use the `4au-em.xyz` (pyramid) template. Replace the placeholder molecule with the tolane backbone. Connect the backbone to the apex Au atoms on each side via thiol groups (S-Au bond).
2.  **`em_btt_hollow.xyz`**: Use the `3au-em.xyz` (trimer) template. Replace the placeholder molecule. Connect the thiol groups to the 3-Au-atom trimer interface.
3.  **`em_bat_top.xyz`**: Use the `4au-em.xyz` template. Replace the placeholder with the tolane backbone. Connect the amine groups (N-Au bond) to the apex Au atoms.
4.  **`em_bnt_trans.xyz`**: Use the `4au-em.xyz` template. Replace the placeholder with the tolane backbone. Connect the nitro groups (O-Au bond) to the apex Au atoms, ensuring the molecule has a *trans* conformation.
5.  **`em_bnt_cis.xyz`**: Use the `4au-em.xyz` template. Same as `em_bnt_trans.xyz`, but manually adjust the geometry to create a *cis* conformation, as described in the paper.
6.  **`em_bct_straight.xyz`**: Use the `4au-em.xyz` template. Replace the placeholder with the tolane backbone. Connect the cyano groups (N-Au bond) to the apex Au atoms in a linear/straight geometry.
7.  **`em_bct_bent.xyz`**: Use the `3au-em.xyz` template. Same as `em_bct_straight.xyz`, but manually introduce a *bent* geometry at the interface, as described in the paper.
8.  **Constraint**: For all 7 files, the Au atoms of the chosen template (pyramid or trimer) must remain a rigid block, and their original atom order from the template file must be strictly maintained.

# 7\. Computational Workflow

## Goal:

Compute and compare the zero-bias T(E) spectra for the 7 different molecule/geometry configurations (BTT-top, BTT-hollow, BAT-top, BNT-trans, BNT-cis, BCT-straight, BCT-bent) to validate how anchors and geometry control the conducting orbital and coupling strength.

## Step 1. Create directories

Create 7 separate directories for the systems being compared and place the corresponding EM files inside:

```
/btt_top/em_btt_top.xyz
/btt_hollow/em_btt_hollow.xyz
/bat_top/em_bat_top.xyz
/bnt_trans/em_bnt_trans.xyz
/bnt_cis/em_bnt_cis.xyz
/bct_straight/em_bct_straight.xyz
/bct_bent/em_bct_bent.xyz
```

## Step 2. Build "EM + Cluster" Systems (L2\_Align)

Run the `L2_Align` module in *each* of the 7 directories.

1.  **For the `btt_top` system:**

    ```bash
    cd btt_top
    L2_Align
    cd ..
    ```

      - At the prompt, enter the EM file name: `em_btt_top.xyz`
      - This generates `aligned.xyz` in the `btt_top` directory.

2.  **Repeat this process** for all 6 other directories (`btt_hollow`, `bat_top`, etc.), entering their respective EM file names at the prompt.

## Step 3. Run Transport Calculations (L2\_Trans)

Run the interactive `L2_Trans` module in *each* of the 7 directories.

1.  **For the `btt_top` system:**

    ```bash
    cd btt_top
    L2_Trans
    ```

      - Follow the interactive prompts:
          - `Enter XYZ file name (...)`: `aligned.xyz`
          - `Enter calculation method (...)`: `1` (for GFN1-xTB)
          - `Specify the cluster atom number (25 or 28)`: `25` (for pyramid or trimer templates)
          - `Specify the energy range (...)`: `3` (to scan $E_F \pm 3$ eV, covering the range in Fig. 3)
          - `Specify the energy interval (...)`: `0.01`

2.  **Repeat this process** for all 6 other directories, ensuring the *exact same* computational parameters (`1`, `25`, `3`, `0.01`) are used for a valid comparison.

## Step 4. Post-processing and Analysis

1.  The workflow will generate `Transmission.txt` and `Transmission.png` in all 7 directories.
2.  Use a plotting tool (e.g., Python/Matplotlib) to load the data from all 7 `Transmission.txt` files.
3.  Plot the spectra on a single graph (or in groups, as in Fig. 3) with the y-axis in log10 scale and energy relative to $E_F$ (cluster HOMO) on the x-axis.
4.  Analyze the spectra to confirm:
      - HOMO-dominance (resonance \< $E_F$) for BTT and BAT systems.
      - LUMO-dominance (resonance \> $E_F$) for BNT and BCT systems.
      - Compare `btt_top` vs. `btt_hollow` to see the effect of binding site.
      - Compare `bnt_trans` vs. `bnt_cis` to see the effect of conformation.
      - Compare `bct_straight` vs. `bct_bent` to see the effect of interface geometry.