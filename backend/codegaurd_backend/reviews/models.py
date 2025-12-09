# reviews/models.py
import uuid
from django.db import models

class Scan(models.Model):
    """
    Primary scan record. Matches the structured storage described in the report.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    code = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    duration_ms = models.PositiveIntegerField(default=0)
    model_version = models.CharField(max_length=256, default="distilbert_v1")
    static_findings = models.JSONField(default=dict)   # structured static analyzer output
    ml_findings = models.JSONField(default=dict)       # structured ML output
    unified_findings = models.JSONField(default=dict)  # final fused findings

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Scan {self.id} at {self.created_at}"
