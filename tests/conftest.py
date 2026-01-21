"""Shared pytest fixtures for basyx-client tests."""

import pytest


@pytest.fixture
def sample_aas_id() -> str:
    """Sample AAS identifier with special characters."""
    return "https://acme.org/ids/aas/55"


@pytest.fixture
def sample_submodel_id() -> str:
    """Sample Submodel identifier."""
    return "https://acme.org/ids/submodel/operational-data"


@pytest.fixture
def sample_id_short_path() -> str:
    """Sample idShortPath with array indices."""
    return "Sensors.Measurements[0].Temperature"


@pytest.fixture
def base_url() -> str:
    """Sample API base URL."""
    return "http://localhost:8081/api/v3.0"


@pytest.fixture
def sample_aas_response() -> dict:
    """Sample AAS response from API."""
    return {
        "modelType": "AssetAdministrationShell",
        "id": "https://acme.org/ids/aas/55",
        "idShort": "MyAAS",
        "assetInformation": {
            "assetKind": "Instance",
            "globalAssetId": "https://acme.org/assets/55",
        },
    }


@pytest.fixture
def sample_submodel_response() -> dict:
    """Sample Submodel response from API."""
    return {
        "modelType": "Submodel",
        "id": "https://acme.org/ids/submodel/operational-data",
        "idShort": "OperationalData",
        "submodelElements": [
            {
                "modelType": "Property",
                "idShort": "Temperature",
                "valueType": "xs:double",
                "value": "25.5",
            }
        ],
    }
