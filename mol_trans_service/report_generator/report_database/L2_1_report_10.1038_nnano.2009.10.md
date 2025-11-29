# 0\. Metadata

 - Title:  Mechanically controlled binary conductance switching of a single-molecule junction
 - DOI: (Omit this part)

# 1\. Literature Summary

This is an 'experiment + computation' study. It investigates the origin of binary (high-conductance and low-conductance) states observed in 4,4'-bipyridine-gold single-molecule junctions. Using an STM break-junction (STM-BJ) method, the authors demonstrate that the junction can be reversibly switched between these two states by mechanically elongating and compressing the junction. The primary finding, supported by first-principles DFT calculations, is that the switching mechanism is not due to molecular conformation or charge state changes, but rather to distinct metal-molecule contact geometries. The low-conductance state corresponds to a vertical molecule where the N-Au bond is perpendicular to the $\pi$-system ($\alpha=90^{\circ}$), while the high-conductance state arises from a compressed, tilted geometry where the N-Au bond angle is smaller ($\alpha < 90^{\circ}$), leading to better orbital overlap and coupling.

# 2\. Computational Objectives

The primary goal of the paper's theoretical transport calculation is to computationally validate the hypothesis that the observed high-G and low-G states are caused by changes in the local contact geometry. The calculation aims to specifically quantify how the junction's transmission (and thus conductance) changes as a function of the tilt angle ($\alpha$) between the N-Au bond and the molecule's $\pi$-system. The expected result is to show that conductance is low when $\alpha=90^{\circ}$ (elongated, low-G state) and increases significantly as $\alpha$ decreases (compressed, high-G state), thereby explaining the mechanically-induced switching.

# 3\. Involved Systems

## System 1: 4,4'-bipyridine (Low-G State)

 - Core Molecule:  
    - abbreviation: bipyridine
    - full\_chemical\_name: 4,4'-bipyridine
    - core\_smiles: c1cc(-c2ccncc2)ccn1
 - Anchors:  
    - anchor\_groups: ['Pyridine\_N']
 - Electrodes:  
    - electrode\_material: Au
    - electrode\_surface: 111
 - Interface:  
    - interface\_geometry\_text: Pyridine-N couples to an undercoordinated Au atom (e.g., adatom, trimer, or pyramid motif) on the Au(111) surface.
 - Variation\_notes: Represents the "low G" state. This geometry is vertical and elongated, where the N-Au bond is perpendicular to the $\pi$-system ($\alpha \approx 90^{\circ}$).

## System 2: 4,4'-bipyridine (High-G State)

 - Core Molecule:  
    - abbreviation: bipyridine
    - full\_chemical\_name: 4,4'-bipyridine
    - core\_smiles: c1cc(-c2ccncc2)ccn1
 - Variation\_notes: Represents the "high G" state. This geometry is compressed, causing the N-Au bond to tilt relative to the $\pi$-system (e.g., $\alpha = 70^{\circ}, 50^{\circ}, 30^{\circ}$). The paper models this state using various contact motifs (adatom, trimer, pyramid) to simulate local roughness.

# 4\. Applicability Assessment

**Applicable.**

The paper's core computational goal is to relate changes in conductance to specific changes in the *interface geometry* (i.e., the N-Au bond tilt angle). This is a qualitative trend that the QDHC framework is designed to capture. While the original paper used DFT with a self-energy correction (DFT+$\Sigma$) for accurate level alignment, MST's L2 scheme can reproduce the essential physical trend (conductance change with contact geometry) using GFN-xTB, which is sufficient to address the central question.

# 5\. Hierarchical Analysis

**Level: L2**

The paper's central claim is that the binary conductance switching is "attributed to distinct contact geometries" and is controlled by "mechanical control of the metal-molecule contact geometry." The core question is not about the intrinsic properties of the bipyridine molecule (L1) nor about its absolute level alignment with the electrode E\_F or finite-bias effects (L3). Instead, the problem is explicitly about how conductance is modulated by the local interface geometry, specifically the "tilt angle" and "anchoring chemistry." This perfectly aligns with the QDHC Guide's criteria for L2, which targets problems governed by "local geometry and electronic coupling at the molecule-electrode interface" and uses "conductance or T(E) changes with tilt angle" as key analytical evidence. The MST L2 scheme, which uses "Extended Molecule + Electrode Clusters" (e.g., adatom, trimer, pyramid templates), is designed to model exactly these interface effects.

# 6\. Input Preparation

Based on the L2 workflow, the user must manually prepare "Extended Molecule" (EM) `.xyz` files based on the templates provided in `[MST_root]/share/em/`. The paper explores adatom, trimer, and pyramid configurations; the `3au-em.xyz` (trimer) or `4au-em.xyz` (pyramid) templates are suitable.

1.  **`em_low_G.xyz`**:
      - Create this file by taking an MST L2 template (e.g., `4au-em.xyz`).
      - Replace the placeholder molecule with 4,4'-bipyridine.
      - Adjust the geometry to represent the "low G" state: the molecule should be vertical, with the N-Au bond angle $\alpha \approx 90^{\circ}$ relative to the $\pi$-system.
2.  **`em_high_G.xyz`**:
      - Create this file using the *same* MST L2 template.
      - Replace the placeholder with 4,4'-bipyridine.
      - Adjust the geometry to represent the "high G" state: the molecule and contacts should be compressed/tilted, resulting in an angle $\alpha < 90^{\circ}$ (e.g., $\alpha \approx 50^{\circ}$).
      - Ensure the Au cluster atoms in both files retain the rigid block and original order from the template.

# 7\. Computational Workflow

## Goal: 

Compute and compare the zero-bias T(E) spectra for the "low G" (vertical, $\alpha \approx 90^{\circ}$) and "high G" (tilted, $\alpha < 90^{\circ}$) junction geometries to validate the switching mechanism.

## Step 1. Create directories
Create two separate directories matching the em systems and place the corresponding xyz files:

```
/low_G/em_low_G.xyz
/high_G/em_high_G.xyz
```

## Step 2. Build "EM + Cluster" Systems (L2\_Align)

Run the `L2_Align` module in each directory to generate the full system file.

1. **For the Low-G state:**

```bash
cd low_G
L2_Align
cd ..
```

* At the prompt, enter the EM file name: `em_low_G.xyz`
* This will generate the `aligned.xyz` file in the `low_G` directory.

2. **For the High-G state:**

```bash
cd high_G
L2_Align
cd ..
```

* At the prompt, enter the EM file name: `em_high_G.xyz`
* This will generate the `aligned.xyz` file in the `high_G` directory.

## Step 3. Run Transport Calculations (L2\_Trans)

Run the interactive `L2_Trans` module in each directory to calculate the transmission.

1. **For the Low-G state:**

```bash
cd low_G
L2_Trans
```

 - Follow the interactive prompts:
    - `Enter XYZ file name (...)`: `aligned.xyz`
    - `Enter calculation method (...)`: `1` (for GFN1-xTB)
    - `Specify the cluster atom number (25 or 28)`: `25` (for trimer or pyramid templates)
    - `Specify the energy range (...)`: `2` (or a similar value to scan around E\_F)
    - `Specify the energy interval (...)`: `0.01`

2. **For the High-G state:**

```bash
cd ../high_G
L2_Trans
```

 - Enter the *exact same* parameters as for the `low_G` calculation to ensure a valid comparison.

## Step 4. Post-processing and Analysis

The workflow will generate `Transmission.txt` and `Transmission.png` in both the `low_G` and `high_G` directories.

1. Compare the `Transmission.png` plots from both directories.
2. Use a plotting tool (e.g., Python/Matplotlib) to load the data from both `Transmission.txt` files and plot them on the same graph for comparison, with y-axis in log10 scale.
3. Analyze the transmission values near the Fermi level (E\_F, which is defined as the cluster HOMO energy and printed to the screen).
4. Verify that the "high G" geometry results in a significantly higher transmission near E\_F than the "low G" geometry, confirming the paper's findings.