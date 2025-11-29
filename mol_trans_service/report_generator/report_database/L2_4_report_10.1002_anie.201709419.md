# 0\. Metadata

  - Title: Side Group-Mediated Mechanical Conductance Switching in Molecular Junctions
  - DOI: (Omit this part)

# 1\. Literature Summary

This is an 'experiment + computation' study. It investigates how different side-groups (alkyl vs. aryl) attached to a bridged dipyridyl molecular backbone influence the well-known mechanical conductance switching of pyridyl-Au junctions. Using the STM-BJ technique with piezo-modulation, the authors demonstrate that bulky *alkyl* side-groups (on molecules 3 and 4) *inhibit* the switching behavior by sterically preventing the molecule from adopting the high-conductance, tilted geometry upon compression. The primary finding is that *aryl* (π-conjugated) side-groups (on molecules 5 and 6) *reinstate* this mechanical switching. DFT calculations support this by showing that in the compressed, tilted geometry, the aryl side-group provides an additional $\pi$-coupling pathway to the gold electrode, which increases the overall coupling and restores the high-conductance state.

# 2\. Computational Objectives

The primary goal of the paper's theoretical transport calculation is to computationally validate the hypothesis that aryl side-groups reinstate mechanical switching while alkyl ones inhibit it. The calculation aims to compare the transmission spectra $T(E)$ of an alkyl-substituted molecule (e.g., **4**) and an aryl-substituted molecule (e.g., **5**) in two distinct geometries: a "relaxed" (elongated, low-G) state and a "compressed" (tilted, high-G) state. The expected result is to show that for the alkyl-substituted molecule **4**, the $T(E)$ spectra of the relaxed and compressed states are nearly identical (no switching). In contrast, for the aryl-substituted molecule **5**, the $T(E)$ spectrum of the compressed state should show significantly broader resonances (higher coupling and transmission) than the relaxed state, thereby explaining the observed switching.

# 3\. Involved Systems

## System 1: Molecule 4 (Alkyl-Substituted, Relaxed)

  - Core Molecule:
      - abbreviation: 4 (or 4A)
      - full\_chemical\_name: Cyclohexyl-substituted phosphoryl-bridged dipyridyl
      - core\_smiles: O=P1(C2CCCCC2)c2cnccc2-c2ccncc21
  - Anchors:
      - anchor\_groups: ['Pyridine\_N']
  - Electrodes:
      - electrode\_material: Au
      - electrode\_surface: N/A (Calculations use clusters)
  - Interface:
      - interface\_geometry\_text: Pyridine-N couples to an undercoordinated Au atom (e.g., adatom or pyramid apex). The molecular bridge is in a relaxed, elongated, or vertical geometry.
  - Variation\_notes: Represents the "relaxed" (low-G) state for the alkyl-substituted molecule that shows no switching.

## System 2: Molecule 4 (Alkyl-Substituted, Compressed)

  - Core Molecule:
      - abbreviation: 4 (or 4B)
      - full\_chemical\_name: Cyclohexyl-substituted phosphoryl-bridged dipyridyl
      - core\_smiles: O=P1(C2CCCCC2)c2cnccc2-c2ccncc21
  - Variation\_notes: Represents the "compressed" (high-G) state. The geometry is tilted, but the bulky alkyl side-group sterically hinders effective electronic coupling to the electrode.

## System 3: Molecule 5 (Aryl-Substituted, Relaxed)

  - Core Molecule:
      - abbreviation: 5 (or 5A)
      - full\_chemical\_name: Phenyl-substituted Si-bridged dipyridyl
      - core\_smiles: c1ccc([Si]2(c3ccccc3)c3cnccc3-c3ccncc32)cc1
  - Variation\_notes: Represents the "relaxed" (low-G) state for the aryl-substituted molecule that shows switching.

## System 4: Molecule 5 (Aryl-Substituted, Compressed)

  - Core Molecule:
      - abbreviation: 5 (or 5B)
      - full\_chemical\_name: Phenyl-substituted Si-bridged dipyridyl
      - core\_smiles: c1ccc([Si]2(c3ccccc3)c3cnccc3-c3ccncc32)cc1
  - Interface:
      - interface\_geometry\_text: Pyridine-N couples to an undercoordinated Au atom. The junction is compressed and the molecule is tilted. The aryl (phenyl) side-group forms a $\pi$-interaction with the Au electrode surface.
  - Variation\_notes: Represents the "compressed" (high-G) state. The phenyl side-group provides an additional coupling pathway to the electrode.

# 4\. Applicability Assessment

**Applicable.**

The paper's core computational objective is to compare the *relative coupling strength* (i.e., transmission resonance broadening) for two different molecules in two different geometries. This is a question of how conductance is modulated by local geometry and interface-specific interactions (steric hindrance vs. $\pi$-coupling). This is a qualitative trend that the QDHC framework is designed to capture. While the original paper used DFT, the MST L2 scheme using GFN-xTB is sufficient to reproduce the essential physical trend—the difference in coupling strength originating from the side-group's interaction with the electrode cluster.

# 5\. Hierarchical Analysis

**Level: L2**

The paper's central question is explicitly about how side-groups (alkyl vs. aryl) mediate the electronic coupling at the molecule-electrode interface during a mechanical change (relaxed vs. compressed). This is not a problem of the molecule's intrinsic properties (L1), as the backbone is similar. It is also not a problem of absolute level alignment or finite bias (L3). The key finding is that the aryl $\pi$-system interacts with the Au electrode in the compressed state, increasing coupling. This is a classic example of transport being "governed primarily by the local geometry and electronic coupling at the molecule-electrode interface." The key analytical evidence is the change in the $T(E)$ spectrum (resonance broadening) as a direct result of this side-group-mediated interface interaction. This aligns perfectly with the QDHC Guide's criteria for L2. The paper's computational model (Fig. 5), which uses explicit Au clusters, is conceptually identical to the "Extended Molecule + Electrode Clusters" model of the MST L2 scheme.

# 6\. Input Preparation

Based on the L2 workflow, the user must manually prepare four "Extended Molecule" (EM) `.xyz` files. The paper's models show tip-like structures, so the `4au-em.xyz` (pyramid) template from `[MST_root]/share/em/` is suitable.

1.  **`em_4_relaxed.xyz`**:
      - Create this file by modifying the `4au-em.xyz` template.
      - Replace the placeholder molecule with molecule **4** (alkyl-substituted).
      - Adjust the geometry to represent the "relaxed" state (e.g., vertical, elongated), similar to Fig. 5A (4A).
2.  **`em_4_compressed.xyz`**:
      - Use the *same* `4au-em.xyz` template with molecule **4**.
      - Adjust the geometry to represent the "compressed" state (e.g., tilted), similar to Fig. 5A (4B).
3.  **`em_5_relaxed.xyz`**:
      - Use the `4au-em.xyz` template.
      - Replace the placeholder molecule with molecule **5** (aryl-substituted).
      - Adjust the geometry to the "relaxed" state, similar to Fig. 5B (5A).
4.  **`em_5_compressed.xyz`**:
      - Use the `4au-em.xyz` template with molecule **5**.
      - Adjust the geometry to the "compressed" state, similar to Fig. 5B (5B).
      - **Crucially**, the phenyl side-group must be positioned to interact with the Au cluster atoms, modeling the $\pi$-coupling.
5.  **Constraint**: For all four files, the Au atoms of the pyramid template must remain a rigid block, and their original atom order from the template file must be strictly maintained.

# 7\. Computational Workflow

## Goal:

Compute and compare the zero-bias T(E) spectra for the relaxed vs. compressed geometries for both molecule 4 (alkyl) and molecule 5 (aryl) to validate the side-group-mediated switching mechanism.

## Step 1. Create directories

Create four separate directories for the systems being compared and place the corresponding EM files inside:

```
/mol4_relaxed/em_4_relaxed.xyz
/mol4_compressed/em_4_compressed.xyz
/mol5_relaxed/em_5_relaxed.xyz
/mol5_compressed/em_5_compressed.xyz
```

## Step 2. Build "EM + Cluster" Systems (L2\_Align)

Run the `L2_Align` module in *each* of the four directories to combine the EM file with the supplied cluster template.

1.  **For the `mol4_relaxed` system:**

```bash
cd mol4_relaxed
L2_Align
cd ..
```

  - At the prompt, enter the EM file name: `em_4_relaxed.xyz`
  - This generates `aligned.xyz` in the `mol4_relaxed` directory.

2.  **Repeat this process** for the `mol4_compressed`, `mol5_relaxed`, and `mol5_compressed` directories, providing their respective `em_...xyz` file names.

## Step 3. Run Transport Calculations (L2\_Trans)

Run the interactive `L2_Trans` module in *each* of the four directories to calculate the transmission.

1.  **For the `mol4_relaxed` system:**

```bash
cd mol4_relaxed
L2_Trans
```

  - Follow the interactive prompts:
      - `Enter XYZ file name (...)`: `aligned.xyz`
      - `Enter calculation method (...)`: `1` (for GFN1-xTB)
      - `Specify the cluster atom number (25 or 28)`: `25` (for the pyramid template)
      - `Specify the energy range (...)`: `3` (to scan $E_F \pm 3$ eV, matching the paper's plot range)
      - `Specify the energy interval (...)`: `0.01`

2.  **Repeat this process** for the other three directories (`mol4_compressed`, `mol5_relaxed`, `mol5_compressed`), ensuring the *exact same* computational parameters are used for a valid comparison.

## Step 4. Post-processing and Analysis

The workflow will generate `Transmission.txt` and `Transmission.png` in all four directories.

1.  Use a plotting tool to load data from `mol4_relaxed/Transmission.txt` and `mol4_compressed/Transmission.txt`. Plot them on the same graph (y-axis in log10 scale).
2.  Use a plotting tool to load data from `mol5_relaxed/Transmission.txt` and `mol5_compressed/Transmission.txt`. Plot them on a second, separate graph (y-axis in log10 scale).
3.  Analyze the plots:
      - Verify that for molecule 4, the "relaxed" and "compressed" spectra are very similar, confirming the *inhibition* of switching.
      - Verify that for molecule 5, the "compressed" spectrum shows significantly higher transmission (broader resonances) near $E_F$ than the "relaxed" spectrum, confirming the *reinstatement* of switching via side-group $\pi$-coupling.