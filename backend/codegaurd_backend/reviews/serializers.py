# reviews/serializers.py
from rest_framework import serializers
from .models import Scan
from .utils import run_full_scan  # we'll implement this

class ScanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Scan
        fields = "__all__"
        read_only_fields = ("id", "created_at", "duration_ms", "model_version",
                            "static_findings", "ml_findings", "unified_findings")

class ScanCreateSerializer(serializers.ModelSerializer):
    """
    Serializer used for POST /api/scan/ to accept raw code and trigger scanning.
    """
    class Meta:
        model = Scan
        fields = ("code",)

    def create(self, validated_data):
        code = validated_data["code"]
        # run_full_scan returns (static, ml, unified, duration_ms, model_version)
        static_findings, ml_findings, unified_findings, duration_ms, model_version = run_full_scan(code)
        scan = Scan.objects.create(
            code=code,
            duration_ms=duration_ms,
            model_version=model_version,
            static_findings=static_findings,
            ml_findings=ml_findings,
            unified_findings=unified_findings,
        )
        return scan
