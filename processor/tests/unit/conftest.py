"""
Shared pytest configuration and fixtures.

This file automatically applies mocks to external dependencies for all tests
in the suite, preventing side effects during import or execution.

Fixtures:

- mock_load_incluster_config (autouse):
    Prevents `kubernetes.config.load_incluster_config()` from running when the
    `k8s` module is imported, avoiding ConfigException during pytest collection.

- mock_database_get_all_items:
    Mocks `processor.database.get_all_items()` to return test-specific data.

- mock_k8s_launch_job:
    Mocks `processor.k8s.launch_job()` to intercept Kubernetes Job submissions.
"""

from unittest.mock import patch

import pytest


@pytest.fixture(autouse=True)
def mock_load_incluster_config():
    """Suppress in-cluster Kubernetes config loading globally."""
    with patch("kubernetes.config.load_incluster_config"):
        yield


@pytest.fixture
def mock_database_get_all_items():
    """Mock `processor.database.get_all_items()` to control returned items."""
    with patch("processor.database.get_all_items") as mock:
        yield mock


@pytest.fixture
def mock_k8s_launch_job():
    """Mock `processor.k8s.launch_job()` to prevent real job submission."""
    with patch("processor.k8s.launch_job") as mock:
        yield mock
