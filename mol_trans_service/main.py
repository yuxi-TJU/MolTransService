"""Entry points for the Molecular Transport MCP service.

Exposes three high-level tools:
- initialize_workflow: return the mode guide and system prompt content.
- generate_report: call the packaged report generator (parse + retrieve + generate).
- build_structures: build L1/L2/L3 input structures (L2 EM, L3 full junction first step).
"""

from __future__ import annotations

import os
import shutil
from pathlib import Path
from typing import Any, Dict, List, Mapping, Optional

from dotenv import load_dotenv

from .report_generator.core import (
    available_models,
    build_client_from_key,
    load_generation_materials,
    run_full_workflow,
)
from .report_generator.retrieval import RetrievalEngine
from .structure_builder import build_mst_em_functions as em_builder
from .structure_builder import build_mst_junction_function as junction_builder

# Paths and environment
PKG_ROOT = Path(__file__).resolve().parent
PROJECT_ROOT = PKG_ROOT.parent
REPORT_ROOT = PKG_ROOT / "report_generator"
STRUCTURE_BUILDER_ROOT = PKG_ROOT / "structure_builder"
PROMPT_PATH = PKG_ROOT / "prompts" / "system_prompt.md"
SYSTEM_PROMPT = PROMPT_PATH.read_text(encoding="utf-8")
MANUAL_DIR = REPORT_ROOT / "manual"
DEFAULT_REPORTS_DIR = REPORT_ROOT / "report_database"
DEFAULT_OUTPUT_DIR = REPORT_ROOT / "generated_outputs"

# Structure builder guide paths
L2_BUILD_GUIDE = STRUCTURE_BUILDER_ROOT / "build_mst_em_prompt.md"
L3_BUILD_GUIDE = STRUCTURE_BUILDER_ROOT / "build_mst_junction_prompt.md"

# Built-in template directories
EM_TEMPLATES_DIR = STRUCTURE_BUILDER_ROOT / "templates" / "extended_molecule_xyz_examples"
JUNCTION_TEMPLATES_DIR = STRUCTURE_BUILDER_ROOT / "templates" / "junction_xyz_examples"

GEN_REPORT_ENV = PROJECT_ROOT / ".env_for_gen_report"
load_dotenv(GEN_REPORT_ENV)


# -----------------------------------------------------------------------------
# Helper utilities
# -----------------------------------------------------------------------------
def _resolve_model(model_key: Optional[str], env_var: str, model_options: List[str]) -> str:
    env_val = os.getenv(env_var)
    if model_key and model_key in model_options:
        return model_key
    if env_val and env_val in model_options:
        return env_val
    return model_options[0]


def _resolve_path(value: Optional[str], env_var: str, default_path: Path) -> Path:
    if value:
        path = Path(value).expanduser()
        if not path.is_absolute():
            path = (PROJECT_ROOT / path).resolve()
        else:
            path = path.resolve()
        return path
    env_val = os.getenv(env_var)
    if env_val:
        env_path = Path(env_val).expanduser()
        if not env_path.is_absolute():
            env_path = (PROJECT_ROOT / env_path).resolve()
        else:
            env_path = env_path.resolve()
        return env_path
    return default_path.resolve()


def _detect_em_template(workdir: Path, template_name: Optional[str] = None) -> Path:
    """Pick EM template. Priority: user workdir > built-in templates. Prefer 4au."""
    candidates = ["4au-em.xyz", "3au-em.xyz"]
    
    # If user specified a template name, look for it first
    if template_name:
        # Check workdir first
        user_path = workdir / template_name
        if user_path.exists():
            return user_path
        # Check built-in templates
        builtin_path = EM_TEMPLATES_DIR / template_name
        if builtin_path.exists():
            return builtin_path
        raise FileNotFoundError(f"Specified EM template '{template_name}' not found")
    
    # Auto-detect: check workdir first, then built-in
    for name in candidates:
        candidate = workdir / name
        if candidate.exists():
            return candidate
    
    # Fall back to built-in templates
    for name in candidates:
        candidate = EM_TEMPLATES_DIR / name
        if candidate.exists():
            return candidate
    
    raise FileNotFoundError("No EM template found (expected 4au-em.xyz or 3au-em.xyz)")


def _detect_junction_template(workdir: Path, template_name: Optional[str] = None) -> Path:
    """Pick junction template. Priority: user workdir > built-in templates."""
    # Map short names to built-in template files
    builtin_templates = {
        "pyramid": "junction_pyramid_elec.xyz",
        "trimer": "junction_trimer_elec.xyz",
        "adatom": "junction_adatom_elec.xyz",
    }
    # Also accept full filenames
    all_candidates = list(builtin_templates.values())
    
    # If user specified a template name
    if template_name:
        # Check if it's a short name
        if template_name.lower() in builtin_templates:
            template_file = builtin_templates[template_name.lower()]
            builtin_path = JUNCTION_TEMPLATES_DIR / template_file
            if builtin_path.exists():
                return builtin_path
        
        # Check workdir first for exact filename
        user_path = workdir / template_name
        if user_path.exists():
            return user_path
        # Check built-in templates
        builtin_path = JUNCTION_TEMPLATES_DIR / template_name
        if builtin_path.exists():
            return builtin_path
        raise FileNotFoundError(f"Specified junction template '{template_name}' not found")
    
    # Auto-detect: check workdir first
    for name in all_candidates:
        candidate = workdir / name
        if candidate.exists():
            return candidate
    
    # Fall back to built-in templates (prefer pyramid)
    for name in all_candidates:
        candidate = JUNCTION_TEMPLATES_DIR / name
        if candidate.exists():
            return candidate
    
    raise FileNotFoundError(
        "No junction template found. Specify one of: pyramid, trimer, adatom"
    )


def _default_bond_length(anchor_element: str) -> float:
    if anchor_element.lower() == "n":
        return 2.2
    return 2.4


# -----------------------------------------------------------------------------
# Tool implementations
# -----------------------------------------------------------------------------
def initialize_workflow() -> Dict[str, Any]:
    """Return mode guide and system prompt to switch the agent into transport mode."""
    return {
        "status": "success",
        "mode": "molecular_transport",
        "message": "The transport calculation automation workflow has been initialized. Please provide a query to generate the report.",
        "system_prompt": SYSTEM_PROMPT,
        "reference_docs": {
            "L2_build_guide": str(L2_BUILD_GUIDE),
            "L3_build_guide": str(L3_BUILD_GUIDE),
        },
    }


def generate_report(
    *,
    query: str,
    top_k: int = 3,
    parse_model: Optional[str] = None,
    gen_model: Optional[str] = None,
    output_prefix: Optional[str] = None,
    output_dir: Optional[str] = None,
    reports_dir: Optional[str] = None,
) -> Dict[str, Any]:
    """Run parse→retrieve→generate and return structured payload."""
    models = available_models()
    parse_key = _resolve_model(parse_model, "PARSE_MODEL", models)
    gen_key = _resolve_model(gen_model, "GEN_MODEL", models)

    reports_path = _resolve_path(reports_dir, "REPORTS_DIR", DEFAULT_REPORTS_DIR)
    output_path = _resolve_path(output_dir, "OUTPUT_DIR", DEFAULT_OUTPUT_DIR)
    prefix = output_prefix or os.getenv("OUTPUT_PREFIX", "test_id")

    engine = RetrievalEngine.from_directory(reports_path)
    materials = load_generation_materials(MANUAL_DIR)

    workflow_data = run_full_workflow(
        query=query,
        parse_client=build_client_from_key(parse_key),
        gen_client=build_client_from_key(gen_key),
        engine=engine,
        reports_dir=reports_path,
        output_dir=output_path,
        output_prefix=prefix,
        top_k=top_k,
        manual_dir=MANUAL_DIR,
        materials=materials,
    )
    return workflow_data.to_response()


def _parse_tilt_params(spec: Mapping[str, Any]) -> Optional[Dict[str, Any]]:
    """Parse tilt/incline parameters from job spec.

    Supported keys:
        - tilt_angle (float): rotation angle in degrees (positive value)
        - tilt_axis (str): "x" or "y" (default: "x")
        - tilt_direction (str): "clockwise"/"cw" or "counterclockwise"/"ccw" (default: "counterclockwise")
        - tilt_bond_R (float, optional): desired right Au-X bond length after tilt

    Returns:
        Dict with parsed params or None if no tilt requested.
    """
    tilt_angle = spec.get("tilt_angle")
    if tilt_angle is None:
        return None

    angle = float(tilt_angle)
    axis_str = str(spec.get("tilt_axis", "x")).lower()
    direction = str(spec.get("tilt_direction", "counterclockwise")).lower()

    # Map axis string to vector
    if axis_str == "x":
        rotation_axis = (1.0, 0.0, 0.0)
    elif axis_str == "y":
        rotation_axis = (0.0, 1.0, 0.0)
    else:
        raise ValueError(f"Unsupported tilt_axis: {axis_str}. Use 'x' or 'y'.")

    # Handle rotation direction (right-hand rule: positive = counterclockwise when looking from axis positive direction)
    if direction in ("clockwise", "cw"):
        angle = -angle
    elif direction not in ("counterclockwise", "ccw"):
        raise ValueError(f"Unsupported tilt_direction: {direction}. Use 'clockwise'/'cw' or 'counterclockwise'/'ccw'.")

    return {
        "angle_degrees": angle,
        "rotation_axis": rotation_axis,
        "bond_R": spec.get("tilt_bond_R"),
    }


def build_structures(
    *,
    level: str,
    jobs: Mapping[str, Mapping[str, Any]],
    workdir: Optional[str] = None,
) -> Dict[str, Any]:
    """Build structures for L1/L2/L3.

    Args:
        level: "L1" | "L2" | "L3"
        jobs: mapping of system_name -> spec dict. Required keys per level:
            - molecule: path to input xyz (required all levels)
            - anchors: [left_idx, right_idx] (1-based, required for L2/L3)
            - template: optional path; if absent, auto-detect in workdir
            - bond_L / bond_R: optional; defaults by anchor element (N=2.2, else 2.4)
            - tilt_angle (float, optional, L2 only): rotation angle in degrees for inclined EM
            - tilt_axis (str, optional): "x" or "y", default "x"
            - tilt_direction (str, optional): "clockwise"/"cw" or "counterclockwise"/"ccw", default "counterclockwise"
            - tilt_bond_R (float, optional): right Au-X bond length after tilt
        workdir: base directory to place outputs; defaults to cwd.
    Returns:
        dict with per-system outputs and any errors encountered.
    """
    level_up = level.upper()
    base_dir = Path(workdir or Path.cwd()).resolve()
    results: Dict[str, Any] = {"level": level_up, "systems": {}}

    for name, spec in jobs.items():
        try:
            molecule_path = Path(spec["molecule"]).expanduser().resolve()
            anchors = spec.get("anchors")
            template = spec.get("template")
            bond_L = spec.get("bond_L")
            bond_R = spec.get("bond_R")

            system_dir = base_dir / name
            system_dir.mkdir(parents=True, exist_ok=True)

            molecule_copy = system_dir / molecule_path.name
            shutil.copyfile(molecule_path, molecule_copy)

            if level_up == "L1":
                results["systems"][name] = {
                    "status": "success",
                    "message": "L1 does not require generating EM/Junction; it directly uses the molecule XYZ file.",
                    "molecule": str(molecule_copy),
                }
                continue

            if not anchors or len(anchors) != 2:
                raise ValueError("anchors (left_idx, right_idx) are required for L2/L3")
            left_idx = int(anchors[0]) - 1
            right_idx = int(anchors[1]) - 1

            if level_up == "L2":
                template_path = _detect_em_template(base_dir, template)
                template_copy = system_dir / template_path.name
                if template_path != template_copy:
                    shutil.copyfile(template_path, template_copy)

                # Default bond lengths if missing
                if bond_L is None or bond_R is None:
                    # Try to infer from anchor elements
                    atoms, _ = em_builder._read_xyz(molecule_copy)  # type: ignore[attr-defined]
                    anchor_L_element = atoms[left_idx]["element"]
                    anchor_R_element = atoms[right_idx]["element"]
                    bond_L = bond_L if bond_L is not None else _default_bond_length(anchor_L_element)
                    bond_R = bond_R if bond_R is not None else _default_bond_length(anchor_R_element)

                aligned_path = em_builder.align_molecule_to_z_axis(
                    molecule_copy,
                    left_anchor_idx=left_idx,
                    right_anchor_idx=right_idx,
                )
                em_path = em_builder.assemble_em(
                    aligned_path,
                    template_copy,
                    float(bond_L),
                    float(bond_R),
                    left_anchor_idx=left_idx,
                    right_anchor_idx=right_idx,
                )
                is_valid, error_msg = em_builder.validate_em_structure(em_path, template_copy)
                if not is_valid:
                    raise ValueError(f"EM validation failed: {error_msg}")

                # Optional: Apply tilt/incline if requested
                tilt_params = _parse_tilt_params(spec)
                tilt_info: Optional[Dict[str, Any]] = None
                if tilt_params is not None:
                    inclined_path = em_builder.incline_em(
                        em_path,
                        template_copy,
                        left_anchor_idx=left_idx,
                        right_anchor_idx=right_idx,
                        angle_degrees=tilt_params["angle_degrees"],
                        rotation_axis=tilt_params["rotation_axis"],
                        bond_R=tilt_params["bond_R"],
                    )
                    # Remove non-inclined EM, use inclined version
                    Path(em_path).unlink(missing_ok=True)
                    em_path = inclined_path
                    tilt_info = {
                        "angle_degrees": abs(tilt_params["angle_degrees"]),
                        "axis": "x" if tilt_params["rotation_axis"] == (1.0, 0.0, 0.0) else "y",
                        "direction": "counterclockwise" if tilt_params["angle_degrees"] >= 0 else "clockwise",
                    }

                final_path = system_dir / f"em_{molecule_path.stem}.xyz"
                shutil.move(em_path, final_path)
                Path(aligned_path).unlink(missing_ok=True)
                result_entry: Dict[str, Any] = {
                    "status": "success",
                    "output": str(final_path),
                    "template": str(template_copy),
                    "bond_L": float(bond_L),
                    "bond_R": float(bond_R),
                }
                if tilt_info:
                    result_entry["tilt"] = tilt_info
                results["systems"][name] = result_entry

            elif level_up == "L3":
                template_path = _detect_junction_template(base_dir, template)
                template_copy = system_dir / template_path.name
                if template_path != template_copy:
                    shutil.copyfile(template_path, template_copy)

                if bond_L is None or bond_R is None:
                    atoms, _ = junction_builder._read_xyz(molecule_copy)  # type: ignore[attr-defined]
                    anchor_L_element = atoms[left_idx]["element"]
                    anchor_R_element = atoms[right_idx]["element"]
                    bond_L = bond_L if bond_L is not None else _default_bond_length(anchor_L_element)
                    bond_R = bond_R if bond_R is not None else _default_bond_length(anchor_R_element)

                aligned_path = junction_builder.align_molecule_to_z_axis(
                    molecule_copy, left_anchor_idx=left_idx, right_anchor_idx=right_idx
                )
                junction_path = junction_builder.assemble_junction(
                    aligned_path,
                    template_copy,
                    float(bond_L),
                    float(bond_R),
                    left_anchor_idx=left_idx,
                    right_anchor_idx=right_idx,
                )
                is_valid, error_msg = junction_builder.validate_junction_structure(junction_path, template_copy)
                if not is_valid:
                    raise ValueError(f"Junction validation failed: {error_msg}")
                final_path = system_dir / f"junction_{molecule_path.stem}.xyz"
                shutil.move(junction_path, final_path)
                Path(aligned_path).unlink(missing_ok=True)
                em_length = junction_builder.compute_em_z_length(
                    final_path, template_copy, left_anchor_idx=left_idx, right_anchor_idx=right_idx
                )
                results["systems"][name] = {
                    "status": "success",
                    "output": str(final_path),
                    "template": str(template_copy),
                    "bond_L": float(bond_L),
                    "bond_R": float(bond_R),
                    "em_z_length": em_length,
                }
            else:
                raise ValueError(f"Unsupported level: {level}")
        except Exception as exc:  # catch per system and continue others
            results["systems"][name] = {"status": "error", "message": str(exc)}
    return results
