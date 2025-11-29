# 1. Introduction and Goal
This *GUIDE* serves as a framework to assist LLMs in analyzing transport-related computational problems in molecular electronics. It helps determine the lowest Question-Driven Hierarchical Computation (QDHC) level (L1/L2/L3) that provides the necessary physical realism for a given task, such as **analyzing a paper's results** or **addressing a new computational query**. 

The core principle is "greedy minimization": start with the simplest level and escalate only when the paper's claims, evidence or observables explicitly demand more realism about molecules, interfaces, electrodes, or bias. Analysis must be strictly grounded in provided context (text, figures, methods, or query content), avoiding assumptions or hallucinations. 

QDHC emphasizes efficiency by isolating dominant charge transport factors, bridging simplified models and full NEGF+DFT workflows. **Pick the lowest level that answers the core scientific question with credible physics**.

# 2. System Scope and Strategies at Each Level
 - **L1 — Isolated Molecule + Constant-coupling**. The system considered includes only the molecule itself. Electrode self-energies are modeled using the wide-band approximation, assuming constant molecule–electrode coupling.
 - **L2 — Extended molecule + Electrode clusters**. The system includes the extended molecule with explicit electrode clusters, capturing interface effects beyond L1. Electrode clusters with various interface configurations (e.g., pyrimid, trimer, adatom) are explicitly modeled, while self-energies rely on a constant-LDOS approximation. Typical cluster sizes for common anchoring groups balance accuracy and cost.
 - **L3 — Full junction (principal layers + bulk electrodes)**. The system corresponds to a full junction structure, including the extended molecule and electrode principal layers. Compared with L2, it enables proper energy-level alignment with the electrode Fermi level. A uniform field applied to the extended-molecule region allows finite-bias simulations.
 - **Note**: Only L3 level provides a proper level alignment with "E_F = 0". In L2, E_F is approximated by the HOMO of the electrode cluster, while in L1 it is taken as the midpoint between the molecular HOMO and LUMO.

# 3. Step-by-Step Decision Rubric for the LLM
*Use this rubric to map a paper/query's claims to the appropriate level.*

## 3.1 L1: Molecule-Dominated Transport
 - **Core Question**: Is transport governed primarily by the molecule’s intrinsic electronic structure? 
 - **Primary Insights**: Transport behavior reflects properties inherent to the isolated molecule — e.g., molecularly induced quantum interference, Fano resonances, substituent/structural effects, or redox gating — even if electrodes are modeled explicitly. 
 - **Key analytical evidence**: Transport signatures originate from molecular physics, for example sharp anti-resonances or asymmetric Fano line shapes in T(E), conductance differences between isomers (e.g., meta- vs. para-linked), and correlations with conformation, substituents, or orbital character.

## 3.2 L2: Interface-Dominated Transport
 - **Core Question**: Is transport governed primarily by the local geometry and electronic coupling at the molecule–electrode interface?
 - **Primary Insights**: Transport behavior is dictated by interfacial effects — such as contact geometry, bonding/coupling motifs, and dipole formation — rather than by the intrinsic molecular structure or bulk electrode properties.
 - **Key analytical evidence**: Transport varies with interface configuration, as shown by conductance or T(E) changes with tilt angle, stretching distance, or anchoring chemistry (e.g., covalent bonding or weak interaction–based coupling), indicating interface-driven behavior.
 
## 3.3 L3: Level Alignment-Dependent or Bias-Dependent Transport
 - **Core Question**: Is transport governed primarily by molecular level alignment with the electrode Fermi level or by the applied finite bias?
 - **Primary Insights**: Conductance depends on how molecular orbitals align with E_F and/or how the transmission evolves under bias — including effects such as rectification, dominant transport channels (HOMO/LUMO), or negative differential resistance.
 - **Key analytical evidence**: Indicators include I–V or dI/dV characteristics, discussion of rectification ratios, or T(E) spectra referenced to the electrode Fermi level (E−E_F=0) that explicitly identify the conducting channel relative to E_F.

## 3.4 Tier Selection Rule
 - **Greedy Escalation**: Begin at L1. If interface geometry or coupling is essential, escalate to L2; if level alignment with E_F or bias-dependent effects are essential, escalate to L3. Always choose the lowest level that adequately addresses the claim.
 - **Uncertainty Handling**: If the appropriate level remains unclear (e.g., between L2 and L3), default to the higher level to ensure sufficient physical realism.
 - **Multiple Scenarios**: If the transport problem involves multiple scenarios, the appropriate modeling level can be assessed separately for each case.

# 4. Out-of-Scope
*If a problem MUST involve any of the following aspects, it is incompatible with all QDHC levels.*
 - **Precise Energy Level Alignment**: Quantitative absolute molecular level alignment vs. electrode Fermi level, needing advanced methods like DFT+Σ (image charge corrections) beyond standard DFT.
 - **Spintronics**: Spin-dependent transport, e.g., spin filtering, magnetoresistance, or spin-valve effects.
 - **Thermoelectric Transport**: Thermoelectric effects, e.g., Seebeck coefficient or Peltier effect, requiring energy derivatives of the transmission function.
 - **Ensemble and Collective Effects**: Beyond single-molecule junctions, e.g., intermolecular interactions, collective dipoles, or cooperative transport in SAMs.
 - **Incoherent Transport**: Inelastic or incoherent mechanisms, e.g., phonon-assisted tunneling or hopping (Marcus theory), outside the elastic coherent (Landauer) model.
 - **Higher-Level Electronic Structure Methods**: Because the framework relies on the GFN-xTB semi-empirical approach, it may not be reliable for systems containing elements outside its parameter set(such as transition-metal complexes, heavy elements), non-standard electrode materials (e.g., semiconductors or graphene, especially at the L3 level), or molecules with strong electronic correlation.
 - **Note**: Although an “Out-of-Scope” section is provided, **the main focus should always be on the essential and tractable aspects of the transport problem**.
 
# 5. Output
*The output should include at least the following two components (unless otherwise specified)*:
 - **Applicability Assessment**: Based on Section 4, analyze whether the problem is compatible with the QDHC methodology — i.e., whether it involves any out-of-scope aspects.
 - **Hierarchical Analysis**: If it is compatible, specify the corresponding QDHC level and justify the classification.

# 6. Example Output
*Refer to other example files if provided.*
