from pathlib import Path
from transformers import AutoTokenizer, AutoModelForSequenceClassification, Trainer, TrainingArguments
from datasets import load_dataset

# Absolute local model path
model_path = Path("./saved-model/distilbert-base-uncased").resolve()

# Auto classes will detect correct tokenizer & model from that path
tokenizer = AutoTokenizer.from_pretrained(str(model_path), local_files_only=True)
model = AutoModelForSequenceClassification.from_pretrained(str(model_path), num_labels=2, local_files_only=True)

# Load dataset
dataset = load_dataset("json", data_files={"train": "data/train.json", "test": "data/test.json"})

def tokenize(batch):
    return tokenizer(batch["code"], padding="max_length", truncation=True, max_length=128)

encoded_dataset = dataset.map(tokenize, batched=True)

training_args = TrainingArguments(
    output_dir="./results",
    num_train_epochs=1,
    per_device_train_batch_size=2,
    logging_dir="./logs",
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=encoded_dataset["train"],
    tokenizer=tokenizer,
)

trainer.train()

# Save new fine‑tuned model
trainer.save_model("./saved-model/distilbert-base-uncased")
tokenizer.save_pretrained("./saved-model/distilbert-base-uncased")

print("✅ Training complete! Model saved locally at ./saved-model/distilbert-base-uncased")
