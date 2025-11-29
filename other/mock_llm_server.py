#!/usr/bin/env python3
"""Lightweight mock server that emulates the OpenAI chat completions endpoint.

It returns deterministic responses tailored for the dithienophosphole oxide
anchor study so that the MCP workflow can run in an offline environment.
"""

from __future__ import annotations

import argparse
import json
import re
from http.server import BaseHTTPRequestHandler, HTTPServer
from typing import Any, Dict, Tuple


def _extract_query_text(user_content: str) -> str:
    match = re.search(r'"""(.*)"""', user_content, re.DOTALL)
    if match:
        return match.group(1).strip()
    return user_content.strip()


def _build_parse_payload() -> Dict[str, Any]:
    return {
        "phenomenon": (
            "Anchor-dependent conductance inversion in dithienophosphole oxide "
            "and bithiophene derivatives, contrasting electron-rich 4-thioanisole "
            "and electron-deficient 4-pyridyl anchors."
        ),
        "objectives": (
            "Run an L2 MST workflow to compare transmission spectra and charge "
            "density variations for 1T, 2T, 1P, and 2P, clarifying how anchor "
            "electronic character modulates Au–molecule coupling."
        ),
        "systems": [
            {
                "name": "1T",
                "core_smiles": "CSc1ccc(-c2cc3c(s2)-c2sc(-c4ccc(SC)cc4)cc2P3(=O)c2ccccc2)cc1",
                "anchor_groups": ["Thioanisole_SMe"],
                "electrode_material": "Au",
                "electrode_surface": "Adatom/Trimer",
                "interface": "Thioanisole S binds an under-coordinated Au apex atom.",
            },
            {
                "name": "2T",
                "core_smiles": "CSc1ccc(-c2ccc(-c3ccc(-c4ccc(SC)cc4)s3)s2)cc1",
                "anchor_groups": ["Thioanisole_SMe"],
                "electrode_material": "Au",
                "electrode_surface": "Adatom/Trimer",
                "interface": "Thioanisole S bound to the Au pyramid/adatom motif.",
            },
            {
                "name": "1P",
                "core_smiles": "O=P1(c2ccccc2)c2cc(-c3ccncc3)sc2-c2sc(-c3ccncc3)cc21",
                "anchor_groups": ["Pyridine_N"],
                "electrode_material": "Au",
                "electrode_surface": "Adatom/Trimer",
                "interface": "Pyridyl N coordinated to Au tip atoms.",
            },
            {
                "name": "2P",
                "core_smiles": "c1cc(-c2ccc(-c3ccc(-c4ccncc4)s3)s2)ccn1",
                "anchor_groups": ["Pyridine_N"],
                "electrode_material": "Au",
                "electrode_surface": "Adatom/Trimer",
                "interface": "Pyridyl N anchored to Au adatom/trimer site.",
            },
        ],
    }


REPORT_MARKDOWN = """# 0. Metadata

- Title: Anchor-controlled transport benchmarking for 1T/2T/1P/2P
- Level: L2 (Extended Molecule + Au cluster)
- Outputs: `aligned.xyz`, `Transmission.txt/.png`, `charge_density_diff.cube`, summary notebook comparing T(E) and anchor charge depletion.

# 1. Phenomenon Summary

Thioanisole anchors are electron rich and strengthen Au–S coupling, whereas pyridyl anchors are electron deficient and decouple Au–N contacts. Experiments show 1T > 2T but 2P > 1P, implying that charge redistribution at the interface dominates the conductance ordering. We must directly inspect charge density changes at the contacts and the resulting transmission coefficients.

# 2. Computational Objectives

1. Build four consistent L2 extended-molecule junctions (1T, 2T, 1P, 2P) using the same Au cluster template.
2. Run `L2_Align` + `L2_Trans` to obtain T(E) spectra and zero-bias conductance for each molecule.
3. Map charge density variations at the electrode–anchor interface to see how anchors donate or withdraw charge relative to isolated molecules.
4. Compare the thioanisole series vs. the pyridyl series to confirm the anchor-governed conductance inversion.

# 3. Proposed Systems

| Label | Backbone | Anchor | Notes |
|-------|----------|--------|-------|
| 1T | Dithienophosphole oxide | 4-thioanisole (SMe) | Electron-rich anchor expected to yield stronger Au–S coupling. |
| 2T | Bithiophene | 4-thioanisole (SMe) | Shorter conjugation, use as thioanisole reference. |
| 1P | Dithienophosphole oxide | 4-pyridyl | Electron-deficient anchor, weaker Au–N coupling. |
| 2P | Bithiophene | 4-pyridyl | Benchmark for pyridyl anchor strength. |

# 4. Level Justification

The conductance inversion is governed by how the anchors hybridize with Au atoms, so an L2 extended-molecule treatment (molecule + explicit Au tips) is required. L1 (gas-phase molecules) cannot capture Au–anchor charge sharing, and L3 would add full electrodes unnecessarily because the energy alignment is already well defined experimentally. L2 captures the interfacial coupling that differentiates S vs. N anchors.

# 5. Input Preparation

1. **Molecule geometries**: Optimize each molecule with `xtb --opt tight molecule.xyz` (gas phase) to remove experimental noise.
2. **Anchor indices**: Record the two anchor atoms for each molecule (S atoms for 1T/2T, N atoms for 1P/2P). These will be used by the builder.
3. **Template**: Use `4au-em.xyz` as the Au tip template (pyramidal cluster). Keep Au order unchanged.
4. **L2 builder setup**:
   - Create directories `1T`, `2T`, `1P`, `2P`.
   - Copy the optimized molecule XYZ into each directory.
   - Run the provided MCP `build_structures` tool in `L2` mode with anchors set to the 1-based indices of the terminal S or N atoms. Default Au–S = 2.4 Å, Au–N = 2.2 Å bond lengths are sufficient.
   - The tool places aligned molecules and generated EM files (e.g., `1T/em/extended_mol.xyz`). Inspect structures to ensure anchor Au spacing remains symmetric.
5. **Consistency**: Use identical vacuum padding and atom ordering across systems so the subsequent workflows remain comparable.

# 6. Computational Workflow

1. **Directory layout**
   ```
   1T/
     aligned.xyz
   2T/
     aligned.xyz
   1P/
     aligned.xyz
   2P/
     aligned.xyz
   ```
   `aligned.xyz` is produced by `L2_Align` below.

2. **L2_Align (geometry preparation)**
   For each directory:
   ```
   cd <system>
   L2_Align
   ```
   - Input EM file: `<system>_em.xyz` (from builder output).
   - Template: `4au-em.xyz`.
   - Confirm anchor atom numbers when prompted. Output: `aligned.xyz`.

3. **L2_Trans (transport & transmission)**
   For each system run:
   ```
   cd <system>
   L2_Trans
   ```
   Recommended answers to prompts:
   - XYZ file: `aligned.xyz`
   - Method: `1` (GFN1-xTB)
   - Cluster atoms: `25` (for the pyramid template)
   - Energy window: `3` (±3 eV)
   - Energy interval: `0.01`
   - Enable density output: `y`
   - Enable charge population report: `y`
   Key outputs: `Transmission.txt`, `Transmission.png`, `charges.json`, `density_A.cube`, `density_B.cube`.

4. **Charge density differences**
   For each system:
   - Convert `density_A.cube` and `density_B.cube` into a single charge-density file via the MST utility `cube_merge.py density_A.cube density_B.cube --output total_density.cube`.
   - Compute the difference between the bonded EM (`total_density.cube`) and the sum of isolated fragments (Au cluster + gas-phase molecule). Use `cube_delta.py total_density.cube isolated_au.cube isolated_molecule.cube --output charge_density_diff.cube`.
   - Visualize `charge_density_diff.cube` in VESTA/Avogadro to inspect charge accumulation on the anchor atoms. Quantify charge transfer using Mulliken (from `charges.json`) focusing on the anchor atoms.

5. **Transmission comparison**
   - Combine `Transmission.txt` from all four systems into a single plot (e.g., use the helper notebook `analysis/transmission_compare.ipynb`).
   - Highlight T(E_F) and the first resonance. Expect 1T > 2T near E_F, whereas 2P > 1P.

6. **Charge-conductance correlation**
   - Tabulate the anchor Mulliken charges and their corresponding T(E_F) values.
   - Plot Δq_anchor vs. log10[G/G0] to show that electron-rich S anchors donate charge and increase coupling, while electron-poor N anchors withdraw charge and suppress coupling.

# 7. Deliverables and Validation

- EM structures and aligned junctions for each molecule.
- `Transmission.txt/.png` and combined comparison plot.
- `charge_density_diff.cube` visualizations and Mulliken charge tables.
- Short report summarizing: (i) conductance ordering, (ii) anchor charge redistribution, (iii) qualitative alignment with experiments.
- Validation: identical numerical settings across molecules, convergence checked by repeating one system with a finer energy grid (0.005 eV) to ensure transmission trends are stable.
"""


class MockHandler(BaseHTTPRequestHandler):
    def do_POST(self) -> None:  # type: ignore[override]
        length = int(self.headers.get("Content-Length", "0"))
        raw = self.rfile.read(length).decode("utf-8")
        try:
            payload = json.loads(raw) if raw else {}
        except json.JSONDecodeError:
            payload = {}

        messages = payload.get("messages", [])
        system_prompt = ""
        if messages and messages[0].get("role") == "system":
            system_prompt = messages[0].get("content", "")
        user_content = messages[-1].get("content", "") if messages else ""

        if "molecular electronics research assistant" in system_prompt.lower():
            content = json.dumps(_build_parse_payload(), ensure_ascii=False)
        else:
            _ = _extract_query_text(user_content)
            content = REPORT_MARKDOWN

        response = {
            "id": "mock-response",
            "object": "chat.completion",
            "choices": [
                {
                    "index": 0,
                    "message": {"role": "assistant", "content": content},
                    "finish_reason": "stop",
                }
            ],
        }
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(response).encode("utf-8"))

    def log_message(self, format: str, *args: Any) -> None:  # type: ignore[override]
        return  # Silence default logging to avoid clutter.


def run_server(port: int) -> None:
    server = HTTPServer(("127.0.0.1", port), MockHandler)
    print(f"Mock LLM server listening on http://127.0.0.1:{port}")
    server.serve_forever()


def main() -> None:
    parser = argparse.ArgumentParser(description="Mock LLM server for MST workflow.")
    parser.add_argument("--port", type=int, default=8045)
    args = parser.parse_args()
    run_server(args.port)


if __name__ == "__main__":
    main()
