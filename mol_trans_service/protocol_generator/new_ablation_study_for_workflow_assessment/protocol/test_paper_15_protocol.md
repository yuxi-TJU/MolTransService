# 1. Query Summary
The query proposes a computational study of four donor-π-acceptor molecules (M1-M4) to investigate the mechanism of reverse rectification in single-molecule junctions. The molecules share a common vinyl-aniline backbone with a terminal cyano acceptor and thiol anchors for connection to gold electrodes. They differ by chemical substituents on the aniline donor ring (M2) and a distal phenyl ring (M3, M4) to systematically tune the donor/acceptor strength. The central hypothesis is that rectification arises from bias-induced LUMO energy pinning and its asymmetric spatial localization. The study aims to test this hypothesis by calculating I-V curves and tracking the evolution of the LUMO's energy, localization, and electrode coupling as a function of applied bias.

# 2. Computational Objectives
1.  Calculate the current-voltage (I-V) curves for the four molecular junctions (M1, M2, M3, M4).
2.  Generate transmission spectra as a function of applied bias, T(E,V), for all systems.
3.  For each system, explicitly track the following properties of the LUMO-derived resonance as a function of applied bias:
    *   Energy level position.
    *   Spatial localization (i.e., on the donor vs. acceptor side of the molecule).
    *   Effective coupling to the left and right electrodes.

# 3. Involved Systems

## System 1: M1
 - Core Molecule:  
	- abbreviation: M1
	- full_chemical_name: (Not provided)
	- core_smiles: (Not provided)
 - Anchors:  
	- anchor_groups: ['Thiol_SH']
 - Electrodes:  
	- electrode_material: Au
	- electrode_surface: (Not specified, model will use 111)
 - Interface:  
	- interface_geometry_text: Thiolate binds to an undercoordinated Au site (e.g., adatom or hollow site) on an Au(111) surface. The contact geometry is consistent across all systems.
 - Variation_notes: "Baseline system with an unsubstituted aniline donor and an unsubstituted distal phenyl."

## System 2: M2
 - Core Molecule:  
	- abbreviation: M2
 - Variation_notes: "Strengthened donor via a para-methoxy group on the aniline ring."

## System 3: M3
 - Core Molecule:  
	- abbreviation: M3
 - Variation_notes: "Weakly strengthened acceptor via a para-fluoro group on the distal phenyl ring."

## System 4: M4
 - Core Molecule:  
	- abbreviation: M4
 - Variation_notes: "Strongly strengthened acceptor via a para-nitro group on the distal phenyl ring."

# 4. Applicability Assessment
**Applicable.**

The query's objectives—calculating I-V curves, rectification, and analyzing bias-dependent changes in orbital energy, localization, and coupling—fall squarely within the scope of the QDHC framework. The systems involve standard Au electrodes and organic molecules compatible with the underlying electronic structure methods. The problem does not require any of the "Out-of-Scope" capabilities such as precise absolute energy level alignment (DFT+Σ), spintronics, or incoherent transport mechanisms.

# 5. Hierarchical Analysis

   - **L3**. This is the lowest sufficient tier. The central questions about I-V characteristics, rectification, and bias-dependent orbital evolution can only be addressed by a non-equilibrium transport calculation, which is the defining feature of the L3 scheme. A staged path is inappropriate as L1 and L2 cannot provide the primary requested observables.

# 6. Input Preparation


# 7. Computational Workflow

