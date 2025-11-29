# MolTransService

An MCP service for molecular junction transport calculations. It transforms general-purpose AI agents (Codex, Gemini-CLI, etc.) into specialized molecular transport calculation assistants.

## Features

- **Report Generation** - Generate structured calculation reports from natural language queries (L1/L2/L3 levels)
- **Structure Building** - Automatically build Extended Molecule (EM) and Full Junction structures
- **Workflow Automation** - AI agents execute computation tasks following the generated report

## Project Structure

```
mol_trans_service/
├── mcp_server.py              # MCP server entry (port 9000)
├── server.py                  # REST API server (optional)
├── .env                       # Environment variables
│
└── mol_trans_service/
    ├── main.py                # Core tool implementations
    ├── prompts/
    │   └── system_prompt.md   # AI agent system prompt
    │
    ├── report_generator/      # Report generation module
    │   ├── core/              # LLM client, query parsing, workflow
    │   ├── retrieval/         # Multi-channel retrieval engine
    │   ├── manual/            # Generation guide documents
    │   └── report_database/   # Report corpus
    │
    └── structure_builder/     # Structure building module
        ├── build_mst_em_functions.py       # L2 EM builder
        ├── build_mst_junction_function.py  # L3 Junction builder
        └── templates/                      # Built-in template files
```

## Requirements

Install dependencies:

```bash
pip install -r requirements.txt
```

## Configuration

Edit `.env.example`:

```env
LLM_PROVIDER=openai
LLM_MODEL=gpt5-nano
LLM_API_KEY=your-api-key-here
LLM_API_URL=https://api.openai.com/v1/chat/completions
```

*The model configuration here is only used for generating computational reports.*

## Usage

### 1. Start MCP Server

```bash
python mcp_server.py
```

Server runs at `http://127.0.0.1:9000/mcp`.

### 2. Configure AI Agent

Add MCP server config to your AI tool (e.g., OPENAI Codex):

```
experimental_use_rmcp_client = true
[mcp_servers.mol_trans_service]
url = "http://127.0.0.1:9000/mcp"
```

### 3. Available Tools

| Tool | Description |
|------|-------------|
| `initialize_transport_workflow` | Initialize workflow, switch to transport mode |
| `report_generator` | Generate calculation report from natural language query |
| `structure_builder` | Build L2/L3 calculation structures |

### 4. Typical Workflow

1. Call `initialize_transport_workflow` to enter transport calculation assistant mode
2. Submit a natural language query (e.g., "Study the conductance of benzenedithiol")
3. `report_generator` produces a calculation report
4. User reviews the report and provides molecule structure files
5. `structure_builder` builds EM/Junction structures automatically
6. AI agent executes the computational workflow from the report

## Calculation Levels

| Level | Description | Structure |
|-------|-------------|-----------|
| L1 | Molecule only | Molecule XYZ file |
| L2 | Extended Molecule | Molecule + small Au clusters (4Au pyramid or 3Au trimer) |
| L3 | Full Junction | Complete junction system with electrode layers |

## Built-in Templates

The service includes all required template files. Users only need to provide the target molecule.

**L2 EM Templates:**
- `4au-em.xyz` - Pyramid type (default)
- `3au-em.xyz` - Trimer type

**L3 Junction Templates:**
- `junction_pyramid_elec.xyz` - Pyramid type (default)
- `junction_trimer_elec.xyz` - Trimer type
- `junction_adatom_elec.xyz` - Adatom type

**Example of constructing a structure**:

- Connect atoms 1 and 2 of the molecule @pyridine.xyz to the left and right clusters to construct the EM system, with a bond length of 2.100 Å.
- Connect atoms 2 and 3 of the molecule @S.xyz to the trimer configuration of the electrode to construct the junction system.


## Note

In order for the AI agent to automatically execute the computational workflow described in the report, you need to install `MolSimTransport` on your Linux system.

