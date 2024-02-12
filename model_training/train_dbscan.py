

import argparse
import numpy as np
import joblib
from azure.storage.blob import BlobServiceClient
from azureml.core import Workspace, Experiment, Model
from transformers import BertTokenizer, BertModel

def load_text_from_blob_storage(account_name, account_key, container_name, blob_name):
    # Create the BlobServiceClient using the storage account name and key
    blob_service_client = BlobServiceClient(account_url=f"https://{account_name}.blob.core.windows.net", credential=account_key)
    
    # Get the blob client
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)
    
    # Download the blob content as a string
    blob_data = blob_client.download_blob(offset=start_byte, length=(end_byte - start_byte)).readall().decode("utf-8")    
    # Split the text into a list of strings (assuming each line is a separate string)
    text_list = blob_data.split("\n")
    
    return text_list




def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('--eps', type=float, default=0.3)
    parser.add_argument('--min_samples', type=int, default=100)

    args = parser.parse_args()

    subscription_id = 'subscription_id'
    resource_group = 'resource_group'
    workspace_name = 'workspace'

    # Load the workspace from the saved configuration
    ws = Workspace(subscription_id, resource_group, workspace_name)

    # loading the dataset
    texts = load_text_from_blob_storage(account_name, account_key, container_name, blob_name)

    # Load pre-trained BERT tokenizer
    tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
    print(tokenizer.vocab_size)
    model = BertModel.from_pretrained('bert-base-uncased')


    emb = np.empty((0, bert_model_n_features))
    for text in texts:
        encoded_text = tokenizer(text, return_tensors="pt", padding="max_length", truncation=True, max_length=512)
        emb = np.append(emb, 
                        model(input_ids= encoded_text.input_ids, attention_mask = encoded_text.attention_mask).pooler_output.cpu().detach().numpy(), axis=0)

    X = np.array(emb).reshape(-1, bert_model_n_features)

 
    dbs = DBSCAN(eps=args.eps, min_samples=args.min_samples, n_jobs=-1, metric="cosine")
    print("fit starts")
    dbs.fit(X)

    registered_model_name="sklearn-cluster-instagram-texts"

    model_path = '../model.pkl'

    joblib.dump(dbs, model_path)

    # Registering the model to the workspace
    model = Model.register(workspace=ws,
                       model_name='model_name',
                       model_path=model_path,  # Path to your serialized model file
                       description='DBSCAN model trained on instagram data',
                       tags={'algorithm': 'DBSCAN'})


    # Upload the trained model file to Azure Blob Storage
    model_blob_service = ws.get_default_datastore()
    model_blob_service.upload_files([model_path], target_path='models/model_name/1/', overwrite=True)


if __name__ == '__main__':
    main()