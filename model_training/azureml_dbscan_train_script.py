from azure.ai.ml import MLClient
from azure.ai.ml.entities import AmlCompute
from azure.identity import DefaultAzureCredential
from azure.ai.ml import command
from azure.ai.ml.entities import Model
from azure.ai.ml.entities import Environment


credential = DefaultAzureCredential()
ml_client = MLClient(
    credential=credential,
    subscription_id="subscription_id",
    resource_group_name="resource_group_name",
    workspace_name="workspace_name",
)

cpu_cluster = AmlCompute(name=cpu_compute_target_name,
                         type="amlcompute",
                         size=size,
                         min_instances=min_instances,
                         max_instances=max_instances,
                         idle_time_before_scale_down=idle_time_before_scale_down,
                         tier=tier)

    # Now, we pass the object to MLClient's create_or_update method
cpu_cluster = ml_client.compute.begin_create_or_update(cpu_cluster).result()


custom_env_name = "dbscan-env"

job_env = Environment(
    name=custom_env_name,
    description="Custom environment for dbscan clustering",
    conda_file="path/to/conda.yaml",
    image="image:tag",
)
job_env = ml_client.environments.create_or_update(job_env)



job = command(
    inputs=dict(eps=0.3, min_samples=100),
    compute=cpu_compute_target_name,
    environment=f"{job_env.name}:{job_env.version}",
    code="code/directory",
    command="python train_dbscan.py --eps ${{inputs.eps}} --min_samples ${{inputs.min_samples}}",
    experiment_name="cluster-instagram-texts",
    display_name="sklearn-cluster-instagram-texts",
)

ml_client.jobs.create_or_update(job)

model = Model(
        path="azureml://sklearn-cluster-instagram-texts/run-model-example",
        name="sklearn-cluster-instagram-texts",
        description="Model created from run.",
        type="custom_model",
    )
