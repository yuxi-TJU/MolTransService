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

## Prerequisites

Before using this project, please install the following prerequisites.

### 1. MolSimTransport

This project relies on `MolSimTransport` for molecular transport workflow execution.

For installation details, please refer to the [MolSimTransport repository](https://github.com/yuxi-TJU/MolSimTransport).

### 2. DFTB+
`DFTB+` is the external electronic-structure backend used by the L3 workflow. We recommend installing DFTB+ with conda:

```bash
conda install -c conda-forge "dftbplus=24.1=nompi_h5d91ca9_100"
```

For more installation options, please refer to the official [DFTB+ download page](https://dftbplus.org/download/stable.html).


### 3. Codex

`Codex` is used as the general-purpose AI agent in this workflow. It is responsible for file operations, workflow management, and connecting to the MCP server provided by this project.

Other coding agents, such as `Claude Code` or `Gemini-cli`, can play a similar role. The main difference is how each agent connects to and manages MCP servers.

For Codex installation and usage, please refer to the official [Codex CLI documentation](https://developers.openai.com/codex/cli).

*Note: To use Codex, you need either a ChatGPT plan that includes Codex access, such as Plus, Pro, or an OpenAI API key.*

## How to use

### 1. Install Python Dependencies

First, install the required Python dependencies from `requirements.txt`.

```bash
pip install -r requirements.txt
````

### 2. Configure Codex to Connect to the MCP Server

Configure Codex by editing its `config.toml` file. This file is usually located in the `.codex` directory under your user home directory, for example:

```text
/home/base/.codex/config.toml
```
*Note: `base` is your environment name*

Add the following content to `config.toml`:

```TOML
[mcp_servers.mol_trans_service]
url = "http://127.0.0.1:9000/mcp"
tool_timeout_sec = 300
```

After this configuration, Codex will be able to connect to the MCP service provided by this project.


### 3. Configure the Protocol Generation API

The protocol generation module requires an OpenAI-compatible LLM API.

Copy the example environment file:

```bash
cp .env.example .env_for_gen_report
```

Then edit `.env_for_gen_report` and configure the required API information, including:

* LLM API key
* LLM API URL
* model name (for both query parsing and protocol generation; usually set to the same model)

Example:

```env
LLM_API_KEY=your_api_key_here
LLM_API_URL=your_api_url_here
PARSE_MODEL=your_model_name_here
GEN_MODEL=your_model_name_here
```

### 4. Start Codex and Check MCP Loading

Run Codex in the project workspace:

```bash
codex --yolo
```

After Codex starts, check whether the MCP service has been loaded correctly:

```text
/mcp
```

You should see the registered MCP service for this project in the MCP list.

### 5. Interact with Codex

After confirming that the MCP service is available, you can start interacting with Codex in natural language.

First, ask Codex to enter the molecular transport calculation assistant mode. For example:

```text
Enter the molecular transport calculation assistant mode.
```

After initialization, you can ask Codex to perform different tasks, such as:

- generating a transport calculation protocol from a research query;
- building L2 or L3 molecular junction structures;
- executing the workflow described in a generated protocol;
- asking Codex for general assistance during the workflow, such as generating geometry-processing or plotting scripts, helping analyze calculation results, and providing suggestions for the next steps.

Example prompts:

```text
Generate a molecular transport calculation protocol for the following research query: ...
```

```text
Build an L2 structure using the molecule file ... with anchor atoms ...
```

```text
Follow the generated protocol and execute the molecular transport workflow step by step.
```










