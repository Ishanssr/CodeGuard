from transformers import AutoTokenizer, AutoModelForSequenceClassification
from datasets import load_dataset
import torch
import numpy as np
from sklearn.metrics import accuracy_score, precision_recall_fscore_support

# Load model + tokenizer
tokenizer = AutoTokenizer.from_pretrained("./saved-model/distilbert-base-uncased")
model = AutoModelForSequenceClassification.from_pretrained("./saved-model/distilbert-base-uncased")

# Load test set
dataset = load_dataset("json", data_files={"test": "data/test.json"})
test_dataset = dataset["test"]

# Tokenize test set
def encode(batch):
    return tokenizer(batch["code"], truncation=True, padding="max_length")
test_dataset = test_dataset.map(encode, batched=True)

# Convert to torch DataLoader
test_loader = torch.utils.data.DataLoader(test_dataset, batch_size=16)

all_preds, all_labels = [], []

# Evaluation loop
model.eval()
with torch.no_grad():
    for batch in test_loader:
        inputs = {k: v for k, v in batch.items() if k in tokenizer.model_input_names}
        labels = batch["label"]
        outputs = model(**inputs)
        preds = torch.argmax(outputs.logits, dim=1)
        all_preds.extend(preds.cpu().numpy())
        all_labels.extend(labels.numpy())

# Metrics
precision, recall, f1, _ = precision_recall_fscore_support(all_labels, all_preds, average="binary")
accuracy = accuracy_score(all_labels, all_preds)
print({"accuracy": accuracy, "precision": precision, "recall": recall, "f1": f1})