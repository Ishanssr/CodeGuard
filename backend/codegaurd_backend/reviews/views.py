# reviews/views.py
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Scan
from .serializers import ScanSerializer, ScanCreateSerializer
from django.shortcuts import get_object_or_404

class ScanViewSet(viewsets.ModelViewSet):
    queryset = Scan.objects.all()

    def get_serializer_class(self):
        # Use a special serializer ONLY for validating POST code
        if self.action == "create":
            return ScanCreateSerializer
        return ScanSerializer

    def create(self, request, *args, **kwargs):
        """
        Override create() so POST /api/scan/ returns FULL scan details,
        not just {"code": "..."}.
        """
        # Validate & run full scan
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        scan = serializer.save()

        # Re-serialize using FULL serializer
        full_scan = ScanSerializer(scan, context={'request': request})
        return Response(full_scan.data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=["get"], url_path="health")
    def health(self, request):
        from .utils import model_status
        return Response(model_status(), status=status.HTTP_200_OK)

    @action(detail=True, methods=["get"], url_path="download")
    def download(self, request, pk=None):
        scan = get_object_or_404(Scan, pk=pk)
        serializer = ScanSerializer(scan)
        return Response(serializer.data)


