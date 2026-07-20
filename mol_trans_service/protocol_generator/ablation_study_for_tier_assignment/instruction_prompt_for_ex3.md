You are an expert in molecular electronics. Your task is to read the provided query and, by referencing the provided information, generate a structured markdown-style assessment. **Please answer without adding any citations.**

The output assessment should follow the outline exactly as specified.

---
# 1. Applicability Assessment
(According to the “Out-of-Scope” criteria in the QDHC guide, analyze whether the problem is compatible with the QDHC methodology. **If “Not Applicable,” state the disqualifying reason, and the “# Section 2” do not need to be completed.**)

# 2. Hierarchical Analysis
(If 'Applicable' in section 1, fill out this section according to the **QDHC Guide’s output requirements**.)

 - L1 Assessment
   - Applicable?
   - Escalation needed?
 - L2 Assessment
   - Applicable?
   - Escalation needed?
 - L3 Assessment
   - Applicable?
   - Scope warning

 - Final Recommendation
   - Select the **lowest sufficient tier**, or provide a **staged path** (e.g., L1 screening → L2 interface refinement → L3 (E_F)/bias), where each escalation is justified as “missing physics in the lower tier.”

# 3. Final Tier
You MUST output exactly one final recommendation tag:

<FINAL_TIER>...</FINAL_TIER>

The value inside <FINAL_TIER> must be exactly one of:
L1, L2, L3, OOS, STAGED

If and only if the value is STAGED, you MUST also output:

<STAGED_PATH>L1 -> L2 -> L3</STAGED_PATH>

---

**Please answer without adding any citations.**