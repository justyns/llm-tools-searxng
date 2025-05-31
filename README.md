# llm-tools-searxng

[PyPI](https://img.shields.io/pypi/v/llm-tools-searxng.svg)](https://pypi.org/project/llm-tools-searxng/)
[![Changelog](https://img.shields.io/github/v/release/justyns/llm-tools-searxng?include_prereleases&label=changelog)](https://github.com/justyns/llm-tools-searxng/releases)
[![Tests](https://github.com/justyns/llm-tools-searxng/actions/workflows/test.yml/badge.svg)](https://github.com/justyns/llm-tools-searxng/actions/workflows/test.yml)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/justyns/llm-tools-searxng/blob/main/LICENSE)

A tool to search the web using SearXNG search engines.

## Installation

Install this plugin in the same environment as [LLM](https://llm.datasette.io/).
```bash
llm install llm-tools-searxng
```

## Configuration

By default, the tool does not have a default SEARXNG_URL set, you must set this environment variable to a searxng instance you have access to:

```bash
export SEARXNG_URL=https://your-searxng-instance.com
export SEARXNG_METHOD=GET  # or POST (default)
```

**Note:** Public SearXNG instances typically don't allow API access or JSON output.

## Usage

### Simple search function

Use the `searxng_search` function for basic web searches:

```bash
llm --tool searxng_search "latest developments in AI" --tools-debug
```

### With LLM chat

This plugin works well with `llm chat`:

```bash
llm chat --tool searxng_search --tools-debug
```

### Python API usage

```python
import llm
from llm_tools_searxng import SearXNG, searxng_search

# Using the simple function
model = llm.get_model("gpt-4.1-mini")
result = model.chain(
    "What are the latest developments in renewable energy?",
    tools=[searxng_search]
).text()
```

## Development

To set up this plugin locally, first checkout the code. Then create a new virtual environment:

```bash
cd llm-tools-searxng
uv sync --all-extras
```

Now install the dependencies and test dependencies:

```bash
llm install -e '.[test]'
```

To run the tests:

```bash
uv run python -m pytest
```
