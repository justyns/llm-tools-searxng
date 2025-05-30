import llm
import json
from llm_tools_searxng import searxng


def test_tool():
    model = llm.get_model("echo")
    chain_response = model.chain(
        json.dumps(
            {
                "tool_calls": [
                    {"name": "searxng", "arguments": {"input": "pelican"}}
                ]
            }
        ),
        tools=[searxng],
    )
    responses = list(chain_response.responses())
    tool_results = json.loads(responses[-1].text())["tool_results"]
    assert tool_results == [
        {"name": "searxng", "output": "hello pelican", "tool_call_id": None}
    ]
