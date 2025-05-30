# llm-tools-searxng

[![PyPI](https://img.shields.io/pypi/v/llm-tools-searxng.svg)](https://pypi.org/project/llm-tools-searxng/)
[![Changelog](https://img.shields.io/github/v/release/justyns/llm-tools-searxng?include_prereleases&label=changelog)](https://github.com/justyns/llm-tools-searxng/releases)
[![Tests](https://github.com/justyns/llm-tools-searxng/actions/workflows/test.yml/badge.svg)](https://github.com/justyns/llm-tools-searxng/actions/workflows/test.yml)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/justyns/llm-tools-searxng/blob/main/LICENSE)

A tool to search the web using SearXNG.

## Installation

Install this plugin in the same environment as [LLM](https://llm.datasette.io/).
```bash
llm install llm-tools-searxng
```
## Usage

To use this with the [LLM command-line tool](https://llm.datasette.io/en/stable/usage.html):

```bash
llm --tool searxng "Example prompt goes here" --tools-debug
```

With the [LLM Python API](https://llm.datasette.io/en/stable/python-api.html):

```python
import llm
from llm_tools_searxng import searxng

model = llm.get_model("gpt-4.1-mini")

result = model.chain(
    "Example prompt goes here",
    tools=[searxng]
).text()
```

## Development

To set up this plugin locally, first checkout the code. Then create a new virtual environment:
```bash
cd llm-tools-searxng
python -m venv venv
source venv/bin/activate
```
Now install the dependencies and test dependencies:
```bash
llm install -e '.[test]'
```
To run the tests:
```bash
python -m pytest
```
