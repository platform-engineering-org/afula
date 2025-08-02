"""
Kubernetes job launcher module.

Loads in‑cluster configuration and provides a function to create and launch
a Kubernetes Job for processing a given item by its ID.

Exports:
    launch_job(item_id): Create and submit a Kubernetes Job named
        "process-item-{item_id}" that runs a container passing the item_id
        as an argument.
"""

import urllib
import uuid

import kubernetes


def launch_job(item):
    """
    Launch a Kubernetes Job to process the specified item.

    Constructs a Job resource named "process-item-{item_id}", using a single
    container based on the predefined Docker image. The container is passed
    the `item_id` as its command-line argument. The Job is submitted to the
    "default" namespace in the current cluster context.

    Args:
        item: Repo raw extracted from the database

    Raises:
        kubernetes.client.exceptions.ApiException: If the Kubernetes API
            call fails (e.g., due to authentication, resource conflicts,
            invalid spec, etc.).

    """
    kubernetes.config.load_incluster_config()

    repo_name = str(item[1]).lower().replace("_", "-").replace(" ", "-")
    suffix = uuid.uuid4().hex[:8]

    job_name = f"process-item-{repo_name}-{suffix}"

    repo_url = str(item[2])
    repo_path = urllib.parse.urlparse(repo_url).path.lstrip("/")

    renovate_version = "41.30.5"

    container = kubernetes.client.V1Container(
        name="renovate",
        image=f"renovate/renovate:{renovate_version}",
        env=[
            kubernetes.client.V1EnvVar(
                name="RENOVATE_TOKEN",
                value_from=kubernetes.client.V1EnvVarSource(
                    secret_key_ref=kubernetes.client.V1SecretKeySelector(
                        name="renovate-env", key="RENOVATE_TOKEN"
                    )
                ),
            ),
            kubernetes.client.V1EnvVar(name="RENOVATE_PLATFORM", value="github"),
        ],
        args=[repo_path],
    )

    template = kubernetes.client.V1PodTemplateSpec(
        metadata=kubernetes.client.V1ObjectMeta(labels={"app": "renovate"}),
        spec=kubernetes.client.V1PodSpec(
            containers=[container], restart_policy="Never"
        ),
    )

    spec = kubernetes.client.V1JobSpec(template=template, backoff_limit=1)

    job = kubernetes.client.V1Job(
        api_version="batch/v1",
        kind="Job",
        metadata=kubernetes.client.V1ObjectMeta(name=job_name),
        spec=spec,
    )

    api = kubernetes.client.BatchV1Api()
    api.create_namespaced_job(namespace="default", body=job)
