# MolTransService

`MolTransService` is an MCP service for molecular junction transport workflows. It exposes a set of tools that let an agent such as Codex:

- turn a natural-language research question into a structured `MolSimTransport` transport protocol,
- build extended-molecule (EM) structures,
- build full-junction structures,
- and then execute the downstream shell workflow if `MolSimTransport` and the required external binaries are installed.

## Recommended Environment

We recommend using this project in WSL on Windows or on a Linux system, because `MolSimTransport` needs to run in a Linux environment.

## Available MCP Tools

The MCP server exposes three tools:

1. `initialize_transport_workflow`
   Returns the transport-assistant system prompt and reference document paths. Call this first.

2. `protocol_generator`
   Parses a research query, retrieves similar reports from the local report database, and generates a transport calculation protocol.

3. `structure_builder`
   Builds L2/L3 input structures from user-provided molecule files and parameters.

The server runs as a streamable HTTP MCP endpoint at:

```text
http://127.0.0.1:9000/mcp
```

## Prerequisites

Before using this project, please install the following prerequisites.

### 1. MolSimTransport

Install `MolSimTransport` first. This project relies on `MolSimTransport` for molecular transport workflow execution.

For installation details, please refer to:

```text
https://github.com/yuxi-TJU/MolSimTransport
```

### 2. DFTB+
We recommend installing DFTB+ with conda:

```bash
conda install -c conda-forge "dftbplus=24.1=nompi_h5d91ca9_100"
```

For more installation options, please refer to the official DFTB+ download page:

```text
https://dftbplus.org/download/stable.html
```

### 3. Codex

`Codex` is used as the general-purpose AI agent in this workflow. It is responsible for file operations, workflow management, and connecting to the MCP server provided by this project.

Other coding agents, such as `Claude Code` or `Gemini-cli`, can play a similar role. The main difference is how each agent connects to and manages MCP servers.

For Codex installation and usage, please refer to the official documentation:

```text
https://developers.openai.com/codex/cli
```

*Note: To use Codex, you need either a ChatGPT plan that includes Codex access, such as Plus, Pro, or an OpenAI API key.
























