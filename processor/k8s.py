"""
Kubernetes job launcher module.

Loads in‑cluster configuration and provides a function to create and launch
a Kubernetes Job for processing a given item by its ID.

Exports:
    launch_job(item_id): Create and submit a Kubernetes Job named
        "process-item-{item_id}" that runs a container passing the item_id
        as an argument.
"""

import kubernetes


def launch_job(item_id):
    """
    Launch a Kubernetes Job to process the specified item.

    Constructs a Job resource named "process-item-{item_id}", using a single
    container based on the predefined Docker image. The container is passed
    the `item_id` as its command-line argument. The Job is submitted to the
    "default" namespace in the current cluster context.

    Args:
        item_id (int or str): Identifier of the item to process; will be
            converted to string and forwarded to the job's container.

    Raises:
        kubernetes.client.exceptions.ApiException: If the Kubernetes API
            call fails (e.g., due to authentication, resource conflicts,
            invalid spec, etc.).

    """
    kubernetes.config.load_incluster_config()

    job_name = f"process-item-{item_id}"

    job = kubernetes.client.V1Job(
        metadata=kubernetes.client.V1ObjectMeta(name=job_name),
        spec=kubernetes.client.V1JobSpec(
            template=kubernetes.client.V1PodTemplateSpec(
                spec=kubernetes.client.V1PodSpec(
                    containers=[
                        kubernetes.client.V1Container(
                            name="worker",
                            image="your-docker-image",
                            args=[str(item_id)],
                        )
                    ],
                    restart_policy="Never",
                )
            ),
            backoff_limit=2,
        ),
    )
    api = kubernetes.client.BatchV1Api()
    api.create_namespaced_job(namespace="default", body=job)
