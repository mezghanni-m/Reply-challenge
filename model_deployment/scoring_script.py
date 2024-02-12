import json
from azureml.core.model import Model
from sklearn.cluster import DBSCAN
import numpy as np
import joblib
from transformers import BertTokenizer, BertModel

def init():
    global model
    global tokenizer
    global bert_model
    model_path = Model.get_model_path('sklearn-cluster-instagram-texts')  # 'sklearn-cluster-instagram-texts' is the registered model name
    model = joblib.load(model_path)
    tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
    bert_model = BertModel.from_pretrained('bert-base-uncased')

def run(input_data):
    text = json.loads(input_data)['data']
    encoded_text = tokenizer(text, return_tensors="pt", padding="max_length", truncation=True, max_length=512)
    emb = model(input_ids= encoded_text.input_ids, attention_mask = encoded_text.attention_mask).pooler_output.cpu().detach().numpy().unsqueeze(0)
    labels = model.fit_predict(emb)
    return labels.tolist()