"""FastAPI server exposing Molecular Transport MCP tools."""

from __future__ import annotations

from typing import Dict

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from mol_trans_service.main import build_structures, generate_report, initialize_workflow


class ReportRequest(BaseModel):
    query: str
    top_k: int | None = 3
    parse_model: str | None = None
    gen_model: str | None = None
    output_prefix: str | None = None
    output_dir: str | None = None
    reports_dir: str | None = None


class BuildJob(BaseModel):
    molecule: str
    anchors: list[int] | None = None
    template: str | None = None
    bond_L: float | None = None
    bond_R: float | None = None


class BuildRequest(BaseModel):
    level: str
    jobs: Dict[str, BuildJob]
    workdir: str | None = None


app = FastAPI(title="Molecular Transport MCP Service")


@app.get("/health")
def health() -> Dict[str, str]:
    return {"status": "ok"}


@app.post("/initialize_workflow")
def api_initialize() -> Dict[str, object]:
    return initialize_workflow()


@app.post("/generate_report")
def api_generate_report(payload: ReportRequest) -> Dict[str, object]:
    try:
        return generate_report(**payload.dict(exclude_none=True))
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.post("/build_structures")
def api_build_structures(payload: BuildRequest) -> Dict[str, object]:
    jobs = {name: job.dict(exclude_none=True) for name, job in payload.jobs.items()}
    try:
        return build_structures(level=payload.level, jobs=jobs, workdir=payload.workdir)
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


# ---------------------------------------------------------------------------
# Minimal MCP-style JSON-RPC bridge on /mcp (for rmcp clients)
# ---------------------------------------------------------------------------
TOOLS = [
    {
        "name": "initialize_workflow",
        "description": "Initialize the molecular transport workflow and return the mode guide.",
        "inputSchema": {"type": "object", "properties": {}, "required": []},
    },
    {
        "name": "generate_report",
        "description": "Generate a structured transport report from a natural-language query.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "query": {"type": "string"},
                "top_k": {"type": "integer"},
                "parse_model": {"type": ["string", "null"]},
                "gen_model": {"type": ["string", "null"]},
                "output_prefix": {"type": ["string", "null"]},
                "output_dir": {"type": ["string", "null"]},
                "reports_dir": {"type": ["string", "null"]},
            },
            "required": ["query"],
        },
    },
    {
        "name": "build_structures",
        "description": "Build L1/L2/L3 structures (L2 EM, L3 junction first step) from molecule files and anchors.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "level": {"type": "string", "enum": ["L1", "L2", "L3"]},
                "workdir": {"type": ["string", "null"]},
                "jobs": {
                    "type": "object",
                    "additionalProperties": {
                        "type": "object",
                        "properties": {
                            "molecule": {"type": "string"},
                            "anchors": {"type": ["array", "null"], "items": {"type": "integer"}},
                            "template": {"type": ["string", "null"]},
                            "bond_L": {"type": ["number", "null"]},
                            "bond_R": {"type": ["number", "null"]},
                        },
                        "required": ["molecule"],
                    },
                },
            },
            "required": ["level", "jobs"],
        },
    },
]


def _rpc_error(id_value, code: int, message: str):
    return {"jsonrpc": "2.0", "id": id_value, "error": {"code": code, "message": message}}


@app.post("/mcp")
async def mcp_bridge(payload: dict):
    method = payload.get("method")
    req_id = payload.get("id")
    params = payload.get("params", {}) or {}

    try:
        if method == "initialize":
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {
                    "protocolVersion": "2024-11-05",
                    "capabilities": {"tools": {}},
                    "serverInfo": {"name": "mol_trans_service", "version": "0.1.0"},
                },
            }
        if method in ("tools/list", "list_tools"):
            return {"jsonrpc": "2.0", "id": req_id, "result": {"tools": TOOLS}}
        if method in ("tools/call", "call_tool"):
            name = params.get("name")
            arguments = params.get("arguments", {}) or {}
            if name == "initialize_workflow":
                result = initialize_workflow()
            elif name == "generate_report":
                result = generate_report(**arguments)
            elif name == "build_structures":
                result = build_structures(**arguments)
            else:
                return _rpc_error(req_id, -32601, f"Unknown tool: {name}")
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {
                    "content": [{"type": "text", "text": str(result)}],
                }
            }
        return _rpc_error(req_id, -32601, f"Unknown method: {method}")
    except Exception as exc:
        return _rpc_error(req_id, -32000, f"{type(exc).__name__}: {exc}")
