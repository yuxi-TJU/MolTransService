# MolTransService

`MolTransService` is an MCP service for molecular junction transport workflows. It exposes a small set of tools that let an agent such as Codex:

- turn a natural-language research question into a structured MST transport report,
- build L2 extended-molecule (EM) structures,
- build L3 full-junction structures,
- and then execute the downstream shell workflow if `MolSimTransport` and the required external binaries are installed.

The service is built for molecular transport work, not as a general chemistry toolkit.

## Recommended Environment

Use Linux or WSL2 if possible.

This project is much easier to run in Linux/WSL because:

- `MolSimTransport` workflows are shell-heavy,
- `DFTB+` integration is primarily relevant for Linux-style environments,
- path handling is simpler when Codex, the MCP server, and MST commands all run in the same environment,
- SSH, Python, and CLI automation are usually less fragile than mixed Windows/WSL setups.

Pure Windows is possible for some parts of the workflow, but Linux or WSL is the recommended setup.

## What This MCP Exposes

The MCP server exposes three tools:

1. `initialize_transport_workflow`
   Returns the transport-assistant system prompt and reference document paths. Call this first.

2. `report_generator`
   Parses a research query, retrieves similar reports from the local report database, and generates a transport calculation report.

3. `structure_builder`
   Builds L1/L2/L3 input structures from user-provided molecule files and parameters.

The server runs as a streamable HTTP MCP endpoint at:

```text
http://127.0.0.1:9000/mcp
```

## External Prerequisites

Before using the full workflow, install the following external software yourself.

### 1. MolSimTransport

Install `MolSimTransport` first if you want to execute the generated workflow, not just generate reports.

For installation details, refer directly to the official repository:

```text
https://github.com/yuxi-TJU/MolSimTransport
```

If you only want to use `report_generator`, MST is not required.

### 2. DFTB+

Install `DFTB+` if you plan to run L3 workflows.

`DFTB+` is the external electronic-structure backend used by the L3 workflow described in the MST manual. In practice:

- L1 and L2 report generation / structure building do not require `DFTB+`,
- L3 execution does require `DFTB+`,
- if you want end-to-end execution from Codex, it is safest to install `DFTB+` up front.

Make sure `dftb+` is callable from the shell:

```bash
dftb+ --version
```

### 3. OpenAI-Compatible LLM API Access

The report-generation pipeline calls an OpenAI-compatible chat completions endpoint. You need:

- an API key,
- an API URL,
- and a model name supported by this repository's model registry.

## Python Setup

### 1. Create and activate an environment

Example with `venv`:

```bash
python -m venv .venv
source .venv/bin/activate
```

### 2. Install Python dependencies

```bash
pip install -r requirements.txt
```

If `rdkit` fails to install from `pip` on your system, install it separately with your preferred package manager, then rerun the remaining dependencies.

## LLM Configuration

This repository loads report-generation settings from a local file named `.env_for_gen_report`.

Create it by copying the template:

```bash
cp .env.example .env_for_gen_report
```

Then edit `.env_for_gen_report` and set at least:

```env
LLM_API_KEY=your-real-api-key
LLM_API_URL=https://api.openai.com/v1/chat/completions
PARSE_MODEL=gpt5-nano
GEN_MODEL=gpt5-nano
```

Notes:

- `.env_for_gen_report` is intended to stay local and should not be committed.
- The code loads `.env_for_gen_report` automatically.
- `LLM_API_URL` can point to any OpenAI-compatible endpoint.

## Start the MCP Server

From the repository root:

```bash
python mcp_server.py
```

By default this starts a streamable HTTP MCP server on:

```text
127.0.0.1:9000/mcp
```

Keep this process running while Codex uses the service.

## Configure Codex

The simplest way to register this MCP server in Codex is via the `codex mcp add` command.

### 1. Add the server

```bash
codex mcp add mol_trans_service --url http://127.0.0.1:9000/mcp
```

### 2. Verify that Codex can see it

```bash
codex mcp list
```

If needed, inspect the registered entry:

```bash
codex mcp get mol_trans_service
```

If you change the server URL later, remove and re-add it:

```bash
codex mcp remove mol_trans_service
codex mcp add mol_trans_service --url http://127.0.0.1:9000/mcp
```

### Important recommendation

Run both Codex and `mcp_server.py` in the same Linux/WSL environment whenever possible.

That avoids:

- Windows vs. WSL path mismatches,
- shell-command differences,
- SSH credential confusion,
- and localhost/network forwarding issues.

## Basic Usage Pattern in Codex

Once the MCP server is registered, a typical session is:

1. Start `mcp_server.py`.
2. Open Codex in the same project/workspace.
3. Ask Codex to call `initialize_transport_workflow` first.
4. Ask Codex to generate a report for your transport question.
5. Provide molecule `.xyz` files and anchor indices if L2/L3 structure building is needed.
6. Let Codex call `structure_builder`.
7. If MST and `DFTB+` are installed, let Codex execute the shell workflow from the generated report.

Example prompts:

```text
Call initialize_transport_workflow first, then generate a transport report for a pyridine-anchored molecular junction on Au electrodes.
```

```text
Use structure_builder at L2. My molecule file is /absolute/path/molecule.xyz, anchors are [1, 12], and workdir is /absolute/path/run_dir.
```

## Important Input Rules

### `structure_builder` requires absolute paths

When calling `structure_builder`:

- `workdir` must be an absolute path,
- the input molecule path should also be absolute,
- anchors for L2/L3 are 1-based atom indices in the user-facing API.

### Report generation and execution are separate concerns

The repository can do several different things:

- report generation only,
- structure building only,
- or full end-to-end execution.

You do not need MST or `DFTB+` just to generate a report.
You do need the external executables if you expect Codex to run the computational workflow itself.

## Direct Local Testing Without Codex

You can test report generation directly from the command line:

```bash
python -m mol_trans_service.report_generator.gen_report_cli \
  --query "Study the conductance trend of pyridine-anchored molecular junctions on Au electrodes" \
  --reports-dir mol_trans_service/report_generator/report_database \
  --output-dir ./generated_outputs
```

You can also start the MCP server and connect another compatible MCP client to:

```text
http://127.0.0.1:9000/mcp
```

## Repository Notes

- The main MCP entrypoint is [mcp_server.py](mcp_server.py).
- The tool orchestration layer is [mol_trans_service/main.py](mol_trans_service/main.py).
- The report-generation core lives in [mol_trans_service/report_generator/](mol_trans_service/report_generator).
- The structure builders live in [mol_trans_service/structure_builder/](mol_trans_service/structure_builder).
- The MST reference manual used by the generator is [mol_trans_service/report_generator/manual/MST_Manual.md](mol_trans_service/report_generator/manual/MST_Manual.md).

## Common Pitfalls

- Forgetting to create `.env_for_gen_report`
- Running Codex on Windows while the MCP server and files live in WSL
- Trying to execute L3 workflows without `DFTB+`
- Providing relative paths to `structure_builder`
- Expecting this repository to install `MolSimTransport` for you

## Summary

If you want the shortest working path:

1. Use Linux or WSL2.
2. Install `MolSimTransport`.
3. Install `DFTB+` if you will run L3 or complete end-to-end workflows.
4. Install Python dependencies with `pip install -r requirements.txt`.
5. Create `.env_for_gen_report` from `.env.example`.
6. Start the server with `python mcp_server.py`.
7. Register it in Codex with:

```bash
codex mcp add mol_trans_service --url http://127.0.0.1:9000/mcp
```

8. In Codex, call `initialize_transport_workflow` first.
