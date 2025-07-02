# Sequential Thinking MCP

[![uv](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json)](https://docs.astral.sh/uv/getting-started/installation/)
[![Python](https://img.shields.io/badge/python-3.10%2B-blue)](https://www.python.org/downloads/)
[![PyPI](https://badge.fury.io/py/sequential-thinking-mcp.svg?cache-control=no-cache)](https://badge.fury.io/py/sequential-thinking-mcp)
[![Actions status](https://github.com/philogicae/sequential-thinking-mcp/actions/workflows/python-package-ci.yml/badge.svg?cache-control=no-cache)](https://github.com/philogicae/sequential-thinking-mcp/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Ask DeepWiki](https://deepwiki.com/badge.svg)](https://deepwiki.com/philogicae/sequential-thinking-mcp)

This repository provides an MCP (Model Context Protocol) server that enables an AI agent to perform advanced meta-cognition and dynamic, reflective problem-solving.

This version of Sequential Thinking is quite different than the original one, as it only forces the agent to virtually log its thoughts and plans, without actually doing anything, except prompting itself. I found it to be sufficient enough for any kind of LLMs.

<a href="https://glama.ai/mcp/servers/@philogicae/sequential-thinking-mcp">
  <img width="380" height="200" src="https://glama.ai/mcp/servers/@philogicae/sequential-thinking-mcp/badge?cache-control=no-cache" alt="Sequential Thinking MCP" />
</a>

## Table of Contents

- [Features](#features)
- [Setup](#setup)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
    - [Install from PyPI (Recommended)](#install-from-pypi-recommended)
    - [For Local Development](#for-local-development)
    - [For Docker](#for-docker)
- [Usage](#usage)
  - [As MCP Server](#as-mcp-server)
  - [Via MCP Clients](#via-mcp-clients)
    - [Example with Windsurf](#example-with-windsurf)
- [Contributing](#contributing)
- [Changelog](#changelog)
- [License](#license)

## Features

-   **Advanced Meta-Cognition**: Provides a `think` tool for dynamic and reflective problem-solving through thought logging.
-   **Agentic Workflow Orchestration**: Guides AI agents through complex tasks by breaking them into precise, manageable, and traceable steps.
-   **Iterative Refinement**: Assesses the success of each step and self-corrects if necessary, adapting to new information or errors.
-   **Proactive Planning**: Utilizes `left_to_be_done` for explicit future state management and task estimation.
-   **Tool Recommendation**: Suggests specific tools via `tool_recommendation` to execute planned actions or gather necessary information.

## Setup

### Prerequisites

-   Python 3.10+
-   [`uv`](https://github.com/astral-sh/uv) (for local development)

### Installation

Choose one of the following installation methods.

#### Install from PyPI (Recommended)

This method is best for using the package as a library or running the server without modifying the code.

1.  Install the package from PyPI:
```bash
pip install sequential-thinking-mcp
```
2.  Run the MCP server (default: stdio):
```bash
python -m sequential_thinking
```

#### For Local Development

This method is for contributors who want to modify the source code.
Using [`uv`](https://github.com/astral-sh/uv):

1.  Clone the repository:
```bash
git clone https://github.com/philogicae/sequential-thinking-mcp.git
cd sequential-thinking-mcp
```
2.  Install dependencies using `uv`:
```bash
uv sync --locked
```
3.  Run the MCP server (default: stdio):
```bash
uv run -m sequential_thinking
```

#### For Docker

1.  Clone the repository (if you haven't already):
```bash
git clone https://github.com/philogicae/sequential-thinking-mcp.git
cd sequential-thinking-mcp
```
2.  Build and run the container using Docker Compose (default port: 8000):
```bash
docker compose up --build -d
```
3.  Access container logs:
```bash
docker logs sequential-thinking-mcp -f
```

## Usage

### As MCP Server

```python
from sequential_thinking import mcp

mcp.run(transport="sse")
```

### Via MCP Clients

Usable with any MCP-compatible client. Available tools:

-   `think`: Log a thought, plan next steps, and recommend tools.

#### Example with Windsurf
Configuration:
```json
{
  "mcpServers": {
    ...
    # with stdio (only requires uv)
    "sequential-thinking-mcp": {
      "command": "uvx",
      "args": [ "sequential-thinking-mcp" ]
    },
    # with sse transport (requires installation)
    "sequential-thinking-mcp": {
      "serverUrl": "http://127.0.0.1:8000/sse"
    },
    # with streamable-http transport (requires installation)
    "sequential-thinking-mcp": {
      "serverUrl": "http://127.0.0.1:8000/mcp" # not yet supported by every client
    },
    ...
  }
}
```

## Changelog

See [CHANGELOG.md](CHANGELOG.md) for a history of changes to this project.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.