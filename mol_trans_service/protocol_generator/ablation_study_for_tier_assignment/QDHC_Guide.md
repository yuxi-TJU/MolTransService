# QDHC Guide

# 1. Introduction and Goal
This guide is a **physics-governed decision manual** for selecting the appropriate QDHC tier (L1/L2/L3) for a new molecular-junction transport calculation question, and for producing a transparent, physically grounded explanation of that choice.

This question should include a description of the **physical phenomenon**, the **computational requirements**, and the **molecular junction system**. If any of this information is missing, you should not invent it yourself; instead, request the minimal additional information.

Question-Driven Hierarchical Computation (QDHC) is a tiered modeling framework for molecular-junction transport that selects the appropriate level of physical realism based on the research question. QDHC emphasizes efficiency by **isolating the dominant transport physics** and matching it to the simplest admissible approximation set, while making **scope boundaries** explicit so that the system can abstain for queries that violate the framework’s assumptions.

---

# 2. QDHC Method Overview

QDHC is built on a simple idea: in molecular-junction transport, the apparent complexity can be reduced by identifying **which physical factor dominantly controls the observable of interest**, and then using the **minimal model tier** that captures that factor. We group the dominant factor into three categories:

 - Molecule-dominant(L1): intrinsic molecular electronic structure and interference effects.
 - Interface-dominant(L2): contact geometry/chemistry, hybridization, and charge transfer at the electrode–molecule interface.
 - Electrode/bias-dominant(L3): molecule–electrode level alignment referenced to the electrode Fermi level, and nonequilibrium transport under applied bias (finite-bias I–V).

The three tiers form a nested hierarchy: moving from higher to lower tiers progressively omits more physical ingredients.  QDHC encourages using the lowest tier that is physically sufficient, however, if the research question **critically relies on any omitted ingredient**, the analysis must be escalated to the tier that explicitly includes it.

---

# 3. System Scope and Physical Principles at Each Level

## 3.1 Tier L1 — Molecule-dominant

### 3.1.1 Physical model & Approximation
 - **System of study**: an open-system molecular junction model where the molecule is treated explicitly, while electrodes are not represented by explicit atomic structure and enter only through effective couplings applied to the anchoring atoms/orbitals.
 - **Physical Approximation**: L1 adopts the Wide-Band Approximation (WBA). The influence of the electrodes is simplified to a constant, energy-independent coupling strength (Γ) and a constant self-energy (Σ=−iΓ/2), which is added to the matrix elements of the molecular effective Hamiltonian (ES - H) corresponding to the anchoring atoms.

### 3.1.2 Dominant physics captured
Under WBA constant embedding, L1 captures:

 - The transmission spectrum T(E) governed by the molecule’s intrinsic electronic structure embedded with constant electrode coupling (e.g. does **not** hinge on electrode-referenced **E_F** alignment).
 - The relative alignment of the dominant frontier resonances (often HOMO/LUMO-derived features) in T(E) and the resulting qualitative transport trends.
 - Transport phenomena that arise primarily from the molecule itself, such as molecule-driven quantum interference.
 - Changes in T(E) induced by molecular structural modifications and by different electrode connection sites, modeled as applying the constant self-energy/coupling to different anchoring atoms.
 
### 3.1.3 Physical effects neglected
 - **Geometry- and chemistry-dependent contact effects**, such as bonding-motif variation, hybridization changes, and contact-induced charge transfer that can renormalize level positions and broadenings.
 - **Alignment between the molecular energy levels and the electrode Fermi level**
 - **Finite-bias nonequilibrium response**, including bias-dependent level shifts and I–V calculation.

### 3.1.4 Typical experimental phenomena
 - **Quantum interference**: a reproducible conductance dip within a narrow tuning range
 - **Fano-like behavior**: rapid conductance variation in a narrow energy range with an asymmetric peak–dip signature
 - **Molecule-structure-driven changes**: with the same electrodes and anchoring groups, conductance shifts systematically with intramolecular structural changes or across a series of molecules differing only in internal structure/connectivity.

### 3.1.5 Evidence for using L1 & Escalation triggers
- **Evidence that L1 is sufficient:**
  - the claim is primarily about **molecular physics** (QI/Fano/symmetry/conformation),
  - the requested conclusion does **not** hinge on electrode-referenced **E_F** alignment,
  - the target is a **relative trend** rather than finite-bias response.

- **Escalation triggers:**
  - if contact geometry / anchoring chemistry controls coupling and broadening → escalate to **L2**,
  - if the mechanism depends on **E_F** alignment or requires I–V / rectification / bias effects → escalate to **L3**.

---

## 3.2 Tier L2 — Interface-dominant

### 3.2.1 Physical model & Approximation
 - **System of Study:** Extended molecule plus explicit electrode clusters capturing local metal–molecule bonding (e.g., adatom/trimer/pyramid motifs).
 - **Physical Approximation**: L2 computes the Hamiltonian for the entire "Extended Molecule (EM) + Cluster" system . The electrode self-energy (Σ) is derived from the coupling matrices obtained via partitioning, combined with a constant local density of states (LDOS) approximation for the bulk electrode's Green's function.

### 3.2.2 Dominant physics captured
With an explicit EM+cluster interface, L2 captures:

 - **Contact-geometry/chemistry effects** on transport, including how different bonding motifs and local coordination change coupling and transmission.
 - **Hybridization-driven renormalization and broadening** of molecular resonances due to explicit metal–molecule interaction at the interface (i.e., changes in peak widths and line shapes tied to contact structure).
 - **Interface-sensitive trends**: how T(E) and conductance change when the same molecule is contacted differently (different anchoring site, distance, motif) or when the interface is the intended variable.

### 3.2.3 Physical effects neglected
 - **Alignment between the molecular energy levels and the electrode Fermi level**
 - **Finite-bias nonequilibrium response** (bias-dependent potential profiles, bias-driven level shifts, I–V/rectification physics) in a controlled way.

### 3.2.4 Typical experimental phenomena
 - **Stretching or small geometric perturbations** (distance/tilt) causing substantial conductance changes, indicating coupling/broadening is contact-dominated.
 - **Anchoring-site or motif dependence**: systematic conductance differences when changing binding site, electrode tip structure, or local contact motif (even with the same molecular backbone).
 - Variation in conductance of the same molecular junction **arising from different anchoring groups**.
 
### 3.2.5 Evidence for using L2 & Escalation triggers
- **Evidence that L2 is sufficient:**
  - the question emphasizes strong sensitivity to **contact geometry or anchoring chemistry**,
  - the objective is still primarily **zero-bias** / equilibrium transmission or contact-controlled conductance (not finite-bias I–V),
  - the narrative does not require electrode-referenced quantitative alignment to **E_F**.

- **Escalation triggers:**
  - the mechanism is assigned by alignment at **E−E_F=0** (electrode-referenced) → escalate to **L3**,
  - any request for **finite-bias observables** (I–V, rectification ratio, dI/dV, NDR) → escalate to **L3**.

---

## 3.3 Tier L3 — Electrode/bias-dominant

### 3.3.1 Physical model & Approximation
 - **System of Study:** Full molecular junction represented as an extended molecule connected to electrode principal layers; electrodes are embedded via surface Green’s functions.
 - **Physical Approximation**: L3 uses pre-calculated, energy-dependent Surface Green's Functions for the bulk electrodes, which are loaded and interpolated during the transport calculation. Compared with L2, it **enables proper energy-level alignment** of molecular orbitals to the electrode's Fermi level (E_F).
 - **Finite-Bias(nonequilibrium)**: Non-equilibrium transport (I-V curves) is simulated by applying a Uniform External Electric Field (EEF) across the Extended Molecule region during the electronic structure calculation.
 
### 3.3.2 Dominant physics captured
With semi-infinite electrode embedding and an electrode-referenced energy scale, L3 captures:
 - **Electrode-referenced level alignment**: how molecular resonances and transmission features align relative to the electrode-defined **E_F**, enabling mechanistic assignments that rely on **E - E_F**(e.g., HOMO- vs LUMO-like conduction as defined relative to the electrode Fermi level).
 - Mechanisms that depend on electrode-referenced alignment (dominant channel identification near **E_F**)
 - **Nonequilibrium finite-bias response (I–V)**: bias-dependent transport signatures (I–V, rectification, dI/dV).
 
### 3.3.3 Physical effects neglected
 - L3 does **not** guarantee experimentally quantitative **absolute** level alignment, which may require image-charge / many-body corrections (e.g., DFT+Σ). Such “precise alignment” is **Out-of-Scope**.
 
### 3.3.4 Typical experimental phenomena
 - Claims explicitly tied to **E - E_F = 0** (e.g., identifying whether a conductance channel is HOMO- or LUMO-dominated relative to the electrode Fermi level)
 - Finite-bias signatures: rectification (I(+V) ≠ I(−V)), strong I–V nonlinearity, features in dI/dV, or bias-driven switching/threshold behavior that cannot be reduced to equilibrium T(E) trends.

### 3.3.5 Evidence for using L3 & Escalation triggers
- **Evidence that L3 is sufficient:**
 - The requested mechanism assignment depends on electrode-referenced **E_F** alignment (explicit use of **E - E_F**).
 - Identify the dominant transport channel(s) near the Fermi level.
 - Analyze the molecular-orbital contributions to a transmission peak at a given energy.
 - Bias-dependent transport calculations (I–V characteristics, rectification ratio).

- **Escalation triggers(beyond QDHC):**
 - L3 does **not** guarantee experimentally quantitative **absolute** level alignment, which may require image-charge / many-body corrections (e.g., DFT+Σ). Such “precise alignment” is **Out-of-Scope**.

---

# 4. Out-of-Scope
If a problem **requires** any of the following aspects, it is incompatible with all current QDHC levels:

 - **Precise Energy Level Alignment**: Quantitative absolute molecular level alignment vs. electrode Fermi level, requiring advanced corrections such as DFT+Σ (image-charge corrections) beyond standard DFT.
   - **Clarifying note:** L3 supports electrode-referenced alignment **within the chosen electrode model**, but not experimentally quantitative absolute alignment.
 
 - **Spintronics**: Spin-dependent transport (spin filtering, magnetoresistance, spin valves).
 - **Thermoelectric Transport**: Seebeck/Peltier effects, requiring thermoelectric response beyond the current scope.
 - **Ensemble and Collective Effects**: Beyond single-molecule junctions (intermolecular interactions, cooperative dipoles, SAM collective transport).
 - **Incoherent Transport**: Inelastic/incoherent mechanisms (phonon-assisted tunneling, hopping/Marcus-type transport) beyond coherent elastic Landauer transport.
 - **Higher-Level Electronic Structure Methods / Parameter Limits**: Because the framework relies on the GFN-xTB semi-empirical approach, it may not be reliable for systems containing elements outside its parameter set (e.g., transition-metal complexes, heavy elements), or molecules with strong electronic correlation.
 - **Non-Gold Electrode**： The electrode material is a non-gold option, such as silver, platinum, or a graphene electrode.

*Even when an “Out-of-Scope” item is present, the analysis should prioritize extracting the **essential and tractable** in-scope aspects of the transport problem whenever possible.*

---

## 5. Tier Selection Rule

**The response must follow this order: Out-of-Scope → L1 → L2 → L3 → Recommended path**.
If essential information is missing, ask minimal targeted questions and do not guess.

 - 1. Check **Out-of-Scope** first. If any Section 4 item is required, state it and stop (no tier selection).
 - 2. Evaluate L1 → L2 → L3 in order. For each tier, you must report:
	 - **Applicable?** (YES/NO/CONDITIONAL) by linking the phenomenon/claim to the tier’s **Dominant physics captured**.
	 - **Need escalation?** (YES/NO) by identifying which required ingredient lies in the tier’s **Physical effects neglected**.
 - 3. Provide your final recommended tier selection. This can be a single tier or a staged path (e.g., L1 screening → L2 for interface sensitivity → L3 for I-V calculation), where each upgrade is justified in terms of the missing physics in the lower tier.

** Mandatory checklist (must appear in the response)**:

 - Out-of-Scope verdict (YES/NO; if YES, which item).
 - L1/L2/L3 tier assessments (Applicable? + Need escalation?).
 - Final recommendation (single-tier or staged path).
 - Minimal missing-information questions (only if needed).

---

# 6. Output
*The output should include at least the following two components (unless otherwise specified)*:
1) **Applicability Assessment**  
   - Based on Section 4, analyze whether the problem is compatible with the QDHC methodology — i.e., whether it involves any out-of-scope aspects.

2) **Hierarchical Analysis (Tier Selection + Evidence)**  
   The response must evaluate tiers **in order (L1 → L2 → L3)** and report **both sufficiency and escalation** for each tier:

   - **L1 Assessment**
     - **Applicable?** YES/NO/CONDITIONAL
       (If YES: cite which **L1 Dominant physics captured** supports the phenomenon/claim.)
     - **Escalation needed?** YES/NO
       (If YES: cite which required ingredient lies in **L1 Physical effects neglected**, and name the next tier that introduces it.)
   - **L2 Assessment (explicit interface)**
     - **Applicable?** YES/NO/CONDITIONAL
       (If YES: cite which **L2 Dominant physics captured** supports the phenomenon/claim.)
     - **Escalation needed?** YES/NO
       (If YES: cite which required ingredient lies in **L2 Physical effects neglected**, and name the next tier that introduces it.)
   - **L3 Assessment (electrode-referenced (E_F) + bias)**
     - **Applicable?** YES/NO/CONDITIONAL
       (If YES: cite which **L3 Dominant physics captured** is required by the claim—e.g., (E-E_F), (\Sigma(E)), finite-bias observables.)
     - **Scope warning (mandatory when relevant):** if the request implies **quantitative absolute level alignment**, mark it **Out-of-Scope** (Section 4) even if L3 is otherwise applicable.

   - **Final Recommendation**
     - Select the **lowest sufficient tier**, or provide a **staged path** (e.g., L1 screening → L2 interface refinement → L3 (E_F)/bias), where each escalation is justified as “missing physics in the lower tier.”
     - If tier choice is **conditional**, list the **minimal missing inputs** required to finalize the selection.