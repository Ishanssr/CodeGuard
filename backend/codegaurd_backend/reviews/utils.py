# reviews/utils.py
import time
import re
import torch
from pathlib import Path
from transformers import AutoTokenizer, AutoModelForSequenceClassification

# Paths (adjust if your model location differs)
MODEL_PATH = Path(__file__).resolve().parent.parent / "ml-model" / "saved-model" / "distilbert-base-uncased"

# ------------------------------------------------
# Static analyzer: structured rules + mapping
# ------------------------------------------------
# Each rule maps to an id, cwe, severity, message, and a regex or function
STATIC_RULES = [
    {
        "id": "S001",
        "cwe": "CWE-94",
        "severity": "High",
        "pattern": r"\beval\s*\(",
        "message": "Use of eval() may allow arbitrary code execution."
    },
    {
        "id": "S002",
        "cwe": "CWE-94",
        "severity": "High",
        "pattern": r"\bexec\s*\(",
        "message": "Use of exec() may allow arbitrary code execution."
    },
    {
        "id": "S003",
        "cwe": "CWE-798",
        "severity": "High",
        "pattern": r'password\s*=\s*["\'].*["\']',
        "message": "Hardcoded password found."
    },
    {
        "id": "S004",
        "cwe": "CWE-89",
        "severity": "Medium",
        "pattern": r"SELECT .* FROM .* \+ ",
        "message": "Possible SQL injection via string concatenation."
    },
]

def scan_code_for_vulnerabilities_structured(code: str):
    """
    Returns a list of structured findings with line numbers.
    """
    findings = []
    lines = code.splitlines()
    for ridx, rule in enumerate(STATIC_RULES):
        pattern = re.compile(rule["pattern"], re.IGNORECASE)
        for lineno, line in enumerate(lines, start=1):
            if pattern.search(line):
                findings.append({
                    "rule_id": rule["id"],
                    "cwe": rule["cwe"],
                    "severity": rule["severity"],
                    "line": lineno,
                    "snippet": line.strip(),
                    "message": rule["message"]
                })
    return findings

# ------------------------------------------------
# ML model loading & prediction
# ------------------------------------------------
try:
    tokenizer = AutoTokenizer.from_pretrained(str(MODEL_PATH), local_files_only=True)
    model = AutoModelForSequenceClassification.from_pretrained(str(MODEL_PATH), local_files_only=True)
except Exception as e:
    print("⚠️ Warning: Could not load ML model.", e)
    tokenizer, model = None, None

def predict_vulnerability_structured(code: str):
    """
    Returns structured ML result:
    {
      "label": "vulnerable" / "safe",
      "confidence": 0.92,
      "probabilities": {"safe": 0.08, "vulnerable": 0.92}
    }
    """
    if tokenizer is None or model is None:
        return {"error": "ML model not available"}

    inputs = tokenizer(code, return_tensors="pt", padding=True, truncation=True, max_length=512)
    with torch.no_grad():
        outputs = model(**inputs)
        probs = torch.softmax(outputs.logits, dim=-1).squeeze().tolist()
        # assume class 0 = safe, class 1 = vulnerable (match your training)
        if isinstance(probs, float):
            # single-label returned as float when classes==1, handle defensively
            probs = [1.0 - probs, probs]
        safe_prob, vuln_prob = probs[0], probs[1] if len(probs) > 1 else (1.0 - probs[0])
        label = "vulnerable" if vuln_prob > safe_prob else "safe"
        return {
            "label": label,
            "confidence": max(safe_prob, vuln_prob),
            "probabilities": {"safe": safe_prob, "vulnerable": vuln_prob},
            "model_version": getattr(model.config, "name_or_path", "unknown")
        }

# ------------------------------------------------
# Orchestration: full scan
# ------------------------------------------------
def run_full_scan(code: str):
    """
    Runs static + ML scans, fuses findings, and returns:
    (static_findings_list, ml_findings_dict, unified_findings_list, duration_ms, model_version)
    """
    start = time.time()

    static_findings = scan_code_for_vulnerabilities_structured(code)
    ml_findings = predict_vulnerability_structured(code)

    # naive fusion strategy: if ML says vulnerable -> add a unified high-level
    unified = []
    for s in static_findings:
        unified.append({
            "source": "static",
            **s
        })

    if "error" not in ml_findings:
        confidence = ml_findings.get("confidence", 0.0)
        label = ml_findings.get("label", "unknown")
        unified.append({
            "source": "ml",
            "label": label,
            "confidence": confidence,
            "probabilities": ml_findings.get("probabilities"),
            "model_version": ml_findings.get("model_version"),
        })

    duration_ms = int((time.time() - start) * 1000)
    model_version = ml_findings.get("model_version", "unknown") if isinstance(ml_findings, dict) else "unknown"

    return static_findings, ml_findings, unified, duration_ms, model_version

def model_status():
    """
    Return a simple status dictionary for the model / inference availability.
    """
    loaded = (tokenizer is not None and model is not None)
    return {
        "model_loaded": loaded,
        "model_name": getattr(model.config, "name_or_path", None) if model else None
    }
