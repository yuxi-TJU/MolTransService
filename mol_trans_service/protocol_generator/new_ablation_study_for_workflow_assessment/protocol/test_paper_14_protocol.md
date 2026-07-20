# 1. Query Summary
The query investigates the origin of current rectification in single-molecule junctions. An asymmetric diblock molecule (2,2′-bipyrimidinyl-4,4′-biphenyl dithiol) shows significant rectification, whereas a symmetric molecule (tetraphenyl dithiol) does not. The goal is to determine if the intrinsic molecular asymmetry is sufficient to cause this behavior by calculating and comparing their current-voltage (I-V) characteristics. The analysis should also consider the role of frontier orbital alignment and differential interactions between the molecular segments and the electrodes.

# 2. Computational Objectives
The primary computational objective is to calculate the non-equilibrium, finite-bias I-V characteristics for both the symmetric and asymmetric molecular junctions. This will allow for a direct comparison of their rectifying behavior. The analysis of the underlying bias-dependent transmission spectra, T(E,V), will be used to explain the mechanism, specifically by examining how the intrinsic molecular asymmetry, frontier orbital alignment, and molecule-electrode interactions contribute to the observed current asymmetry.

# 3. Involved Systems

## System 1: Symmetric Tetraphenyl Dithiol
 - Core Molecule:
	- abbreviation: Symmetric
	- full_chemical_name: Tetraphenyl dithiol
	- core_smiles: N/A
 - Anchors:
	- anchor_groups: ['Thiol_SH']
 - Electrodes:
	- electrode_material: Au
	- electrode_surface: (111)
 - Interface:
	- interface_geometry_text: Thiolate binds to an undercoordinated Au site (e.g., trimer tip) on the Au(111) surface, preserving molecular conformation.
 - Variation_notes: "Symmetric baseline system, expected to show no rectification."

## System 2: Asymmetric 2,2′-bipyrimidinyl-4,4′-biphenyl Dithiol
 - Core Molecule:
	- abbreviation: Asymmetric
	- full_chemical_name: 2,2′-bipyrimidinyl-4,4′-biphenyl dithiol
	- core_smiles: N/A
 - Anchors:
	- anchor_groups: ['Thiol_SH']
 - Electrodes:
	- electrode_material: Au
	- electrode_surface: (111)
 - Interface:
	- interface_geometry_text: Thiolate binds to an undercoordinated Au site (e.g., trimer tip) on the Au(111) surface, preserving molecular conformation.
 - Variation_notes: "Asymmetric diblock system, expected to show rectification."

# 4. Applicability Assessment
**Applicable.**

The query focuses on calculating I-V characteristics and rectification in single-molecule junctions with gold electrodes. This falls within the scope of coherent, elastic transport modeling. The problem does not require any of the "Out-of-Scope" items listed in the QDHC guide, such as precise absolute energy level alignment, spintronics, or non-gold electrodes. The core objective—simulating finite-bias transport to understand rectification—is a primary use case for the QDHC framework.

# 5. Hierarchical Analysis

   - **L3**. The lowest sufficient tier is L3. The central computational objective is to calculate I-V curves and explain rectification, which are finite-bias, non-equilibrium phenomena. Both L1 and L2 are insufficient as they are limited to zero-bias equilibrium calculations. The L3 scheme, particularly with its `L3_EEF` module, is explicitly designed to address this type of problem.

# 6. Input Preparation


# 7. Computational Workflow

