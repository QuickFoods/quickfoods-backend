
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import StoreViewSet, DealViewSet, FreshItemViewSet

router = DefaultRouter()
router.register("stores", StoreViewSet, basename="store")
router.register("deals", DealViewSet, basename="deal")
router.register("fresh-items", FreshItemViewSet, basename="freshitem")

urlpatterns = [
    path("", include(router.urls)),
]
