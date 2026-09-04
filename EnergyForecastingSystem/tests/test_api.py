"""
Unit Tests - Flask REST API Endpoints
"""

import pytest
from src.app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_health_endpoint(client):
    rv = client.get('/api/health')
    json_data = rv.get_json()
    assert rv.status_code == 200
    assert json_data['status'] == 'online'
    assert json_data['system'] == 'EnergyDemandAI'

def test_models_endpoint(client):
    rv = client.get('/api/models')
    json_data = rv.get_json()
    assert rv.status_code == 200
    assert len(json_data['models']) == 6

def test_states_endpoint(client):
    rv = client.get('/api/states')
    json_data = rv.get_json()
    assert rv.status_code == 200
    assert "Maharashtra" in json_data['states']

def test_forecast_endpoint(client):
    rv = client.get('/api/forecast?horizon=24&model=xgboost')
    json_data = rv.get_json()
    assert rv.status_code == 200
    assert json_data['success'] is True
    assert len(json_data['forecast']) == 24
