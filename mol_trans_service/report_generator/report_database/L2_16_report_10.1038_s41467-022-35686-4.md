# 0\. Metadata

 - Title:  Cleavage of non-polar C(sp²)-C(sp²) bonds in cycloparaphenylenes via electric field-catalyzed electrophilic aromatic substitution
 - DOI: (Omit this part)  

# 1\. Literature Summary

This is an 'experiment + computation' study. It investigates the charge transport properties of [n]cycloparaphenylenes ([n]CPPs) using the STM-BJ technique. The primary experimental finding is that these junctions exhibit two distinct conductance states that are dependent on the applied bias voltage. At low bias (e.g., 0.1 V), the junctions show a high-conductance (High-G) state, attributed to the typical $\pi$-coupling of the [n]CPP ring to the Au electrodes. When the bias is increased to \>0.6 V, a new, much longer, low-conductance (Low-G) state emerges and becomes dominant, with a yield of \~97% at 1 V. The paper hypothesizes that the high bias creates an oriented external electric field (OEEF) that catalyzes an electrophilic aromatic substitution (EAS) reaction, cleaving a $C(sp^{2})-C(sp^{2})$ bond in the strained [n]CPP ring. This reaction converts the hoop-shaped [n]CPP (reactant) into a linear oligophenylene ([n]LPP, product) that is terminated with covalent Au-C bonds. DFT-based total energy calculations support this mechanism by showing that the OEEF stabilizes the key $\sigma$-complex intermediate. DFT transport calculations are also mentioned (in SI) to confirm that the conductance of the [n]LPP product is indeed lower than that of the [n]CPP reactant, matching the experimental High-G to Low-G transition.

# 2\. Computational Objectives

The primary goal of the paper's theoretical **transport** calculation is to computationally validate the identities of the experimentally observed High-G and Low-G states. The calculation aims to compare the zero-bias conductance of the two proposed junction structures: (1) the initial [n]CPP molecule bound to Au electrodes via $\pi$-coupling, and (2) the final [n]LPP product molecule bound to the electrodes via covalent Au-C bonds. The expected result is to show that the $\pi$-coupled [n]CPP junction has a significantly higher transmission at the Fermi level than the covalently-bound [n]LPP junction, which would confirm the assignment of the High-G and Low-G features.

# 3\. Involved Systems

## System 1: [n]CPP (Reactant, High-G)

 - Core Molecule:  
      - abbreviation: [n]CPP (High-G)
      - full\_chemical\_name: [n]Cycloparaphenylene
      - core\_smiles: N/A
 - Anchors:  
      - anchor\_groups: ['Pi-Coupling']
 - Electrodes:  
      - electrode\_material: Au
      - electrode\_surface: N/A (STM-BJ)
 - Interface:  
      - interface\_geometry\_text: Au apex (tip/substrate) binds directly to the $\pi$-system of a phenylene ring in an $\eta^2$ fashion.
 - Variation\_notes: Represents the initial, high-conductance state observed at low bias.

## System 2: [n]LPP (Product, Low-G)

 - Core Molecule:  
      - abbreviation: [n]LPP (Low-G)
      - full\_chemical\_name: [n]Oligophenylene
      - core\_smiles: N/A
 - Anchors:  
      - anchor\_groups: ['Covalent\_C']
 - Electrodes:  
      - electrode\_material: Au
      - electrode\_surface: N/A (STM-BJ)
 - Interface:  
      - interface\_geometry\_text: Linear [n]LPP backbone is terminated with direct covalent Au-C $\sigma$-bonds to the Au apex (tip/substrate).
 - Variation\_notes: Represents the final product, the low-conductance state formed at high bias via C-C bond cleavage.

# 4\. Applicability Assessment

**Applicable.**

The core *reaction mechanism* involving an OEEF-driven chemical transformation is out-of-scope for the QDHC transport framework. However, the paper's core *transport* objective—to compare the zero-bias conductance of the "before" (reactant) and "after" (product) states—is fully applicable. This objective requires comparing two systems with fundamentally different interface bonding: $\pi$-coupling vs. covalent Au-C. This is a problem of interface-dominated transport, which the QDHC framework is designed to handle.

# 5\. Hierarchical Analysis

**Level: L2**

The computational goal is to determine the difference in conductance between two systems defined by their distinct molecule-electrode interfaces. The problem is not about the intrinsic properties of an isolated molecule (L1) or about finite-bias effects (L3), but about how the transport changes when the "anchoring chemistry" and "contact geometry" are fundamentally altered (from $\pi$-coupled [n]CPP to $\sigma$-bonded [n]LPP). This is a classic L2 problem, as defined by the QDHC Guide. The MST L2 scheme, using an "Extended molecule + electrode clusters" model, is the appropriate choice to capture the effects of these two different bonding motifs.

# 6\. Input Preparation

Based on the L2 workflow, the user must manually prepare two "Extended Molecule" (EM) `.xyz` files, using [6]CPP as the representative molecule (from Fig. 2). The `4au-em.xyz` (pyramid) template from `[MST_root]/share/em/` is a suitable choice for modeling the apex-to-molecule binding.

1.  **`em_cpp6_pi.xyz`**:
      - Create this file by modifying the `4au-em.xyz` template.
      - Replace the placeholder molecule with the [6]CPP molecule.
      - Adjust the geometry so the apex Au atoms of the two pyramids bind directly to C-C bonds on opposite sides of the [6]CPP ring in an $\eta^2$ ($\pi$-coupled) fashion.
2.  **`em_lpp6_covalent.xyz`**:
      - Create this file using the *same* `4au-em.xyz` template.
      - Replace the placeholder molecule with a linear [6]Oligophenylene ([6]LPP) molecule.
      - Adjust the geometry to form a direct covalent $\sigma$-bond between the terminal carbons of the [6]LPP and the apex Au atoms of the two pyramids.
3.  **Constraint**: For both files, the Au atoms of the pyramid template must remain a rigid block, and their original atom order from the template file must be strictly maintained.

# 7\. Computational Workflow

## Goal:

Compute and compare the zero-bias T(E) spectra for the $\pi$-coupled [6]CPP (High-G state) and the covalently-bonded [6]LPP (Low-G state).

## Step 1. Create directories

Create two separate directories for the systems being compared and place the corresponding EM files inside:

```
/cpp6_pi/em_cpp6_pi.xyz
/lpp6_covalent/em_lpp6_covalent.xyz
```

## Step 2. Build "EM + Cluster" Systems (L2\_Align)

Run the `L2_Align` module in each directory to combine the EM file with the supplied cluster template.

1.  **For the `cpp6_pi` system:**

    ```bash
    cd cpp6_pi
    L2_Align
    cd ..
    ```

      - At the prompt, enter the EM file name: `em_cpp6_pi.xyz`
      - This generates the `aligned.xyz` file in the `cpp6_pi` directory.

2.  **For the `lpp6_covalent` system:**

    ```bash
    cd lpp6_covalent
    L2_Align
    cd ..
    ```

      - At the prompt, enter the EM file name: `em_lpp6_covalent.xyz`
      - This generates the `aligned.xyz` file in the `lpp6_covalent` directory.

## Step 3. Run Transport Calculations (L2\_Trans)

Run the interactive `L2_Trans` module in each directory to calculate the transmission.

1.  **For the `cpp6_pi` system:**

    ```bash
    cd cpp6_pi
    L2_Trans
    ```

      - Follow the interactive prompts:
          - `Enter XYZ file name (...)`: `aligned.xyz`
          - `Enter calculation method (...)`: `1` (for GFN1-xTB)
          - `Specify the cluster atom number (25 or 28)`: `25` (for the pyramid template)
          - `Specify the energy range (...)`: `3` (to scan $E_F \pm 3$ eV)
          - `Specify the energy interval (...)`: `0.01`

2.  **For the `lpp6_covalent` system:**

    ```bash
    cd ../lpp6_covalent
    L2_Trans
    ```

      - Enter the *exact same* parameters as for the `cpp6_pi` calculation to ensure a valid comparison.

## Step 4. Post-processing and Analysis

1.  The workflow will generate `Transmission.txt` and `Transmission.png` in both the `/cpp6_pi` and `/lpp6_covalent` directories.
2.  Use a plotting tool to load the data from both `Transmission.txt` files and plot them on the same graph (with the y-axis in log10 scale).
3.  Analyze the spectra. Verify that the transmission values near the Fermi level (E\_F, which is the cluster HOMO energy printed to the screen) are significantly higher for the `cpp6_pi` system than for the `lpp6_covalent` system, computationally confirming the paper's assignment of the experimental High-G and Low-G states.