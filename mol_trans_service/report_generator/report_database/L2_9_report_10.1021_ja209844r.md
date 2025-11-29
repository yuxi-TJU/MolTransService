# 0\. Metadata

  - Title:  Single Molecular Conductance of Tolanes: Experimental and Theoretical Study on the Junction Evolution Dependent on the Anchoring Group
  - DOI: (Omit this part)

# 1\. Literature Summary

This is an 'experiment + computation' study. It investigates the charge transport and mechanical evolution of single-molecule junctions of tolane (diphenylacetylene) with four different anchoring groups: pyridyl (PY), thiol (SH), amine (NH2), and cyano (CN). Using STM-BJ and MCBJ techniques, the authors find that the junctions evolve through multiple conductance states (labeled H, M, L) upon mechanical stretching. The study compares the junction formation probability, stability, and conductance-decay behavior of the four anchors. The primary finding, supported by DFT-NEGF calculations and MD simulations, is that the conductance evolution is determined by the specific anchoring chemistry, which dictates the binding geometries, the dominant transport channel (HOMO or LUMO), and the mechanical response to stretching (e.g., sliding vs. bond elongation).

# 2\. Computational Objectives

The primary goal of the paper's theoretical transport calculation is to computationally validate the experimentally observed differences in conductance and junction evolution across the four anchoring groups. This involves two main objectives:

1.  To determine the dominant transport channel (HOMO or LUMO) and the position of the Fermi level relative to it, which explains the high-conductance (H) state value for each anchor group.
2.  To simulate the conductance-distance traces by calculating transmission for a series of geometries representing the stretching process. The expected result is to reproduce the observed conductance decay and the evolution through different configurations (e.g., 'SIDE' to 'END' binding) that correspond to the H, M, and L states.

# 3\. Involved Systems

## System 1: Tolane-PY

  - Core Molecule:  
      - abbreviation: 1a (PY)
      - full\_chemical\_name: Tolane (Diphenylacetylene)
      - core\_smiles: C(#Cc1ccncc1)c1ccncc1
  - Anchors:  
      - anchor\_groups: ['Pyridine\_N']
  - Electrodes:  
      - electrode\_material: Au
      - electrode\_surface: 111
  - Interface:  
      - interface\_geometry\_text: Pyridine-N binds to an undercoordinated Au apex atom of a pyramidal cluster (END configuration). The simulation also considers a compressed 'SIDE' configuration where the $\pi$-system interacts with the pyramid.
  - Variation\_notes: Represents the pyridyl-anchored system. Transport is found to be LUMO-dominated.

## System 2: Tolane-SH

  - Core Molecule:  
      - abbreviation: 1b (SH)
      - full\_chemical\_name: Tolane (Diphenylacetylene)
      - core\_smiles: Sc1ccc(C#Cc2ccc(S)cc2)cc1
  - Anchors:  
      - anchor\_groups: ['Thiol\_SH']
  - Electrodes:  
      - electrode\_material: Au
      - electrode\_surface: 111
  - Interface:  
      - interface\_geometry\_text: Thiolate-S binds to the Au apex atom of a pyramidal cluster (END configuration), potentially in an atop or bridge site. The simulation involves migration from 'SIDE' to 'END' contact.
  - Variation\_notes: Represents the thiol-anchored system. Transport is found to be HOMO-dominated.

## System 3: Tolane-NH2

  - Core Molecule:  
      - abbreviation: 1c (NH2)
      - full\_chemical\_name: Tolane (Diphenylacetylene)
      - core\_smiles: Nc1ccc(C#Cc2ccc(N)cc2)cc1
  - Anchors:  
      - anchor\_groups: ['Amine\_NH2']
  - Electrodes:  
      - electrode\_material: Au
      - electrode\_surface: 111
  - Interface:  
      - interface\_geometry\_text: Amine-N binds to an undercoordinated Au apex atom of a pyramidal cluster (END configuration). The simulation considers evolution from a 'SIDE' to 'END' contact.
  - Variation\_notes: Represents the amine-anchored system. Transport is found to be HOMO-dominated.

## System 4: Tolane-CN

  - Core Molecule:  
      - abbreviation: 1d (CN)
      - full\_chemical\_name: Tolane (Diphenylacetylene)
      - core\_smiles: N#Cc1ccc(C#Cc2ccc(C#N)cc2)cc1
  - Anchors:  
      - anchor\_groups: ['Nitrile\_CN']
  - Electrodes:  
      - electrode\_material: Au
      - electrode\_surface: 111
  - Interface:  
      - interface\_geometry\_text: Nitrile-N binds to an undercoordinated Au apex atom of a pyramidal cluster (END configuration). The simulation considers evolution from a 'SIDE' to 'END' contact.
  - Variation\_notes: Represents the nitrile-anchored system. Transport is found to be LUMO-dominated.

# 4\. Applicability Assessment

**Applicable.**

The paper's core computational objective is to relate the *evolution of conductance* to *stretching distance* and *anchoring chemistry*. While the original paper used a full DFT-NEGF (L3-style) method (SIESTA+SMEAGOL) and employed empirical $E_F$ shifting to match I-V data (an L3-level concern), the central *physical process* being modeled (Fig 7) is the change in transport due to geometric evolution (e.g., sliding, stretching) at an interface explicitly modeled with *pyramid clusters*. This is a problem of interface-dominated transport. The MST L2 scheme is designed to capture exactly these qualitative trends in conductance versus geometry and to differentiate between anchoring chemistries, making it suitable for reproducing the paper's essential findings.

# 5\. Hierarchical Analysis

**Level: L2**

The paper's central computational task is to explain how conductance changes as a function of junction geometry (stretching) and to compare this behavior across different "anchoring chemistries" (PY, SH, NH2, CN). The problem is explicitly governed by the "local geometry and electronic coupling at the molecule-electrode interface." The key analytical evidence sought is the change in conductance (and T(E)) as the molecule transitions from a compressed 'SIDE' configuration to a stretched 'END' configuration. This perfectly aligns with the QDHC Guide's criteria for L2, which targets "conductance or T(E) changes with... stretching distance, or anchoring chemistry." The paper's own simulation model, which connects the molecule to "a six-atom gold pyramid at each end," is conceptually identical to the "Extended molecule + electrode clusters" model (using a pyramid template) of the MST L2 scheme.

# 6\. Input Preparation

Based on the L2 workflow, the user must manually prepare a *series* of "Extended Molecule" (EM) `.xyz` files to represent the different anchors and the key geometries during stretching. The `4au-em.xyz` (pyramid) template from `[MST_root]/share/em/` should be used, as the paper explicitly models pyramidal contacts.

To capture the evolution, at least two geometries for each anchor group should be created:

1.  **'SIDE' Configuration (e.g., `em_py_side.xyz`)**: A compressed geometry where the molecule is in a 'SIDE' configuration relative to the pyramids, mimicking the initial high-conductance state (e.g., config `a2`-`d2` in Fig 7).
2.  **'END' Configuration (e.g., `em_py_end.xyz`)**: A stretched geometry where the anchor groups bind directly to the apex Au atoms, mimicking the 'END' configuration before rupture (e.g., config `a4`-`d4` in Fig 7).

This results in a set of 8 EM files:

  - `em_py_side.xyz`, `em_py_end.xyz`
  - `em_sh_side.xyz`, `em_sh_end.xyz`
  - `em_nh2_side.xyz`, `em_nh2_end.xyz`
  - `em_cn_side.xyz`, `em_cn_end.xyz`

**Constraint**: For all 8 files, the Au atoms of the pyramid template must remain a rigid block, and their original atom order from the `4au-em.xyz` template file must be strictly maintained.

# 7\. Computational Workflow

## Goal:

Compute and compare the zero-bias T(E) spectra for the four tolane anchors (PY, SH, NH2, CN) at 'SIDE' (compressed) and 'END' (stretched) configurations to simulate the conductance evolution during stretching and identify dominant transport channels.

## Step 1. Create directories

Create eight separate directories, one for each system being compared, and place the corresponding EM file inside:

```
/py_side/em_py_side.xyz
/py_end/em_py_end.xyz
/sh_side/em_sh_side.xyz
/sh_end/em_sh_end.xyz
/nh2_side/em_nh2_side.xyz
/nh2_end/em_nh2_end.xyz
/cn_side/em_cn_side.xyz
/cn_end/em_cn_end.xyz
```

## Step 2. Build "EM + Cluster" Systems (L2\_Align)

Run the `L2_Align` module in *each* of the eight directories to combine the EM file with the supplied cluster template.

1.  **For the `py_side` system:**

<!-- end list -->

```bash
cd py_side
L2_Align
cd ..
```

  - At the prompt, enter the EM file name: `em_py_side.xyz`
  - This generates the `aligned.xyz` file in the `py_side` directory.

<!-- end list -->

2.  **Repeat this process** for all other 7 directories (e.g., `py_end`, `sh_side`, etc.), providing the respective EM file name at the prompt.

## Step 3. Run Transport Calculations (L2\_Trans)

Run the interactive `L2_Trans` module in *each* of the eight directories.

1.  **For the `py_side` system:**

<!-- end list -->

```bash
cd py_side
L2_Trans
```

  - Follow the interactive prompts:
      - `Enter XYZ file name (...)`: `aligned.xyz`
      - `Enter calculation method (...)`: `1` (for GFN1-xTB)
      - `Specify the cluster atom number (25 or 28)`: `25` (for the pyramid template)
      - `Specify the energy range (...)`: `3` (to scan $E_F \pm 3$ eV)
      - `Specify the energy interval (...)`: `0.01`

<!-- end list -->

2.  **Repeat this process** for all other 7 directories, ensuring the *exact same* computational parameters are used for a valid comparison.

## Step 4. Post-processing and Analysis

The workflow will generate `Transmission.txt` and `Transmission.png` in all eight directories.

1.  Use a plotting tool to load the data from all `Transmission.txt` files.
2.  For each anchor group (e.g., PY), plot the T(E) spectra for the `_side` and `_end` geometries on the same graph (log-scale y-axis) to visualize the conductance decay.
3.  Extract the transmission value at $E_F$ (the cluster HOMO energy, which is printed to the screen) for all eight systems.
4.  Compare the $T(E_F)$ values to confirm that conductance decreases from the 'SIDE' to the 'END' configuration, reproducing the paper's simulated stretching curves.
5.  Analyze the T(E) spectra for the 'END' configurations to qualitatively identify the dominant transport channel (i.e., whether the HOMO or LUMO resonance is closer to $E_F$) for each anchor group, and compare this to the paper's HOMO/LUMO assignments.