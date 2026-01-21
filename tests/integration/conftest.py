"""Fixtures for integration tests.

These tests require running BaSyx services via Docker.
Start services with: docker compose up -d

To run integration tests:
    pytest tests/integration -v -m integration
"""

from __future__ import annotations

import os
from typing import TYPE_CHECKING

import pytest

from basyx_client import AASClient

if TYPE_CHECKING:
    from collections.abc import Generator


def pytest_configure(config: pytest.Config) -> None:
    """Register custom markers."""
    config.addinivalue_line("markers", "integration: mark test as integration test")


# Default URLs for BaSyx services (can be overridden via environment)
AAS_REPOSITORY_URL = os.environ.get("AAS_REPOSITORY_URL", "http://localhost:8081/api/v3.0")
SUBMODEL_REPOSITORY_URL = os.environ.get(
    "SUBMODEL_REPOSITORY_URL", "http://localhost:8082/api/v3.0"
)
AAS_REGISTRY_URL = os.environ.get("AAS_REGISTRY_URL", "http://localhost:8084/api/v3.0")


@pytest.fixture
def aas_client() -> Generator[AASClient, None, None]:
    """Create a client for the AAS Repository service."""
    with AASClient(AAS_REPOSITORY_URL) as client:
        yield client


@pytest.fixture
def submodel_client() -> Generator[AASClient, None, None]:
    """Create a client for the Submodel Repository service."""
    with AASClient(SUBMODEL_REPOSITORY_URL) as client:
        yield client


@pytest.fixture
def registry_client() -> Generator[AASClient, None, None]:
    """Create a client for the AAS Registry service."""
    with AASClient(AAS_REGISTRY_URL) as client:
        yield client


@pytest.fixture
def sample_aas_identifier() -> str:
    """Return a unique AAS identifier for testing."""
    import uuid

    return f"urn:example:aas:test:{uuid.uuid4()}"


@pytest.fixture
def sample_submodel_identifier() -> str:
    """Return a unique Submodel identifier for testing."""
    import uuid

    return f"urn:example:submodel:test:{uuid.uuid4()}"
