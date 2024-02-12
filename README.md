# Documentation for Model Deployment Process in Azure ML

## Introduction:
This document outlines the process of training and deploying a machine learning model using Azure Machine Learning (Azure ML) services. It covers the selection of the model, the resources and services utilized, the deployment process, and potential pitfalls to be aware of.

## 1. Model Selection:
- **Problem Statement and Objectives:**
    - Topic Classification: Develop a model capable of accurately classifying Instagram posts into predefined topics. The number of topics should be flexible, with a business requirement stating that we should identify at least 20 and at most 100 such topics.

- **Chosen Method:**
    - The method combines external text data with topic labels to train a binary classification model, leveraging pretrained text feature extractors and DBSCAN clustering to assign topics to Instagram text clusters based on the highest average probability inferred by the binary model among 100 possible topics.

- **Criteria for Model Selection:**
    - Unlabeled data available, requiring an unsupervised technique (e.g., clustering).
    - Unknown number of possible topics, making DBSCAN a suitable algorithm.
    - Utilization of pretrained text feature extractors for meaningful clustering.
    - Selection based on performance metrics, with the binary model used to evaluate DBSCAN clustering performance.

## 2. Model Training

1. **External Text Data Collection:**
   - Search for an external text dataset with topic labels.

2. **Binary Classification Model Training:**
   - Train a binary classification model using the external text dataset. The model predicts the probability that a text belongs to a specified topic.
   - Save the trained model as `cls_model`.

3. **Feature Extraction for DBSCAN:**
   - Use a pre-trained text feature extractor to generate feature maps from Instagram posts. These feature maps are input to DBSCAN.

4. **DBSCAN Clustering:**
   - Apply DBSCAN to the feature maps to cluster the Instagram posts based on density.

5. **Topic List Preparation:**
   - Prepare a list of 100 possible Instagram topics.

6. **Topic Inference for Clusters:**
   - Sample a subset of samples from each cluster. Samples should be near to the cluster center.
   - Use `cls_model` and each of the 100 possible topics to make inferences on the sampled data for each cluster.
   - Determine the most likely topic for each cluster.

7. **Topic Assignment to Instagram Texts:**
   - Assign determined topics to corresponding Instagram texts based on clustering results.


## 3. Resources and Services Used:
- All necessary Azure resources are created using Terraform and AzureRM provider.
- **Azure Resources Utilized:**
    - Azure Machine Learning Studio: Data preprocessing, model training, and evaluation.
    - Azure Machine Learning Compute: Provisioning compute resources for model training at scale.
    - Azure Blob Storage: Storing datasets and model artifacts.
    - Azure Container Registry (ACR): Required for Azure ML workspace
    - Azure key-vault: Required for Azure ML workspace
    - Azure Application Insights: Required for Azure ML workspace

## 4. Model Deployment Process:
### Deployment Process Overview:
The deployment process involves deploying a machine learning model for clustering Instagram texts using Azure Machine Learning (Azure ML). The model, based on DBSCAN clustering algorithm, is trained to label Instagram texts with cluster indices representing different topics.

### Steps in the Deployment Process:
1. **Azure ML Workspace Setup**
2. **Create MLClient**
3. **Create Managed Online Endpoint:**
    - Define and create a managed online endpoint for deploying the model.
    - Specify the endpoint name, description, and authentication mode.
4. **Model Versioning:**
    - Retrieve the latest version of the trained model from the Azure ML workspace.
5. **Define Online Deployment:**
    - Define the online deployment configuration, including deployment name, endpoint name, model, instance type, instance count, and scoring script.
6. **Create or Update Online Deployment**

### Files and Scripts:
- **deploy_dbscan.py:**
    - Python script orchestrating the deployment process.
    - Handles authentication, workspace setup, endpoint creation, model retrieval, deployment configuration, and endpoint traffic management.
- **scoring_script.py:**
    - Python script containing the scoring logic for the deployed model.
    - Implements initialization logic to load the model and tokenizer.
    - Defines the run function to process input data and return cluster labels.

### Dependencies:
- **Azure ML SDK:** Used for interacting with Azure ML services and deploying models.
- **Azure Identity:** Used for authentication with Azure services.
- **Transformers Library:** Used for handling text tokenization and feature extraction.
- **Scikit-learn:** Used for DBSCAN clustering.
- **Terraform hashicorp/azurerm Provider** Used to create Azure Resources
- **Terraform hashicorp/time Provider** Used to create Azure Resources
- **Terraform hashicorp/null Provider** Used to create Azure Resources

### Usage:
- **Deploying the Model:**
    - Execute deploy_dbscan.py script to deploy the model using Azure ML services.
    - The script orchestrates the deployment process and handles all necessary configurations and interactions with Azure ML.
- **Scoring Requests:**
    - After deployment, the model's scoring endpoint is accessible for processing inference requests.
    - Send HTTP POST requests containing input data to the scoring endpoint to obtain cluster labels.

### Deployment Process Alternative:
- Convert the pkl model to ONNX format and deploy a Docker image with Triton Inference Server using an Azure Container Group.

