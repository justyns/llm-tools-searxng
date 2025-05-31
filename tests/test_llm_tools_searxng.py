import json

import llm

from llm_tools_searxng import SearXNG, searxng_search


def test_searxng_search_function_get(httpx_mock, monkeypatch):
    """Test the simple searxng_search function with GET method"""
    # Set required environment variable and explicitly set GET method
    monkeypatch.setenv("SEARXNG_URL", "https://searx.be")
    monkeypatch.setenv("SEARXNG_METHOD", "GET")

    # Mock the HTTP response
    mock_response = {
        "query": "test query",
        "results": [
            {
                "title": "Test Result",
                "url": "https://example.com",
                "content": "This is a test result",
                "engine": "duckduckgo",
            }
        ],
    }
    httpx_mock.add_response(
        url="https://searx.be/search?q=test+query&format=json&language=en&pageno=1&safesearch=1",
        json=mock_response,
        method="GET",
    )

    model = llm.get_model("echo")
    chain_response = model.chain(
        json.dumps({"tool_calls": [{"name": "searxng_search", "arguments": {"query": "test query"}}]}),
        tools=[searxng_search],
    )
    responses = list(chain_response.responses())
    tool_results = json.loads(responses[-1].text())["tool_results"]

    # The output should be a JSON string containing the formatted results
    output = json.loads(tool_results[0]["output"])
    assert output["query"] == "test query"
    assert len(output["results"]) == 1
    assert output["results"][0]["title"] == "Test Result"


def test_searxng_search_function_post(httpx_mock, monkeypatch):
    """Test the searxng_search function with POST method"""
    # Set required environment variable and POST method
    monkeypatch.setenv("SEARXNG_URL", "https://searx.be")
    monkeypatch.setenv("SEARXNG_METHOD", "POST")

    mock_response = {
        "query": "test query",
        "results": [
            {
                "title": "Test Result POST",
                "url": "https://example.com",
                "content": "This is a test result via POST",
                "engine": "duckduckgo",
            }
        ],
    }
    httpx_mock.add_response(url="https://searx.be/search", json=mock_response, method="POST")

    model = llm.get_model("echo")
    chain_response = model.chain(
        json.dumps({"tool_calls": [{"name": "searxng_search", "arguments": {"query": "test query"}}]}),
        tools=[searxng_search],
    )
    responses = list(chain_response.responses())
    tool_results = json.loads(responses[-1].text())["tool_results"]

    # The output should be a JSON string containing the formatted results
    output = json.loads(tool_results[0]["output"])
    assert output["query"] == "test query"
    assert len(output["results"]) == 1
    assert output["results"][0]["title"] == "Test Result POST"


def test_searxng_class_direct_get(httpx_mock, monkeypatch):
    """Test the SearXNG class directly with GET method"""
    # Explicitly set GET method
    monkeypatch.setenv("SEARXNG_METHOD", "GET")

    mock_response = {
        "query": "python",
        "results": [
            {
                "title": "Python.org",
                "url": "https://python.org",
                "content": "The official Python website",
                "engine": "google",
            }
        ],
    }
    httpx_mock.add_response(
        url="https://custom.searxng.com/search?q=python&format=json&language=en&pageno=1&safesearch=1",
        json=mock_response,
        method="GET",
    )

    # Test the SearXNG class directly
    searxng = SearXNG("https://custom.searxng.com")
    result = searxng.search("python")

    output = json.loads(result)
    assert output["query"] == "python"
    assert len(output["results"]) == 1
    assert output["results"][0]["url"] == "https://python.org"


def test_searxng_class_direct_post_default(httpx_mock):
    """Test the SearXNG class directly with POST method (default)"""
    mock_response = {
        "query": "python",
        "results": [
            {
                "title": "Python.org",
                "url": "https://python.org",
                "content": "The official Python website",
                "engine": "google",
            }
        ],
    }
    httpx_mock.add_response(url="https://custom.searxng.com/search", json=mock_response, method="POST")

    # Test the SearXNG class directly without setting method (should default to POST)
    searxng = SearXNG("https://custom.searxng.com")
    result = searxng.search("python")

    output = json.loads(result)
    assert output["query"] == "python"
    assert len(output["results"]) == 1
    assert output["results"][0]["url"] == "https://python.org"
