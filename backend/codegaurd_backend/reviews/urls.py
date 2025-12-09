# reviews/urls.py
from rest_framework import routers
from .views import ScanViewSet

router = routers.DefaultRouter()
router.register(r"scan", ScanViewSet, basename="scan")

urlpatterns = router.urls
