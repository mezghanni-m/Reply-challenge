import torch
import torch.nn as nn
from transformers import BertModel, BertTokenizer
from torch.utils.data import DataLoader, TensorDataset
from sklearn.metrics import precision_recall_fscore_support

class DummyTransformerModel(nn.Module):
    def __init__(self, num_classes):
        super(DummyTransformerModel, self).__init__()
        self.bert = BertModel.from_pretrained('bert-base-uncased')
        self.dropout = nn.Dropout(0.1)
        self.fc = nn.Linear(self.bert.config.hidden_size, num_classes)
        self.sigmoid = nn.Sigmoid()
    
    def forward(self, input_ids, attention_mask):
        outputs = self.bert(input_ids=input_ids, attention_mask=attention_mask)
        pooled_output = outputs.pooler_output
        pooled_output = self.dropout(pooled_output)
        logits = self.fc(pooled_output)
        probs = self.sigmoid(logits)
        return probs
    
    def evaluate_model(self, val_dataloader):
        all_preds = []
        all_labels = []

        with torch.no_grad():
            for batch in val_dataloader:
                input_ids_batch, attention_mask_batch, labels_batch = batch
                probs = self(input_ids_batch, attention_mask_batch)
                preds = (probs > 0.5).long() 
                all_preds.extend(preds.cpu().numpy())
                all_labels.extend(labels_batch.cpu().numpy())

        # Calculate precision, recall, F1 score, and support
        precision, recall, f1, _ = precision_recall_fscore_support(all_labels, all_preds, average='binary')
        return precision, recall, f1

# Generate dummy data
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
texts = ["This is a sample sentence.", "Another example sentence."]
labels = [0, 1]  # Dummy labels 0 topic don't match, 1 topic matchs

# Tokenize texts
inputs = tokenizer(texts, return_tensors="pt", padding=True, truncation=True)
input_ids = inputs["input_ids"]
attention_mask = inputs["attention_mask"]

labels_tensor = torch.tensor(labels)

# Create dataset and dataloader
dataset = TensorDataset(input_ids, attention_mask, labels_tensor)
dataloader = DataLoader(dataset, batch_size=2, shuffle=True)

# Initialize model
num_classes = 2 
model = DummyTransformerModel(num_classes)

# Dummy training loop
num_epochs = 3
optimizer = torch.optim.Adam(model.parameters(), lr=2e-5)
criterion = torch.nn.BCELoss()

for epoch in range(num_epochs):
    for batch in dataloader:
        input_ids_batch, attention_mask_batch, labels_batch = batch

        probs = model(input_ids_batch, attention_mask_batch)
        loss = criterion(probs.squeeze(), labels_batch.float())
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        
        print(f'Epoch [{epoch+1}/{num_epochs}], Loss: {loss.item()}')

val_dataloader = DataLoader(dataset, batch_size=2, shuffle=True)
precision, recall, f1 = model.evaluate_model(val_dataloader)