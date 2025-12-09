# quickfoods/urls.py
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from core.views import StoreViewSet, DealViewSet, FreshItemViewSet

router = DefaultRouter()
router.register(r"stores", StoreViewSet, basename="store")
router.register(r"deals", DealViewSet, basename="deal")
router.register(r"fresh-items", FreshItemViewSet, basename="freshitem")

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include(router.urls)),          # existing deals/fresh/store
    path("api/auth/", include("accounts.urls")), # <-- signup/login/member
]
