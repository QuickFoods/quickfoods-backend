# core/views.py

from django.db.models import Q
from rest_framework import viewsets

from .models import Store, Deal, FreshItem
from .serializers import StoreSerializer, DealSerializer, FreshItemSerializer


class StoreViewSet(viewsets.ReadOnlyModelViewSet):
    """
    GET /api/stores/
    """
    queryset = Store.objects.all().order_by("name")
    serializer_class = StoreSerializer


class DealViewSet(viewsets.ReadOnlyModelViewSet):
    """
    GET /api/deals/?store_code=JERSEY01&segment=deal&category=drinks

    Behaviour:
    - is_active=True only
    - store_code:
        * if provided  → deals where store = that code OR store is null (global)
        * if missing   → only global deals (store is null)
    - segment:
        * "", "all"   → no segment filter
        * "deal"/"redeem"/"my" → filter by that segment
    - category:
        * "", "all"   → no category filter (show all categories)
        * others      → deals where category = given OR category = "all"
                         (so "all" deals appear in every segment tab)
    """

    serializer_class = DealSerializer

    def get_queryset(self):
        qs = Deal.objects.filter(is_active=True)

        request = self.request
        store_code = (request.query_params.get("store_code") or "").strip()
        segment = (request.query_params.get("segment") or "").strip().lower()
        category = (request.query_params.get("category") or "").strip().lower()

        # Store filter: global + store-specific
        if store_code:
            qs = qs.filter(
                Q(store__code__iexact=store_code) | Q(store__isnull=True)
            )
        else:
            # If no store selected, only show global deals
            qs = qs.filter(store__isnull=True)

        # Segment filter (deal / redeem / my)
        if segment and segment != "all":
            qs = qs.filter(segment=segment)

        # Category filter
        if category and category != "all":
            qs = qs.filter(
                Q(category=category) | Q(category="all")
            )

        return qs.order_by("-created_at")


class FreshItemViewSet(viewsets.ReadOnlyModelViewSet):
    """
    GET /api/fresh-items/?store_code=JERSEY01&category=subs

    - is_active=True only
    - store_code:
        * if provided → items where store = code OR store is null (global)
        * if missing  → only global items (store is null)
    - category:
        * "", "all"   → show all categories
        * otherwise   → filter by category
    """

    serializer_class = FreshItemSerializer

    def get_queryset(self):
        qs = FreshItem.objects.filter(is_active=True)

        request = self.request
        store_code = (request.query_params.get("store_code") or "").strip()
        category = (request.query_params.get("category") or "").strip().lower()

        if store_code:
            qs = qs.filter(
                Q(store__code__iexact=store_code) | Q(store__isnull=True)
            )
        else:
            qs = qs.filter(store__isnull=True)

        if category and category != "all":
            qs = qs.filter(category=category)

        return qs.order_by("name")
