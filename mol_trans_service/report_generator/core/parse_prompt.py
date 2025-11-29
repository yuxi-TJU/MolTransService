from __future__ import annotations

QUERY_PARSER_SYSTEM_PROMPT = """\
You are a molecular electronics research assistant. When given a user query about
computational needs, extract three kinds of structured information:
1. Phenomenon information: A concise semantic description of the physical effect or observation of interest.
2. Computational objectives: A concise semantic description of the calculation(s) requested.
3. System descriptions: Each system mentioned along with optional core molecular SMILES, anchors, electrodes, or interface details.

Always respond in JSON and never add explanations or commentary."""

QUERY_PARSER_USER_TEMPLATE = """\
Parse the following request and return JSON with this structure:
{{
  "phenomenon": "<string or null>",
  "objectives": "<string or null>",
  "systems": [
    {{
      "name": "<optional label>" (the abbreviation/label of the system),
      "core_smiles": "<SMILES or null>",
      "anchor_groups": ["<anchor>", "..."] ((Tags-only, no descriptions. Follow the format: "Name_ChemicalFormula", e.g., ['Thiol_SH', 'Pyridine_N'], ['Amine_NH2'], ['Alkyl_C'], ['Benzene_Pi'])),
      "electrode_material": "<material or null>" (e.g., Au, Ag, Graphene),
      "electrode_surface": "<surface or null>",
      "interface": "<free-form description or null>" (A concise semantic description of the molecule-electrode interface)
    }}
  ]
}}

Rules:
- Use null for any field not mentioned.
- Keep descriptions concise (<= 5 sentences).
- Combine multiple related molecules as separate entries in the "systems" array.
- If the user does not specify a system, return an empty list.

User query:
\"\"\"{query}\"\"\""""


def build_query_parsing_prompt(query: str) -> str:
    return QUERY_PARSER_USER_TEMPLATE.format(query=query.strip())
