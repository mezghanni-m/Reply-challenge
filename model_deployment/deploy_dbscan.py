from azure.ai.ml import MLClient
from azure.identity import DefaultAzureCredential
from azure.ai.ml.entities import ManagedOnlineEndpoint, ManagedOnlineDeployment


# authenticate
credential = DefaultAzureCredential()

# Get a handle to the workspace
ml_client = MLClient(
    credential=credential,
    subscription_id="subscription_id",
    resource_group_name="resource_group_name",
    workspace_name="workspace_name",
)

# Let's pick the latest version of the model
latest_model_version = max(
    [int(m.version) for m in ml_client.models.list(name="sklearn-cluster-instagram-texts")]
)

online_endpoint_name = "sklearn-cluster-instagram-texts-endpoint"


# define an online endpoint
endpoint = ManagedOnlineEndpoint(
    name=online_endpoint_name,
    description="dbscan online endpoint",
    auth_mode="aml_token"
)

# create the online endpoint
endpoint = ml_client.online_endpoints.begin_create_or_update(endpoint).result()

# Choose the latest version of our registered model for deployment
model = ml_client.models.get(name="sklearn-cluster-instagram-texts", version=latest_model_version)

# define an online deployment
deployment = ManagedOnlineDeployment(
    name="sklearn-cluster-instagram-texts-deployment",
    endpoint_name=online_endpoint_name,
    model=model,
    instance_type="Standard_DS3_v2",
    instance_count=1,
    scoring_script="scoring_script.py",
)

# create the online deployment
deployment = ml_client.online_deployments.begin_create_or_update(deployment).result()

endpoint.traffic = {"sklearn-cluster-instagram-texts-deployment": 100}
ml_client.online_endpoints.begin_create_or_update(endpoint).result()