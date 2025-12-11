# core/serializers.py
from rest_framework import serializers
from .models import Store, Deal, FreshItem


class StoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = ["id", "name", "code", "address", "city"]


class DealSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()
    store_code = serializers.SerializerMethodField()

    class Meta:
        model = Deal
        fields = [
            "id",
            "tag",
            "title",
            "description",
            "segment",
            "category",
            "points_required",
            "show_on_home",
            "is_active",
            "store",
            "store_code",
            "image_url",
            "upc",          
            "pos_action",   
            "punch_required",
            "created_at",
        ]


    def get_image_url(self, obj):
        """
        Returns the full image URL so Flutter can show it directly.
        If you want to use buildImageUrl() in Flutter, this still works,
        because the URL starts with http/https.
        """
        request = self.context.get("request")
        if obj.image and hasattr(obj.image, "url"):
            url = obj.image.url
            if request is not None:
                return request.build_absolute_uri(url)
            return url
        return None

    def get_store_code(self, obj):
        if obj.store:
            return obj.store.code
        return None


class FreshItemSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()
    store_code = serializers.SerializerMethodField()

    class Meta:
        model = FreshItem
        fields = [
            "id",
            "name",
            "description",
            "price_label",
            "category",
            "store",
            "store_code",
            "image_url",
            "breads",
            "cheeses",
            "meats",
            "toppings",
            "is_active",
        ]

    def get_image_url(self, obj):
        request = self.context.get("request")
        if obj.image and hasattr(obj.image, "url"):
            url = obj.image.url
            if request is not None:
                return request.build_absolute_uri(url)
            return url
        return None

    def get_store_code(self, obj):
        if obj.store:
            return obj.store.code
        return None
