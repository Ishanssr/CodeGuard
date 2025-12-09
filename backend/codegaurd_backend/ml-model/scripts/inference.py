from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
from pathlib import Path

# Path to your fine-tuned model (the one saved by train.py)
model_path = Path("./saved-model/distilbert-base-uncased").resolve()

# Load tokenizer and model
tokenizer = AutoTokenizer.from_pretrained(str(model_path), local_files_only=True)
model = AutoModelForSequenceClassification.from_pretrained(str(model_path), local_files_only=True)

def predict(code_snippet: str):
    """Classify a code snippet as safe or vulnerable"""
    inputs = tokenizer(code_snippet, return_tensors="pt", padding=True, truncation=True, max_length=128)
    with torch.no_grad():
        outputs = model(**inputs)
        probs = torch.softmax(outputs.logits, dim=-1)
        pred = torch.argmax(probs, dim=1).item()
    
    label = "⚠️ Vulnerable" if pred == 1 else "✅ Safe"
    return {"code": code_snippet, "prediction": label, "probs": probs.tolist()}

# Example runs
if __name__ == "__main__":
    snippets = [
        "print('Hello world')",                   # Safe
        "eval(user_input)",                       # Vulnerable
        "password = '12345'",                     # Vulnerable
        "query = 'SELECT * FROM users where id=' + user_input"  # Vulnerable
    ]
    
    for s in snippets:
        result = predict(s)
        print(result)
