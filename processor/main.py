"""
Processor microservice for repository renovation.

This module serves as the entry point for the "processor" microservice.
It retrieves all repository IDs from the database and dispatches a Kubernetes
Job to renovate each repository using `k8s.launch_job`.

Exports:
    - main(): Load all repository IDs and launch renovation jobs for each.
"""

from processor import database, k8s


def main():
    """
    Retrieve all repository IDs and dispatch renovation jobs.

    Uses `database.get_all_items()` to fetch all repository identifiers.
    Iterates over each ID and calls `k8s.launch_job(item_id)` to launch a
    Kubernetes Job responsible for renovating that repository.

    Side Effects:
        - Reads repository IDs from the database.
        - Submits renovation Jobs to the Kubernetes cluster.

    Returns:
        None

    """
    items = database.get_all_items()
    for item in items:
        k8s.launch_job(item)


if __name__ == "__main__":
    main()
