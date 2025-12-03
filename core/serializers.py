from rest_framework import serializers
from .models import Store, Deal, FreshItem


class StoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = ["id", "name", "code", "address", "city"]


# core/serializers.py
from rest_framework import serializers
from .models import Deal, Store


class DealSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

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
            "image_url",
            "show_on_home",
        ]

    def get_image_url(self, obj):
        if obj.image and hasattr(obj.image, "url"):
            return obj.image.url
        return None



class FreshItemSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = FreshItem
        fields = [
            "id",
            "name",
            "description",
            "price_label",
            "category",
            "image_url",
            "breads",
            "cheeses",
            "meats",
            "toppings",
        ]

    def get_image_url(self, obj):
        request = self.context.get("request")
        if obj.image:
            if request is not None:
                return request.build_absolute_uri(obj.image.url)
            return obj.image.url
        return None

# core/serializers.py
from rest_framework import serializers
from .models import Store, Deal, FreshItem


class StoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = ["id", "name", "code", "address", "city"]


class DealSerializer(serializers.ModelSerializer):
    store_code = serializers.CharField(source="store.code", read_only=True)
    image_url = serializers.SerializerMethodField()

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
            "is_active",
            "store",
            "store_code",
            "image_url",
            "created_at",
        ]

    def get_image_url(self, obj):
        request = self.context.get("request")
        if obj.image and hasattr(obj.image, "url"):
            url = obj.image.url
            if request is not None:
                return request.build_absolute_uri(url)
            return url
        return None



class FreshItemSerializer(serializers.ModelSerializer):
    ...
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
            "delivery_url",  
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



class StoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = ["id", "name", "code", "address", "city"]


class DealSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = Deal
        fields = [
            "id",
            "store",
            "tag",
            "title",
            "description",
            "segment",
            "category",
            "points_required",
            "show_on_home",
            "is_active",
            "image_url",
        ]

    def get_image_url(self, obj):
        request = self.context.get("request")
        if obj.image and hasattr(obj.image, "url"):
            if request:
                return request.build_absolute_uri(obj.image.url)
            return obj.image.url
        return None


class FreshItemSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = FreshItem
        fields = [
            "id",
            "store",
            "name",
            "description",
            "price_label",
            "category",
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
            if request:
                return request.build_absolute_uri(obj.image.url)
            return obj.image.url
        return None
