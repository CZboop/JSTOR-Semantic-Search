from fastapi.testclient import TestClient
from fastapi import FastAPI
from ..main import app

def test_query_without_filters_returns_number_of_matches_in_query_top_n_path_var():
    # given - a set number of matches to request in the query
    num_matches = 3
    with TestClient(app) as client:
        # when - we call the endpoint with the desired number of matches
        response = client.get(f"/api/v1/query/test/{num_matches}")
        # then - the response comes through successfully, with the expected number of matches
        assert response.status_code == 200
        assert len(response.json()["matches"]) == num_matches

def test_query_with_filters_returns_number_of_matches_in_query_top_n_path_var():
    # given - a set number of matches to request in the query and some broad filters that shouldn't narrow results too much
    num_matches = 3
    filters = {
                "document_type": {"$eq" : "article"},
                "word_count": {"$gte": 2000}
                }
    with TestClient(app) as client:
        # when - we call the endpoint with the desired number of matches and the defined filters
        response = client.post(f"/api/v1/filter-query/test/{num_matches}",
            json = filters,
            )
        # then - the response comes through successfully, with the expected number of matches
        assert response.status_code == 200
        assert len(response.json()["matches"]) == num_matches