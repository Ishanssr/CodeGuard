from transformers import AutoTokenizer, AutoModel

tokenizer = AutoTokenizer.from_pretrained("microsoft/codebert-base")
model = AutoModel.from_pretrained("microsoft/codebert-base")

model.save_pretrained("../saved-model/codebert-base")
tokenizer.save_pretrained("../saved-model/codebert-base")

print("✅ CodeBERT downloaded and saved locally.")