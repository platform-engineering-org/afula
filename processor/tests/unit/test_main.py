"""
Test suite for the processor microservice.

Contains unit tests for the `main()` function in the `processor` module,
verifying correct orchestration of job dispatching using mocked dependencies.
"""

from processor import main


def test_main(mock_database_get_all_items, mock_k8s_launch_job):
    """
    Ensure that main() retrieves all repository IDs and launches jobs accordingly.

    Given a mocked database returning [1, 2, 3], when main() is invoked,
    it should:
      - Call database.get_all_items() exactly once.
      - Call k8s.launch_job(item_id) for each ID in the returned list.
      - Total of 3 calls to k8s.launch_job with IDs 1, 2, and 3.

    This test uses fixtures to mock external dependencies:
      - `mock_database_get_all_items` patches the database layer.
      - `mock_k8s_launch_job` patches the Kubernetes launcher.
    """
    mock_database_get_all_items.return_value = [1, 2, 3]

    main.main()

    mock_database_get_all_items.assert_called_once()
    mock_k8s_launch_job.assert_any_call(1)
    mock_k8s_launch_job.assert_any_call(2)
    mock_k8s_launch_job.assert_any_call(3)
    assert mock_k8s_launch_job.call_count == 3
