# 0\. Metadata

  - Title: Mechanically controlled quantum interference in individual π-stacked dimers
  - DOI: (Omit this part)

# 1\. Literature Summary

This is an experiment + computation study. The authors investigate how mechanically controlling the conformation of a π-stacked molecular dimer affects its electronic conductance. Using a mechanically controlled break junction (MCBJ) setup, they repeatedly pull apart a junction formed by a π-stacked dimer of S-OPE3 (an OPE3 molecule with one thiol anchor). They observe pronounced, quasiperiodic drops in conductance as the two monomers slide relative to each other. Theoretical calculations using DFT and the Landauer formalism (within the wide-band approximation) are performed on the dimer. The key finding is that these conductance drops are a direct result of destructive quantum interference (DQI), which is turned "on" and "off" by the changing stacking geometry and orbital overlap, demonstrating mechanical control of a quantum effect. A single, covalently-bonded S-OPE3-S molecule is used as a high-conductance control.

# 2\. Computational Objectives

The primary computational objective is to theoretically validate the experimental observation that mechanical sliding of a π-stacked dimer can induce large, quasiperiodic conductance modulations. The calculation aims to compute the zero-bias conductance of the S-OPE3 dimer as a function of the relative displacement of the two monomers. The expected result is a plot showing sharp drops in conductance at specific, periodic displacements, and to confirm that these drops are caused by destructive quantum interference occurring at the Fermi energy. A secondary objective is to calculate the high conductance of the single-molecule S-OPE3-S control for comparison.

# 3\. Involved Systems

## System 1: S-OPE3 dimer

  - Core Molecule:
	  - abbreviation: S-OPE3
      - full\_chemical_name: dimer of oligo-phenylene-ethynylene with one thiol
      - core\_smiles: Sc1ccc(C#Cc2ccc(C#Cc3ccccc3)cc2)cc1
  - Anchors:
      - anchor\_groups: ['Thiol\_SH']
  - Electrodes:
      - electrode\_material: Au
      - electrode\_surface: N/A (Paper mentions "lithographically defined" electrodes and "explicit gold clusters" in some calculations)
  - Interface:
      - interface\_geometry\_text: The junction is formed by two S-OPE3 molecules arranged in a π-stacked dimer. Each molecule is anchored to one gold electrode via its single thiol group. The transport pathway is therefore from one electrode, through one monomer, across the non-covalent π-stacked interface to the second monomer, and into the other electrode.
  - Variation\_notes: "Main system, non-covalently bonded dimer. Calculations are performed by scanning the relative displacement of the two monomers."

## System 2: S-OPE3-S

  - Core Molecule:
	  - abbreviation: S-OPE3-S
      - full\_chemical_name: Oligo-phenylene-ethynylene with two thiol anchors
      - core\_smiles: Sc1ccc(C#Cc2ccc(C#Cc3ccc(S)cc3)cc2)cc1
  - Anchors:
      - anchor\_groups: ['Thiol\_SH']
  - Electrodes:
      - electrode\_material: Au
      - electrode\_surface: N/A
  - Interface:
      - interface\_geometry\_text: A single S-OPE3-S molecule covalently bridges the two gold electrodes via thiol-Au bonds at both ends.
  - Variation\_notes: "Control system, single-molecule covalent junction."

# 4\. Applicability Assessment

**Applicable.**

The core computational objective is to analyze the effect of molecular conformation (relative sliding/stretching) on quantum interference and conductance. This falls squarely within the capabilities of the L1 scheme, which is designed for such problems. The paper's own theoretical method uses the wide-band-limit (WBA) approximation, which is the physical basis of the L1 scheme. While the original paper also mentions calculations with explicit gold clusters (suggesting L2 physics), the primary finding (Fig 1c) is a WBA calculation of conductance vs. displacement, which is an L1-type "conformation scan". MST can reproduce this qualitative trend and mechanism.

# 5\. Hierarchical Analysis

**Level: L1**

According to the QDHC criteria, this problem maps to the **L1 level**. The central question is how transport is "governed primarily by the molecule’s intrinsic electronic structure" and its conformation. The quasiperiodic conductance drops are caused by DQI, an effect inherent to the dimer's electronic structure at different stacking geometries. This is a classic example of "Effects of molecular conformation... on transport" and "Quantum Interference effects (DQI)", both of which are listed as L1-applicable problems. The problem does not depend on the specific details of the electrode cluster geometry (L2) or on finite-bias/level-alignment effects (L3).

# 6\. Input Preparation

This task will use the `L1_EHT` module. The `L1_EHT` module is explicitly noted as suitable for "scenarios requiring scans over many conformations (e.g., stretching)" and is very fast, making it ideal for generating the conductance vs. displacement curve, which requires many individual calculations.

1.  **Structure Files**:
      - **Dimer Scan**: first build the fully overlapped S–OPE3 dimer as the initial configuration (π–π stacking distance set to 3.5 Å). Then, while keeping the π–π distance fixed, translate one monomer relative to the other along the molecular backbone with equal steps, for a total displacement of 10 Å (1 nm). Divide 0–10 Å into 200 equal steps (step size 0.05 Å), yielding 201 configurations in total, preferably named `0.xyz`, `1.xyz`, …, `200.xyz` (one-to-one correspondence between index and step).
      - **Control**: A single `S-OPE3-S.xyz` file for the control molecule.
2.  **Anchor Atom Indices**:
      - **Dimer Files**: The user must inspect the dimer `.xyz` files to find the atom indices for the two sulfur (S) atoms (one on each monomer) that connect to the electrodes. Let these be `[L_idx]` and `[R_idx]` (in this case the indices should remain invariant across all frames).
      - **Control File**: The user must inspect `S-OPE3-S.xyz` to find the indices for its two sulfur atoms. Let these be `[L_S2_idx]` and `[R_S2_idx]`.
3.  **Directory Structure**:
      - Create a directory `dimer_scan/` and place all dimer `.xyz` files inside it.
      - Create a separate directory `control_S2/` and place `S-OPE3-S.xyz` inside it.
4.  **Key Parameters (`L1_EHT`)**:
      - `-C`, `--coupling`: `0.1` (Default value, suitable for this system).
      - `--Erange`: `-12 -8.5`
      - `--Enum`: `300`

# 7\. Computational Workflow

## Goal:

Compute the zero-bias conductance of the S-OPE3 dimer as a function of monomer displacement and calculate the conductance of the S-OPE3-S control.

## Step 1. Create directories

Create the directory structure and place the corresponding `.xyz` files as described in section 6:

```
/dimer_scan/0.xyz
/dimer_scan/1.xyz
/dimer_scan/...
/dimer_scan/200.xyz
/control_S2/S-OPE3-S.xyz
```

## Step 2. Run Calculation

This workflow involves one single-point calculation and one batch scan.

**1. Calculate Control:**
Navigate to the `control_S2` directory and run `L1_EHT`.

```bash
cd control_S2/
# Replace [L_S2_idx] and [R_S2_idx] with the correct sulfur atom indices
L1_EHT -f S-OPE3-S.xyz -L [L_S2_idx] -R [R_S2_idx] -C 0.1
cd ..
```

Note the HOMO/LUMO energies and the "Fermi energy" (mid-gap) from the screen output.

**2. Run Dimer Scan:**
Navigate to the `dimer_scan` directory. A batch script (e.g., `run_scan.sh`) is needed to loop over all displacement structures.

```bash
cd dimer_scan/
# Create a bash script named run_scan.sh:
#!/bin/bash
# Replace [L_idx] and [R_idx] with the correct S-atom indices for the dimer
LEFT_IDX=[L_idx]
RIGHT_IDX=[R_idx]

mkdir -p output
for i in {0..200}; do
  if [ -f "output/$i/output.log" ]; then
    echo "Skipping $i (already completed)"
    continue
  fi
  mkdir -p "output/$i"
  cd "output/$i" || exit 1
  L1_EHT -f "../../${i}.xyz" -L $LEFT_IDX -R $RIGHT_IDX -C 0.1 --Erange -12 -8.5 --Enum 300 > output.log 2>&1
  cd - > /dev/null
done

# Make the script executable and run it
chmod +x run_scan.sh
./run_scan.sh
cd ..
```

*Note: /output/[i]/ directories containing results for each configuration.

## Step 3. Post-processing and Analysis

1.  Open the file `control_S2/Transmission.txt`. Extract the transmission value at its "Fermi energy" (noted from its log output). This is the control conductance.
2.  Merge all dimer transmission spectra into [E × displacement] array; to generate:
 - 2D heatmap of log10(T)
 - 1D line cut at E = -10.0 eV
 - Average oscillation period (Å) vs. displacement
3.  Compare the resulting plot to the control conductance. The plot should show quasiperiodic drops, while the control value should be a single, high conductance value.