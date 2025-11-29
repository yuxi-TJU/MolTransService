# 0\. Metadata

  - Title:  Single cycloparaphenylene molecule devices: Achieving large conductance modulation via tuning radial $\pi$-conjugation
  - DOI: (Omit this part)

# 1\. Literature Summary

This is an 'experiment + computation' study. It investigates the charge transport properties of a series of [n]cycloparaphenylenes ([n]CPPs, where n=5 to 12) using the scanning tunneling microscope-break junction (STM-BJ) technique. The primary finding is that CPPs exhibit a unique size-dependent transport behavior that is the reverse of their linear counterparts (LPPs): as the ring size *n* decreases, the HOMO-LUMO gap *shrinks* due to increased ring strain and radial $\pi$-conjugation. This results in the smaller [n]CPPs having significantly higher conductance, while the series as a whole displays a large tunneling attenuation coefficient ($\beta$) comparable to saturated alkanes. DFT-NEGF calculations computationally confirm these findings, reproducing the trend of the narrowing HOMO-LUMO gap with decreasing *n* and validating the large $\beta$ value.

# 2\. Computational Objectives

The primary goal of the paper's theoretical transport calculation is to computationally validate the unique size-dependent electronic and transport properties observed experimentally. The calculation aims to compute the transmission functions for the [n]CPP series (n=5 to 10). The expected result is to show that: 1) The energy separation between the HOMO and LUMO resonances in the transmission spectrum *decreases* as the ring size *n* shrinks. 2) The transmission at the Fermi level ($T(E_F)$) decreases exponentially as *n* increases, allowing for the calculation of a theoretical $\beta$ value that matches the experimental one.

# 3\. Involved Systems

## System 1: [n]CPP (n=5-12)

  - Core Molecule:  
      - abbreviation: [n]CPP
      - full\_chemical\_name: [n]Cycloparaphenylene
      - core\_smiles: N/A
  - Anchors:  
      - anchor\_groups: ['Pi-Coupling']
  - Electrodes:  
      - electrode\_material: Au
      - electrode\_surface: N/A (Calculations use pyramidal clusters)
  - Interface:  
      - interface\_geometry\_text: Au pyramid apex binds directly to a C-C bond of a phenylene ring in an $\eta^2$ ($\pi$-coupled) fashion.
  - Variation\_notes: This represents a series of molecules where *n* (the number of phenylene units) varies, e.g., from 5 to 12. The goal is to compare the transport properties across this series.

# 4\. Applicability Assessment

**Applicable.**

The paper's computational objective is to model transport across a molecular series, which involves a specific and unconventional $\pi$-coupling interface ( $\eta^2$ bonding to Au pyramids, as shown in Fig. 4A). The paper explicitly states that electrode-molecule coupling strength (resonance width) and affinity decrease as *n* increases (and ring curvature decreases). This is a problem of interface-dominated transport. The paper's computational model ("Au pyramids containing 60 Au atoms") is conceptually identical to the "Extended Molecule + Electrode Clusters" model of the MST L2 scheme. While the original paper used DFT, the MST L2 scheme using GFN-xTB is sufficient to capture the *qualitative trends* of the HOMO-LUMO gap and coupling strength versus ring size *n*.

# 5\. Hierarchical Analysis

**Level: L2**

The paper's central question involves two coupled effects: the intrinsic electronic structure of the molecule (gap vs. *n*) and the specific molecule-electrode interface (coupling vs. *n*). The paper's own computational setup (Fig. 4A) uses explicit Au pyramid clusters, not a simple constant coupling (L1) or a full periodic slab (L3). The findings explicitly link transport to "decreased molecule-electrode affinity" and "decreased coupling" for larger rings. This is a clear case of transport being governed by the "local geometry and electronic coupling at the molecule-electrode interface," where the "Extended Molecule + Electrode Clusters" model of L2 is the appropriate choice. The goal is to analyze the *trend* across a series, not to find the absolute level alignment with $E_F$ (L3) or to assume the interface is irrelevant (L1).

# 6\. Input Preparation

Based on the L2 workflow and the paper's computational model (Fig. 4A), the user must manually prepare a *series* of "Extended Molecule" (EM) `.xyz` files using the `4au-em.xyz` (pyramid) template from `[MST_root]/share/em/`.

1.  **Create EM files**: A set of files (e.g., `em_cpp5.xyz`, `em_cpp6.xyz`, `em_cpp7.xyz`... `em_cpp10.xyz`) must be created.
2.  **Modify Template**: For each file, the placeholder molecule in the `4au-em.xyz` template must be replaced with the corresponding [n]CPP molecule.
3.  **Geometry**: The geometry must be adjusted so that the apex Au atoms of the two pyramids bind directly to C-C bonds on opposite sides of the [n]CPP molecule in an $\eta^2$ fashion, mimicking the setup in Fig. 4A.
4.  **Constraint**: For all files, the Au atoms of the pyramid template must remain a rigid, unified block, and their original atom order from the `4au-em.xyz` template file must be strictly maintained.

# 7\. Computational Workflow

## Goal:

Compute and compare the zero-bias T(E) spectra for the [n]CPP series (e.g., n=5 to 10) to validate that the HOMO-LUMO gap and coupling strength decrease as *n* increases.

## Step 1. Create directories

Create a separate directory for each [n]CPP system and place the corresponding EM file inside:

```
/cpp5/em_cpp5.xyz
/cpp6/em_cpp6.xyz
/cpp7/em_cpp7.xyz
...
```

## Step 2. Build "EM + Cluster" Systems (L2\_Align)

Run the `L2_Align` module in *each* directory to combine the EM file with the supplied cluster template.

1.  **For the [5]CPP system:**

```bash
cd cpp5
L2_Align
cd ..
```

  - At the prompt, enter the EM file name: `em_cpp5.xyz`
  - This generates the `aligned.xyz` file in the `cpp5` directory.

2.  **Repeat this process** for all other directories (`cpp6`, `cpp7`, etc.).

## Step 3. Run Transport Calculations (L2\_Trans)

Run the interactive `L2_Trans` module in *each* directory to calculate the transmission.

1.  **For the [5]CPP system:**

```bash
cd cpp5
L2_Trans
```

  - Follow the interactive prompts:
      - `Enter XYZ file name (...)`: `aligned.xyz`
      - `Enter calculation method (...)`: `1` (for GFN1-xTB)
      - `Specify the cluster atom number (25 or 28)`: `25` (for the pyramid template)
      - `Specify the energy range (...)`: `4` (to match the paper's plot range of $E_F \pm 4$ eV)
      - `Specify the energy interval (...)`: `0.01`

2.  **Repeat this process** for all other `cppN` directories, ensuring the *exact same* computational parameters are used for a valid comparison.

## Step 4. Post-processing and Analysis

1.  The workflow will generate `Transmission.txt` and `Transmission.png` in each `cppN` directory.
2.  Use a plotting tool to load the data from all `Transmission.txt` files and plot them on a single graph (with the y-axis in log10 scale).
3.  Visually compare the spectra to confirm that the separation between the main (HOMO and LUMO) resonances narrows as *n* decreases, reproducing the trend in Fig. 4B.
4.  Extract the transmission value at the Fermi level (E\_F, which is the cluster HOMO energy printed to the screen) from each `Transmission.txt` file.
5.  Plot these $T(E_F)$ values as a function of the transport length (Au-Au distance) on a log-linear plot to calculate the tunneling attenuation coefficient ($\beta$) and compare it to the paper's value.