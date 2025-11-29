You are an expert in molecular electronics. Your task is to read the provided query and, by referencing the **QDHC Guide** and **MST Manual**, generate a structured markdown-style report. Three examples report file has been provided for reference. **Please answer without adding any citations.**

The output report should follow the 7-section outline exactly as specified.

---
# 0. Metadata
 - Title:  (Omit this part)  
 - DOI: (Omit this part)  

# 1. Query Summary

# 2. Computational Objectives

# 3. Involved Systems

## System 1: [Molecule Name/Abbreviation]
 - Core Molecule:  
	- abbreviation: (The abbreviation/label used in the query)  
	- full_chemical_name: Complete chemical name of the molecule if provided. (e.g., 2,7-bis(4-(methylthio)phenyl)-9H-carbazole).  
	- core_smiles: (SMILES string of the central molecular bridge only, without the anchors)  
 - Anchors:  
	- anchor_groups: (Tags-only, no descriptions. Follow the format: "Name_ChemicalFormula", e.g., ['Thiol_SH', 'Pyridine_N'], ['Amine_NH2'], ['Alkyl_C'], ['Benzene_Pi'])  
 - Electrodes:  
	- electrode_material: (e.g., Au, Ag, Graphene)  
	- electrode_surface: (Surface facet, e.g., 111, 100)  
 - Interface:  
	- interface_geometry_text: (A concise semantic description of the interface. **Focus on key terms.** Include: bonding/coupling configuration, anchor site, orientation/tilt, local electrode structure at the interface, and preprocessing. E.g., "Thiolate binds to Au(111) hollow site with a 30-degree tilt", "Pyridine-N couples to an Au adatom".)  
 - Variation_notes: (Describe what makes this system unique, e.g., "Baseline", "Linearly conjugated core".) 
 
(*Note: if different system share the exact same Anchors, Electrodes, and Interface as System 1, ONLY write the Core Molecule section and Variation_notes. Do not repeat the other sections.*)

# 4. Applicability Assessment
(According to the “Out-of-Scope” criteria in the QDHC guide, assess whether the core computational objective can be reproduced using MST. If “Not Applicable,” state the disqualifying reason)

# 5. Hierarchical Analysis
(If 'Applicable' in section 4, identify the correct QDHC tier for this problem. State the tier clearly.)

# 6. Input Preparation
(After determining the appropriate tier, follow the corresponding Computation Guide in the MST Manual, list the specific input files and key parameters (e.g., anchor atom indices, choice of electrode template like 'adatom' or 'pyramid') that are required for the MST workflow.)

# 7. Computational Workflow
(Provide a step-by-step procedure to execute the calculation using MST modules. This part mainly refers to the MST Manual and example files.)

## Goal:
(Write a single, concise sentence describing the final output of this workflow. e.g., "Compute and compare the zero-bias T(E) spectra for the AC, AQ, and AH systems.")

## Step 1. Create directories
(Detail the initial setup, such as creating directories and organizing the input files listed in section 6.)

## Step 2. [Action Name, e.g., Run Calculation]
(Detail the main calculation step. Specify the exact MST module to be run (e.g., L1_XTB, L2_Align, L3_Trans) and list all required parameters, user inputs, or scripts to be executed.)

## Step 3. [Action Name, e.g., Post-processing]
(Detail any subsequent steps required to get the final result, e.g., Merge spectra, Plot T(E) curves.)

---

**Please answer without adding any citations.**