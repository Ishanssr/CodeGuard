CodeGuard – An AI Tool That Detects Vulnerabilities in Code

CodeGuard is a project that I built to automatically check whether a piece of code is safe or unsafe using Machine Learning.
It works like a small security assistant: you paste your code into a simple web page, and the system tells you if anything inside it looks dangerous.

To make this work, I combined:

A React.js frontend

A Django REST API backend

A fine-tuned DistilBERT/CodeBERT machine learning model

⭐ What CodeGuard Does

You enter a code snippet (Python, etc.)

The backend runs it through an ML model

The model predicts if the code is safe or unsafe

You instantly get the result on the frontend

It mainly catches patterns like:

Use of eval()

Untrusted user input

Potential vulnerabilities

Insecure functions or logic

🧠 How the ML Model Works (Simple Explanation)

I fine-tuned a transformer model (DistilBERT/CodeBERT) on a dataset where each code snippet is labeled:

0 → Safe

1 → Unsafe

Example of training data:

{
  "text": "print(eval(input()))",
  "label": 1
}


The model learns to recognize unsafe coding patterns and predicts the classification when new code is submitted.

🎨 Frontend (React.js)

Clean interface

Text box for code input

Button to scan code

Displays SAFE / UNSAFE message

This makes the tool very easy to use.

⚙️ Backend (Django REST Framework)

The backend exposes a simple API endpoint.
It receives code from the frontend, runs it through the ML model, and returns the result.

Example API response:

{
  "prediction": "unsafe",
  "confidence": 0.92
}

📁 Project Structure (Readable Version)
CodeGuard/
|
|-- backend/                 # Django API
|   |-- reviews/             # Handles scan requests
|   |-- ml-model/            # ML scripts (train, inference)
|
|-- frontend/                # React web interface
|   |-- codeguard-frontend/
|
|-- ml-model/                # Training & inference scripts
|
|-- README.md


The large model files (saved weights, checkpoints, datasets) are not included in GitHub to keep the repo clean.

🚀 How to Run the App Locally
Backend:
cd backend
source venv/bin/activate   # activate virtual environment
python manage.py runserver

Frontend:
cd frontend/codeguard-frontend
npm install
npm start

📦 Training the Model (Simple Commands)

To retrain the ML model:

python train.py


To run a prediction manually:

python inference.py --text "your code here"

🎯 Why I Built This

Code vulnerabilities are easy to miss.
CodeGuard helps catch unsafe patterns automatically using AI, making coding safer for beginners and faster for developers.

It also showcases:

Full-stack development (React + Django)

Machine learning integration

Transformer fine-tuning

API development

👨‍💻 Author

Ishanssr

A full-stack + machine learning project integrating modern web development with transformer-based AI models.