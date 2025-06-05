import json
from unittest.mock import Mock, patch

import pytest
import llm

from llm_tools_searxng import SearXNG, searxng_search


@pytest.fixture
def mock_searxng_instance():
    """Mock SearXNG instance with predefined response"""
    instance = Mock()
    instance.search.return_value = json.dumps(
        {
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
    )
    return instance


@pytest.fixture
def tool_call_payload():
    """Tool call payload for llm.chain"""
    return json.dumps({"tool_calls": [{"name": "searxng_search", "arguments": {"query": "test query"}}]})


@pytest.fixture
def python_search_response():
    """Response for direct class tests with Python query"""
    return {
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


class TestSearxngSearchFunction:
    """Tests for the searxng_search function"""

    @patch("llm_tools_searxng.SearXNG")
    def test_direct_call(self, mock_searxng_class, mock_searxng_instance):
        """Test searxng_search function by calling it directly"""
        # Setup mock
        mock_searxng_class.return_value = mock_searxng_instance

        # Call function directly
        result = searxng_search({"query": "test query"})

        # Verify mock was called correctly
        mock_searxng_class.assert_called_once()
        mock_searxng_instance.search.assert_called_once_with({"query": "test query"})

        # Verify result
        result_data = json.loads(result)
        assert result_data["query"] == "test query"
        assert len(result_data["results"]) == 1
        assert result_data["results"][0]["title"] == "Test Result"

    @patch("llm_tools_searxng.SearXNG")
    def test_via_chain(self, mock_searxng_class, mock_searxng_instance, tool_call_payload):
        """Test searxng_search function through llm.chain"""
        # Setup mock
        mock_searxng_class.return_value = mock_searxng_instance

        # Call through llm.chain
        model = llm.get_model("echo")
        chain_response = model.chain(
            tool_call_payload,
            tools=[searxng_search],
        )

        # Verify results
        responses = list(chain_response.responses())
        tool_results = json.loads(responses[-1].text())["tool_results"]
        output = json.loads(tool_results[0]["output"])

        assert output["query"] == "test query"
        assert len(output["results"]) == 1
        assert output["results"][0]["title"] == "Test Result"


class TestSearxngClassDirect:
    """Tests for the SearXNG class directly"""

    def test_get_method(self, httpx_mock, monkeypatch, python_search_response):
        """Test SearXNG class directly with GET method"""
        monkeypatch.setenv("SEARXNG_METHOD", "GET")

        httpx_mock.add_response(
            url="https://custom.searxng.com/search?q=python&format=json&language=en&pageno=1&safesearch=1",
            json=python_search_response,
            method="GET",
        )

        searxng = SearXNG("https://custom.searxng.com")
        result = searxng.search("python")

        output = json.loads(result)
        assert output["query"] == "python"
        assert len(output["results"]) == 1
        assert output["results"][0]["url"] == "https://python.org"

    def test_post_method_default(self, httpx_mock, python_search_response):
        """Test SearXNG class directly with POST method (default)"""
        httpx_mock.add_response(
            url="https://custom.searxng.com/search",
            json=python_search_response,
            method="POST",
        )

        searxng = SearXNG("https://custom.searxng.com")
        result = searxng.search("python")

        output = json.loads(result)
        assert output["query"] == "python"
        assert len(output["results"]) == 1
        assert output["results"][0]["url"] == "https://python.org"

    def test_post_method(self, httpx_mock, monkeypatch, python_search_response):
        """Test SearXNG class directly with POST method"""
        monkeypatch.setenv("SEARXNG_METHOD", "POST")

        httpx_mock.add_response(
            url="https://custom.searxng.com/search",
            json=python_search_response,
            method="POST",
        )

        searxng = SearXNG("https://custom.searxng.com")
        result = searxng.search("python")

        output = json.loads(result)
        assert output["query"] == "python"
        assert len(output["results"]) == 1
        assert output["results"][0]["url"] == "https://python.org"
