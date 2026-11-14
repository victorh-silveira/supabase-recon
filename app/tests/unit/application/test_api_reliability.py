"""Testes unitarios para o caso de uso ApiReliabilityTester."""

import pytest

from application.use_cases.test_api_reliability import ApiReliabilityTester


@pytest.fixture
def tester():
    """Retorna ApiReliabilityTester com cliente HTTP falso."""

    class FakeClient:
        def request(self, method, url, headers=None, json_data=None):
            return 200, "OK", '{"success": true}'

        def get_text(self, url):
            return None

        def get_bytes(self, url):
            return None

    return ApiReliabilityTester(http_client=FakeClient())


@pytest.mark.unit
@pytest.mark.application
def test_tester_execute(tester):
    """Testa execucao completa dos testes de API."""
    swagger_spec = {"paths": {"/rest/v1/users": {"get": {"tags": ["rest"], "summary": "test"}}}}

    results = tester.execute(swagger_spec=swagger_spec, anon_key="abc", methods_to_test={"GET"})

    assert len(results) == 1
    assert results[0]["status"] == 200
    assert results[0]["method"] == "GET"


@pytest.mark.unit
@pytest.mark.application
def test_tester_execute_non_dict_ops(tester):
    """Testa caminho com operacoes que nao sao dicionario (deve ser ignorado)."""
    swagger_spec = {"paths": {"/invalid": "not-a-dict"}}
    results = tester.execute(swagger_spec, "abc", {"GET"})
    assert len(results) == 0


@pytest.mark.unit
@pytest.mark.application
def test_tester_execute_filter_methods(tester):
    """Testa filtragem por metodos HTTP."""
    swagger_spec = {"paths": {"/test": {"get": {}, "post": {}}}}
    results = tester.execute(swagger_spec, "abc", {"POST"})
    assert len(results) == 1
    assert results[0]["method"] == "POST"


@pytest.mark.unit
@pytest.mark.application
def test_tester_execute_with_filters(tester):
    """Testa filtragem e operacoes nao dicionario."""
    spec = {"paths": {"/p1": {"get": {}, "post": {}}, "/p2": "not-a-dict"}}
    results = tester.execute(spec, "k", methods_to_test={"GET"})
    assert len(results) == 1
    assert results[0]["method"] == "GET"


@pytest.mark.unit
@pytest.mark.application
def test_tester_fill_path_params(tester):
    """Testa substituicao de parametros de caminho."""
    path = "/users/{id}/profile/{name}"
    filled = tester._fill_path_params(path)
    assert "{id}" not in filled
    assert "{name}" not in filled
