"""Unit tests for ApiReliabilityTester use case."""

import pytest

from app.application.use_cases.test_api_reliability import ApiReliabilityTester


@pytest.fixture
def tester():
    """Return ApiReliabilityTester with mocked HTTP client."""

    class MockClient:
        def request(self, method, url, headers=None, json_data=None):
            return 200, "OK", '{"success": true}'

    return ApiReliabilityTester(http_client=MockClient())


@pytest.mark.unit
@pytest.mark.application
def test_tester_execute(tester):
    """Test full execution of API testing."""
    swagger_spec = {"paths": {"/rest/v1/users": {"get": {"tags": ["rest"], "summary": "test"}}}}

    results = tester.execute(swagger_spec=swagger_spec, anon_key="abc", methods_to_test={"GET"})

    assert len(results) == 1
    assert results[0]["status"] == 200
    assert results[0]["method"] == "GET"


@pytest.mark.unit
@pytest.mark.application
def test_tester_execute_non_dict_ops(tester):
    """Test path with non-dictionary operations (should be skipped)."""
    swagger_spec = {"paths": {"/invalid": "not-a-dict"}}
    results = tester.execute(swagger_spec, "abc", {"GET"})
    assert len(results) == 0


@pytest.mark.unit
@pytest.mark.application
def test_tester_execute_filter_methods(tester):
    """Test filtering by HTTP methods."""
    swagger_spec = {"paths": {"/test": {"get": {}, "post": {}}}}
    results = tester.execute(swagger_spec, "abc", {"POST"})
    assert len(results) == 1
    assert results[0]["method"] == "POST"


@pytest.mark.unit
@pytest.mark.application
def test_tester_execute_with_filters(tester):
    """Test filtering and non-dict ops."""
    spec = {"paths": {"/p1": {"get": {}, "post": {}}, "/p2": "not-a-dict"}}
    results = tester.execute(spec, "k", methods_to_test={"GET"})
    assert len(results) == 1
    assert results[0]["method"] == "GET"


@pytest.mark.unit
@pytest.mark.application
def test_tester_fill_path_params(tester):
    """Test path parameter replacement."""
    # pylint: disable=protected-access
    path = "/users/{id}/profile/{name}"
    filled = tester._fill_path_params(path)
    assert "{id}" not in filled
    assert "{name}" not in filled
