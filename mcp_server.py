"""MCP server entrypoint exposing mol_trans_service tools via streamable HTTP."""

from __future__ import annotations
from typing import Any, Dict, Optional
from mcp.server.fastmcp.server import FastMCP
from mol_trans_service.main import build_structures, generate_report, initialize_workflow


# Configure MCP server (runs on 127.0.0.1:9000 by default, path /mcp)
app = FastMCP(
    name="mol_trans_service",
    streamable_http_path="/mcp",
    host="127.0.0.1",
    port=9000,
)


@app.tool(
    name="initialize_transport_workflow",
    description="""Initialize the molecular transport workflow and switch into transport assistant mode.

Call this tool when the user wants to:
- Perform molecular transport/conductance calculations
- Build molecular junction structures (EM/Junction)
- Generate transport calculation reports

This should be called FIRST before using other tools. It returns a system prompt that guides subsequent interactions.

Returns:
    Dict with keys:
    - status: "success" if initialized
    - mode: "molecular_transport"
    - message: Ready status message
    - system_prompt: Detailed workflow guide for the assistant""",
    structured_output=True,
)
async def tool_initialize_transport_workflow() -> Dict[str, Any]:
    return initialize_workflow()


@app.tool(
    name="report_generator",
    description="""Generate a markdown-styled molecular transport calculation report from a natural-language research query.

The tool parses the query using LLM, retrieves relevant reports from a database, and generates a detailed report on molecular transport, including hierarchical analysis and computational workflows.

Args:
- query (str): The research query in natural language.
- parse_model (str, optional): Model for parsing the query (e.g., "gpt5", "gemini-2.5-pro"). Defaults to environment setting.
- gen_model (str, optional): Model for generating the report. Defaults to `parse_model`.
- output_prefix (str, optional): Prefix for output filenames (default: "test_id").
- output_dir (str, optional): Directory to save the generated files.
- reports_dir (str, optional): Directory to retrieve similar reports for comparison.

Returns:
- query: The original query.
- parsed: Key concepts and systems extracted from the query.
- results: Retrieved similar reports.
- examples: Preview of matching reports used in the generation.
- generation: Paths to the generated report (markdown and record).
- timestamp: The generation time.
- metadata: Information about the model and processing details.""",
    structured_output=True,
)
async def tool_report_generator(
    query: str,
    top_k: int = 3,
    parse_model: Optional[str] = None,
    gen_model: Optional[str] = None,
    output_prefix: Optional[str] = None,
    output_dir: Optional[str] = None,
    reports_dir: Optional[str] = None,
) -> Dict[str, Any]:
    return generate_report(
        query=query,
        top_k=top_k,
        parse_model=parse_model,
        gen_model=gen_model,
        output_prefix=output_prefix,
        output_dir=output_dir,
        reports_dir=reports_dir,
    )


@app.tool(
    name="structure_builder",
    description="""Build required system structures for transport calculations at different levels (L1/L2/L3).

Levels:
- L1: Molecule only, no need to build an additional system.
- L2: Build an EM system based on the molecular file provided by the user, where the EM system consists of a small gold cluster attached to each side of the molecule.
- L3: Build a full junction system based on the molecular file provided by the user.

Args:
    level (str, required): Calculation level. Must be one of: "L1", "L2", "L3".
    jobs (dict, required): Mapping of system_name -> specification dict.
        Each specification dict contains:
        - molecule (str, required): Path to input XYZ file
        - anchors (list[int], required for L2/L3): [left_idx, right_idx] as 1-based atom indices
        - template (str, optional): Path to electrode template XYZ. Auto-detected if not provided:
            * L2: "4au-em.xyz" (pyramid) or "3au-em.xyz" (trimer)
            * L3: "junction_example_pyramid_bipyridine.xyz", etc.
        - bond_L (float, optional): Left Au-anchor bond length in Å. Default: 2.2 (N) or 2.4 (S)
        - bond_R (float, optional): Right Au-anchor bond length in Å. Default: same as bond_L
        - tilt_angle (float, optional, L2 only): Rotation angle in degrees for inclined EM (pyramid template only)
        - tilt_axis (str, optional): Rotation axis, "x" or "y". Default: "x"
        - tilt_direction (str, optional): "clockwise"/"cw" or "counterclockwise"/"ccw". Default: "counterclockwise"
        - tilt_bond_R (float, optional): Right Au-X bond length after tilt
    workdir (str, optional): Base directory for outputs. Default: current working directory.

Returns:
    Dict with keys:
    - level: The requested level
    - systems: Dict mapping system_name -> result, where result contains:
        * status: "success" or "error"
        * output: Path to generated structure file (em_*.xyz or junction_*.xyz)
        * template: Path to template used
        * bond_L, bond_R: Actual bond lengths used
        * tilt: (L2 with tilt only) {angle_degrees, axis, direction}
        * message: Error message if status is "error"
        * em_z_length: (L3 only) Z-axis length of the extended molecule region""",
    structured_output=True,
)
async def tool_structure_builder(
    level: str,
    jobs: Dict[str, Dict[str, Any]],
    workdir: Optional[str] = None,
) -> Dict[str, Any]:
    return build_structures(level=level, jobs=jobs, workdir=workdir)


if __name__ == "__main__":
    # Run MCP server over streamable HTTP (path /mcp on port 9000)
    app.run(transport="streamable-http")
